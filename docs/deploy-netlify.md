# Deploy no Netlify

## Estrategia recomendada

Use build com pasta publica gerada. O Netlify deve publicar `public/`, nunca a raiz do repositorio.

Motivo: a raiz contem arquivos de trabalho local, backend legado, bancos SQLite, documentacao interna e midias grandes. Publicar a raiz poderia expor codigo administrativo, bancos locais ou documentos que nao fazem parte do site estatico.

## Arquivos publicados

O build `node scripts/build-public.mjs` publica somente:

- `index.html`
- `IMAGENS/AOM STANDARDjpg.jpg`
- `IMAGENS/discord-white-icon.png`
- `IMAGENS/LOGO MOSCA.jpg`
- `IMAGENS/luquipedia logo 2017.png`
- `IMAGENS/twitch-white-icon.png`
- `IMAGENS/youtube.png`

## Arquivos fora do deploy

Devem ficar fora da pasta publicada:

- bancos locais: `leads_mosca.db`, `sistema.db`, `*.db`, `*.sqlite*`
- backend local: `server.py`
- paginas administrativas/diagnostico: `painel_leads.html`, `exemplo_visualizacao_leads.html`
- documentacao e handoffs internos: `CLAUDE.md`, `README.md`, `docs/`, `specs/`, `*.txt`, arquivos internos `.md`
- estrutura futura de app/backend: `backend/`, `frontend/`, `shared/`, `design-system/`, `infra/`
- midias grandes nao referenciadas pelo site: `*.mp4`, `*.mov`, `*.avi`, `*.mkv`
- variaveis locais: `.env`, `.env.*`

Observacao: alguns desses arquivos ja estao rastreados pelo Git no estado atual. O `.gitignore` evita novos arquivos locais, mas nao remove arquivos ja rastreados. Para parar de versionar bancos, scripts locais e videos, use `git rm --cached` depois de confirmar o escopo.

## Netlify Forms

O formulario continua detectavel porque o `index.html` final em `public/` preserva:

- `form name="lead-mosca"`
- `data-netlify="true"`
- `input type="hidden" name="form-name" value="lead-mosca"`
- envio via `fetch("/")` com `application/x-www-form-urlencoded`

O script de build falha se nao encontrar os marcadores principais do Netlify Forms.

## Configuracao no Netlify

As configuracoes ficam em `netlify.toml`:

- Build command: `node scripts/build-public.mjs`
- Publish directory: `public`

Antes de publicar, rode localmente:

```bash
node scripts/build-public.mjs
```

Depois confira se `public/index.html` e `public/IMAGENS/` contem apenas os arquivos esperados.
