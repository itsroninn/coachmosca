# Design Tokens - Coach do Mosca

## Direcao Visual

O site do Mosca deve parecer competitivo, mitologico e premium. A base visual e uma arena noturna: fundos azul-profundo quase pretos, paineis translucidos, ouro como sinal de valor, vermelho como energia competitiva e azul eletrico como magia/raio. O resultado deve lembrar Age of Mythology sem virar UI de jogo pesada demais para conversao comercial.

Antes do Chat 3, novas telas devem consumir os tokens daqui e de `frontend/src/styles/tokens.css`, evitando cores soltas no CSS.

## Paleta De Cores

| Token | Valor | Uso |
| --- | --- | --- |
| `--color-bg` | `#090f18` | Fundo principal da pagina |
| `--color-bg-deep` | `#070b12` | Areas mais escuras, rodape e overlays |
| `--color-bg-elevated` | `#101826` | Secoes elevadas e fundos secundarios |
| `--color-surface` | `rgba(11, 17, 26, 0.82)` | Cards e paineis translucidos |
| `--color-surface-soft` | `rgba(255, 255, 255, 0.05)` | Camadas internas discretas |
| `--color-surface-strong` | `rgba(255, 255, 255, 0.08)` | Destaques dentro de cards |
| `--color-border` | `rgba(255, 255, 255, 0.10)` | Bordas neutras |
| `--color-border-gold` | `rgba(214, 180, 108, 0.28)` | Bordas de destaque |
| `--color-text` | `#f6f0e6` | Texto principal |
| `--color-text-soft` | `#c5ccd8` | Texto de apoio |
| `--color-text-muted` | `#7f8893` | Metadados, captions e texto desativado |
| `--color-gold` | `#d6b46c` | CTAs, bullets, bordas premium |
| `--color-gold-strong` | `#f1d28c` | Hover, brilho e estados ativos |
| `--color-blue` | `#4f77b9` | Apoio visual, magia/raio, botoes secundarios |
| `--color-blue-strong` | `#76b4ff` | Efeitos luminosos e foco contextual |
| `--color-red` | `#b5453c` | Energia, urgencia, variante destrutiva |
| `--color-success` | `#61b490` | Confirmacoes |
| `--color-error` | `#d06b63` | Erros e validacao |

Regras:

- Ouro e a cor de acao comercial. Use em CTA principal, preco, destaque de plano e foco.
- Azul e cor de suporte mitologico/tecnico. Use em efeitos, informacao e botoes secundarios.
- Vermelho deve ser pontual. Use para energia competitiva, perigo ou erro, nao como base de grandes blocos.
- Evitar novas familias de roxo, bege, marrom ou verde fora dos estados sem justificativa visual.

## Tipografia

| Token | Valor | Uso |
| --- | --- | --- |
| `--font-display` | `Cinzel, Georgia, serif` | Marca, H1, titulos de secao, precos |
| `--font-body` | `Rajdhani, "Segoe UI", Arial, sans-serif` | Corpo, navegacao, formularios e UI |
| `--font-size-xs` | `0.75rem` | Badges compactos, captions |
| `--font-size-sm` | `0.875rem` | Labels e textos auxiliares |
| `--font-size-md` | `1rem` | Texto padrao |
| `--font-size-lg` | `1.25rem` | Leads, subtitulos e cards |
| `--font-size-xl` | `2rem` | Titulos de secao |
| `--font-size-2xl` | `3rem` | Precos e chamadas fortes |
| `--font-size-display` | `clamp(2.8rem, 6vw, 5.8rem)` | H1/hero |

Regras:

- Titulos devem usar `Cinzel` com uppercase apenas em marca, hero, secoes e precos.
- Corpo deve usar `Rajdhani` com peso `500` ou `600` quando precisar de leitura rapida.
- Letter spacing pode ser usado em textos uppercase curtos, entre `0.04em` e `0.12em`.
- Nao escalar fonte com `vw` fora de `clamp()` em headings grandes.

## Espacamentos

| Token | Valor | Uso |
| --- | --- | --- |
| `--space-1` | `4px` | Ajustes finos |
| `--space-2` | `8px` | Gap pequeno |
| `--space-3` | `12px` | Gap de controle |
| `--space-4` | `16px` | Padding compacto |
| `--space-5` | `20px` | Respiro entre texto e acao |
| `--space-6` | `24px` | Padding padrao de card |
| `--space-8` | `32px` | Gap de grid |
| `--space-10` | `40px` | Separacao de blocos |
| `--space-12` | `48px` | Secoes compactas |
| `--space-16` | `64px` | Secoes principais |

Regras:

- Container padrao: `width: min(calc(100% - 32px), 1180px)`.
- Cards comerciais usam padding entre `22px` e `28px`.
- Secoes principais devem ficar entre `56px` e `88px` no desktop.
- Em mobile, reduzir gaps grandes em cerca de 25% e preservar altura minima de toque.

## Raios, Bordas E Sombras

| Token | Valor | Uso |
| --- | --- | --- |
| `--radius-sm` | `8px` | Badges pequenos |
| `--radius-md` | `12px` | Inputs, links sociais |
| `--radius-lg` | `16px` | Paineis compactos |
| `--radius-xl` | `22px` | Cards hero/oferta existentes |
| `--radius-pill` | `999px` | CTAs, badges e pills |
| `--shadow-panel` | `0 24px 70px rgba(0, 0, 0, 0.34)` | Cards e paineis |
| `--shadow-panel-strong` | `0 32px 92px rgba(0, 0, 0, 0.42)` | Plano em destaque |
| `--shadow-focus` | `0 0 0 4px rgba(214, 180, 108, 0.12)` | Foco visivel |

