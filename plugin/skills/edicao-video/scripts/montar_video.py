# -*- coding: utf-8 -*-
"""Monta um vídeo vertical de fala (Reels/anúncio) numa passada só de FFmpeg.

MODELO: copiar para scripts/montar_<nome>.py do projeto, preencher a
CONFIGURAÇÃO (as listas vêm da decupagem aprovada) e rodar:
    python scripts/montar_<nome>.py
Cores, fontes, logo e CTA vêm de marca/marca.json do projeto.

Etapas:
  1. áudio: só o take PRINCIPAL. CADEIA de limpeza no take inteiro, corte nos
     TRECHOS_AUDIO com acrossfade dentro da pausa, fade final depois da última
     palavra, trilha opcional, ganho + limitador até -14 LUFS (mede e corrige
     em laço), silêncio (ou trilha) no cartão final;
  2. imagem: PLANOS em tempo do vídeo FINAL. Plano do PRINCIPAL pega o quadro do
     bruto que casa com o áudio (sincronia labial); insertos entram sem som.
     Tonemap HDR para SDR automático por take, eq por plano, punch-in por recorte;
  3. texto: um ASS só (legenda karaokê + gancho, selos, CTA), queimado uma vez
     depois da montagem;
  4. cartão final (cartelas.py), último quadro nunca preto.

Travas: linha de legenda larga demais, mais de 2 linhas, sinal proibido pela
marca, plano do PRINCIPAL atravessando emenda de áudio, soma de quadros errada.
"""
import json
import os
import re
import subprocess
import sys

from PIL import ImageFont

def _acha_scripts():
    """Pasta scripts/ da skill: EDICAO_VIDEO_SCRIPTS > ~/.edicao-video/config.json > pasta deste arquivo."""
    p = os.environ.get("EDICAO_VIDEO_SCRIPTS")
    if not p:
        try:
            with open(os.path.join(os.path.expanduser("~"), ".edicao-video", "config.json"), encoding="utf-8") as f:
                p = json.load(f).get("scripts")
        except (OSError, ValueError):
            p = None
    if not p or not os.path.exists(os.path.join(p, "marca.py")):
        p = os.path.dirname(os.path.abspath(__file__))
    return p


SKILL = _acha_scripts()
sys.path.insert(0, SKILL)
import cartelas  # noqa: E402
from ambiente import codificador_args  # noqa: E402
from marca import carrega  # noqa: E402

# ============================================================ CONFIGURAÇÃO
PROJETO = None                          # raiz do projeto (None = procura marca/ subindo do cwd)
BASE = r"<pasta-do-video>"            # ex.: ...\Edicao-Video\<Projeto>\2026-11-05_<nome>
BRUTOS = os.path.join(BASE, "brutos")
TMP = os.path.join(BASE, "tmp", "montagem")
SAIDA = os.path.join(BASE, "final", "01_<NOME>_V1.mp4")

ARQ = {                                 # apelido do take -> arquivo em brutos\
    "principal": "<take_principal>.MOV",
    # "inserto1": "<take>.MOV",
}
PRINCIPAL = "principal"                 # take cujo áudio é a base
FPS = 30
FIM_CARTAO = 1.8
XF = 0.015                              # acrossfade entre trechos de áudio (10 a 20 ms)
ALVO_LUFS = -14.0
PICO_MAX = -1.5
GANHO_INICIAL = 0.0                     # dB; o laço corrige

# cadeia aprovada pelo usuário no ouvido (cadeias_audio.py); "anull" = sem limpeza
CADEIA = "pan=mono|c0=0.5*c0+0.5*c1"

# trilha opcional: (arquivo, dB abaixo da voz). None = sem trilha.
TRILHA = None                           # ex.: (r"<pasta>\trilha.mp3", 14)

# eq por take (do catálogo): aplicado depois do tonemap, antes do recorte
EQ = {
    # "inserto1": ",eq=gamma=1.1:saturation=0.9",
}

