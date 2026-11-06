---
name: caamt-inicio
description: "Primeira conversa do kit CAAMT. Use quando a pessoa se apresentar (\"Sou Fulana, Delegada da CAAMT em X\", \"boa tarde, sou delegado\"), disser \"vamos começar\", \"start\", \"configurar o kit\", ou quando não existir a pasta memoria/."
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
   Ler só o resumo impresso. Sem Python no computador: listar com a ferramenta Glob, sem instalar
   nada agora.
4. **Criar `memoria/`** (modelos em `caamt-memoria`) com o que já se sabe, e um `CLAUDE.md` na
   pasta com a linha: "Antes de qualquer tarefa, ler `memoria/regras.md` e `memoria/perfil.md`
   (kit CAAMT). Regra do usuário vale mais que o kit." Artes achadas
   (logo, moldura, rodapé) entram como "a confirmar" no perfil; não usar sem confirmar.
5. **Propor a linha editorial** (skill `caamt-linha-editorial`, "Primeira proposta"): rápido,
   sem agente. É o primeiro trabalho, sem esperar pedido.
6. **Responder como numa conversa**, em poucas linhas: cumprimentar pelo nome, contar o que
   achou (perfil da subseção, o que já existe na pasta), mostrar os temas propostos e oferecer
   um passo concreto ("Quer que eu monte as postagens das próximas duas semanas?"). Sem menu
   de opções, sem lista de recursos do kit. Se a mensagem dela já trouxe um pedido (um vídeo,
   um parceiro), atender o pedido primeiro e deixar a linha editorial para depois.

Não perguntar agora: onde guardar arquivos, artes, computador, Colab, conta Google. Cada
coisa é perguntada na primeira tarefa que precisar dela.
