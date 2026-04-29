# Coach do Mosca - Site

Site institucional e comercial para venda de coaching de Age of Mythology.

## Arquivos principais

- `index.html`: pagina principal do site.
- `IMAGENS/`: imagens usadas no layout, logo e icones.
- `video efeitos.mp4`: video de referencia/asset local do projeto.
- `server.py`: servidor local usado para testes de captura de leads.
- `leads_mosca.db`: banco local de teste.

Nao publique arquivos `.db`, `.py`, `.md` ou `.txt` junto com o site estatico em producao. O servidor local bloqueia esses arquivos por seguranca, mas a hospedagem final tambem precisa impedir download direto de banco, codigo e documentos internos.

## Como abrir localmente

Para visualizar o site sem backend:

1. Abra `index.html` no navegador.
2. O visual, animacoes, botoes e troca de idioma funcionam normalmente.
3. O formulario pode nao salvar em producao se o backend/API nao estiver configurado.

Para testar com o servidor Python local:

```bash
set MOSCA_ADMIN_USER=admin
set MOSCA_ADMIN_PASSWORD=troque-esta-senha
python server.py
```

Depois acesse o endereco local indicado pelo terminal, normalmente:

```text
http://127.0.0.1:5500
```

O painel `painel_leads.html` e as rotas de leitura/exportacao de leads exigem autenticacao HTTP Basic configurada por `MOSCA_ADMIN_USER` e `MOSCA_ADMIN_PASSWORD`. Sem essas variaveis, a leitura de leads fica bloqueada.

## Idiomas

O site possui alternancia entre:

- Portugues
- Ingles

O botao `PT / EN` fica no topo da pagina. Apenas a escolha de idioma e salva no navegador com `localStorage`; dados pessoais de leads nao devem ser persistidos no navegador.

## Formulario e leads

Atencao: o formulario do site usa atualmente:

```js
const PLANILHA_URL = "/api/leads";
```

Isso significa que ele depende de uma API/backend para salvar os leads. Se o site for hospedado apenas como estatico em Netlify, Cloudflare Pages ou GitHub Pages, o visual funciona, mas o envio real dos leads precisa ser adaptado.

Opcoes recomendadas:

- Netlify Forms
- Formspree
- Google Forms ou Google Sheets com webhook
- Supabase
- Backend proprio com banco de dados

## Hospedagem gratuita recomendada

### Netlify

Melhor opcao para publicar rapido.

Passos:

1. Acesse `https://app.netlify.com/drop`.
2. Envie a pasta final do projeto.
3. O Netlify gera um link gratuito.
4. Depois, se quiser, conecte um dominio proprio.

Recomendado se for usar Netlify Forms para captar leads.

### Cloudflare Pages

Boa opcao gratuita para site estatico com boa performance.

Recomendado se o formulario for integrado com Formspree, Supabase ou outro servico externo.

### GitHub Pages

Bom para preview ou portfolio, mas nao e a melhor opcao para um site comercial com captacao de leads.

## Hospedagem paga

Se o cliente quiser algo mais profissional:

- Netlify Pro
- Cloudflare Pages Pro
- Vercel Pro
- Render, Railway ou VPS para backend proprio

Use hospedagem paga se houver:

- backend proprio;
- banco de dados em producao;
- painel administrativo;
- alto volume de trafego;
- dominio profissional;
- necessidade de suporte e estabilidade maior.

## Dominio

Opcoes:

- dominio gratuito da hospedagem, exemplo: `coachdomosca.netlify.app`;
- dominio proprio, exemplo: `coachdomosca.com`;
- subdominio, exemplo: `coach.mosca.com`.

Ao usar dominio proprio, configurar:

- DNS;
- SSL/HTTPS;
- redirecionamento entre `www` e dominio raiz;
- propriedade da conta do cliente.

## Contas e propriedade

O ideal e que o Mosca seja dono das contas principais:

- conta da hospedagem;
- dominio;
- banco/formulario;
- GitHub ou repositorio;
- e-mail de notificacao dos leads.

Quem desenvolve o site deve entrar como colaborador, nao como dono final.

## Checklist antes de entregar

- Testar desktop.
- Testar mobile.
- Testar navegacao.
- Testar troca PT/EN.
- Testar links externos: Discord, Twitch, Liquipedia e Instagram.
- Testar formulario real.
- Confirmar onde os leads chegam.
- Confirmar notificacao de novo lead.
- Configurar dominio e SSL.
- Remover arquivos desnecessarios.
- Otimizar imagens e videos.
- Revisar textos, precos e regras comerciais.
- Adicionar favicon.
- Adicionar imagem de compartilhamento para WhatsApp/Discord.
- Criar politica de privacidade se coletar nome e WhatsApp.
- Fazer backup da versao final.

## LGPD e dados pessoais

O formulario coleta nome, WhatsApp, elo, plano de interesse e objetivo do aluno.

Antes de usar em producao, o cliente deve estar ciente de que esses dados sao dados pessoais. O ideal e incluir uma politica simples informando:

- quais dados sao coletados;
- por que sao coletados;
- onde sao armazenados;
- por quanto tempo ficam salvos;
- como o interessado pode pedir remocao.

## Manutencao

Itens que podem precisar de atualizacao:

- precos dos planos;
- disponibilidade de vagas;
- links de redes sociais;
- textos em portugues e ingles;
- integracao do formulario;
- dominio;
- hospedagem;
- backup dos leads.

## Entrega recomendada

Entregar ao cliente:

- link publicado;
- pasta final ou repositorio GitHub;
- acesso da hospedagem;
- acesso do banco/formulario;
- instrucoes de manutencao;
- confirmacao de teste do formulario;
- custos mensais, se houver.

## Observacao final

Para publicar rapidamente uma versao visual, use Netlify Drop.

Para entregar pronto para vender e captar interessados, configure antes o formulario com Netlify Forms, Formspree, Supabase ou backend proprio.