# Versão enxuta: trechos (ini, fim) em segundos do bruto PRINCIPAL
TRECHOS_AUDIO = [
    # (1.08, 6.74),   # texto do trecho
]
FIM_FALA = None                          # fim da última palavra no bruto; fade de 0,2 s logo depois


def P(ini, fim, take, z=1.0, x=None, y=0, src=None, leg_topo=None):
    """Plano em tempo do vídeo FINAL.
    take PRINCIPAL: o quadro do bruto é calculado pelo áudio (src ignorado).
    Inserto: src = início no bruto do inserto.
    z = punch-in (1.18 = 118%); (x, y) = canto do recorte em 1080x1920 (x None = centralizado).
    leg_topo = y do topo da legenda neste plano (None = legenda na base, y 1248)."""
    return dict(ini=ini, fim=fim, take=take, z=z, x=x, y=y, src=src, leg_topo=leg_topo)


PLANOS = [
    # P(0.00, 1.97, "principal", 1.22, 168, 100),
    # P(1.97, 3.50, "inserto1", src=2.0, leg_topo=620),
]

POP = r"{\fscx70\fscy70\t(0,160,\fscx106\fscy106)\t(160,260,\fscx100\fscy100)}"

# Textos fixos: (ini, fim, estilo, texto). Tempo: número = tempo do FINAL;
# "bNN.NN" = tempo no bruto PRINCIPAL (convertido). "\N" quebra linha.
# Estilos: Gancho, Selo, Total, Cta. Destaque inline: {AM}texto.
TEXTOS = [
    # (0.05, 1.97, "Gancho", POP + r"GANCHO\NDA PRIMEIRA FRASE?"),
    # ("b8.50", 7.82, "Selo", POP + r"R$ 1.621"),
    # ("b43.19", 36.78, "Cta", POP + "{CTA}"),
]

# Legenda escrita à mão. Cada cartão: lista de (PALAVRA, ini, fim) em tempo do
# bruto PRINCIPAL (SRT por palavra conferido); "/" = quebra de linha.
LEGENDA = [
    # [("GRÁVIDA", 1.16, 1.55), ("E", 1.58, 1.88), "/", ("DESEMPREGADA.", 1.92, 3.00)],
]

LEG_BASE = 1248                 # base da legenda (faixa livre do Reels: y 269 a 1248)
LEG_FONTE = 80
LEG_MAX = 20                    # caracteres por linha (limite: 22)
TOPO = 300                      # topo da faixa de cima (gancho, selos, CTA)
# ========================================================== FIM DA CONFIGURAÇÃO

M = carrega(PROJETO) if __name__ == "__main__" else None
_TM = {}


