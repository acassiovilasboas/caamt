# -*- coding: utf-8 -*-
"""Sobe arquivos grandes (vídeo, imagem, PDF) para o Google Drive sem o app do Drive.

Só biblioteca padrão do Python. Permissão pedida ao Google: drive.file (o kit só vê e
mexe nos arquivos e pastas que ele mesmo criou). Uso:

  python drive_upload.py configurar <client_secret.json>   # uma vez (ver permissoes-google.md)
  python drive_upload.py login                             # uma vez: abre o navegador
  python drive_upload.py status
  python drive_upload.py pasta "CAAMT-Barra/publicacoes/2026-11-05_box77"
  python drive_upload.py enviar <arquivo> --pasta "CAAMT-Barra/Edicao-Video/2026-11-05_box77/final"
  python drive_upload.py listar --pasta "CAAMT-Barra/publicacoes"

Saída curta (uma linha por arquivo): id, nome, link. Credenciais em ~/.kit-caamt/.
"""
import base64
import hashlib
import http.server
import json
import mimetypes
import os
import secrets
import shutil
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

DIR = os.path.join(os.path.expanduser("~"), ".kit-caamt")
CLIENTE = os.path.join(DIR, "google-client.json")
TOKEN = os.path.join(DIR, "google-token.json")
ESCOPO = "https://www.googleapis.com/auth/drive.file"
AUTH = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://www.googleapis.com/drive/v3/files"
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
PASTA_MIME = "application/vnd.google-apps.folder"
BLOCO = 8 * 1024 * 1024  # múltiplo de 256 KB, como o Google pede


def sair(msg, cod=1):
    print(msg)
    sys.exit(cod)


def cliente():
    if not os.path.exists(CLIENTE):
        sair("FALTA configurar: siga permissoes-google.md e rode 'configurar <arquivo.json>'.")
    with open(CLIENTE, encoding="utf-8") as f:
        d = json.load(f)
    d = d.get("installed") or d.get("web") or d
    return d["client_id"], d.get("client_secret", "")


def post_form(url, dados):
    req = urllib.request.Request(url, urllib.parse.urlencode(dados).encode(), method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def salvar_token(t):
    os.makedirs(DIR, exist_ok=True)
    t["obtido_em"] = int(time.time())
    with open(TOKEN, "w", encoding="utf-8") as f:
        json.dump(t, f)


def configurar(arq):
    with open(arq, encoding="utf-8") as f:
        d = json.load(f)
    if not (d.get("installed") or d.get("web") or {}).get("client_id"):
        sair("Esse arquivo não parece um cliente OAuth do Google (falta client_id).")
    os.makedirs(DIR, exist_ok=True)
    shutil.copyfile(arq, CLIENTE)
    print("OK: cliente salvo. Agora: python drive_upload.py login")


def login():
    cid, segredo = cliente()
    verif = secrets.token_urlsafe(64)
    desafio = base64.urlsafe_b64encode(hashlib.sha256(verif.encode()).digest()).rstrip(b"=").decode()
    estado = secrets.token_urlsafe(16)
    recebido = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if "code" in q or "error" in q:
                recebido.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Pronto. Pode fechar esta aba e voltar ao Claude.".encode("utf-8"))

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    redir = "http://127.0.0.1:%d" % srv.server_address[1]
    url = AUTH + "?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": redir, "response_type": "code", "scope": ESCOPO,
        "code_challenge": desafio, "code_challenge_method": "S256", "state": estado,
        "access_type": "offline", "prompt": "consent"})
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print("Abrindo o navegador para você entrar na sua conta Google.")
    print("Se não abrir, copie este endereço no navegador:\n" + url)
    webbrowser.open(url)
    fim = time.time() + 300
    while not recebido and time.time() < fim:
        time.sleep(0.5)
    srv.shutdown()
    if not recebido:
        sair("Tempo esgotado (5 min) sem resposta do Google.")
    if recebido.get("error") or recebido.get("state") != estado:
        sair("O Google não autorizou: %s" % recebido.get("error", "estado diferente"))
    t = post_form(TOKEN_URL, {"code": recebido["code"], "client_id": cid, "client_secret": segredo,
                              "redirect_uri": redir, "grant_type": "authorization_code",
                              "code_verifier": verif})
    if "refresh_token" not in t:
        sair("O Google não devolveu o token de renovação. Rode 'login' de novo.")
    salvar_token(t)
    print("OK: conta ligada. O kit só vê os arquivos que ele mesmo criar no seu Drive.")


def acesso():
    if not os.path.exists(TOKEN):
        sair("FALTA login: python drive_upload.py login")
    with open(TOKEN, encoding="utf-8") as f:
        t = json.load(f)
    if time.time() < t["obtido_em"] + int(t.get("expires_in", 0)) - 120:
        return t["access_token"]
    cid, segredo = cliente()
    try:
        novo = post_form(TOKEN_URL, {"client_id": cid, "client_secret": segredo,
                                     "refresh_token": t["refresh_token"], "grant_type": "refresh_token"})
    except urllib.error.HTTPError as e:
        sair("O Google recusou a renovação (%s). Rode 'login' de novo. Se o app está em modo"
             " Teste, o acesso vence em 7 dias: veja permissoes-google.md." % e.code)
    novo["refresh_token"] = novo.get("refresh_token", t["refresh_token"])
    salvar_token(novo)
    return novo["access_token"]


def chamar(metodo, url, corpo=None, cab=None):
    req = urllib.request.Request(url, corpo, method=metodo)
    req.add_header("Authorization", "Bearer " + acesso())
    for k, v in (cab or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=120) as r:
        txt = r.read().decode()
        return (json.loads(txt) if txt else {}), r.headers


