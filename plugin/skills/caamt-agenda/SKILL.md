---
name: caamt-agenda
description: "Lembretes na agenda da pessoa (Google Agenda ou outra agenda com conector no Claude) para os prazos do kit CAAMT: cobrar ou retomar parceiro, data de post, prazo de documento. Use quando uma data de próxima ação ou de post for gravada ou mudar, ou quando a pessoa pedir lembrete, aviso ou agenda."
---

# Agenda e lembretes

O celular avisa pela agenda da própria pessoa. O Claude cria o evento; ninguém precisa abrir o
Claude para lembrar.

## Qual agenda
1. Ver quais conectores de agenda estão ligados nesta sessão (Google Agenda, Outlook ou outro).
   Um só: usar. Mais de um: perguntar uma vez qual e gravar em `memoria/perfil.md` (Agenda:).
2. Nenhum: dizer em uma linha "Para eu te avisar no celular, ligue a sua agenda em Personalizar ›
   Conectores (Google Agenda, por exemplo)" e anotar o lembrete em `memoria/pendencias.md`.
   Enquanto isso, no começo de cada conversa, mostrar o que venceu ou vence em 3 dias.

## Criar ou mudar o evento
- Quando: data da próxima ação (aba Parceiros) ou data do post (aba Cronograma), às 9h, ou o
  horário que a pessoa preferir (`memoria/regras.md`). Lembrete: na hora e 1 dia antes.
- Título curto e claro: "Cobrar documentos · <Parceiro>", "Postar · <Pauta>",
  "Retomar · <Parceiro>".
- Descrição: o que fazer em uma linha, o link do WhatsApp com a mensagem pronta (`https://wa.me/55...`,
  só se houver telefone e mensagem) e o link da pasta ou da arte, com nome ("Pasta do parceiro").
- Gravar o id do evento na coluna "Evento na agenda" (skill `caamt-planilha`).
- Data mudou: **atualizar o mesmo evento**, não criar outro. Ação feita ou parceiro fora:
  perguntar antes de apagar o evento.
- Confirmar em uma linha: "Lembrete na sua agenda: 10/11, 9h, Cobrar documentos · Clínica X."

Nunca convidar outras pessoas para o evento nem mudar evento que o kit não criou.