def tonemap_de(arq):
    """Filtro HDR->SDR conforme o color_transfer do arquivo ('' se já for SDR)."""
    if arq in _TM:
        return _TM[arq]
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=color_transfer", "-of", "json", arq], capture_output=True, text=True)
    trc = (json.loads(r.stdout or "{}").get("streams") or [{}])[0].get("color_transfer", "")
    tin = {"arib-std-b67": "arib-std-b67", "smpte2084": "smpte2084"}.get(trc)
    _TM[arq] = "" if not tin else (
        f"zscale=tin={tin}:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,"
        "format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
        "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
    return _TM[arq]


def mapa_trechos():
    out, t = [], 0.0
    for a, b in TRECHOS_AUDIO:
        out.append((a, b, t))
        t += b - a
    return out, t


MAPA, DUR_FALA = mapa_trechos()


def bruto_para_final(tb):
    for a, b, t0 in MAPA:
        if a - 1e-6 <= tb <= b + 1e-6:
            return t0 + tb - a
    raise ValueError(f"tempo {tb} do bruto fora dos trechos (caiu numa parte cortada)")


def ts(v):
    v = max(0.0, v)
    return f"{int(v // 3600)}:{int((v % 3600) // 60):02d}:{v % 60:05.2f}"


def tempo(v):
    return bruto_para_final(float(v[1:])) if isinstance(v, str) else v


def cabecalho():
    b, am, pr = M.ass("legenda"), M.ass("destaque"), M.ass("contorno")
    ve, es, cr = M.ass("principal"), M.ass("texto_escuro"), M.ass("fundo")
    fam = M.familia("legenda")
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Leg,{fam},{LEG_FONTE},{am},{b},{pr},&H80000000,0,0,0,0,100,100,0,0,1,7,3,2,40,40,{1920 - LEG_BASE},1
Style: Gancho,{fam},84,{cr},{cr},{ve},{ve},0,0,0,0,100,100,0,0,3,22,0,8,40,40,{TOPO},1
Style: Selo,{fam},128,{es},{es},{am},{am},0,0,0,0,100,100,0,0,3,24,0,8,40,40,{TOPO + 20},1
Style: Total,{fam},160,{am},{am},{ve},{ve},0,0,0,0,100,100,0,0,3,28,0,8,40,40,{TOPO + 10},1
Style: Cta,{fam},104,{am},{am},{ve},{ve},0,0,0,0,100,100,0,0,3,24,0,8,40,40,{TOPO + 40},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def texto_final(t):
    return (t.replace("{AM}", "{\\c" + M.ass_inline("destaque") + "}")
             .replace("{CTA}", M.texto("cta", "tela", padrao=r"CLIQUE EM\NSAIBA MAIS")))


def confere():
    if not TRECHOS_AUDIO or not PLANOS or FIM_FALA is None:
        sys.exit("preencher TRECHOS_AUDIO, PLANOS e FIM_FALA")
    for v in [BASE, SAIDA, *ARQ.values()]:
        if "<" in v or ">" in v:
            sys.exit(f"trocar o marcador <...> na configuração: {v}")
    f = ImageFont.truetype(M.fonte("legenda"), LEG_FONTE)
    for cartao in LEGENDA:
        linhas = " ".join(p if p == "/" else p[0] for p in cartao).split(" / ")
        if len(linhas) > 2:
            sys.exit(f"mais de 2 linhas: {linhas}")
        for ln in linhas:
            if len(ln) > LEG_MAX or f.getlength(ln) > 1000:
                sys.exit(f"linha longa demais ({len(ln)} car., {f.getlength(ln):.0f} px): {ln}")
    M.confere_texto([p[0] for c in LEGENDA for p in c if p != "/"] + [texto_final(t[3]) for t in TEXTOS])
    for a, b in zip(PLANOS, PLANOS[1:]):
        if abs(a["fim"] - b["ini"]) > 1e-6:
            sys.exit(f"buraco ou sobreposição entre planos em {a['fim']} / {b['ini']}")
    if PLANOS[0]["ini"] != 0:
        sys.exit("primeiro plano tem de começar em 0")


def faixas_legenda(dur):
    fx = []
    for i, p in enumerate(PLANOS):
        fim = dur if i == len(PLANOS) - 1 else round(p["fim"] * FPS) / FPS
        fx.append((round(p["ini"] * FPS) / FPS, fim, p["leg_topo"]))
    return fx


def karaoke(cartao, t_ev):
    pal = [p for p in cartao if p != "/"]
    cs = [round(max(0.0, bruto_para_final(p[1]) - t_ev) * 100) for p in pal]
    partes, k = ["{\\k%d}" % cs[0]], 0
    for p in cartao:
        if p == "/":
            partes.append(r"\N")
            continue
        if k + 1 < len(pal):
            d = cs[k + 1] - cs[k]
        else:
            d = max(1, round((bruto_para_final(p[2]) - t_ev) * 100) - cs[k])
        partes.append("{\\k%d}%s " % (d, p[0]))
        k += 1
    return "".join(partes).replace(r" \N", r"\N").strip()


def escreve_ass(caminho, dur):
    ev = [(1, tempo(a), tempo(b), estilo, 0, texto_final(txt)) for a, b, estilo, txt in TEXTOS]
    fx = faixas_legenda(dur)
    for i, cartao in enumerate(LEGENDA):
        pal = [p for p in cartao if p != "/"]
        ini = bruto_para_final(pal[0][1])
        fim_fala = bruto_para_final(pal[-1][2])
        prox = bruto_para_final(LEGENDA[i + 1][0][1]) if i + 1 < len(LEGENDA) else dur
        fim = min(prox, fim_fala + 0.5, dur)
        # cartão cortado nas trocas de plano (a faixa da legenda pode mudar)
        for a, b, topo in fx:
            a2, b2 = max(a, ini), min(b, fim)
            if b2 - a2 < 0.005 or (b2 - a2 < 0.25 and a2 > ini + 1e-6):
                continue
            pre = r"{\an8}" if topo is not None else ""
            ev.append((0, a2, b2, "Leg", topo or 0, pre + karaoke(cartao, a2)))
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(cabecalho())
        for camada, a, b, estilo, mv, txt in ev:
            f.write(f"Dialogue: {camada},{ts(a)},{ts(b)},{estilo},,0,0,{mv},,{txt}\n")


def roda(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("ffmpeg falhou:\n" + " ".join(cmd)[:2000] + "\n" + r.stderr[-3000:])
    return r


def ebur(arq):
    r = roda(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"])
    s = r.stderr[r.stderr.rfind("Summary:"):]
    return (float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)),
            float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1)),
            float(re.search(r"LRA:\s+(-?[\d.]+) LU", s).group(1)))


