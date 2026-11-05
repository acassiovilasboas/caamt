# Planilha "Parceiros CAAMT – <Subseção>"

## Como criar (com o "pode" da pessoa)

Crie pelo conector do Google Drive, mandando o conteúdo em CSV (`text/csv`, sem desligar a
conversão). O Google transforma em planilha. Crie as três abas:
- Se der para criar a planilha com uma aba só, crie com **Parceiros** e depois adicione **Config**
  e **Histórico** pelo conector do Sheets (adicionar aba + gravar cabeçalho).
- Se não der para adicionar abas, não crie três planilhas separadas. Peça para a pessoa
  clicar no "+" no rodapé da planilha e criar as abas Config e Histórico. Depois grave os
  cabeçalhos.

Depois de criar, leia de volta o cabeçalho para conferir. Guarde o link na aba Config.

## Aba Parceiros (uma linha por parceiro)

Cabeçalho, nesta ordem:
```
Parceiro,Tipo (PJ/PF),Categoria,Cidade,Responsável,WhatsApp/Telefone,Benefício,Etapa,Carta proposta,Alvará (PJ),CNPJ (PJ),Comprovante de endereço (PF),Documento com foto,Logo JPG,Tabela de valores (opcional),Falta,Próxima mensagem,Última cobrança,Nível da cobrança,Próxima ação,Data da próxima ação,Atualizado em,Observações
```
- Colunas de documento: vazio = não recebido; "recebido 05/11" = recebido; "não se aplica"
  quando é coluna do outro tipo (PJ/PF).
- **Falta:** texto curto calculado por você ("alvará, logo"). Atualize sempre que mudar um
  documento.
- **Nível da cobrança:** vazio, 1, 2 ou 3 (1ª, lembrete, última).
- **Atualizado em:** data da última mudança na linha.
- Achar a linha pelo nome do parceiro, sem diferenciar maiúsculas nem acento. Se houver dois
  parecidos, pergunte qual.

## Aba Cronograma e aba Pautas
Colunas na skill `caamt-cronograma`. Criar junto com as outras abas.

## Modo local (sem Drive)
Um CSV por aba em `planilha/` (`parceiros.csv`, `cronograma.csv`, `pautas.csv`, `config.csv`,
`historico.csv`), UTF-8 com BOM e separador vírgula. Mesmas colunas e mesmas regras de gravação.
Ler o arquivo antes de gravar: a pessoa pode ter editado no Excel.

## Aba Config (chave, valor)

```
Chave,Valor,Atualizado em
Subseção,,
Cidades atendidas,,
Instagram pessoal da Delegada/do Delegado,,
Instagram da subseção,,
Instagram da CAAMT,,
Link desta planilha,,
Pasta das artes no Drive,,
Preferências,,
```
Preferência nova vira uma linha "Preferências" com o texto e a data. A mais recente vale.

## Aba Histórico (só acrescentar, nunca editar)

```
Data,Parceiro,O que mudou,De,Para
```

## Regras de gravação
- Leia antes de gravar. Grave só as células que mudaram (intervalo exato, ex.: `Parceiros!J7`).
- Linha nova: acrescentar no fim, nunca sobrescrever.
- Nada de número de CPF, RG ou outro documento em nenhuma aba.
