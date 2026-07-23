import json

with open("/Users/Aron/Desktop/Casus/data/distinct_cases.json", encoding="utf-8") as f:
    cases = json.load(f)

PATCH = {
    "defrenne-ii": {
        "secondary_tags": ["non_discrimination"],
        "secondary_tags_note": "Matches old Casus tag 'Non-discrimination' (case concerns equal pay for equal work, Art. 119/157)."
    },
    "maribel-dominguez": {
        "secondary_tags": ["non_discrimination", "workers_rights"],
        "secondary_tags_note": "Matches old Casus tags 'Non-discrimination' + \"Worker's rights\" (paid annual leave under Directive 2003/88)."
    },
    "konstantinidis": {
        "secondary_tags": ["market_freedoms"],
        "secondary_tags_note": "Matches old Casus tag 'Market freedoms' (freedom to provide services, transliteration of name affecting professional practice)."
    },
    "bavarian-lager": {
        "secondary_tags": [],
        "secondary_tags_note": "None of the 5 legacy substantive categories apply — the case concerns transparency/data-protection balance (Reg 1049/2001 vs Reg 45/2001), not primacy, non-discrimination, market freedoms, worker's rights, collective action, or solidarity. The old 'Primacy of EU law' tag was a mistagging, not a taxonomy-coverage gap; no legacy tag should be forced here."
    },
}

for c in cases:
    if c["id"] in PATCH:
        c.update(PATCH[c["id"]])

with open("/Users/Aron/Desktop/Casus/data/distinct_cases.json", "w", encoding="utf-8") as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

for cid in PATCH:
    match = [c for c in cases if c["id"] == cid][0]
    print(cid, "->", match.get("secondary_tags"), "|", match.get("secondary_tags_note")[:60])
