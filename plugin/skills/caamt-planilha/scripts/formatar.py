# -*- coding: utf-8 -*-
"""Formatação da planilha da subseção: cabeçalho fixo e colorido, filtro, larguras, listas de
escolha e cores (data vencida, etapa, estado de cada documento, status do post).

  python formatar.py xlsx <planilha.xlsx>        # aplica no arquivo do computador
  python formatar.py drive <abas.json>           # imprime os pedidos para o conector do Sheets

abas.json (lido do Drive na hora): {"Parceiros": {"sheetId": 123, "cabecalho": ["Parceiro", ...]}, ...}
A saída de "drive" é a lista `requests` do update_spreadsheet. Tudo é achado pelo nome da coluna,
então vale para planilha antiga, com outra ordem. Formatação completa só na criação: ela
substitui fontes, listas e cores da planilha.
"""
import json
import sys

AZUL, CINZA_TX = "1F3B73", "8A8F98"
VERDE, AMBAR, VERM, CINZA, AZULC = "D9F2E3", "FCEFD2", "F9D9D9", "EEEEEE", "E3EAFB"
VERM_TX = "B00020"
ETAPAS = ["Prospecção", "Contato", "Aguardando documentos", "Documentos completos",
          "Enviado à CAAMT", "Aprovado", "Divulgado", "Não fechou"]
DOCS = ["Carta proposta", "Alvará (PJ)", "CNPJ (PJ)", "Comprovante de endereço (PF)",
        "Documento com foto", "Logo JPG", "Tabela de valores (opcional)"]
TECNICAS = {"Evento na agenda", "Atualizado em"}
LARG = {"Parceiro": 24, "Etapa": 22, "Próxima ação": 28, "Falta": 18, "O que está travando": 28,
        "Responsável": 18, "Benefício": 24, "Próxima mensagem": 50, "Observações": 30, "Legenda": 55,
        "Pauta": 28, "Tema": 22, "Primeiro comentário": 30, "Roteiro": 30, "Resumo": 60, "Título": 32,
        "Para quê": 36, "Valor": 50, "Chave": 30, "Endereço": 30, "Como usar": 28}
QUEBRA = {"Próxima mensagem", "Observações", "Próxima ação", "Benefício", "Legenda", "Primeiro comentário",
          "Roteiro", "Pauta", "Resumo", "Título", "Para quê", "O que está travando", "Como usar"}
COR_ABA = {"Parceiros": "1F3B73", "Cronograma": "7C5CD6", "Pautas": "B39CFF", "Linha editorial": "E8B45A",
           "Config": "999999", "Histórico": "999999"}
LISTAS = {"Parceiros": {"Etapa": ETAPAS, "Tipo (PJ/PF)": ["PJ", "PF"]},
          "Cronograma": {"Status": ["ideia", "pronto", "publicado"]}}
FIM = 1000  # linhas cobertas por listas e cores


