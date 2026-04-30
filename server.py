import json
import sqlite3
import csv
import io
import base64
import binascii
import os
import re
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "leads_mosca.db"
HOST = "127.0.0.1"
PORT = 5500
MAX_BODY_BYTES = 32 * 1024
ALLOWED_PLANS = {"avulso-1h", "pacote-6h", "pacote-12h"}
BLOCKED_STATIC_SUFFIXES = {".db", ".py", ".md", ".txt", ".sqlite", ".sqlite3"}
TEXT_LIMITS = {
    "coach": 40,
    "nome": 80,
    "whatsapp": 20,
    "plano": 20,
    "objetivo": 800,
    "data": 40,
}
SAFE_TEXT_RE = re.compile(r"^[\w\sÀ-ÿ.,:;!?()+/@#&'\"-]+$", re.UNICODE)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coach TEXT NOT NULL,
                nome TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                elo INTEGER NOT NULL,
                plano TEXT NOT NULL,
                horas_avulsas INTEGER,
                objetivo TEXT NOT NULL,
                data_cliente TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        # Migra bancos antigos que ainda nao possuem a coluna de horas avulsas.
        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(leads)").fetchall()
        }
        if "horas_avulsas" not in columns:
            conn.execute("ALTER TABLE leads ADD COLUMN horas_avulsas INTEGER")
        conn.commit()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def send_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_csv(self, status_code, filename, content):
        body = content.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_security_headers()
        super().end_headers()

    def send_security_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "media-src 'self'; "
            "connect-src 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'"
        )

    def send_auth_required(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Mosca Leads"')
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Autenticacao obrigatoria.".encode("utf-8"))

    def is_admin_authenticated(self):
        user = os.environ.get("MOSCA_ADMIN_USER")
        password = os.environ.get("MOSCA_ADMIN_PASSWORD")
        if not user or not password:
            return False

        header = self.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            return False

        try:
            decoded = base64.b64decode(header.split(" ", 1)[1], validate=True).decode("utf-8")
            supplied_user, supplied_password = decoded.split(":", 1)
        except (binascii.Error, ValueError, UnicodeDecodeError):
            return False

        return supplied_user == user and supplied_password == password

    def require_admin(self):
        if self.is_admin_authenticated():
            return True
        self.send_auth_required()
        return False

    def validate_same_origin(self):
        origin = self.headers.get("Origin")
        if not origin:
            return True

        allowed = {
            f"http://{HOST}:{PORT}",
            f"http://localhost:{PORT}",
        }
        return origin in allowed

    def normalize_text(self, payload, field, required=True):
        value = str(payload.get(field, "")).strip()
        if required and not value:
            raise ValueError(f"Campo obrigatorio ausente: {field}.")

        limit = TEXT_LIMITS[field]
        if len(value) > limit:
            raise ValueError(f"Campo muito longo: {field}.")

        if value and not SAFE_TEXT_RE.match(value):
            raise ValueError(f"Campo contem caracteres invalidos: {field}.")

        return value

    def csv_safe(self, value):
        text = "" if value is None else str(value)
        if text.startswith(("=", "+", "-", "@", "\t", "\r")):
            return "'" + text
        return text

    def parse_filters(self, query):
        try:
            limit = int(query.get("limit", ["100"])[0])
        except ValueError:
            limit = 100

        limit = max(1, min(limit, 1000))
        plano = query.get("plano", [""])[0].strip()
        if plano and plano not in ALLOWED_PLANS:
            plano = ""
        busca = query.get("q", [""])[0].strip()
        busca = busca[:80]

        try:
            min_elo = int(query.get("min_elo", ["0"])[0])
        except ValueError:
            min_elo = 0

        return {"limit": limit, "plano": plano, "q": busca, "min_elo": min_elo}

    def query_leads(self, filters):
        where = []
        params = []

        if filters["plano"]:
            where.append("plano = ?")
            params.append(filters["plano"])

        if filters["min_elo"] > 0:
            where.append("elo >= ?")
            params.append(filters["min_elo"])

        if filters["q"]:
            where.append("(nome LIKE ? OR whatsapp LIKE ? OR objetivo LIKE ?)")
            like = f'%{filters["q"]}%'
            params.extend([like, like, like])

        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        sql = f"""
            SELECT id, coach, nome, whatsapp, elo, plano, horas_avulsas, objetivo, data_cliente, created_at
            FROM leads
            {where_sql}
            ORDER BY id DESC
            LIMIT ?
        """
        params.append(filters["limit"])

        with get_connection() as conn:
            rows = conn.execute(sql, tuple(params)).fetchall()
        return [dict(row) for row in rows]

    def do_GET(self):
        parsed = urlparse(self.path)
        requested_path = Path(parsed.path)

        if parsed.path == "/api/health":
            return self.send_json(200, {"ok": True})

        if parsed.path in {"/painel_leads.html", "/api/leads", "/api/leads.csv"}:
            if not self.require_admin():
                return

        if requested_path.suffix.lower() in BLOCKED_STATIC_SUFFIXES or any(part.startswith(".") for part in requested_path.parts):
            return self.send_json(403, {"ok": False, "error": "Arquivo nao publicado."})

        if parsed.path == "/api/leads":
            query = parse_qs(parsed.query)
            filters = self.parse_filters(query)
            leads = self.query_leads(filters)
            return self.send_json(200, {"count": len(leads), "items": leads})

        if parsed.path == "/api/leads.csv":
            query = parse_qs(parsed.query)
            filters = self.parse_filters(query)
            leads = self.query_leads(filters)

            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(
                ["id", "coach", "nome", "whatsapp", "elo", "plano", "horas_avulsas", "objetivo", "data_cliente", "created_at"]
            )
            for item in leads:
                writer.writerow(
                    [
                        item["id"],
                        self.csv_safe(item["coach"]),
                        self.csv_safe(item["nome"]),
                        self.csv_safe(item["whatsapp"]),
                        item["elo"],
                        self.csv_safe(item["plano"]),
                        item["horas_avulsas"],
                        self.csv_safe(item["objetivo"]),
                        self.csv_safe(item["data_cliente"]),
                        item["created_at"],
                    ]
                )

            return self.send_csv(200, "leads_mosca.csv", buffer.getvalue())

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/leads":
            return self.send_json(404, {"ok": False, "error": "Endpoint nao encontrado."})

        if not self.validate_same_origin():
            return self.send_json(403, {"ok": False, "error": "Origem nao autorizada."})

        content_length = self.headers.get("Content-Length")
        if not content_length:
            return self.send_json(400, {"ok": False, "error": "Body ausente."})

        try:
            content_length_int = int(content_length)
        except ValueError:
            return self.send_json(400, {"ok": False, "error": "Content-Length invalido."})

        if content_length_int < 1 or content_length_int > MAX_BODY_BYTES:
            return self.send_json(413, {"ok": False, "error": "Body excede o limite permitido."})

        try:
            raw = self.rfile.read(content_length_int)
            payload = json.loads(raw.decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            return self.send_json(400, {"ok": False, "error": "JSON invalido."})

        if not isinstance(payload, dict):
            return self.send_json(400, {"ok": False, "error": "JSON deve ser um objeto."})

        try:
            coach = self.normalize_text(payload, "coach")
            nome = self.normalize_text(payload, "nome")
            whatsapp = self.normalize_text(payload, "whatsapp")
            plano = self.normalize_text(payload, "plano")
            objetivo = self.normalize_text(payload, "objetivo")
            data_cliente = self.normalize_text(payload, "data", required=False)
        except ValueError as exc:
            return self.send_json(400, {"ok": False, "error": str(exc)})

        try:
            elo = int(payload["elo"])
        except (KeyError, TypeError, ValueError):
            return self.send_json(400, {"ok": False, "error": "Elo invalido."})

        if elo < 1100 or elo > 3000:
            return self.send_json(
                400, {"ok": False, "error": "Elo deve ficar entre 1100 e 3000."}
            )

        if plano not in ALLOWED_PLANS:
            return self.send_json(400, {"ok": False, "error": "Plano invalido."})

        if not re.fullmatch(r"\d{10,15}", whatsapp):
            return self.send_json(400, {"ok": False, "error": "WhatsApp invalido."})

        if plano == "avulso-1h":
            horas_avulsas = 1
        else:
            horas_avulsas = None

        now = datetime.now(timezone.utc).isoformat()

        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO leads (coach, nome, whatsapp, elo, plano, horas_avulsas, objetivo, data_cliente, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    coach,
                    nome,
                    whatsapp,
                    elo,
                    plano,
                    horas_avulsas,
                    objetivo,
                    data_cliente,
                    now,
                ),
            )
            conn.commit()
            lead_id = cursor.lastrowid

        return self.send_json(201, {"ok": True, "id": lead_id})


def run():
    init_db()
    if not os.environ.get("MOSCA_ADMIN_USER") or not os.environ.get("MOSCA_ADMIN_PASSWORD"):
        print("Aviso: painel e API de leitura desativados ate definir MOSCA_ADMIN_USER e MOSCA_ADMIN_PASSWORD.")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Servidor ativo em http://{HOST}:{PORT}")
    print(f"Banco local: {DB_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    run()
