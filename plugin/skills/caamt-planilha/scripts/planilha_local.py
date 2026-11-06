# -*- coding: utf-8 -*-
"""Planilha de trabalho da subseção no modo local (um CSV por aba) e as colunas de cada aba.

  python planilha_local.py colunas [<aba>]                 # cabeçalhos (vale também para o Drive)
  python planilha_local.py criar <pasta>                    # cria <pasta>/planilha/*.csv que faltarem
  python planilha_local.py ler <pasta> <aba> [--busca txt]
  python planilha_local.py nova <pasta> <aba> "Coluna=valor" ...      # acrescenta uma linha
  python planilha_local.py mudar <pasta> <aba> <chave> "Coluna=valor" ... [--quem usuário|Claude]

<chave> = valor da 1ª coluna da linha (ex.: nome do parceiro, data do post), sem diferenciar
maiúsculas nem acento. "mudar" grava só as células citadas, mantém o resto como está no arquivo
(inclusive o que a pessoa editou no Excel) e registra cada mudança na aba Histórico.
"""
import csv
import datetime
import html
import os
import sys
import unicodedata

ABAS = {
    "linha-editorial": ["Tema", "Para quê", "Frequência", "Dia sugerido", "Formatos", "De onde vem a pauta",
                        "Atualizado em"],
    "cronograma": ["Data", "Tema", "Pauta", "Formato", "Roteiro", "Legenda", "Hashtags",
                   "Primeiro comentário", "Arte (link)", "Status", "Fonte", "Evento na agenda", "Atualizado em"],
    "pautas": ["Data", "Tema", "Título", "Fonte", "Resumo", "Usada em"],
    "parceiros": ["Parceiro", "Etapa", "Próxima ação", "Data da próxima ação", "Falta",
                  "O que está travando", "Na etapa desde", "Responsável", "WhatsApp/Telefone",
                  "Outros telefones", "E-mail", "Instagram", "Outras redes", "Site", "Endereço",
                  "Categoria", "Cidade", "Tipo (PJ/PF)", "Benefício", "Cupom ou voucher", "Como usar",
                  "Validade do benefício", "Carta proposta", "Alvará (PJ)", "CNPJ (PJ)",
                  "Comprovante de endereço (PF)", "Documento com foto", "Logo JPG",
                  "Tabela de valores (opcional)", "Próxima mensagem", "Última cobrança", "Pasta (link)",
                  "Observações", "Evento na agenda", "Atualizado em"],
    "config": ["Chave", "Valor", "Atualizado em"],
    "historico": ["Data", "Aba", "Item", "O que mudou", "De", "Para", "Quem"],
}
NOMES = {"linha-editorial": "Linha editorial", "cronograma": "Cronograma", "pautas": "Pautas",
         "parceiros": "Parceiros", "config": "Config", "historico": "Histórico"}


def sair(msg):
    print(msg)
    sys.exit(1)


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return " ".join(s.lower().split())


def aba_de(nome):
    for k, v in NOMES.items():
        if norm(nome) in (norm(k), norm(v)):
            return k
    sair("Aba desconhecida: %s. Abas: %s" % (nome, ", ".join(NOMES.values())))


def arq(pasta, aba):
    return os.path.join(pasta, "planilha", aba + ".csv")


def ler(pasta, aba):
    p = arq(pasta, aba)
    if not os.path.exists(p):
        sair("Falta a planilha local. Rode: planilha_local.py criar " + pasta)
    with open(p, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.reader(f))
    return (linhas[0] if linhas else list(ABAS[aba])), linhas[1:]


def gravar(pasta, aba, cab, linhas):
    p = arq(pasta, aba)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(cab)
        w.writerows(linhas)
    os.replace(tmp, p)


def pares(args):
    d = {}
    for a in args:
        if "=" not in a:
            sair('Use "Coluna=valor": ' + a)
        k, v = a.split("=", 1)
        d[k.strip()] = v
    return d


def coluna(cab, nome):
    for i, c in enumerate(cab):
        if norm(c) == norm(nome):
            return i
    sair("Coluna '%s' não existe. Colunas: %s" % (nome, ", ".join(cab)))


def achar(cab, nome):
    for i, c in enumerate(cab):
        if norm(c) == norm(nome):
            return i
    return None


def hoje():
    return datetime.date.today().strftime("%d/%m/%Y")


def historico(pasta, aba, item, mudancas, quem):
    cab, linhas = ler(pasta, "historico")
    for col, de, para in mudancas:
        linhas.append([hoje(), NOMES[aba], item, col, de, para, quem])
    gravar(pasta, "historico", cab, linhas)


