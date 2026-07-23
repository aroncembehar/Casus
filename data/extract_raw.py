import pdfplumber, re, json

path = "/Users/Aron/Desktop/IUR I/Droit européen/jurisprudence UE.pdf"

CATEGORY_ORDER = []
with pdfplumber.open(path) as pdf:
    for page in pdf.pages:
        text = page.extract_text() or ''
        for line in text.split('\n'):
            if re.match(r'^n\s+\S', line) and 'arrêt' in line.lower() and 'aussi' not in line.lower():
                m = re.match(r'^n\s+(.*?)\s*\((\d+)\s*arrêts?\)\s*$', line.strip())
                if m:
                    CATEGORY_ORDER.append({"name": m.group(1).strip(), "expected_count": int(m.group(2))})

categories_out = []
current = None

with pdfplumber.open(path) as pdf:
    queue = list(CATEGORY_ORDER)
    for pageno, page in enumerate(pdf.pages, start=1):
        tables = page.extract_tables()
        for table in tables:
            if not table:
                continue
            first_cell = (table[0][0] or '').strip()
            is_header = first_cell.startswith('Juridict')
            if is_header:
                if current is not None:
                    categories_out.append(current)
                cat = queue.pop(0)
                current = {"name": cat["name"], "expected_count": cat["expected_count"], "rows": [], "start_page": pageno}
                data_rows = table[1:]
            else:
                data_rows = table
            for row in data_rows:
                current["rows"].append({"page": pageno, "cells": row})
    if current is not None:
        categories_out.append(current)

total_rows = sum(len(c["rows"]) for c in categories_out)
print("categories found:", len(categories_out))
print("total data rows:", total_rows)
for c in categories_out:
    status = "OK" if len(c["rows"]) == c["expected_count"] else "MISMATCH"
    print(f'{status:8} {c["name"]:45} expected={c["expected_count"]:3} got={len(c["rows"]):3} start_page={c["start_page"]}')

with open("/Users/Aron/Desktop/Casus/data/raw_extraction.json", "w", encoding="utf-8") as f:
    json.dump(categories_out, f, ensure_ascii=False, indent=2)
