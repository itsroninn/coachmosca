# Spec - Captura de Leads

## Objetivo

Permitir que um Student interessado em coaching envie seus dados para o Mosca e receba feedback visual claro.

## Escopo

- Formulario publico de interesse.
- Validacao de UX no frontend.
- Validacao autoritativa no backend.
- Persistencia do Lead.
- Painel administrativo consome a lista autenticada.

## Campos

- `coach`: fixo como `Mosca`.
- `nome`: obrigatorio, ate 80 caracteres.
- `whatsapp`: obrigatorio, 10 a 15 digitos apos normalizacao.
- `elo`: obrigatorio, 1100 a 3000.
- `plano`: um de `avulso-1h`, `pacote-6h`, `pacote-12h`.
- `objetivo`: obrigatorio, ate 800 caracteres.
- `data`: opcional, ISO string enviada pelo cliente.

## Casos de borda

- Elo abaixo de 1100 deve bloquear envio.
- WhatsApp com mascara deve ser normalizado antes do envio.
- API indisponivel deve mostrar mensagem de erro sem perder dados preenchidos.
- Envio duplicado durante loading deve ser bloqueado.
- Bot-field preenchido deve ser ignorado ou rejeitado em integracao anti-spam.

## Testes esperados

- Unitario: normalizacao de WhatsApp.
- Unitario: schema de criacao de Lead.
- Integracao: `POST /api/leads` retorna `201`.
- Integracao: plano invalido retorna `400`.
- E2E: usuario preenche formulario e ve estado de sucesso.

