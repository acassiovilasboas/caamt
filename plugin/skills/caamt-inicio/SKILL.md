---
name: caamt-inicio
description: Primeira conversa do kit CAAMT. Use quando a pessoa se apresentar ("Sou Fulana, Delegada da CAAMT em X", "boa tarde, sou delegado"), disser "vamos começar", "start", "configurar o kit", ou quando não existir a pasta memoria/.
---

# Início

Objetivo: em poucos minutos, entender quem é a pessoa e o que já existe na pasta, **sem
questionário**. O resto se aprende no uso (skill `caamt-memoria`).

1. **Já existe `memoria/perfil.md`?** Não é a primeira vez: cumprimentar pelo nome, dizer em
   2 linhas o que está pendente (`memoria/pendencias.md`) e atender o pedido.
2. **Da própria mensagem**, tirar nome, cargo e subseção. Completar com
   `caamt-memoria/dados/subsecoes.md` (número da subseção, cidades, Instagram, e-mail da
   CAAMT). Não achou a subseção? Perguntar só isso.
3. **Olhar a pasta** (sem abrir conteúdo):
   `python <skill>/scripts/varrer_pasta.py . --saida memoria/inventario.md`
   Ler só o resumo impresso.
4. **Criar `memoria/`** (modelos em `caamt-memoria`) com o que já se sabe. Artes achadas
   (logo, moldura, rodapé) entram como "a confirmar" no perfil; não usar sem confirmar.
5. **Começar a linha editorial** (skill `caamt-linha-editorial`): rascunho a partir dos
   perfis de Instagram conhecidos. É o primeiro trabalho, sem esperar pedido.
6. **Responder em até 8 linhas**: o que entendi (nome, subseção, perfis); o que achei na
   pasta; o rascunho da linha editorial; e "o que quer fazer primeiro: vídeo, post,
   parceiro ou cronograma?".

Não perguntar agora: onde guardar arquivos, artes, computador, Colab, conta Google. Cada
coisa é perguntada na primeira tarefa que precisar dela.
