# Documento vivo de marca

Um por projeto. Dois arquivos, sempre juntos:

- `marca/MARCA.md`: para ler. Cada item com valor, fonte e situação.
- `marca/marca.json`: para os scripts. Só valores já confirmados. É gerado a
  partir do `MARCA.md`; os dois mudam no mesmo passo.

Arquivos de apoio: `marca/fontes/` (.ttf/.otf), `marca/logos/`, `marca/referencias/`
(prints, peças que funcionaram, material enviado pelo usuário).

## De onde tirar (nesta ordem de confiança)

1. **O que o usuário disse ou aprovou** na conversa. Situação: `confirmado`.
2. **Arquivos enviados pelo usuário** (manual de marca, PDF, imagens, prints):
   ler o arquivo inteiro. Situação: `extraído`.
3. **Arquivos do projeto**: `CLAUDE.md`, `AGENTS.md`, CSS/Tailwind
   (`tailwind.config.*`, `:root { --cor }`), `public/brand/`, pastas de marca,
   roteiros, anúncios já aprovados. Situação: `extraído`.
4. **Site da marca**: página inicial e páginas principais (WebFetch). Cores e
   fontes vêm do CSS (baixar o CSS e procurar `color`, `background`,
   `font-family`, `fonts.googleapis.com`), não do "olhar" da página. Respeitar
   robots.txt e bloqueio anti-robô. Situação: `extraído`.
5. **Logo em imagem**: cores dominantes medidas com Pillow
   (`Image.quantize(colors=6)`), não estimadas. Situação: `extraído`.
6. **Redes sociais e Biblioteca de Anúncios do Meta**: CTA, tom e públicos
   usados de fato. Situação: `extraído`.

Nada vem de suposição. Sem fonte, o campo fica `pendente` com a pergunta que
falta fazer ao usuário.

Fontes: baixar o arquivo do Google Fonts (ou do lugar indicado pelo usuário)
para `marca/fontes/`. Fonte paga que não está no projeto: `pendente`, não trocar
por parecida sem o usuário aprovar.

## Situação de cada item

- `confirmado`: o usuário disse ou aprovou. Só muda com pedido dele.
- `extraído`: tirado de fonte, ainda não aprovado. Pode ir para o vídeo, mas
  entra na lista de conferência ao entregar.
- `pendente`: sem valor. O script não usa; pergunta ao usuário.

## Quando atualizar

- O usuário trouxe informação nova, arquivo novo ou decisão ("o CTA agora é X").
- Aprovou ou reprovou uma peça: registrar o motivo em "Peças e lições".
- Antes de cada vídeo: conferir se há `extraído` ou `pendente` que afete o vídeo
  e perguntar junto com os outros pontos do passo 4.
- Fonte original mudou (site novo, manual novo).

## Como atualizar (sem perder dado)

1. Ler o `MARCA.md` inteiro antes.
2. Mudar só o item afetado. O resto fica como está: item ausente do pedido
   não é apagado nem volta ao padrão.
3. Item `confirmado` só muda com pedido explícito do usuário. Se uma fonte nova
   contradiz um `confirmado`, não trocar: registrar em "Conflitos" e perguntar.
4. Item antigo que deixou de valer: mover para "Histórico", não apagar.
5. Linha nova em "Histórico de mudanças" (data, item, antes, depois, fonte).
6. Regerar `marca.json` e conferir que ele abre (`python -c "import json;json.load(open('marca/marca.json',encoding='utf-8'))"`).
7. Avisar o usuário em uma linha o que mudou.

## Modelo do `MARCA.md`

```markdown
# Marca: <nome>

Atualizado em <aaaa-mm-dd>. Legenda: confirmado | extraído | pendente.

## Quem é
| Item | Valor | Fonte | Situação |
|---|---|---|---|
| Nome como aparece | | | |
| Quem aparece nos vídeos | | | |
| Ramo / produto principal | | | |
| Região | | | |

## Cores
| Papel | Hex | Fonte | Situação |
|---|---|---|---|
| principal (fundo de caixa, cartão final) | | | |
| fundo claro | | | |
| texto escuro | | | |
| destaque (palavra falada, selo, botão) | | | |
| legenda (texto ainda não falado) | #FFFFFF | padrão da skill | extraído |
| contorno da legenda | #000000 | padrão da skill | extraído |

## Fontes
| Uso | Família | Arquivo em marca/fontes/ | Fonte | Situação |
|---|---|---|---|---|
| legenda e selos | | | | |
| título | | | | |

## Logos e elementos
| Arquivo | Uso (cartão final, marca d'água, capa) | Fonte | Situação |
|---|---|---|---|

## Tom de voz
- Como fala (ex.: "como uma atendente fala", "sem termo técnico"):
- Palavras, sinais e construções proibidas (ex.: travessão largo, metáfora, "cara de IA"):
- Fonte / situação:

## Públicos
| Público | Situação de vida / dor | Como chamar na tela | Fonte | Situação |
|---|---|---|---|---|

## CTAs
| Texto na tela | Botão do anúncio | Destino (WhatsApp, site) | Quando usar | Fonte | Situação |
|---|---|---|---|---|---|

## Ofertas, valores e afirmações liberadas
| Afirmação / valor | Fonte no projeto | Situação |
|---|---|---|

## Regras visuais do projeto
(o que difere do padrão técnico da skill: faixa de legenda, trilha, selos, capa)

## Peças e lições
| Data | Peça | Aprovada/reprovada | Motivo dito pelo usuário |
|---|---|---|---|

## Conflitos a decidir
## Pendências (perguntas ao usuário)
## Histórico
## Histórico de mudanças
| Data | Item | Antes | Depois | Fonte |
|---|---|---|---|---|
```

## Modelo do `marca.json`

Caminhos relativos à pasta `marca/`. Só valores `confirmado` ou `extraído`.

```json
{
  "nome": "",
  "cores": {
    "principal": "#5B5A37",
    "fundo": "#FAF8F3",
    "texto_escuro": "#232A23",
    "destaque": "#FFE14D",
    "legenda": "#FFFFFF",
    "contorno": "#000000"
  },
  "fontes": {
    "legenda": "fontes/Poppins-ExtraBold.ttf",
    "titulo": "fontes/Poppins-Bold.ttf"
  },
  "logo_cartao_final": "logos/logo.png",
  "cta": {
    "tela": "CLIQUE EM\\NSAIBA MAIS",
    "cartao_linha1": "CLIQUE EM",
    "cartao_botao": "SAIBA MAIS"
  },
  "proibido_no_texto": ["—"]
}
```

`cores.principal` etc. são os papéis que `scripts/montar_video.py`,
`scripts/cartelas.py` e `scripts/capa.py` leem. Papel sem valor: o script para
e diz qual falta.
