---
name: caamt-painel
description: "Painel da subseção no navegador (o que a pessoa vê da planilha): hoje, postagens, parceiros, temas e pautas, com botões de WhatsApp, copiar e abrir. Use depois de qualquer mudança na planilha e quando a pessoa pedir para ver, abrir ou acompanhar o que está pendente."
---

# Painel

1. Dados:
   - computador: a pasta `planilha/` (skill `caamt-planilha`);
   - Drive: ler as abas pelo conector e gravar uma cópia em `memoria/espelho/<aba>.csv`, com os
     nomes e colunas de `caamt-planilha/scripts/planilha_local.py colunas`.
2. `python <skill>/scripts/painel.py <pasta dos csv> <pasta CAAMT>/painel.html`
3. Dar o caminho do `painel.html` (abre com duplo clique) e dizer em uma linha o que mudou.

O painel só mostra o que está na planilha. Não acrescentar texto explicativo nem dado de exemplo.
Link sempre com nome ("Abrir pasta", "Abrir arte"), nunca o endereço cru. Ajuste de visual que a
pessoa pedir: `memoria/regras.md`, e aplicar no painel.
