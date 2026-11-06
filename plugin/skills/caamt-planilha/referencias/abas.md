# Abas da planilha "CAAMT – <Subseção>"

Cabeçalhos exatos: `scripts/planilha_local.py colunas`. Aqui fica o que cada coluna quer dizer.

## Linha editorial
Uma linha por tema. **Frequência**: fixa (ex.: "toda quarta", "2 por semana") ou "por
demanda" (ex.: convênio disponível, que entra quando um parceiro é aprovado); em branco até a
pessoa dizer ou os posts mostrarem.

## Cronograma
Uma linha por post. **Status**: ideia, pronto, publicado. **Tema** vem da aba Linha editorial.
**Arte (link)**: link do Drive ou caminho do arquivo. **Evento na
agenda**: id do evento do lembrete do post. **Fonte**: de onde veio a informação do post.

## Pautas
Memória das pesquisas: uma linha por pauta, sempre com **Fonte** (URL). **Usada em**: data do
post do Cronograma que usou a pauta.

## Parceiros
Uma linha por parceiro. Colunas de documento: vazio = falta; "recebido 05/11" = chegou, falta
conferir; "ok 06/11" = conferido e válido; "problema: vencido" = conferido com problema (motivo
curto, sem dado pessoal); "não se aplica" quando é do outro tipo (PJ/PF). **Responsável**: nome de quem
responde pelo parceiro, usado nas mensagens. **WhatsApp/Telefone**: o número do WhatsApp do responsável; os outros
números vão em **Outros telefones**. **Instagram**: o @ do parceiro; Facebook, TikTok e outras em
**Outras redes**. **Benefício**: os descontos e vantagens para a advocacia ("15% em consultas, 10% em
exames"). **Cupom ou voucher**: o código, se tiver. **Como usar**: o que o advogado faz para ter o
benefício ("apresentar a carteira da OAB"). **Endereço**: o endereço público do negócio
(onde o advogado vai para usar o benefício). Nunca endereço residencial nem tirado de documento. **Validade do benefício**: data, se tiver. **Na etapa
desde**: data em que entrou na Etapa atual (muda junto com a Etapa). **O que está travando**: a
dificuldade nas palavras da pessoa ("não acha o alvará novo"); apagar quando resolver. **Falta**: texto curto ("alvará, logo"), com o que
está vazio ou com problema, atualizado a cada documento. **Próxima mensagem**: o rascunho pronto para copiar e mandar no WhatsApp.
**Pasta (link)**: link da pasta do parceiro no Drive ou caminho no computador.
**Evento na agenda**: id do evento criado pela skill `caamt-agenda` (evita evento duplicado). Achar a linha pelo nome, sem
diferenciar maiúsculas nem acento; dois parecidos: perguntar qual. Etapas em
`caamt-parceiros/referencias/regras-caixa.md`.

## Config (chave, valor)
Chaves: Subseção, Cidades atendidas, Instagram pessoal da Delegada/do Delegado, Instagram da
subseção, Instagram da CAAMT, Link desta planilha, Pasta das artes no Drive. Preferências e
regras da pessoa não ficam aqui: vão para `memoria/regras.md`.

## Histórico
Só acrescentar, nunca editar. **Quem**: usuário ou Claude.
