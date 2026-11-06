# Receita: vídeo de parceiro da CAAMT (Caixa de Assistência dos Advogados de Mato Grosso)

Regra de negócio da CAAMT para vídeo de parceiro.

## Quem fala, para quem, para quê

- **Quem publica:** a CAAMT, no perfil da subseção ou da OAB local. A Delegada ou o
  Delegado da CAAMT na Subseção é a voz principal.
- **Para quem:** advogados e advogadas inscritos na OAB/MT da região.
- **Objetivo:** mostrar **o benefício que a CAAMT trouxe para a advocacia**. A notícia é
  "a CAAMT fechou uma **nova parceria**", não "conheça a empresa X".
- **O parceiro é o assunto, não o anunciante.** Se o vídeo ficar com cara de propaganda do
  parceiro (foco na empresa, nas vendas dela, no vendedor), o roteiro está errado.
  Seria certo só se o vídeo fosse para o perfil do parceiro, e não é.

## Estrutura do roteiro

1. **Gancho (0 a 3 s): destaque da nova parceria.** Na tela: "NOVA PARCERIA" ou "CONVÊNIO
   CAA/MT" + nome do parceiro + o benefício em poucas palavras (ex.: "plano de saúde com valor
   diferenciado para a advocacia"). Na fala: o trecho em que o(a) delegado(a) anuncia o convênio
   com a CAAMT.
2. **O benefício concreto para o advogado:** desconto, valor diferenciado, condição especial,
   quem pode usar (dependentes?), região atendida.
3. **Como aderir:** contato, endereço, link. Só com fonte (o número falado sem estar escrito no
   projeto vira pendência para o usuário).
4. **Fechamento:** "mais uma vantagem da CAAMT" (ou a frase equivalente que a
   pessoa falou) + cartão final com os logos da OAB da subseção e da CAAMT.

Fala do parceiro entra só se reforça o benefício (ex.: abrangência, condição). História da
negociação, agradecimentos longos e bastidores saem.

## Travas

- **Condição com data** (promoção do mês, "sem carência em fevereiro"): conferir se ainda vale.
  Vencida não entra. Na dúvida, perguntar.
- Valor, percentual, prazo ou telefone na tela: só com fonte ou aprovação do usuário.
- Nome e cargo de quem aparece: confirmar com o usuário antes de queimar na tela.
- Vídeo antigo ("Fevereiro chegou" num vídeo publicado em novembro): avisar a data.

## Artes (modelo `modelos/caamt/` da skill)

- Moldura de Stories "Convênio CAA/MT" (padrão para nova parceria) ou "Empresa conveniada".
  O vídeo fica por baixo e o PNG transparente fica por cima. Área livre para texto e legenda:
  **y 200 a 1550**. A faixa de logos começa em y 1604. A linha diagonal sobe pela direita
  até y≈1250, então nada de texto no canto inferior direito acima da faixa. A borda
  esquerda é fina.
- Rodapé com logos (CAAMT + OAB + nome da subseção), de y 1458 para baixo: usar no **cartão
  final** ou em vídeo sem moldura. **É da subseção do usuário**, porque cada delegado(a) é de uma
  cidade. O arquivo de Barra do Garças que vem no kit é só exemplo: usar o rodapé que o usuário
  enviou. Se não tiver, avisar e não usar o de outra cidade.
- Texto do post e legenda: seguir o padrão "Convênio Disponível" de `modelos/caamt/MARCA.md`.
  O vídeo segue a mesma ordem do post: nova parceria, depois o benefício, depois o contato.

## Perguntar em cada post (uma mensagem só, antes do roteiro)

Pular o que já estiver claro no material ou no pedido.
1. Qual é o parceiro e qual o benefício para o advogado (desconto, condição, dependentes)?
   Tem prazo?
2. Contato e endereço que vão no fim (do parceiro, da CAAMT ou da subseção)?
3. O post sai em colaboração? Com quais perfis?

## Desta subseção (preencher no primeiro uso)

- Subseção / cidades:
- Perfis (pessoal, subseção, CAAMT):
- Rodapé e artes: `Edicao-Video/CAAMT-<subseção>/marca/logos/`
- Cores medidas nas artes: roxo `#562094`, azul `#33229B`, magenta `#C71279`, roxo escuro `#831C8A`.