Observacao: novos cards em componentes reutilizaveis devem preferir raio maximo de `16px`; `22px` fica reservado para manter compatibilidade visual com a landing atual ou para blocos premium grandes.

## Botoes

### Base

- Altura minima desktop: `52px`.
- Altura minima mobile: `46px`.
- Padding desktop: `0 26px`.
- Padding mobile: `0 18px`.
- Border radius: `--radius-pill`.
- Fonte: `Rajdhani`, `700`, uppercase, `0.04em`.
- Transicao: `transform`, `box-shadow`, `border-color`, `background` em `200ms-240ms ease`.

### Variantes

| Variante | Uso | Estilo |
| --- | --- | --- |
| `primary` | CTA principal | Gradiente ouro, texto escuro, sombra dourada |
| `secondary` | Acao secundaria | Fundo azul translucido, borda azul |
| `ghost` | Navegacao discreta | Fundo transparente, texto suave, hover claro |
| `danger` | Acao destrutiva/risco | Fundo vermelho translucido, borda vermelha |

Estados:

- `hover`: subir `-2px`, intensificar borda/sombra, opcionalmente usar brilho rapido em CTAs.
- `focus-visible`: outline removido apenas se substituido por `--shadow-focus` e borda ouro.
- `disabled`: opacidade entre `0.56` e `0.72`, sem transform, cursor `not-allowed`.
- `loading`: manter largura do botao, desabilitar clique e mostrar texto/icone de progresso sem layout shift.

## Cards

Tipos padrao:

- `SurfaceCard`: card neutro para conteudo, borda neutra, fundo translucido.
- `OfferCard`: card de plano, com preco em `Cinzel`, bullets dourados e CTA.
- `FeaturedCard`: destaque comercial, borda ouro forte, sombra maior e sem deslocamento vertical no mobile.
- `InfoCard`: regras, agenda e detalhes de compra.
- `CommunityCard`: card com midia/logo e links externos.

Regras:

- Cards nao devem ser usados como secoes inteiras flutuantes.
- Evitar card dentro de card.
- Hover de cards clicaveis: `translateY(-6px)` a `-8px`, borda ouro e sombra mais intensa.
- Cards nao clicaveis podem ter borda e fundo premium, mas sem hover chamativo.

## Inputs E Formulario

Base:

- Label visivel obrigatorio.
- Gap label/campo: `8px`.
- Padding do campo: `14px 16px`.
- Raio: `--radius-md`.
- Fundo: `rgba(2, 6, 12, 0.48)`.
- Borda: `rgba(255, 255, 255, 0.12)`.
- Placeholder: texto claro com baixa opacidade.

Estados:

- `focus`: borda ouro e `--shadow-focus`.
- `error`: borda `--color-error`, fundo vermelho translucido leve e mensagem visivel abaixo.
- `success`: borda `--color-success` quando houver confirmacao local relevante.
- `disabled`: fundo menos contrastado, texto `--color-text-muted`, cursor `not-allowed`.

Mensagens de formulario:

- Loading: fundo azul translucido, texto azul claro.
- Sucesso: fundo verde translucido, borda verde, texto claro.
- Erro: fundo vermelho translucido, borda vermelha, texto claro.

## Estados De Interacao

| Estado | Padrao |
| --- | --- |
| Hover | Movimento sutil, brilho dourado ou borda mais clara |
| Focus | Sempre visivel por teclado com anel ouro |
| Active | Reduzir movimento, leve `translateY(0)` ou escurecimento |
| Loading | Desabilitar acao, manter dimensao, feedback textual claro |
| Error | Vermelho pontual com mensagem proxima ao controle |
| Success | Verde pontual, sem competir com o CTA principal |

Todos os estados interativos devem respeitar `prefers-reduced-motion`.

## Regras Para Mobile

- Breakpoints principais: `1080px` para grids virarem uma coluna; `760px` para layout mobile.
- Header pode deixar de ser sticky no mobile.
- CTAs principais em nav ou hero podem ocupar `width: 100%` quando houver pouco espaco.
- Hero deve reduzir efeitos visuais e esconder elementos decorativos densos.
- Cards em destaque nao devem usar deslocamento vertical no mobile.
- Inputs e botoes devem manter alvo minimo de toque de `44px`.
- Menus flutuantes devem respeitar `env(safe-area-inset-*)`.
- Textos longos devem quebrar linha sem comprimir botoes ou cards.

## Acessibilidade

- Contraste minimo WCAG AA para texto funcional.
- `:focus-visible` obrigatorio em links, botoes, inputs, selects e textareas.
- Icones decorativos devem usar `aria-hidden="true"`.
- Links/botoes apenas com icone precisam de `aria-label`.
- Mensagens de formulario devem poder ser anunciadas por tecnologias assistivas quando o frontend for componentizado.
- Animacoes decorativas devem ser reduzidas ou removidas em `prefers-reduced-motion: reduce`.

## Padronizar Antes Do Chat 3

1. Sincronizar `design-system/tokens.json`, `frontend/src/styles/tokens.css` e esta documentacao.
2. Criar componentes base no frontend: `Button`, `Card`, `Input`, `Select`, `Textarea`, `StatusMessage`, `Badge` e `Container`.
3. Definir variantes canonicas de botao: `primary`, `secondary`, `ghost`, `danger`.
4. Definir variantes canonicas de card: `surface`, `offer`, `featured`, `info`, `community`.
5. Centralizar breakpoints `1080px` e `760px`.
6. Criar exemplos de uso dos componentes com estados de hover/focus/disabled/loading/error/success.
7. Remover cores hardcoded gradualmente ao migrar o `index.html` para componentes, sem mudar a identidade visual.
