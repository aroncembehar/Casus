import json

with open("/Users/Aron/Desktop/Casus/data/distinct_cases.json", encoding="utf-8") as f:
    cases = json.load(f)
with open("/Users/Aron/Desktop/Casus/data/category_taxonomy.json", encoding="utf-8") as f:
    taxonomy = json.load(f)
with open("/Users/Aron/Desktop/Casus/data/legacy_taxonomy.json", encoding="utf-8") as f:
    legacy_taxonomy = json.load(f)
with open("/Users/Aron/Desktop/Casus/data/ambiguity_log.json", encoding="utf-8") as f:
    ambig = json.load(f)

slug_to_label = {t["slug"]: t["label_fr"] for t in taxonomy}
legacy_slug_to_label = {t["slug"]: t["label_en"] for t in legacy_taxonomy}
cases_sorted = sorted(cases, key=lambda c: c["name"])

lines = []
lines.append("# Casus — Jurisprudence UE Tracking File")
lines.append("")
lines.append(f"Source: `IUR I/Droit européen/jurisprudence UE.pdf` — 284 rows across 17 category tables, extracted via `pdfplumber` table extraction (not text scraping). Document self-reports 176 distinct cases.")
lines.append("")
lines.append(f"**Distinct cases identified after dedup: {len(cases)}** (document's own estimate: 176; honest working range discussed with user: 169-176). This run landed at {len(cases)}, above that range — see \"Count reconciliation\" below for why, and it needs your sign-off before Step 4 sizing.")
lines.append("")
lines.append("## Status")
lines.append("")
lines.append("- [x] PDF table extraction (284/284 rows, all 17 category counts verified against document header claims)")
lines.append("- [x] Deduplication + category union per distinct case")
lines.append("- [x] Ambiguous grouped-row resolution (see Ambiguity Log)")
lines.append("- [x] 17-category taxonomy adopted, old 10-theme cases remapped")
lines.append("- [x] Dual-taxonomy resolution: 5 legacy substantive themes kept as a secondary tag layer")
lines.append("- [ ] Case-by-case content development (Step 4) — NOT STARTED, 0/{} cases at full depth".format(len(cases)))
lines.append("")
lines.append("## Count reconciliation")
lines.append("")
lines.append(f"Exact case-name-string grouping of the 284 rows gives 171 distinct labels. Ten of those labels are the ambiguous bundled/duplicated rows you flagged (or that showed inconsistent jurisdiction/aussi cross-referencing on inspection) — splitting them into their real sub-cases adds 11, for {len(cases)} total. The document's self-reported 176 likely just didn't split all of these the same way. Nothing was forced to hit a target number — see the Ambiguity Log for the reasoning behind every split. If you disagree with a split, flag it and I'll merge it back.")
lines.append("")
lines.append("## 17-category taxonomy (replacing the old 10-theme list)")
lines.append("")
for t in taxonomy:
    n = sum(1 for c in cases if t["slug"] in c["categories"])
    lines.append(f"- `{t['slug']}` — **{t['label_fr']}** ({n} cases)")
lines.append("")
lines.append("**Structural note:** this taxonomy classifies cases by institutional/procedural doctrine (primacy, competences, judicial-review channels, external relations, institutional balance, etc.) — the same axis as a droit constitutionnel européen course. It does **not** include the old taxonomy's substantive-law categories: *Non-discrimination, Market freedoms, Worker's rights, Collective action vs. economic liberty, Solidarity*. Resolved as a **dual-taxonomy structure** (see next section) rather than dropping those categories or forcing them into the 17.")
lines.append("")
lines.append("## Secondary taxonomy layer (legacy substantive themes)")
lines.append("")
lines.append("The 17 categories above are primary/structural. The 5 old substantive categories that don't fit that axis are kept as a **secondary tag layer**, applied only where they genuinely describe the case — not backfilled across all 182 cases, just applied where Step 4 research (or this remap) confirms the fit. Starting set:")
lines.append("")
for t in legacy_taxonomy:
    n = sum(1 for c in cases if t["slug"] in c.get("secondary_tags", []))
    lines.append(f"- `{t['slug']}` — **{t['label_en']}** ({n} cases tagged so far)")
