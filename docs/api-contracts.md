# Contratos de API - Coach do Mosca

## Base

Ambiente local legado:

```text
http://127.0.0.1:5500
```

Formato padrao:

- JSON UTF-8 para API.
- CSV UTF-8 para exportacao administrativa.
- Erros retornam `{ "ok": false, "error": "mensagem" }`.

## POST /api/leads

Cria um lead de interesse no coaching.

### Autenticacao

Publica, com protecao de origem e limite de body.

### Request

```json
{
  "coach": "Mosca",
  "nome": "Rafael Silva",
  "whatsapp": "71999999999",
  "elo": 1350,
  "plano": "pacote-6h",
  "objetivo": "Melhorar macro, matchups e tomada de decisao.",
  "data": "2026-04-29T18:30:00.000Z"
}
```

### Regras

- `coach`: obrigatorio, ate 40 caracteres.
- `nome`: obrigatorio, ate 80 caracteres.
- `whatsapp`: obrigatorio, somente digitos, 10 a 15 caracteres.
- `elo`: obrigatorio, inteiro entre 1100 e 3000.
- `plano`: obrigatorio, um de `avulso-1h`, `pacote-6h`, `pacote-12h`.
- `objetivo`: obrigatorio, ate 800 caracteres.
- `data`: opcional, ate 40 caracteres.

### Resposta 201

```json
{
  "ok": true,
  "id": 123
}
```

### Erros esperados

- `400`: JSON invalido, campo ausente, campo longo, plano invalido, elo invalido ou WhatsApp invalido.
- `403`: origem nao autorizada.
- `413`: body maior que o limite.

## GET /api/leads

Lista leads para painel administrativo.

### Autenticacao

HTTP Basic via `MOSCA_ADMIN_USER` e `MOSCA_ADMIN_PASSWORD`.

### Query params

- `limit`: inteiro de 1 a 1000, padrao 100.
- `plano`: filtro por plano canonico.
- `q`: busca textual em nome, WhatsApp e objetivo.
- `min_elo`: elo minimo.

### Resposta 200

```json
{
  "count": 1,
  "items": [
    {
      "id": 123,
      "coach": "Mosca",
      "nome": "Rafael Silva",
      "whatsapp": "71999999999",
      "elo": 1350,
      "plano": "pacote-6h",
      "horas_avulsas": null,
      "objetivo": "Melhorar macro.",
      "data_cliente": "2026-04-29T18:30:00.000Z",
      "created_at": "2026-04-29T18:31:00.000Z"
    }
  ]
}
```

## GET /api/leads.csv

Exporta leads para CSV administrativo.

### Autenticacao

HTTP Basic via `MOSCA_ADMIN_USER` e `MOSCA_ADMIN_PASSWORD`.

### Observacao de seguranca

Campos textuais devem ser escapados para evitar formula injection em planilhas.

## GET /api/health

Healthcheck local.

### Resposta 200

```json
{
  "ok": true
}
```

