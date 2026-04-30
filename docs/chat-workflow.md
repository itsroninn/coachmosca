# Workflow de Chats - Coach do Mosca

## Quando abrir novo chat

Abra um novo chat sempre que mudar de dominio:

- planejamento para design;
- design para frontend;
- frontend para backend;
- implementacao para testes;
- implementacao para seguranca;
- feature funcional para refatoracao;
- produto pronto para deploy.

## Template de abertura

```text
Contexto do projeto: @CLAUDE.md
Meu objetivo neste chat: implementar a feature X no dominio Y.
Arquivos relevantes: @arquivo-1 @arquivo-2
Contrato de API: @docs/api-contracts.md#endpoint-relevante
Spec da feature: @specs/feature-x.md
Restricoes: nao alterar arquivos fora deste dominio.
```

## Handoffs

- Chat 1 entrega `CLAUDE.md` e `docs/architecture.md`.
- Chat 2 entrega `docs/design-tokens.md` e `design-system/`.
- Chat 4 entrega `docs/api-contracts.md` e `shared/types/`.
- Chat 5 entrega resultados de testes e gaps.
- Chat 6 entrega achados de auditoria.
- Chat 7 entrega melhorias com testes verdes.
- Chat 8 entrega scripts de deploy e variaveis necessarias.

## Exemplo aplicado ao Mosca

```text
Contexto do projeto: @CLAUDE.md
Meu objetivo neste chat: implementar a captura de leads no frontend.
Arquivos relevantes: @frontend/src/app @frontend/src/components/features @shared/types/lead.ts
Contrato de API: POST /api/leads em @docs/api-contracts.md
Spec da feature: @specs/lead-capture.md
Restricoes: nao alterar backend; usar mocks baseados no contrato.
```

