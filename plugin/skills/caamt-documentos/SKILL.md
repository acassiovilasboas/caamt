---
name: caamt-documentos
description: Confere os documentos que um parceiro mandou para o convênio com a CAAMT (na pasta do parceiro, no Drive ou no computador, ou numa foto na conversa) e devolve o que falta ou está errado com a mensagem pronta. Use quando a pessoa perguntar se os documentos estão ok, mandar documento para conferir, ou antes de enviar à CAAMT.
---

# Conferir documentos do parceiro

1. Achar a pasta `parceiros/<Parceiro>/` (local ou Drive, ver `caamt-arquivos`) e a linha
   dele na planilha (tipo PJ ou PF).
2. Mandar o agente `documentos-conferente` com: a pasta, o tipo (PJ/PF) e a lista oficial de
   `caamt-parceiros/referencias/regras-caixa.md`. Muitos arquivos ou PDFs grandes: sempre pelo
   agente, para não encher a conversa.
3. Responder com a tabela que ele devolver (documento, situação, motivo) e:
   - o que falta ou está errado: mensagem pronta para o parceiro (`mensagens.md`, nível certo);
   - tudo certo: "pronto para enviar à CAAMT" e o link do formulário.
4. Na planilha: marcar "recebido <data>" só no que passou. Etapa "Documentos completos" quando
   não faltar nada.

Sigilo: não copiar número de CPF, RG, CNPJ ou endereço de pessoa para a planilha nem para a
resposta. Dizer só "documento com foto: legível, válido".
