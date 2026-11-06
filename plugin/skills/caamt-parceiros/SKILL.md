---
name: caamt-parceiros
description: "Gestão dos parceiros (convênios) da subseção da CAAMT na aba Parceiros da planilha, da prospecção à divulgação. Use quando a pessoa falar de parceiro, convênio, conveniado, prospecção, cobrar ou retomar parceiro, quem está pendente, status dos convênios ou resumo da semana."
---

# Parceiros

A pessoa fala do jeito dela ("comecei a conversar com a doceria X", "chegou o alvará da
clínica", "cobra a ótica"). Você entende, atualiza a planilha e entrega o próximo passo.

Ler antes: `referencias/regras-caixa.md` (documentos oficiais e etapas),
`caamt-planilha/referencias/abas.md` (colunas) e `referencias/mensagens.md` (modelos). Ler e
gravar a planilha: skill `caamt-planilha`. Pastas: skill `caamt-arquivos`.

## Pedidos comuns
| Como ela fala | O que fazer |
|---|---|
| "Comecei com a empresa X, 10% para advogados" | Linha nova, Etapa "Prospecção"; criar `parceiros/<X>/` (no Drive, pelo conector: `caamt-arquivos`); mostrar a sequência de mensagens (1ª: documentos e onde conseguir; 2ª: convencimento) |
| "Chegou o CNPJ da X" | Marcar "recebido <data>" (falta conferir), recalcular "Falta"; oferecer a conferência |
| "Os documentos da X estão ok?" | Skill `caamt-documentos` |
| "Quem está pendente?" | Conferir planilha × pastas (abaixo); depois a tabela curta: parceiro, etapa, falta, dias parado (do mais atrasado) |
| "Cobra a X" | Mensagem no nível certo: contar no Histórico as mudanças de "Última cobrança" desde "Na etapa desde" (0 = 1ª, 1 = lembrete, 2 ou mais = última). Histórico sem cobrança mas "Última cobrança" preenchida (planilha antiga), ou coluna antiga "Nível da cobrança": não presumir a 1ª; usar o nível antigo ou perguntar qual foi a última mensagem. Anotar a data e a próxima |
| "Retomar quem não fechou" | Quem está em "Não fechou" ou parado há mais de 30 dias: uma retomada para cada |
| "Foi aprovado" / "já postei" | Mudar a Etapa; em Aprovado, oferecer o post (`caamt-criativo` + `caamt-legenda`) |
| "Resumo da semana" | Parceiros por etapa, o que andou em 7 dias, as 3 próximas ações |

## Conferir planilha × pastas (pendências, resumo, cobrança)
A planilha pode estar atrasada em relação ao que chegou. Antes de responder, ler também as pastas
`parceiros/<Parceiro>/`, onde a pessoa guarda os arquivos (ver `memoria/perfil.md`):
- **Drive:** pelo conector do Google Drive (buscar a pasta `parceiros` e listar os arquivos de
  cada parceiro). Sem o conector: pedir para ligar (Personalizar › Conectores) e, até lá,
  responder só pela planilha, dizendo isso em uma linha.
- **Computador:** listar a pasta (Glob), sem abrir o conteúdo.

Pelo nome do arquivo, ligar cada um ao documento da lista oficial. Na resposta, antes da tabela,
uma seção **"Planilha e pastas não batem"** com cada divergência: arquivo na pasta que a planilha
não marca como recebido; recebido na planilha sem arquivo na pasta; pasta sem linha na planilha;
linha sem pasta. Não corrigir a planilha sozinho: propor a correção e gravar só com o OK. Abrir e
conferir o conteúdo é da skill `caamt-documentos`. Começar a resposta dizendo o que foi lido
("Li a planilha e as pastas dos parceiros no Drive").

## Regras
- Confirmar em uma linha o que vai mudar; gravar só as células que mudaram; toda mudança vira
  uma linha no Histórico.
- Contato e benefício: gravar tudo o que a pessoa contar (telefones, e-mail, Instagram e outras
  redes, site, endereço do negócio, descontos, cupom ou voucher, como usar, validade). Faltou algum dado?
  Perguntar uma vez, em uma frase, o que falta; sem resposta, a célula fica vazia.
- Mudou a Etapa: gravar a data em "Na etapa desde".
- Mensagem usa o nome do **Responsável** do parceiro. Não tem? Perguntar uma vez, na hora da
  primeira mensagem, e gravar.
- Mensagem é rascunho: quem envia é a pessoa. Fica também na coluna Próxima mensagem, pronta
  para copiar.
- A planilha guarda só **se** recebeu e **quando**. Nunca número de CPF, RG ou outro documento.
- Fim de cada resposta: o próximo passo em uma linha.
