# Abas da planilha "CAAMT – <Subseção>"

Cabeçalhos exatos: `scripts/planilha_local.py colunas`. Aqui fica o que cada coluna quer dizer.

## Linha editorial
Uma linha por tema. **Frequência**: fixa (ex.: "toda quarta", "2 por semana") ou "por
demanda" (ex.: convênio disponível, que entra quando um parceiro é aprovado); em branco até a
pessoa dizer ou os posts mostrarem.

## Cronograma
Uma linha por post. **Status**: ideia, pronto, publicado. **Tema** vem da aba Linha editorial.
**Arte (link)**: link do Drive ou caminho do arquivo (botão "Abrir arte"). **Evento na
agenda**: id do evento do lembrete do post. **Fonte**: de onde veio a informação do post.

## Pautas
Memória das pesquisas: uma linha por pauta, sempre com **Fonte** (URL). **Usada em**: data do
post do Cronograma que usou a pauta.

## Parceiros
Uma linha por parceiro. Colunas de documento: vazio = falta; "recebido 05/11" = chegou, falta
conferir; "ok 06/11" = conferido e válido; "problema: vencido" = conferido com problema (motivo
curto, sem dado pessoal); "não se aplica" quando é do outro tipo (PJ/PF). **Responsável**: nome de quem
responde pelo parceiro, usado nas mensagens. **Falta**: texto curto ("alvará, logo"), com o que
está vazio ou com problema, atualizado a cada documento. **Nível da cobrança**: vazio, 1, 2 ou 3 (1ª, lembrete,
última). **Próxima mensagem**: o rascunho pronto para copiar (vira o botão WhatsApp do painel).
**Pasta (link)**: link da pasta do parceiro no Drive ou caminho no computador (botão "Abrir pasta").
**Evento na agenda**: id do evento criado pela skill `caamt-agenda` (evita evento duplicado). Achar a linha pelo nome, sem
diferenciar maiúsculas nem acento; dois parecidos: perguntar qual. Etapas em
`caamt-parceiros/referencias/regras-caixa.md`.

## Config (chave, valor)
Chaves: Subseção, Cidades atendidas, Instagram pessoal da Delegada/do Delegado, Instagram da
subseção, Instagram da CAAMT, Link desta planilha, Pasta das artes no Drive. Preferências e
regras da pessoa não ficam aqui: vão para `memoria/regras.md`.

## Histórico
Só acrescentar, nunca editar. **Quem**: usuário ou Claude.