def criar(pasta):
    os.makedirs(os.path.join(pasta, "planilha"), exist_ok=True)
    feitas, novas = [], []
    for aba, cab in ABAS.items():
        if not os.path.exists(arq(pasta, aba)):
            gravar(pasta, aba, cab, [])
            feitas.append(NOMES[aba])
            continue
        atual, linhas = ler(pasta, aba)  # coluna nova do kit entra no fim, sem mexer no resto
        falta = [c for c in cab if norm(c) not in {norm(x) for x in atual}]
        if falta:
            gravar(pasta, aba, atual + falta, [l + [""] * (len(atual) - len(l) + len(falta)) for l in linhas])
            novas.append("%s (+%s)" % (NOMES[aba], ", ".join(falta)))
    print("Criadas: " + (", ".join(feitas) or "nenhuma"))
    if novas:
        print("Colunas novas: " + "; ".join(novas))


def nova(pasta, aba, dados, quem):
    cab, linhas = ler(pasta, aba)
    linha = [""] * len(cab)
    for k, v in dados.items():
        linha[coluna(cab, k)] = v
    e, d = achar(cab, "Etapa"), achar(cab, "Na etapa desde")
    if aba == "parceiros" and e is not None and d is not None and linha[e] and not linha[d]:
        linha[d] = hoje()
    if "Atualizado em" in cab:
        linha[cab.index("Atualizado em")] = hoje()
    linhas.append(linha)
    gravar(pasta, aba, cab, linhas)
    if aba != "historico":
        historico(pasta, aba, linha[0], [("linha nova", "", linha[0])], quem)
    print("OK: linha nova em %s: %s" % (NOMES[aba], linha[0]))


def mudar(pasta, aba, chave, dados, quem):
    cab, linhas = ler(pasta, aba)
    achou = [i for i, l in enumerate(linhas) if l and norm(l[0]) == norm(chave)]
    if not achou:
        parecidas = [l[0] for l in linhas if l and norm(chave) in norm(l[0])]
        sair("Não achei '%s' em %s.%s" % (chave, NOMES[aba],
             (" Parecidas: " + "; ".join(parecidas)) if parecidas else ""))
    if len(achou) > 1:
        sair("Há %d linhas '%s' em %s: perguntar qual." % (len(achou), chave, NOMES[aba]))
    linha = linhas[achou[0]] + [""] * (len(cab) - len(linhas[achou[0]]))
    mud = []
    for k, v in dados.items():
        i = coluna(cab, k)
        if linha[i] != v:
            mud.append((cab[i], linha[i], v))
            linha[i] = v
    e, d = achar(cab, "Etapa"), achar(cab, "Na etapa desde")
    if (aba == "parceiros" and e is not None and d is not None and any(m[0] == cab[e] and norm(m[1]) != norm(m[2]) for m in mud)
            and not any(norm(k) == norm(cab[d]) for k in dados) and linha[d] != hoje()):
        mud.append((cab[d], linha[d], hoje()))
        linha[d] = hoje()
    if not mud:
        print("Nada mudou.")
        return
    if "Atualizado em" in cab:
        linha[cab.index("Atualizado em")] = hoje()
    linhas[achou[0]] = linha
    gravar(pasta, aba, cab, linhas)
    historico(pasta, aba, linha[0], mud, quem)
    for c, de, para in mud:
        print("OK: %s · %s: '%s' → '%s'" % (linha[0], c, de, para))


def mostrar(pasta, aba, busca):
    cab, linhas = ler(pasta, aba)
    if busca:
        linhas = [l for l in linhas if norm(busca) in norm(" ".join(l))]
    print(" | ".join(cab))
    for l in linhas:
        print(" | ".join(l))
    print("(%d linhas)" % len(linhas))


def main(a):
    if not a:
        sys.exit(__doc__)
    quem = "Claude"
    if "--quem" in a:
        j = a.index("--quem")
        quem = a[j + 1] if j + 1 < len(a) else quem
        del a[j:j + 2]
    busca = None
    if "--busca" in a:
        j = a.index("--busca")
        busca = a[j + 1] if j + 1 < len(a) else None
        del a[j:j + 2]
    cmd = a[0]
    if cmd == "colunas":
        for aba in ([aba_de(a[1])] if len(a) > 1 else ABAS):
            print("%s: %s" % (NOMES[aba], ",".join(ABAS[aba])))
    elif cmd == "criar" and len(a) > 1:
        criar(a[1])
    elif cmd == "ler" and len(a) > 2:
        mostrar(a[1], aba_de(a[2]), busca)
    elif cmd == "nova" and len(a) > 3:
        nova(a[1], aba_de(a[2]), pares(a[3:]), quem)
    elif cmd == "mudar" and len(a) > 4:
        mudar(a[1], aba_de(a[2]), a[3], pares(a[4:]), quem)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
