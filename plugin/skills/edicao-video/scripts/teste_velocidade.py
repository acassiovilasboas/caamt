# -*- coding: utf-8 -*-
"""Mede quanto tempo este computador leva para gravar um Reels, sem usar vídeo de ninguém.

Uso: python teste_velocidade.py [segundos=8]

Gera um vídeo sintético 1080x1920 (imagem de teste + tom), aplica o mesmo tipo de
filtro da montagem (escala lanczos, punch-in, legenda ASS queimada) e grava com o
codificador escolhido pelo ambiente.py. Resultado: "fator de tempo real"
(1.0 = 1 s de vídeo gravado em 1 s) e estimativa para um Reels de 60 s.
Salva em ~/.edicao-video/ambiente.json (chave teste_velocidade). Leve: poucos
segundos de processamento, tudo em pasta temporária apagada no fim.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ambiente  # noqa: E402

ASS = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Leg,Arial,80,&H004DE1FF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,2,40,40,672,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:30.00,Leg,,0,0,0,,{\\k40}TESTE {\\k40}DE {\\k40}VELOCIDADE
"""


def main():
    seg = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
    a = ambiente.carrega()
    cod = ambiente.codificador_args()
    tmp = tempfile.mkdtemp(prefix="ev_teste_")
    try:
        ass = os.path.join(tmp, "t.ass")
        with open(ass, "w", encoding="utf-8") as f:
            f.write(ASS)
        cwd_ass = "t.ass"   # roda dentro da pasta: evita escapar C: no filtro
        vf = ("format=yuv420p,scale=1080:1920:flags=lanczos,crop=914:1626:80:120,"
              f"scale=1080:1920:flags=lanczos,setsar=1,subtitles={cwd_ass}")
        cmd = ["ffmpeg", "-hide_banner", "-v", "error", "-y",
               "-f", "lavfi", "-i", f"testsrc2=s=1080x1920:r=30:d={seg}",
               "-f", "lavfi", "-i", f"sine=f=440:d={seg}:sample_rate=48000",
               "-vf", vf, *cod, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", "saida.mp4"]
        t0 = time.time()
        r = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, encoding="utf-8", errors="replace")
        dt = time.time() - t0
        if r.returncode != 0:
            sys.exit("teste falhou:\n" + r.stderr[-1500:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    fator = round(seg / dt, 2)
    res = {"medido_em": time.strftime("%Y-%m-%d %H:%M"), "segundos_video": seg,
           "segundos_gastos": round(dt, 1), "fator_tempo_real": fator, "codificador": cod[1],
           "estimativa_60s_min": round(60 / fator / 60 * 1.6, 1)}   # 1,6 = tonemap, áudio e 2ª passada de loudness
    a["teste_velocidade"] = res
    a["veredito"] = ambiente.veredito(a)
    ambiente.grava_json(ambiente.ARQ_AMB, a)
    print(ambiente.resumo(a))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
