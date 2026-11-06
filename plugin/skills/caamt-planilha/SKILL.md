---
name: caamt-planilha
description: "Única dona da planilha de trabalho da subseção (abas Linha editorial, Cronograma, Pautas, Parceiros, Config, Histórico): acha, cria na hora em que for útil e grava só o que mudou, no Google Drive ou no computador. Use sempre que outra skill do kit precisar ler ou gravar na planilha, ou quando a pessoa falar em planilha."
---

# Planilha da subseção

A planilha é a memória e o banco de dados do Claude. A pessoa conversa com o Claude e, quando quiser,
abre a planilha para consultar: ela precisa ser fácil de ler por gente.
Nome: **"CAAMT – <Subseção>"**. Colunas de cada aba: `python <skill>/scripts/planilha_local.py colunas`
(vale para o Drive e para o computador). Significado das colunas: `referencias/abas.md`.

## Achar
`memoria/perfil.md` tem `planilha:` com o id do Drive ou `local`. Não tem: a planilha ainda não
existe. Não criar "por garantia".

## Criar (só quando a conversa precisar guardar algo nela)
1. Primeira vez? Perguntar junto, numa frase natural: "Vou deixar isso numa planilha. Prefere no
   seu Google Drive, que abre no celular, ou aqui no computador?" (gravar a escolha no perfil;
   se já está no perfil, não perguntar).
2. **Drive**, com os conectores do Google Drive e do Google Sheets ligados: criar pelo conector do
   Drive (CSV com o cabeçalho da primeira aba, `text/csv`, convertido em planilha), dentro da
   pasta `CAAMT-<Subseção>`. Adicionar as outras abas pelo conector do Sheets e gravar os
   cabeçalhos. Ler de volta para conferir. **Formatar uma vez:** montar o `abas.json` com o
   sheetId e o cabeçalho de cada aba, rodar `python <skill>/scripts/formatar.py drive abas.json` e
   mandar a lista que ele imprime no `update_spreadsheet`. Guardar o id no perfil e o link na aba
   Config. Ao terminar, mandar o link da planilha.
3. **Computador**, ou Drive sem o conector do Sheets: `planilha_local.py criar <pasta CAAMT>`.
   Cria `planilha/planilha.xlsx` já formatado (abre no Excel). Precisa do openpyxl (gratuito):
   faltando, pedir o "pode" e rodar `pip install openpyxl`. Quem tinha a planilha antiga em CSV:
   o `criar` copia os dados para o Excel e deixa os CSV na pasta. Planilha aberta no Excel não
   aceita gravação: pedir para fechar. Gráfico ou imagem colados em `planilha.xlsx` se perdem ao
   gravar: o script recusa e pede para tirar (podem ficar numa cópia).
   No segundo caso, dizer em uma linha: "Liguei a planilha aqui no computador porque o conector do
   Google Sheets não está ativo; quando ligar, eu passo para o Drive."

## Gravar (todas as skills passam por aqui)
- Ler antes. Gravar **só as células que mudaram**; linha nova vai no fim. Nunca regravar a
  planilha ou a aba inteira: a pessoa pode ter editado à mão, e o que ela escreveu vale.
- Drive: conector do Sheets, intervalo exato (ex.: `Cronograma!J7`). A letra da coluna sai do
  cabeçalho da própria planilha, lido na hora: planilha antiga tem outra ordem e as colunas novas
  no fim. Nunca contar pela ordem de `planilha_local.py colunas`. Computador:
  `planilha_local.py mudar` / `nova` (já registram o Histórico).
- No Drive, registrar cada mudança na aba Histórico (data, aba, item, o que mudou, de, para,
  quem: usuário ou Claude).
- Coluna nova do kit (lista de `planilha_local.py colunas`) que a planilha ainda não tem: acrescentar
  no fim do cabeçalho, sem mexer no resto. Computador: `planilha_local.py criar` já faz isso. Drive:
  ao abrir, comparar o cabeçalho e gravar só as colunas que faltam.
- Aba Parceiros: linha nova ou Etapa que mudou leva a data de hoje em "Na etapa desde"
  (no computador, `nova` e `mudar` já fazem isso).
- **Só dado real.** Nunca gravar linha de exemplo, parceiro fictício, telefone ou data inventados.
  Faltou um dado (telefone, data, link da pasta)? Perguntar à pessoa antes; sem resposta, a
  célula fica vazia.
- Data com prazo (próxima ação, data do post): avisar a agenda (skill `caamt-agenda`).
- Nada de CPF, RG ou número de documento em nenhuma aba.

