# Coach do Mosca - CLAUDE.md

## Papel deste arquivo

Este arquivo e a ancora global de contexto para o projeto ficticio "Coach do Mosca". Ele deve ser colado ou referenciado no inicio de cada novo chat quando o trabalho mudar de dominio de responsabilidade.

## Produto

Site comercial para coaching de Age of Mythology com:

- landing page premium em portugues e ingles;
- formulario de interesse para jogadores 1100+;
- registro de leads;
- painel administrativo protegido para leitura e exportacao;
- links para Discord, Twitch, Liquipedia e demais canais do Mosca.

## Stack alvo

- Frontend alvo: Next.js com App Router, TypeScript e CSS Modules ou CSS global com tokens.
- Backend alvo: API TypeScript com validacao Zod e persistencia SQL.
- Estado global: Zustand quando houver necessidade real de estado compartilhado.
- Testes: unitarios por dominio, integracao para API e E2E para fluxos comerciais.
- Infra: Docker e CI/CD documentados desde o inicio.

## Estado atual do repositorio

O projeto atual ainda esta em formato legado:

- `index.html` concentra pagina, estilos e scripts.
- `server.py` oferece servidor local, headers de seguranca, captura de leads e painel protegido.
- `painel_leads.html` exibe leads administrativos.
- `leads_mosca.db` e banco local de teste e nao deve ser publicado.

As pastas `frontend/`, `backend/`, `shared/`, `design-system/`, `infra/` e `docs/` representam a organizacao ficticia alvo para evolucao do projeto.

## Regras de dominio por chat

- Chat 1 - Planejamento e Arquitetura: decide stack, pastas, nomenclatura, contratos e atualiza este arquivo. Nao escreve codigo de producao.
- Chat 2 - Design System e UI: tokens, componentes base, acessibilidade e documentacao de uso.
- Chat 3 - Frontend: rotas, paginas e features visuais usando componentes do design system. Nao escreve backend.
- Chat 4 - Backend e API: rotas, controllers, services, models, middlewares, validadores e contratos JSON.
- Chat 5 - Testes e QA: testes unitarios, integracao e E2E. Nao escreve codigo de producao.
- Chat 6 - Seguranca e Auditoria: inputs, headers, autenticacao, autorizacao, logs, dependencias e exposicao de dados.
- Chat 7 - Refatoracao e Otimizacao: performance, duplicacao e limpeza apenas depois dos testes passarem.
- Chat 8 - Deploy e CI/CD: Docker, pipeline, variaveis de ambiente e requisitos de infraestrutura.

## Convencoes de nomenclatura

- Dominio: usar `Lead`, `Plan`, `Coach`, `Student` e `Rating`.
- Produto: usar "Coach do Mosca" no marketing e `mosca` em identificadores tecnicos.
- Leads: usar `Lead`, nunca `Prospect` ou `Contact`.
- Usuario interessado: usar `Student`, nao `Client`, quando o contexto for aula/coaching.
- Planos: manter valores canonicos `avulso-1h`, `pacote-6h`, `pacote-12h`.
- Commits: usar tags de rastreabilidade, exemplo `[chat-3][frontend] feat: lead form page`.

## Regras tecnicas

- `shared/types/` e a fonte compartilhada de tipos entre frontend e backend.
- Contratos de API vivem em `docs/api-contracts.md`.
- Tokens de design vivem em `docs/design-tokens.md` e `frontend/src/styles/tokens.css`.
- Toda feature relevante deve ter spec em `specs/feature-name.md` antes da implementacao.
- Comentarios inline devem explicar apenas decisoes nao obvias.
- Nao colar arquivos inteiros entre chats sem necessidade; usar referencias a arquivos.

## Seguranca obrigatoria

- Todo input de usuario deve ser validado no backend com Zod antes de chegar ao banco.
- Rotas administrativas exigem autenticacao e nunca retornam dados sensiveis sem controle de acesso.
- Headers globais obrigatorios: CSP, HSTS em producao, X-Frame-Options, X-Content-Type-Options, Referrer-Policy e Permissions-Policy.
- Dados pessoais de leads nao devem ser persistidos em `localStorage`.
- Arquivos `.db`, `.py`, `.md`, `.txt`, `.env` e diretorios ocultos nao devem ser servidos em producao.
- Logs nao devem conter WhatsApp completo nem objetivo completo do aluno.

## Performance obrigatoria

- Frontend deve considerar lazy loading, code splitting, imagens otimizadas e reducao de re-render.
- Videos devem ter poster, tamanho controlado e estrategia de carregamento.
- Backend deve definir indices junto com models quando filtros forem usados.
- Consultas de leads devem ter limite maximo e paginacao ou cursor antes de producao.

## Handoffs oficiais

- Chat 1 gera e atualiza `CLAUDE.md` e `docs/architecture.md`.
- Chat 2 gera `docs/design-tokens.md`, `design-system/` e `frontend/src/styles/tokens.css`.
- Chat 4 gera e mantem `docs/api-contracts.md` e `shared/types/`.
- Chat 5 consome specs, contratos e interfaces publicas.
- Chat 6 registra achados em `docs/security-audit.md` quando houver auditoria.

