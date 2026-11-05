---
name: caamt-instagram
description: Instagram da subseção: ler perfis públicos para pautas e linha editorial e, quando configurado, publicar, responder e curtir comentários. Use quando a pessoa pedir para analisar perfis, ver o que outras subseções postam, publicar, agendar, responder ou curtir comentário.
---

# Instagram

## Ler perfis (para linha editorial e cronograma)
Agente `perfis-instagram`. Perfis conhecidos: `caamt-memoria/dados/subsecoes.md`.

## Publicar, responder, curtir
Exige ligar o Instagram por API da Meta, uma vez: conta profissional ligada a uma Página do
Facebook e um token. Se a skill `meta-api-token` estiver instalada, seguir ela. Se não, dizer
o que falta e oferecer o caminho manual (baixar a arte do Drive no celular e postar).

Com o token configurado:
- Publicar: a Meta pede a imagem ou o vídeo num **endereço público**. O kit ainda não testou
  isso com o Drive. Antes da primeira publicação, testar com a pessoa e anotar o que funcionou
  em `memoria/aprendizados.md`.
- Toda publicação, resposta ou curtida só depois do OK da pessoa para aquele item. Mostrar
  o texto exato antes.
- Depois de publicar: Status "publicado" no Cronograma.