def letra(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def regras(aba, cab):
    """[(coluna inicial, coluna final, fórmula com {c} = coluna inicial, fundo, negrito, cor do texto)]"""
    ix = {c: i + 1 for i, c in enumerate(cab)}
    out = []
    if aba == "Parceiros":
        if "Etapa" in ix:
            e = letra(ix["Etapa"])
            out += [(e, e, 'OR($%s2="Aprovado",$%s2="Divulgado")' % (e, e), VERDE, False, None),
                    (e, e, 'OR($%s2="Aguardando documentos",$%s2="Documentos completos",$%s2="Enviado à CAAMT")'
                     % (e, e, e), AMBAR, False, None),
                    (e, e, '$%s2="Não fechou"' % e, CINZA, False, None)]
        if "Data da próxima ação" in ix:
            d = letra(ix["Data da próxima ação"])
            out += [(d, d, 'AND($%s2<>"",$%s2<TODAY())' % (d, d), VERM, True, VERM_TX),
                    (d, d, '$%s2=TODAY()' % d, AMBAR, True, None)]
        for doc in DOCS:
            if doc in ix:
                c = letra(ix[doc])
                out += [(c, c, 'AND($A2<>"",%s2="")' % c, VERM, False, None) if doc != DOCS[-1] else None,
                        (c, c, 'LEFT(%s2,2)="ok"' % c, VERDE, False, None),
                        (c, c, 'LEFT(%s2,8)="recebido"' % c, AMBAR, False, None),
                        (c, c, 'LEFT(%s2,8)="problema"' % c, VERM, True, VERM_TX),
                        (c, c, '%s2="não se aplica"' % c, CINZA, False, "AAAAAA")]
    if aba == "Cronograma" and "Status" in ix:
        s, ult = letra(ix["Status"]), letra(len(cab))
        if "Data" in ix:  # primeiro: data vencida vence a cor da linha
            d = letra(ix["Data"])
            out.append((d, d, 'AND($%s2<>"",$%s2<TODAY(),$%s2<>"publicado")' % (d, d, s), VERM, True, VERM_TX))
        out += [("A", ult, '$%s2="publicado"' % s, VERDE, False, None),
                ("A", ult, '$%s2="pronto"' % s, AZULC, False, None)]
    return [r for r in out if r]


def xlsx(caminho, so_colunas=None):
    """so_colunas={aba: [colunas]}: só cabeçalho e largura dessas colunas; o resto fica como está."""
    from openpyxl import load_workbook
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.formatting.formatting import ConditionalFormattingList
    F = lambda c: PatternFill("solid", start_color=c, end_color=c)
    wb = load_workbook(caminho)
    if so_colunas:
        for ws in wb.worksheets:
            cab = [c.value or "" for c in ws[1]]
            for nome in so_colunas.get(ws.title, []):
                if nome in cab:
                    i = cab.index(nome) + 1
                    h = ws.cell(1, i)
                    h.font = Font(bold=True, color="FFFFFF", size=11)
                    h.fill = F(CINZA_TX if nome in TECNICAS else AZUL)
                    h.alignment = Alignment(vertical="center", wrap_text=True)
                    ws.column_dimensions[letra(i)].width = LARG.get(nome, 16)
        wb.save(caminho)
        print("Formatado (só colunas novas): " + caminho)
        return
    for ws in wb.worksheets:
        cab = [c.value or "" for c in ws[1]]
        if not any(cab):
            continue
        ws.sheet_properties.tabColor = COR_ABA.get(ws.title, "999999")
        for i, nome in enumerate(cab, 1):
            h = ws.cell(1, i)
            h.font = Font(bold=True, color="FFFFFF", size=11)
            h.fill = F(CINZA_TX if nome in TECNICAS else AZUL)
            h.alignment = Alignment(vertical="center", wrap_text=True)
            ws.column_dimensions[letra(i)].width = LARG.get(nome, 16)
            for r in range(2, ws.max_row + 1):
                cel = ws.cell(r, i)
                cel.alignment = Alignment(vertical="top", wrap_text=nome in QUEBRA)
                cel.border = Border(bottom=Side(style="thin", color="DDDDDD"))
                if not cel.hyperlink:
                    cel.font = Font(size=11, color=CINZA_TX if nome in TECNICAS else "222222", bold=(i == 1))
        ws.row_dimensions[1].height = 34
        ws.freeze_panes = "B2"
        ws.auto_filter.ref = "A1:%s%d" % (letra(len(cab)), max(ws.max_row, FIM))
        ws.data_validations.dataValidation = []
        for nome, ops in LISTAS.get(ws.title, {}).items():
            if nome in cab:
                c = letra(cab.index(nome) + 1)
                dv = DataValidation(type="list", formula1='"%s"' % ",".join(ops), allow_blank=True)
                ws.add_data_validation(dv)
                dv.add("%s2:%s%d" % (c, c, FIM))
        ws.conditional_formatting = ConditionalFormattingList()
        for a, b, f, fundo, neg, tx in regras(ws.title, cab):
            ws.conditional_formatting.add("%s2:%s%d" % (a, b, FIM), FormulaRule(
                formula=[f], fill=F(fundo), font=Font(bold=neg, color=tx) if (neg or tx) else None))
    wb.save(caminho)
    print("Formatado: " + caminho)


def rgb(h):
    return {"red": int(h[0:2], 16) / 255, "green": int(h[2:4], 16) / 255, "blue": int(h[4:6], 16) / 255}


def drive(arq):
    abas = json.load(open(arq, encoding="utf-8"))
    req = []
    for nome, info in abas.items():
        sid, cab = info["sheetId"], info["cabecalho"]
        n = len(cab)
        req.append({"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {
            "frozenRowCount": 1, "frozenColumnCount": 1}, "tabColorStyle": {"rgbColor": rgb(COR_ABA.get(nome, "999999"))}},
            "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount,tabColorStyle"}})
        for i, col in enumerate(cab):
            req.append({"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1,
                        "startColumnIndex": i, "endColumnIndex": i + 1},
                        "cell": {"userEnteredFormat": {"backgroundColorStyle": {"rgbColor": rgb(CINZA_TX if col in TECNICAS else AZUL)},
                                 "textFormat": {"bold": True, "foregroundColorStyle": {"rgbColor": rgb("FFFFFF")}},
                                 "wrapStrategy": "WRAP", "verticalAlignment": "MIDDLE"}},
                        "fields": "userEnteredFormat(backgroundColorStyle,textFormat,wrapStrategy,verticalAlignment)"}})
            req.append({"updateDimensionProperties": {"range": {"sheetId": sid, "dimension": "COLUMNS",
                        "startIndex": i, "endIndex": i + 1}, "properties": {"pixelSize": LARG.get(col, 16) * 7},
                        "fields": "pixelSize"}})
            if col in QUEBRA:
                req.append({"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": FIM,
                            "startColumnIndex": i, "endColumnIndex": i + 1},
                            "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP", "verticalAlignment": "TOP"}},
                            "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"}})
        req.append({"setBasicFilter": {"filter": {"range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": FIM,
                    "startColumnIndex": 0, "endColumnIndex": n}}}})
        for col, ops in LISTAS.get(nome, {}).items():
            if col in cab:
                i = cab.index(col)
                req.append({"setDataValidation": {"range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": FIM,
                            "startColumnIndex": i, "endColumnIndex": i + 1}, "rule": {"condition": {
                            "type": "ONE_OF_LIST", "values": [{"userEnteredValue": o} for o in ops]},
                            "strict": False, "showCustomUi": True}}})
        for k, (a, b, f, fundo, neg, tx) in enumerate(regras(nome, cab)):
            ia, ib = cab_index(a), cab_index(b)
            fmt = {"backgroundColorStyle": {"rgbColor": rgb(fundo)}}
            if neg or tx:
                fmt["textFormat"] = {"bold": neg}
                if tx:
                    fmt["textFormat"]["foregroundColorStyle"] = {"rgbColor": rgb(tx)}
            req.append({"addConditionalFormatRule": {"index": k, "rule": {"ranges": [{"sheetId": sid,
                        "startRowIndex": 1, "endRowIndex": FIM, "startColumnIndex": ia, "endColumnIndex": ib + 1}],
                        "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": "=" + f}]},
                                        "format": fmt}}}})
    print(json.dumps(req, ensure_ascii=False))


def cab_index(l):
    n = 0
    for ch in l:
        n = n * 26 + ord(ch) - 64
    return n - 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "xlsx":
        xlsx(a[1])
    elif len(a) == 2 and a[0] == "drive":
        drive(a[1])
    else:
        sys.exit(__doc__)
