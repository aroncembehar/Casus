import json, re

with open("/Users/Aron/Desktop/Casus/data/raw_extraction.json", encoding="utf-8") as f:
    categories = json.load(f)

VALID_JUR = {"CJCE","CJUE","CourEDH","CourED","BVerfGE","ATF","AG","TPI","Trib"}

def clean(s):
    return re.sub(r'\s+', ' ', (s or '').strip())

parsed_categories = []
anomalies = []

for cat in categories:
    out_rows = []
    last_jur = None
    for r in cat["rows"]:
        cells = r["cells"]
        if len(cells) != 3:
            anomalies.append({"category": cat["name"], "page": r["page"], "issue": f"cell count {len(cells)}", "cells": cells})
            while len(cells) < 3:
                cells.append('')
            cells = cells[:3]
        jur_raw, name_raw, subj_raw = cells
        jur = clean(jur_raw)
        if not jur:
            anomalies.append({"category": cat["name"], "page": r["page"], "issue": "empty jurisdiction, forward-filled", "prev": last_jur, "name": clean(name_raw)})
            jur = last_jur
        else:
            last_jur = jur
        name = clean(name_raw)
        subj_full = subj_raw or ''
        # split out "aussi :" lines
        lines = [l.strip() for l in subj_full.split('\n')]
        aussi = []
        keyword_lines = []
        for l in lines:
            m = re.match(r'^n?\s*aussi\s*:\s*(.*)$', l, re.IGNORECASE)
            if m:
                aussi.extend([a.strip() for a in m.group(1).split(',') if a.strip()])
            else:
                if l:
                    keyword_lines.append(l)
        subj = clean(' '.join(keyword_lines))
        out_rows.append({"page": r["page"], "jurisdiction": jur, "name": name, "keywords": subj, "aussi": aussi})
    parsed_categories.append({"name": cat["name"], "rows": out_rows})

with open("/Users/Aron/Desktop/Casus/data/parsed_rows.json", "w", encoding="utf-8") as f:
    json.dump(parsed_categories, f, ensure_ascii=False, indent=2)

print("total anomalies:", len(anomalies))
for a in anomalies:
    print(a)

# distinct jurisdiction values seen
jurs = set()
for cat in parsed_categories:
    for r in cat["rows"]:
        jurs.add(r["jurisdiction"])
print("distinct jurisdiction tokens:", sorted(jurs))
