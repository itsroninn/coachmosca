# 📋 Como Integrar Planilha Google ao Site

## 🔥 Opção 1: Webhook (MAIS FÁCIL - 5 minutos)

### Passo 1: Criar Webhook gratuito
1. Acesse: https://make.com
2. Crie conta gratuita
3. Crie novo cenário "Webhook → Google Sheets"
4. Copie o URL do webhook

### Passo 2: Configurar Google Sheets
1. Crie planilha com colunas:
   - A: Nome
   - B: WhatsApp
   - C: Nível
   - D: Objetivo
   - E: Data

2. No Make.com:
   - Conecte sua conta Google
   - Selecione "Add Row"
   - Mapeie os campos do webhook

### Passo 3: Atualizar o site
No arquivo `index.html`, linha ~340, troque:
```javascript
const PLANILHA_URL = 'COLE_O_URL_DO_WEBHOOK_AQUI';
```

---

## 🚀 Opção 2: WebSimulate (INSTANTÂNEO - TESTE)

Para testar agora mesmo:

1. Use: https://webhook.site
2. Copie o URL fornecido
3. Cole no site
4. Preencha o formulário
5. Veja os dados aparecerem em tempo real! ✨

---

## 📊 Opção 3: Make.com Template (RECOMENDADO)

Template pré-configurado:
```
Webhook (POST) → Google Sheets → Adicionar Linha
```

**Mapeamento:**
- body.nome → Coluna A (Nome)
- body.whatsapp → Coluna B (WhatsApp)
- body.nivel → Coluna C (Nível)
- body.objetivo → Coluna D (Objetivo)
- body.data → Coluna E (Data)

---

## 🎯 FLUXO COMPLETO

User preenche site → Webhook recebe → Salva na planilha → Notifica WhatsApp

**Benefícios:**
✅ Backup automático na planilha
✅ Continua funcionando no WhatsApp
✅ Lista de todos os leads
✅ Pode exportar para Excel
✅ Filtros e gráficos

---

## ⚡ TESTE RÁPIDO (1 minuto)

1. Abra: https://webhook.site
2. Copie o URL
3. Cole no index.html
4. Salve o arquivo
5. Teste o formulário
6. Verifique os dados no webhook.site!

---

✅ **Pronto!** Seu lead agora será salvo automaticamente!