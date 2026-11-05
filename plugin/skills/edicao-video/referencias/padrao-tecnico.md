# Padrão técnico

Valores medidos e usados em vídeos aprovados (set/2026). São o ponto de partida;
o `MARCA.md` do projeto e as lições do usuário mandam onde divergirem.

## Saída
- 1080x1920, 30 fps, H.264 `crf 17` `preset medium` na CPU (na GPU: NVENC `cq 19`,
  escolhido sozinho por `ambiente.codificador_args`), `yuv420p`, bt709 marcado
  (`-color_primaries bt709 -color_trc bt709 -colorspace bt709`), `+faststart`.
- AAC 192k, 48 kHz, mono se os canais do bruto forem desbalanceados.
- Nome: `final\<NN>_<NOME>_V<n>.mp4`.

## Faixas da tela (1080x1920)
- **Faixa livre do Reels: y 269 a 1248.** Topo ~14% e rodapé ~35% ficam cobertos pela interface.
- Faixa de cima (y ~300 a 600): gancho, selos, CTA.
- Legenda: base em y 1248 (fica no peito, abaixo do queixo). Quando o plano tem
  conteúdo importante embaixo (papel, produto, mão), a legenda sobe para logo
  abaixo dos selos (`\an8`, topo ~620) só naquele plano.
- Capa: texto dentro do recorte 4:5 do feed, **y 285 a 1635**.
- Nada cobre o rosto. Conferir quadro por quadro com grade de y.

