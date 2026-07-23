import json

with open("/Users/Aron/Desktop/Casus/data/parsed_rows.json", encoding="utf-8") as f:
    cats = json.load(f)

FIX = {"BVerfG E": "BVerfGE", "CourED H": "CourEDH"}
for cat in cats:
    for r in cat["rows"]:
        r["jurisdiction"] = FIX.get(r["jurisdiction"], r["jurisdiction"])

with open("/Users/Aron/Desktop/Casus/data/parsed_rows.json", "w", encoding="utf-8") as f:
    json.dump(cats, f, ensure_ascii=False, indent=2)

jurs = set()
for cat in cats:
    for r in cat["rows"]:
        jurs.add(r["jurisdiction"])
print("distinct jurisdictions after fix:", sorted(jurs))

# collect distinct 'aussi' values to check mapping against the 17 category names
cat_names = set(c["name"] for c in cats)
aussi_vals = set()
for cat in cats:
    for r in cat["rows"]:
        for a in r["aussi"]:
            aussi_vals.add(a)

unmatched = sorted(a for a in aussi_vals if a not in cat_names)
print("\ntotal distinct aussi values:", len(aussi_vals))
print("aussi values NOT matching a category name exactly:")
for a in unmatched:
    print(" -", repr(a))
