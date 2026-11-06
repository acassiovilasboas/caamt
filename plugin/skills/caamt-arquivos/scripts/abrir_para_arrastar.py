# -*- coding: utf-8 -*-
"""Abre a pasta do Drive no navegador e o arquivo selecionado no computador, lado a lado,
para a pessoa só arrastar.

  python abrir_para_arrastar.py <link da pasta no Drive> <arquivo>
"""
import os
import platform
import subprocess
import sys
import webbrowser


def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    url, arq = a[0], os.path.abspath(a[1])
    if not os.path.exists(arq):
        sys.exit("Arquivo não encontrado: " + arq)
    webbrowser.open(url)
    sis = platform.system()
    if sis == "Windows":
        subprocess.Popen(["explorer", "/select,", arq])
    elif sis == "Darwin":
        subprocess.Popen(["open", "-R", arq])
    else:
        subprocess.Popen(["xdg-open", os.path.dirname(arq)])
    print("Aberto: pasta do Drive no navegador e o arquivo %s (%.1f MB)"
          % (os.path.basename(arq), os.path.getsize(arq) / 1048576))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