## Legenda karaokê
- Escrita à mão a partir da transcrição conferida (Whisper erra: "salário na
  tendade", "Sarba Mais", "em durece").
- Máximo 2 linhas, até 22 caracteres por linha (usar 20 para folga). Medir a
  largura com a fonte real (Pillow `getlength`): linha > 1000 px é recusada.
- Caixa alta, fonte grossa (Poppins ExtraBold 80 / Montserrat Bold 94),
  contorno 7, sombra 2 a 3.
- Palavra falada na cor de destaque, as seguintes em branco: estilo ASS com
  `PrimaryColour` = destaque e `SecondaryColour` = branco, tags `{\kNN}` em
  centésimos a partir do início do evento.
- Tempo de cada palavra vem do SRT por palavra (`max_len=1`). Dentro de blocos
  de número o Whisper junta palavras: dividir em proporção e marcar "estimado".
- Cor em ASS é `&H00BBGGRR` (ordem invertida): `#FFE14D` vira `&H004DE1FF`.

## Selos, gancho, CTA
- Gancho na faixa de cima desde o primeiro quadro.
- Selo entra no instante em que a palavra é falada (tempo do bruto convertido
  para tempo final), com "pop": `{\fscx70\fscy70\t(0,160,\fscx106\fscy106)\t(160,260,\fscx100\fscy100)}`.
- Selo em caixa (`BorderStyle=3`) para contraste. Texto claro sobre fundo claro
  sem caixa fica ilegível no sol.
- CTA na tela nos segundos finais da fala e cartão final de ~1,8 s com logo e
  botão. **Último quadro nunca preto** (o Reels dá loop) e sem fade para preto.
- Conferir antes se o bruto já tem texto queimado ou marca d'água onde vai o selo.

## Imagem
- iPhone grava HDR (HLG, Dolby Vision): converter para SDR ou fica acinzentado.
  HLG (`color_transfer=arib-std-b67`):
  `zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p`
  PQ (`smpte2084`): mesmo filtro com `tin=smpte2084`. SDR: sem tonemap.
  Ver com `ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer,color_primaries -of csv=p=0 <arquivo>`.
- Rotação nos metadados (-90 = vertical): o FFmpeg aplica sozinho.
- `eq` por plano para casar brilho e saturação (medir com `signalstats`: Y, U, V
  médios). Salto grande de brilho entre planos parece flash.
- Punch-in por recorte (`crop` + `scale` lanczos), alternando ~118% / 128% para
  ritmo; zoom maior no momento forte (valor, pergunta, CTA). Recorte também
  serve para tirar objeto ou mão estranha da borda.
- Plano com texto escrito (zenital de papel): 100%, zoom empurra o conteúdo
  para fora da faixa segura.

## Montagem
- **Uma passada só** com `concat` de filtros. Nunca concat de arquivos com
  `-c copy` (tempos sobrepõem, `xfade` perde quadros).
- Transição só na imagem; texto queimado depois, uma vez só, sobre o vídeo já
  montado (senão aparecem textos sobrepostos na transição).
- Plano da câmera principal nunca atravessa emenda de áudio (perde a sincronia
  labial). Emenda de áudio cai em troca de plano ou debaixo de inserto (B-roll).
- B-roll por cima da fala quando ela olha para baixo, quando ajuda a entender,
  ou para esconder emenda. A imagem mostra o que a fala promete.
- Não emendar dois insertos de takes diferentes seguidos: pôr a câmera principal
  entre eles, nem que seja 0,8 s.
- Ritmo: 2,2 a 2,5 s por plano quando é locução sobre B-roll. Plano falando para a
  câmera pode ser mais longo, com punch-in alternado.

## Áudio
- Cortes: tirar ar morto, respiração e pausa longa; emenda só dentro de pausa,
  `acrossfade` 10 a 20 ms (tri); nenhuma palavra cortada.
- Limpeza: não existe dereverb perfeito no FFmpeg. Testar 3 a 5 cadeias em
  amostras A/B igualadas em -14 LUFS e o usuário escolhe no ouvido.
  Cadeia aprovada para eco de sala ("cadeia 5"):
  `pan=mono|c0=0.5*c0+0.5*c1,highpass=f=90,afftdn=nf=-42:nr=15:nt=w,atrim=start_sample=1200,asetpts=N/SR/TB,equalizer=f=250:t=q:w=1.2:g=-4,equalizer=f=3000:t=q:w=1:g=2,agate=threshold=0.022:ratio=2.5:range=0.18:attack=4:release=90:knee=3,deesser=i=0.3,acompressor=threshold=0.063:ratio=2.5:attack=10:release=150`
  (`atrim=start_sample=1200` compensa o atraso de 25 ms do `afftdn` a 48 kHz;
  completar com `apad` para manter a duração).
  Voz metálica é pior que eco leve: não exagerar.
- **-14 LUFS integrado**, pico real até **-1,5 dBTP**, 48 kHz. Medir com
  `ebur128=peak=true` no arquivo final e corrigir o ganho em laço (±0,2 LU).
- Fade de voz no máximo 0,3 s e só depois do fim da fala (fade de 0,7 s já comeu
  a última frase).
- Trilha (opcional, decisão do projeto): 14 dB abaixo da voz (20 dB se a fala
  for longa e contínua). Ajuda a esconder costura entre takes.

## Transcrição (whisper.py: GPU, filtro do FFmpeg ou faster-whisper)
- `scripts/whisper.py <entrada> <saida.srt> [ini] [fim] [max_len]`.
- O filtro não aceita `C:` no caminho do modelo: roda com a pasta do modelo como
  diretório atual. Destino com `:` escapado.
- `queue` grande (clipe inteiro) para não cortar palavra em bloco de 3 s.
- Trecho duvidoso (número, nome, palavra estranha): retranscrever a janela isolada.

## Capa
- Quadro nítido do próprio vídeo, 1080x1920. Nunca a miniatura automática do
  Meta (sai 160x284, borrada, e pega boca começando a falar).
- Sorriso de verdade: procurar antes da primeira palavra ou logo depois da última,
  olhando olhos e bochechas junto com a boca, em tamanho grande. Sem sorriso
  aberto no material: avisar o usuário.
- Aproximar no rosto (~130%), texto em caixas na cor da marca, dentro de y 285 a 1635.

## Conferência antes de entregar (quem montou)
- Quadros de cada emenda e de cada texto em folha com grade de y, olhados um a um.
- `ffprobe`: resolução, fps, número de quadros, codecs.
- `ebur128` no final.
- Retranscrever o vídeo final: nenhuma palavra cortada.
- Listar o que ficou em dúvida para o humano ouvir e ver.
