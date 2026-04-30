# Arquitetura Ficticia - Coach do Mosca

## Objetivo

Organizar o site do Mosca como um projeto evolutivo com dominios claros, mesmo que a versao atual ainda rode como `index.html` + `server.py`.

## Modulos

### Frontend

Responsavel por paginas, formularios, componentes, animacoes e consumo de API.

Arquivos alvo:

- `frontend/src/app/`
- `frontend/src/components/ui/`
- `frontend/src/components/features/`
- `frontend/src/hooks/`
- `frontend/src/lib/`
- `frontend/src/store/`
- `frontend/src/styles/tokens.css`

### Backend

Responsavel por contratos HTTP, validacao, persistencia, autenticacao administrativa e exportacao.

Arquivos alvo:

- `backend/src/routes/`
- `backend/src/controllers/`
- `backend/src/services/`
- `backend/src/models/`
- `backend/src/middlewares/`
- `backend/src/validators/`

### Shared

Fonte unica de tipos e contratos usados pelos dois lados.

Arquivos alvo:

- `shared/types/lead.ts`

### Design System

Fonte unica de tokens e componentes base antes da criacao de novas telas.

Arquivos alvo:

- `design-system/tokens.json`
- `frontend/src/styles/tokens.css`
- `docs/design-tokens.md`

## Fluxo de dados

1. Student preenche o formulario de interesse no frontend.
2. Frontend normaliza dados somente para UX, sem substituir validacao do backend.
3. Backend valida payload com schema Zod.
4. Service grava o Lead em banco SQL.
5. API retorna `201` com `id`.
6. Painel administrativo consulta leads via rota autenticada.
7. Exportacao CSV aplica protecao contra formula injection.

## Fronteiras

- Frontend conhece apenas contratos publicados em `docs/api-contracts.md` e tipos de `shared/types/`.
- Backend nao conhece componentes, CSS ou detalhes de layout.
- Testes nao alteram codigo de producao.
- Refatoracao so acontece depois de feature funcional e testada.
- Deploy nao decide regra de negocio.

## Decisoes negativas

- Sem Redux por padrao; usar Zustand apenas quando houver estado global real.
- Sem duplicar tipos de Lead no frontend e backend.
- Sem publicar banco SQLite local.
- Sem misturar scripts administrativos dentro do bundle do frontend publico.
- Sem passar codigo bruto entre chats; usar arquivos de handoff.

