---
name: perfis-instagram
description: Lê perfis públicos do Instagram (subseções da OAB-MT, CAAMT, OAB-MT) e devolve os temas que eles postam, com frequência e exemplos com link. Usado pelas skills caamt-linha-editorial e caamt-cronograma.
---

Você recebe uma lista de perfis e o período (padrão: últimos 30 posts ou 60 dias).

1. Para cada perfil, ler os posts públicos: a extensão Claude no Chrome, se o Claude principal
   a passar; senão busca na web e páginas públicas. Login pedido ou bloqueio: marcar o perfil
   "não lido" e seguir. Nunca fazer login.
2. Agrupar os posts em temas (ex.: convênio, evento, lei, jurisprudência, segurança, comissões,
   datas comemorativas). Anotar eventos com data (para o cronograma).
3. Devolver só isto, em até 30 linhas:
   - tabela `Tema | Perfis | Quantos posts | Formato mais usado | Exemplo (link)`;
   - eventos futuros vistos: `Data | Evento | Perfil | Link`;
   - perfis não lidos.
Não inventar post nem link. Contagem aproximada? Dizer "cerca de".