lines.append("")
lines.append("## Old Casus cases (12, not 10) remapped onto the new taxonomy")
lines.append("")
lines.append("Note: the current site has **12** case entries, not 10 (10 is the old *theme* count). All 12 were found in the PDF index itself, so the mapping below uses the document's own category tags as ground truth rather than my guessing, where a match exists.")
lines.append("")
lines.append("| Case | Old theme(s) | New primary categories | Secondary (legacy) tags | Note |")
lines.append("|---|---|---|---|---|")
remap_rows = [
    ("Costa v ENEL", "Primacy of EU law", "`ordre_juridique`", "—", ""),
    ("Internationale Handelsgesellschaft", "Primacy of EU law; Fundamental rights", "`droits_fondamentaux`, `identite_constitutionnelle`, `ordre_juridique`", "—", ""),
    ("Melloni v Ministerio Fiscal", "Primacy of EU law; Fundamental rights", "`droits_fondamentaux`, `identite_constitutionnelle`, `ordre_juridique`", "—", ""),
    ("Commission v Bavarian Lager", "Primacy of EU law", "`equilibre_institutionnel`", "*(none)*", "Old tag was a **mistagging**, not a taxonomy gap — case is about transparency/data-protection balance (Reg 1049/2001 vs Reg 45/2001), not primacy, and none of the 5 legacy substantive tags apply either. No secondary tag added; the old theme is simply dropped as incorrect."),
    ("Kadi I", "Primacy of EU law; EU legal order", "`droits_fondamentaux`, `ordre_juridique`, `relations_exterieures`", "—", ""),
    ("Kadi II", "Primacy of EU law; EU legal order", "`ordre_juridique`, `relations_exterieures`", "—", ""),
    ("Van Gend en Loos", "Direct effect of EU law; EU legal order", "`competences`, `ordre_juridique`", "—", "PDF tags it partly under `competences` — unexpected for the direct-effect classic; kept as document ground truth, worth a sanity check in Step 4."),
    ("Defrenne v Sabena (No 2)", "Direct effect of EU law; Non-discrimination", "`droits_fondamentaux`, `ordre_juridique`", "`non_discrimination`", "Legacy tag restores the old theme via the secondary layer."),
    ("Dominguez", "Direct effect of EU law; Non-discrimination; Worker's rights", "`citoyennete`, `droit_derive`", "`non_discrimination`, `workers_rights`", "Both legacy tags restored; `citoyennete` as primary is still a loose fit for a working-time-directive case, worth a second look in Step 4."),
    ("Opinion 2/13", "EU legal order", "`cedh`, `ordre_juridique`, `relations_exterieures`", "—", ""),
    ("Stauder v City of Ulm", "Fundamental rights", "`droits_fondamentaux`", "—", ""),
    ("Konstantinidis v Stadt Altensteig", "Fundamental rights; Market freedoms", "`citoyennete`, `droits_fondamentaux`", "`market_freedoms`", "Legacy tag restores the old theme via the secondary layer."),
]
for row in remap_rows:
    lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |")
lines.append("")
lines.append("## Ambiguity log (grouped/duplicated rows requiring judgment)")
lines.append("")
for a in ambig:
    lines.append(f"- **{a['raw_label']}** — {a['resolution']}")
    lines.append(f"  - {a['reasoning']}")
lines.append("")
lines.append("## Distinct case checklist (182)")
lines.append("")
lines.append("Format: `- [ ] name — jurisdiction — categories [+ legacy tags]`. Citations are all unverified pending Step 4 research (the source PDF is a keyword index, not a citation list — none were invented).")
lines.append("")
for c in cases_sorted:
    cat_labels = ", ".join(slug_to_label.get(s, s) for s in c["categories"])
    flag = " ⚠️" if c.get("ambiguity") else ""
    legacy = c.get("secondary_tags") or []
    legacy_str = ""
    if legacy:
        legacy_str = " [legacy: " + ", ".join(legacy_slug_to_label.get(s, s) for s in legacy) + "]"
    lines.append(f"- [ ] **{c['name']}** — {c['jurisdiction']} — {cat_labels}{legacy_str}{flag}")

with open("/Users/Aron/Desktop/Casus/TRACKING.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("wrote TRACKING.md,", len(lines), "lines")
