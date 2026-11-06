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
| "Comecei com a empresa X, 10% para advogados" | Linha nova, Etapa "Prospecção"; criar `parceiros/<X>/` (no Drive, só pelo script: `caamt-arquivos`); mostrar a sequência de mensagens (1ª: documentos e onde conseguir; 2ª: convencimento) |
| "Chegou o CNPJ da X" | Marcar "recebido <data>" (falta conferir), recalcular "Falta"; oferecer a conferência |
| "Os documentos da X estão ok?" | Skill `caamt-documentos` |
| "Quem está pendente?" | Tabela curta: parceiro, etapa, falta, dias parado (do mais atrasado) |
| "Cobra a X" | Mensagem no nível certo (1ª, lembrete, última) pelo Histórico; anotar a data e a próxima |
| "Retomar quem não fechou" | Quem está em "Não fechou" ou parado há mais de 30 dias: uma retomada para cada |
| "Foi aprovado" / "já postei" | Mudar a Etapa; em Aprovado, oferecer o post (`caamt-criativo` + `caamt-legenda`) |
| "Resumo da semana" | Parceiros por etapa, o que andou em 7 dias, as 3 próximas ações |

## Regras
- Confirmar em uma linha o que vai mudar; gravar só as células que mudaram; toda mudança vira
  uma linha no Histórico.
- Mensagem usa o nome do **Responsável** do parceiro. Não tem? Perguntar uma vez, na hora da
  primeira mensagem, e gravar.
- Mensagem é rascunho: quem envia é a pessoa. Fica também na coluna Próxima mensagem, pronta
  para copiar.
- A planilha guarda só **se** recebeu e **quando**. Nunca número de CPF, RG ou outro documento.
- Fim de cada resposta: o próximo passo em uma linha.
