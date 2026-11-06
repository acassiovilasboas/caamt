---
name: caamt-cronograma
description: "Cronograma de postagens da subseção na aba Cronograma da planilha, com pautas pesquisadas na aba Pautas. Use quando a pessoa falar em cronograma, calendário, planejar o mês, \"o que postar esta semana\", evento na cidade, ou quando um post for feito ou publicado."
---

# Cronograma de postagens

## Colunas (aba Cronograma)
`Data | Tema | Pauta | Formato | Roteiro | Legenda | Hashtags | Primeiro comentário | Arte (link) | Status | Fonte | Atualizado em`
Status: ideia, pronto, publicado. Tema vem da aba Linha editorial (ler antes), respeitando a
Frequência de cada tema; tema "por demanda" (ex.: convênio) só entra quando houver o fato.
Ler e gravar sempre pela skill `caamt-planilha`. A planilha não existe ainda: ela cria.

## Montar ou estender
1. Ler a aba Linha editorial, a aba Cronograma (o que já existe) e `memoria/` (rotina: dias e
   horários em que a pessoa posta).
2. Eventos: os que a pessoa contar e os vistos nos perfis públicos (agente `perfis-instagram`).
   Cada evento ganha posts **antes** (convite), **no dia** (Stories) e **depois** (cortes, fotos).
3. Pautas de fora (segurança na advocacia, lei nova, jurisprudência, benefício da CAAMT):
   agente `pauta-pesquisador` (fontes em `referencias/fontes.md`, a mais recente primeiro). Cada
   pauta vira uma linha na aba Pautas (`Data | Tema | Título | Fonte | Resumo | Usada em`).
   **Toda sugestão de post vinda de pauta é mostrada com o link validado**, para a pessoa
   conferir antes. Sem link validado, não entra.
4. Gravar só as linhas novas ou as células que mudaram. Mostrar as próximas 2 semanas numa
   tabela curta.

## Atualizar
- Antes de dizer o que está pronto ou faltando: conferir cada linha com `publicacoes/<data>_<tema>/`
  (Drive ou computador). Arte na pasta e Status "ideia", ou Status "pronto" sem arte: mostrar e
  propor a correção (regra 4 de `caamt-memoria`).
- A pessoa muda a planilha à mão: respeitar. Pede pelo chat: mudar só o pedido.
- O Claude percebe (post publicado, evento novo, data passada sem post): atualizar o Status ou
  sugerir a troca e avisar em uma linha.
- Formato é sugestão: "não quero gravar vídeo" vira post de texto com foto de fundo
  (skill `caamt-criativo`).

## Fazer o post de uma linha
Arte: `caamt-criativo`. Textos: `caamt-legenda`. Depois gravar o link da arte e Status "pronto".
