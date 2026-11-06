# Lições que já custaram retrabalho

Cada uma com origem. Lição nova que vale para qualquer projeto entra aqui;
lição só de uma marca vai para o `MARCA.md` daquele projeto.

| # | Lição | Origem |
|---|---|---|
| 1 | Capa com sorriso de verdade, depois da fala. A boca começando a falar parece sorriso, mas quem vê percebe que não é. | edição anterior |
| 2 | Capa sempre própria. A miniatura automática do Meta sai 160x284 e borrada. | edição anterior |
| 3 | Legenda dentro de y 269 a 1248. Em y 1424 ficava coberta pela interface do Reels. | edição anterior |
| 4 | Legenda escrita à mão. A transcrição automática erra palavra e número, e o erro queimado todo mundo vê. | Projetos A e B |
| 5 | Fade de voz no máximo 0,3 s, só depois do fim da fala. Fade de 0,7 s comeu a última frase. | edição anterior |
| 6 | Não dissolver imagem que já tem texto queimado: três textos sobrepostos por 0,3 s. Texto entra uma vez, no fim. | edição anterior |
| 7 | Concat de arquivos com `-c copy` sobrepõe tempos e o `xfade` perde quadros. Uma passada com `concat` de filtros. | edição anterior |
| 8 | Som abaixo do padrão toca quase mudo no feed (criativos entre -18,9 e -31 LUFS). Sempre -14 LUFS medido no final. | edição anterior |
| 9 | Brutos do iPhone são HDR: sem tonemap a imagem fica acinzentada. | edição anterior |
| 10 | Selo claro sem caixa atrás sobre fundo claro: contraste 1,5:1, ilegível no sol. | edição anterior |
| 11 | Take que crava número (dias, prazo, valor) diferente do real não entra. | edição anterior |
| 12 | Imagem mostra o que o áudio promete. | edição anterior |
| 13 | Analisar áudio e imagem antes (subagentes em paralelo), mostrar ao usuário o que é dele decidir, depois montar. Esse método deu resultado bem melhor que montar direto. | Usuário, 26/09/2026 |
| 14 | Catalogar a mídia em `.md` antes de montar, para não reanalisar a cada sessão. | edição anterior |
| 15 | Texto na tela não pode soar como IA: sem metáfora, sem frase de efeito paralela. Escrever como a pessoa fala. | edição anterior |
| 16 | Revisão por quem não editou pegou o que o editor não viu. Revisor aponta só o que afeta o resultado. | Regra global do usuário |
| 17 | Texto queimado antigo (preço velho) não se apaga com remendo/clone da parede: em tamanho real vira retângulo liso com borda reta. Cobrir com faixa opaca da marca, largura total, e punch-in no plano para empurrar o texto antigo para dentro dela. | edição anterior |
| 18 | Vídeo de processo segue a ordem real de execução, tirada da data de criação no metadado (`creation_time`) e conferida com o número IMG. Um plano fora de ordem ("cena adiante no tempo") quebra a sensação de evolução. | edição anterior |
| 19 | Fala longa num take só pesa. Quebrar em frases curtas e espalhar pelos momentos que elas comentam. Tirar fala de assunto pessoal (atestado, saúde) mesmo que o usuário tenha aprovado a fala antes. | edição anterior |
| 20 | Versão enxuta não pode cortar a pergunta de um par pergunta/resposta. "E a resposta é? Não." depois de uma frase que não é pergunta não faz sentido. Ao enxugar, ler o texto montado em sequência e conferir que cada resposta tem a pergunta antes. | edição anterior |
| 21 | Antes do roteiro, definir quem publica, para quem e qual é a notícia. Quem aparece no vídeo (o parceiro, o vendedor) não é quem anuncia. Vídeo de parceiro da Caixa de Assistência destaca a nova parceria e o benefício para o advogado; roteiro com foco na empresa parceira foi reprovado. | Usuário, 03/11/2026 |

## Legenda não rouba a cena
A altura da legenda não é fixa. Na análise quadro a quadro, definir o que cada take quer mostrar (rosto, mãos, peça em foco, texto queimado) e posicionar a legenda por plano na área livre, dentro da faixa segura do Reels. O assunto em foco é mais importante que a legenda. Trocar a altura só na troca de plano ou de frase. Conferir com quadro de cada plano já legendado.