def aspas(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def garantir_pasta(caminho):
    pai = "root"
    for nome in [p for p in caminho.replace("\\", "/").split("/") if p.strip()]:
        q = ("name = '%s' and mimeType = '%s' and '%s' in parents and trashed = false"
             % (aspas(nome), PASTA_MIME, pai))
        r, _ = chamar("GET", API + "?" + urllib.parse.urlencode({"q": q, "fields": "files(id)"}))
        if r.get("files"):
            pai = r["files"][0]["id"]
        else:
            meta = json.dumps({"name": nome, "mimeType": PASTA_MIME, "parents": [pai]}).encode()
            r, _ = chamar("POST", API + "?fields=id", meta, {"Content-Type": "application/json"})
            pai = r["id"]
    return pai


def enviar(arq, caminho):
    if not os.path.isfile(arq):
        sair("Arquivo não encontrado: " + arq)
    pai = garantir_pasta(caminho)
    nome = os.path.basename(arq)
    tam = os.path.getsize(arq)
    tipo = mimetypes.guess_type(arq)[0] or "application/octet-stream"
    q = "name = '%s' and '%s' in parents and trashed = false" % (aspas(nome), pai)
    r, _ = chamar("GET", API + "?" + urllib.parse.urlencode(
        {"q": q, "fields": "files(id,size,md5Checksum,webViewLink)"}))
    md5 = None
    for f in r.get("files", []):
        if int(f.get("size", -1)) != tam:
            continue
        if md5 is None:
            h = hashlib.md5()
            with open(arq, "rb") as fh:
                for b in iter(lambda: fh.read(1 << 20), b""):
                    h.update(b)
            md5 = h.hexdigest()
        if f.get("md5Checksum") == md5:
            print("JA_EXISTE\t%s\t%s\t%s" % (f["id"], nome, f.get("webViewLink", "")))
            return
    meta = json.dumps({"name": nome, "parents": [pai]}).encode()
    _, cab = chamar("POST", UPLOAD + "?uploadType=resumable&fields=id,name,webViewLink", meta,
                    {"Content-Type": "application/json; charset=UTF-8",
                     "X-Upload-Content-Type": tipo, "X-Upload-Content-Length": str(tam)})
    sessao = cab["Location"]
    feito, falhas, consultar = 0, 0, False
    with open(arq, "rb") as f:
        while True:
            if consultar:  # depois de queda: pergunta ao Google até onde chegou
                pedaco, rng = b"", "bytes */%d" % tam
            else:
                f.seek(feito)
                pedaco = f.read(BLOCO)
                rng = "bytes %d-%d/%d" % (feito, feito + len(pedaco) - 1, tam) if pedaco else "bytes */%d" % tam
            req = urllib.request.Request(sessao, pedaco, method="PUT")
            req.add_header("Content-Range", rng)
            try:
                with urllib.request.urlopen(req, timeout=300) as resp:
                    d = json.loads(resp.read().decode())
                    print("ENVIADO\t%s\t%s\t%s" % (d["id"], d["name"], d.get("webViewLink", "")))
                    return
            except urllib.error.HTTPError as e:
                if e.code == 308:
                    faixa = e.headers.get("Range")
                    feito = int(faixa.split("-")[1]) + 1 if faixa else 0
                    consultar, falhas = False, 0
                    print("  %d%%" % (100 * feito // max(tam, 1)), flush=True)
                    continue
                if e.code in (404, 410):
                    sair("A sessão de envio expirou no Google. Rode o mesmo comando de novo.")
                if e.code < 500:
                    sair("Falha no envio (%s): %s" % (e.code, e.read().decode()[:300]))
                erro = "HTTP %s" % e.code
            except (urllib.error.URLError, OSError) as e:
                erro = str(e)
            falhas += 1
            if falhas > 8:
                sair("A internet caiu várias vezes (%s). Rode o mesmo comando de novo mais tarde." % erro)
            espera = min(2 ** falhas, 60)
            print("  conexão falhou (%s); tentando de novo em %d s" % (erro, espera), flush=True)
            time.sleep(espera)
            consultar = True


def listar(caminho):
    pai = garantir_pasta(caminho)
    q = "'%s' in parents and trashed = false" % pai
    r, _ = chamar("GET", API + "?" + urllib.parse.urlencode(
        {"q": q, "fields": "files(id,name,size,webViewLink)", "pageSize": 1000}))
    for f in r.get("files", []):
        print("%s\t%s\t%s\t%s" % (f["id"], f["name"], f.get("size", "-"), f.get("webViewLink", "")))


def status():
    print("cliente: %s" % ("ok" if os.path.exists(CLIENTE) else "FALTA (configurar)"))
    if not os.path.exists(TOKEN):
        print("login: FALTA (login)")
        return
    acesso()
    print("login: ok")


def main(a):
    if not a:
        sair(__doc__, 0)
    cmd, resto = a[0], a[1:]
    caminho = resto[resto.index("--pasta") + 1] if "--pasta" in resto else None
    if cmd == "configurar" and resto:
        configurar(resto[0])
    elif cmd == "login":
        login()
    elif cmd == "status":
        status()
    elif cmd == "pasta" and resto:
        print(garantir_pasta(resto[0]))
    elif cmd == "enviar" and resto and caminho:
        enviar(resto[0], caminho)
    elif cmd == "listar" and caminho:
        listar(caminho)
    else:
        sair(__doc__, 0)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
