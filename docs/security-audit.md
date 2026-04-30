# Auditoria de Seguranca - Chat 6

Data: 2026-04-30
Escopo: prontidao para deploy estatico no Netlify usando `node scripts/build-public.mjs` e publish directory `public`.

## Resultado

Status: aprovado para deploy estatico no Netlify, desde que o Netlify use exatamente a configuracao do repositorio (`publish = "public"`).

## Verificacoes executadas

- `netlify.toml` publica somente `public/`.
- `scripts/build-public.mjs` remove e recria `public/` antes do build.
- O build copia somente `index.html` e a lista fechada de assets em `IMAGENS/`.
- `public/` nao contem arquivos `.db`, `.sqlite`, `.py`, `.env`, `.md`, `.txt`, `.csv`, `.json`, videos, painel admin, backend local ou arquivos internos.
- Todas as imagens referenciadas por `public/index.html` em `IMAGENS/` existem em `public/IMAGENS/`.
- O formulario `lead-mosca` permanece detectavel pelo Netlify Forms.
- O formulario envia via `fetch("/")` com `application/x-www-form-urlencoded` e `form-name=lead-mosca`.
- Dados pessoais de leads nao sao persistidos em `localStorage`, `sessionStorage`, `indexedDB`, arquivos locais ou bancos no frontend publicado.
- `localStorage` e usado apenas para a preferencia de idioma `mosca_lang`.
- `public/index.html` nao contem referencias a `server.py`, `leads_mosca.db`, `sistema.db`, `painel_leads.html`, `exemplo_visualizacao_leads.html`, `.env`, `localhost`, tokens, secrets ou chaves de API.

## Arquivos publicados apos build

- `public/index.html`
- `public/IMAGENS/AOM STANDARDjpg.jpg`
- `public/IMAGENS/discord-white-icon.png`
- `public/IMAGENS/LOGO MOSCA.jpg`
- `public/IMAGENS/luquipedia logo 2017.png`
- `public/IMAGENS/simbolo-do-youtube-white.png`
- `public/IMAGENS/twitch-white-icon.png`

## Formulario

Marcadores preservados em `public/index.html`:

- `<form name="lead-mosca" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field">`
- `<input type="hidden" name="form-name" value="lead-mosca">`
- payload JavaScript com `"form-name": "lead-mosca"`

Campos enviados ao Netlify Forms:

- `coach`
- `nome`
- `whatsapp`
- `elo`
- `plano`
- `objetivo`
- `data`
- `bot-field`

## Observacoes e limites

- A raiz do projeto contem arquivos sensiveis ou internos (`server.py`, bancos SQLite, paineis, documentos e videos), mas eles nao sao publicados quando o publish directory e `public`.
- `.gitignore` protege bancos locais, `.env`, saidas geradas, caches e midias grandes.
- O Netlify Forms so deve ser considerado confirmado em producao depois do primeiro deploy, quando o painel do Netlify mostrar o formulario `lead-mosca` detectado.
- O backend local e o painel administrativo continuam fora do deploy estatico. Se forem publicados em outro ambiente no futuro, precisam de auditoria propria.

## Achados

Nenhum bloqueador encontrado para o deploy estatico no Netlify.
