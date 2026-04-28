import json
import sqlite3
import csv
import io
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "leads_mosca.db"
HOST = "127.0.0.1"
PORT = 5500


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

    def parse_filters(self, query):
        try:
            limit = int(query.get("limit", ["100"])[0])
        except ValueError:
            limit = 100

        limit = max(1, min(limit, 1000))
        plano = query.get("plano", [""])[0].strip()
        busca = query.get("q", [""])[0].strip()

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

        if parsed.path == "/api/health":
            return self.send_json(200, {"ok": True})

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
                        item["coach"],
                        item["nome"],
                        item["whatsapp"],
                        item["elo"],
                        item["plano"],
                        item["horas_avulsas"],
                        item["objetivo"],
                        item["data_cliente"],
                        item["created_at"],
                    ]
                )

            return self.send_csv(200, "leads_mosca.csv", buffer.getvalue())

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/leads":
            return self.send_json(404, {"ok": False, "error": "Endpoint nao encontrado."})

        content_length = self.headers.get("Content-Length")
        if not content_length:
            return self.send_json(400, {"ok": False, "error": "Body ausente."})

        try:
            raw = self.rfile.read(int(content_length))
            payload = json.loads(raw.decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            return self.send_json(400, {"ok": False, "error": "JSON invalido."})

        required_fields = ["coach", "nome", "whatsapp", "elo", "plano", "objetivo"]
        missing = [field for field in required_fields if not payload.get(field)]
        if missing:
            return self.send_json(
                400,
                {"ok": False, "error": f"Campos obrigatorios ausentes: {', '.join(missing)}"},
            )

        try:
            elo = int(payload["elo"])
        except ValueError:
            return self.send_json(400, {"ok": False, "error": "Elo invalido."})

        if elo < 1100:
            return self.send_json(
                400, {"ok": False, "error": "O coaching exige elo minimo de 1100."}
            )

        plano = str(payload.get("plano", "")).strip()
        horas_avulsas = payload.get("horas_avulsas")

        if plano == "avulso":
            try:
                horas_avulsas = int(horas_avulsas)
            except (TypeError, ValueError):
                return self.send_json(
                    400, {"ok": False, "error": "Informe uma quantidade valida de horas avulsas."}
                )
            if horas_avulsas < 1 or horas_avulsas > 20:
                return self.send_json(
                    400, {"ok": False, "error": "Horas avulsas devem ficar entre 1 e 20."}
                )
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
                    str(payload.get("coach", "")).strip(),
                    str(payload.get("nome", "")).strip(),
                    str(payload.get("whatsapp", "")).strip(),
                    elo,
                    plano,
                    horas_avulsas,
                    str(payload.get("objetivo", "")).strip(),
                    str(payload.get("data", "")).strip(),
                    now,
                ),
            )
            conn.commit()
            lead_id = cursor.lastrowid

        return self.send_json(201, {"ok": True, "id": lead_id})


def run():
    init_db()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Servidor ativo em http://{HOST}:{PORT}")
    print(f"Banco local: {DB_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    run()