def monta_audio(dur_total):
    bruto = os.path.join(BRUTOS, ARQ[PRINCIPAL])
    limpo = os.path.join(TMP, "voz_limpa.wav")
    roda(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af", CADEIA, "-ar", "48000", "-ac", "1",
          "-c:a", "pcm_f32le", limpo])
    entradas = ["-i", limpo]
    ganho_trilha = None
    if TRILHA:
        i_m, _, _ = ebur(TRILHA[0])
        ganho_trilha = ALVO_LUFS - TRILHA[1] - i_m
        entradas += ["-stream_loop", "-1", "-i", TRILHA[0]]
    ganho = GANHO_INICIAL
    final = os.path.join(TMP, "audio_final.wav")
    for _ in range(6):
        n = len(TRECHOS_AUDIO)
        f = [f"[0:a]asplit={n}" + "".join(f"[s{i}]" for i in range(n))]
        for i, (a, b) in enumerate(TRECHOS_AUDIO):
            ultimo = i == n - 1
            fim = b if ultimo else b + XF          # sobra engolida pelo acrossfade
            extra = ",afade=t=in:d=0.02" if i == 0 else ""
            if ultimo:
                extra += f",afade=t=out:st={FIM_FALA + 0.03 - a:.3f}:d=0.2"
            f.append(f"[s{i}]atrim={a:.3f}:{fim:.3f},asetpts=PTS-STARTPTS{extra}[t{i}]")
        cur = "t0"
        for i in range(1, n):
            f.append(f"[{cur}][t{i}]acrossfade=d={XF}:c1=tri:c2=tri[x{i}]")
            cur = f"x{i}"
        f.append(f"[{cur}]volume={ganho:.2f}dB,apad=whole_dur={dur_total:.3f},atrim=0:{dur_total:.3f}[voz]")
        if TRILHA:
            f.append(f"[1:a]aformat=sample_rates=48000:channel_layouts=mono,atrim=0:{dur_total:.3f},"
                     f"volume={ganho_trilha:.2f}dB,"
                     f"afade=t=out:st={dur_total - 1.0:.3f}:d=1.0[tr]")
            f.append("[voz][tr]amix=inputs=2:normalize=0:duration=first[mix]")
            cur = "mix"
        else:
            cur = "voz"
        lim = 10 ** ((PICO_MAX - 0.6) / 20)
        f.append(f"[{cur}]alimiter=limit={lim:.3f}:attack=5:release=50:level=false:latency=1[out]")
        roda(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(f),
              "-map", "[out]", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s24le", final])
        i_, tp, lra = ebur(final)
        print(f"  áudio: ganho {ganho:.2f} dB -> I {i_} LUFS, pico real {tp} dBTP, LRA {lra}")
        if abs(i_ - ALVO_LUFS) <= 0.2 and tp <= PICO_MAX:
            break
        ganho += ALVO_LUFS - i_
    return final


def recorte(z, x, y):
    if z == 1.0:
        return ""
    w, h = round(1080 / z / 2) * 2, round(1920 / z / 2) * 2
    x = (1080 - w) // 2 if x is None else min(max(0, x), 1080 - w)
    y = min(max(0, y), 1920 - h)
    return f",crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos"


def monta():
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    confere()
    nq = round(DUR_FALA * FPS)
    dur_corpo = nq / FPS
    dur_total = dur_corpo + FIM_CARTAO

    cartao = os.path.join(BASE, "cartelas", "cartao_final.png")
    os.makedirs(os.path.dirname(cartao), exist_ok=True)
    cartelas.cartao_final(cartao, M)

    voz = monta_audio(dur_total)
    ass = os.path.join(TMP, "textos.ass")
    escreve_ass(ass, dur_corpo)

    entradas, filtros, rot, feitos = [], [], [], 0
    for i, p in enumerate(PLANOS):
        q0 = round(p["ini"] * FPS)
        q1 = nq if i == len(PLANOS) - 1 else round(p["fim"] * FPS)
        nfr = q1 - q0
        if nfr <= 0:
            sys.exit(f"plano {i} sem quadros")
        if p["take"] == PRINCIPAL:
            meio = (p["ini"] + p["fim"]) / 2
            ab = [m for m in MAPA if m[2] <= meio < m[2] + m[1] - m[0]][0]
            src = ab[0] + q0 / FPS - ab[2]
            if q0 / FPS < ab[2] - 1.0 / FPS or q1 / FPS > ab[2] + ab[1] - ab[0] + 1.0 / FPS:
                sys.exit(f"plano {i} do {PRINCIPAL} atravessa emenda de áudio (perde a sincronia)")
        else:
            src = p["src"]
            if src is None:
                sys.exit(f"plano {i} ({p['take']}) sem src")
        arq = os.path.join(BRUTOS, ARQ[p["take"]])
        tm = tonemap_de(arq)
        entradas += ["-ss", f"{src:.3f}", "-t", f"{nfr / FPS + 0.5:.3f}", "-i", arq]
        filtros.append(f"[{i}:v]{tm + ',' if tm else ''}format=yuv420p{EQ.get(p['take'], '')},fps={FPS},"
                       f"scale=1080:1920:flags=lanczos,setsar=1{recorte(p['z'], p['x'], p['y'])},setsar=1,"
                       f"trim=end_frame={nfr},setpts=PTS-STARTPTS[v{i}]")
        rot.append(f"[v{i}]")
        feitos += nfr
    assert feitos == nq, (feitos, nq)
    n = len(PLANOS)
    filtros.append("".join(rot) + f"concat=n={n}:v=1:a=0[vc]")
    fonte_ass = ass.replace("\\", "/").replace(":", "\\:")
    fontes = M.pasta_fontes().replace("\\", "/").replace(":", "\\:")
    filtros.append(f"[vc]subtitles='{fonte_ass}':fontsdir='{fontes}'[vs]")
    entradas += ["-loop", "1", "-t", f"{FIM_CARTAO}", "-i", cartao]
    filtros.append(f"[{n}:v]scale=1080:1920,setsar=1,fps={FPS},format=yuv420p,"
                   f"trim=end_frame={round(FIM_CARTAO * FPS)}[fim]")
    filtros.append("[vs][fim]concat=n=2:v=1:a=0[vout]")
    entradas += ["-i", voz]

    roda(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros),
          "-map", "[vout]", "-map", f"{n + 1}:a", *codificador_args(),
          "-pix_fmt", "yuv420p", "-r", str(FPS), "-color_primaries", "bt709", "-color_trc", "bt709",
          "-colorspace", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "1",
          "-shortest", "-movflags", "+faststart", SAIDA])
    i_, tp, lra = ebur(SAIDA)
    print(f"{SAIDA}: {dur_total:.2f} s | final I {i_} LUFS, pico real {tp} dBTP, LRA {lra}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    monta()
