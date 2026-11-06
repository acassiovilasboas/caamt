# Biblioteca de imagens do kit

Imagens para dar vida aos posts: pessoas, ambientes e objetos. Todas são **geradas por IA**
(Gemini) e não mostram pessoas reais: nunca apresentar como foto de advogado ou de delegado de
verdade. O Instagram pode marcar o post como "Conteúdo de IA"; isso é esperado.

A pessoa pode pedir para usar ou não usar a biblioteca, ou só algumas imagens. A regra dela fica
em `memoria/regras.md` e vale mais que este catálogo. A subseção pode acrescentar imagens próprias
em `CAAMT-<Subseção>/biblioteca/`, com uma linha nova no catálogo dela (mesmas colunas).

Foco = ponto que não pode sair do corte (x,y de 0 a 1), usado no `--foco` do `fundo.py`.

| Arquivo | O que mostra | Pessoa | Foco | Bom para | Evitar |
|---|---|---|---|---|---|
| `advogado-terno-azul-estante.jpg` | Advogado sorrindo, terno azul, estante de livros jurídicos, balança na mesa | homem, 40-50 anos | 0.58,0.28 | lei nova, Quarta de Lei, benefícios, Dia do Advogado | alerta de golpe |
| `advogada-janela-cidade.jpg` | Advogada sorrindo, blazer cinza-azulado, janela com prédios ao fundo | mulher, 40-50 anos | 0.50,0.25 | benefícios da CAAMT, auxílio-maternidade, comissões, Comissão da Mulher Advogada | alerta de golpe |
| `advogado-aperto-de-mao.jpg` | Advogado estendendo a mão sobre a mesa, escritório claro | homem negro, 35-45 anos | 0.50,0.30 | convênio disponível, parceria nova, boas-vindas, atendimento | aviso sério ou triste |
| `advogada-pasta-escritorio-claro.jpg` | Advogada sorrindo segurando pasta, escritório claro com estante | mulher negra, 30-40 anos | 0.50,0.28 | benefícios, eventos, comissões, Comissão da Mulher Advogada | alerta de golpe |
| `celular-ligacao-no-carro.jpg` | Mão segurando celular em ligação ("Mãe"), dentro do carro | sem rosto | 0.48,0.55 | alerta de golpe, ligação falsa, golpe do falso advogado, segurança | benefícios, datas festivas |

Tratamentos que funcionam com estas imagens (detalhe no agente `diretor-de-arte`):
- **Pessoas:** `topo` (rosto nítido em cima, texto embaixo) ou `lado` (pessoa à direita).
- **Muito texto** (passo a passo, lei): `fundo` com força 0.6 a 0.75, para a foto ficar atrás.
- **Celular:** `fundo` ou `duotone`; o texto da tela do celular não deve competir com o título.
