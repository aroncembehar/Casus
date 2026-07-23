import json, re
from collections import defaultdict

with open("/Users/Aron/Desktop/Casus/data/parsed_rows.json", encoding="utf-8") as f:
    cats = json.load(f)

CATEGORY_SLUGS = [
    ("cedh", "CEDH / Droits CEDH"),
    ("citoyennete", "Citoyenneté / libre circulation"),
    ("competences", "Compétences / base juridique"),
    ("droit_derive", "Droit dérivé / actes juridiques"),
    ("droits_fondamentaux", "Droits fondamentaux"),
    ("identite_constitutionnelle", "Identité constitutionnelle nationale"),
    ("jurisprudence_nationale", "Jurisprudence nationale (BVerfGE / ATF)"),
    ("mise_en_oeuvre", "Mise en œuvre / autonomie procédurale"),
    ("ordre_juridique", "Ordre juridique / primauté / effet direct"),
    ("procedures_legislatives", "Procédures législatives"),
    ("recours_annulation", "Recours en annulation"),
    ("recours_manquement", "Recours en manquement"),
    ("relations_exterieures", "Relations extérieures / DI"),
    ("renvoi_prejudiciel", "Renvoi préjudiciel"),
    ("responsabilite_extracontractuelle", "Responsabilité extracontractuelle"),
    ("revision_traites", "Révision des traités / Kompetenz"),
    ("equilibre_institutionnel", "Équilibre institutionnel"),
]
NAME_TO_SLUG = {name: slug for slug, name in CATEGORY_SLUGS}

by_name = defaultdict(list)
for cat in cats:
    for r in cat["rows"]:
        by_name[r["name"]].append({"category": cat["name"], **r})

def slugify(s):
    s = s.lower()
    s = re.sub(r'[^\w\s-]', '', s, flags=re.UNICODE)
    s = re.sub(r'\s+', '-', s.strip())
    return s

# ---- manual overrides for ambiguous grouped/duplicated names ----
# each override: split a raw name-group into N sub-cases.
# 'rows' selects which row indices (0-based, in by_name[name] order) feed each sub-case;
# if omitted, all rows of the group feed that sub-case (used when the bundling is a single
# row and cannot be disambiguated from the source data alone).
OVERRIDES = {
    "Dhabib ; Schipani ; Arlewin": {
        "reasoning": "Single bundled row citing three separate CourEDH applicants under one label (study-notes shorthand). Dhahbi v Italy and Schipani and Others v Italy both concern a domestic court's duty to give reasons when declining an Art. 267 TFEU preliminary reference (Art. 6 ECHR fair trial); Arlewin v Sweden concerns extraterritorial jurisdiction over defamation. Distinct facts, likely distinct holdings -> split into 3, sharing the row's category set (cannot subdivide categories per sub-case from the source alone).",
        "cases": [
            {"name": "Dhahbi v Italie", "jurisdiction": "CourEDH"},
            {"name": "Schipani et autres c. Italie", "jurisdiction": "CourEDH"},
            {"name": "Arlewin c. Suède", "jurisdiction": "CourEDH"},
        ],
    },
    "Solange I et Solange II": {
        "reasoning": "Explicitly two BVerfGE judgments (1974 and 1986) forming a well-known doctrinal pair; not a single case.",
        "cases": [
            {"name": "Solange I", "jurisdiction": "BVerfGE"},
            {"name": "Solange II", "jurisdiction": "BVerfGE"},
        ],
    },
    "Publicité sur le tabac (I et II)": {
        "reasoning": "Two distinct CJUE judgments, Germany v Parliament and Council (2000 and 2006), on tobacco-advertising directive competence.",
        "cases": [
            {"name": "Publicité sur le tabac I (Allemagne c. Parlement et Conseil)", "jurisdiction": "CJUE"},
            {"name": "Publicité sur le tabac II (Allemagne c. Parlement et Conseil)", "jurisdiction": "CJUE"},
        ],
    },
    "Tas-Hagen ; Morgan & Bucher": {
        "reasoning": "Semicolon separates two distinct citizenship cases: Tas-Hagen and Tas (C-192/05), and the joined case Morgan and Bucher (C-11/06 & C-12/06) — the ampersand here is part of that joined case's conventional shorthand, not a further split.",
        "cases": [
            {"name": "Tas-Hagen et Tas", "jurisdiction": "CJUE"},
            {"name": "Morgan et Bucher", "jurisdiction": "CJUE"},
        ],
    },
    "Aranyosi et Caldararu et Poplawski": {
        "reasoning": "Aranyosi and Caldararu (joined cases C-404/15 & C-659/15 PPU) is itself a single joined judgment. Poplawski is a separate later case (either Poplawski I, C-579/15, or Poplawski II, C-573/17 — citation to be confirmed) on the same EAW/primacy theme. Split into 2, not 3.",
        "cases": [
            {"name": "Aranyosi et Caldararu", "jurisdiction": "CJUE"},
            {"name": "Poplawski", "jurisdiction": "CJUE"},
        ],
    },
    "Unibet ; Avis 1/09": {
        "reasoning": "Semicolon separates two unrelated matters: Unibet (C-432/05, effective judicial protection) and Opinion 1/09 (draft unified patent litigation agreement).",
        "cases": [
            {"name": "Unibet", "jurisdiction": "CJUE"},
            {"name": "Avis 1/09", "jurisdiction": "AG"},
        ],
    },
    "Kolpinghuis et Adeneler": {
        "reasoning": "Two distinct judgments on different (though related) doctrines: Kolpinghuis Nijmegen (80/86, no direct effect of an unimplemented directive against an individual in criminal proceedings) and Adeneler (C-212/04, consistent-interpretation / indirect-effect duty).",
        "cases": [
            {"name": "Kolpinghuis Nijmegen", "jurisdiction": "CJCE"},
            {"name": "Adeneler e.a.", "jurisdiction": "CJUE"},
        ],
    },
    "Holtz & Willemsen et Bergaderm": {
        "reasoning": "'Holtz & Willemsen' is itself a single case's proper name (153/73, the ampersand is part of the applicant company name, not a bundling marker). 'et Bergaderm' adds a second, later case (C-352/98 P) aligning non-contractual EU liability with the Member State liability standard. Split into 2.",
        "cases": [
            {"name": "Holtz & Willemsen", "jurisdiction": "CJCE"},
            {"name": "Bergaderm et Goupil c. Commission", "jurisdiction": "CJUE"},
        ],
    },
}

# Discovered (not user-flagged) ambiguous duplicate-name clusters, resolved via aussi cross-reference analysis.
CLUSTER_OVERRIDES = {
    "Parlement c. Conseil": {
        "reasoning": "Same case-name label reused for two unrelated CJCE/AG matters. Rows in Compétences/base juridique, Procédures législatives and Équilibre institutionnel mutually cross-reference each other via 'aussi' (consistent triangle) and share identical keyword text ('double base juridique') -> one case. The Révision des traités/Kompetenz row (AG opinion) has no aussi links to the others and describes an unrelated subject (customary-law treaty revision) -> a second, different case. Exact citations for both need Step 4 verification (many 'Parlement c. Conseil' cases exist in CJCE case law, e.g. Chernobyl C-70/88, Bangladesh aid C-181/91, GSP C-45/86).",
        "clusters": [
            {"name": "Parlement c. Conseil (double base juridique)", "jurisdiction": "CJCE",
             "categories": ["competences", "procedures_legislatives", "equilibre_institutionnel"]},
            {"name": "Parlement c. Conseil (révision par voie coutumière)", "jurisdiction": "AG",
             "categories": ["revision_traites"]},
        ],
    },
    "Conseil c. Commission": {
        "reasoning": "Two 'Équilibre institutionnel' rows exist for this name label with different keyword phrasing and different jurisdictions (CJCE vs CJUE); only one of them cross-references the Procédures législatives row via 'aussi'. Read together this looks like two different loyal-cooperation cases decided years apart rather than one case appearing three times. Citations to be confirmed in Step 4.",
        "clusters": [
            {"name": "Conseil c. Commission (coopération loyale — répartition des attributions)", "jurisdiction": "CJCE",
             "categories": ["procedures_legislatives", "equilibre_institutionnel"]},
            {"name": "Conseil c. Commission (coopération loyale — accords interinstitutionnels)", "jurisdiction": "CJUE",
             "categories": ["equilibre_institutionnel"]},
        ],
    },
}

distinct_cases = []
ambiguity_log = []

for name, rows in by_name.items():
    if name in OVERRIDES:
        ov = OVERRIDES[name]
        all_cat_slugs = sorted(set(NAME_TO_SLUG[r["category"]] for r in rows) |
                                set(NAME_TO_SLUG[a] for r in rows for a in r["aussi"]))
        for sub in ov["cases"]:
            distinct_cases.append({
                "id": slugify(sub["name"]),
                "name": sub["name"],
                "jurisdiction": sub["jurisdiction"],
                "citation": None,
                "citation_status": "unverified — needs Step 4 research",
                "categories": all_cat_slugs,
                "source": {
                    "bundled_from_row_label": name,
                    "pages": sorted(set(r["page"] for r in rows)),
                    "raw_keywords": [r["keywords"] for r in rows],
                },
                "ambiguity": ov["reasoning"],
            })
        ambiguity_log.append({"raw_label": name, "resolution": f"split into {len(ov['cases'])} cases", "reasoning": ov["reasoning"]})
        continue

    if name in CLUSTER_OVERRIDES:
        ov = CLUSTER_OVERRIDES[name]
        jur_by_row = [r["jurisdiction"] for r in rows]
        for sub in ov["clusters"]:
            distinct_cases.append({
                "id": slugify(sub["name"]),
                "name": sub["name"],
                "jurisdiction": sub["jurisdiction"],
                "citation": None,
                "citation_status": "unverified — needs Step 4 research",
                "categories": sub["categories"],
                "source": {
                    "bundled_from_row_label": name,
                    "pages": sorted(set(r["page"] for r in rows)),
                    "raw_keywords": [r["keywords"] for r in rows],
                },
                "ambiguity": ov["reasoning"],
            })
        ambiguity_log.append({"raw_label": name, "resolution": f"split into {len(ov['clusters'])} cases (discovered via aussi cross-reference inconsistency, not in original flagged list)", "reasoning": ov["reasoning"]})
        continue

    # default path: union of each row's own category + its aussi-referenced categories
    all_cat_slugs = sorted(set(NAME_TO_SLUG[r["category"]] for r in rows) |
                            set(NAME_TO_SLUG[a] for r in rows for a in r["aussi"]))
    jurs = sorted(set(r["jurisdiction"] for r in rows))
    note = None
    if len(jurs) > 1:
        note = f"Same case cited under multiple jurisdiction labels across rows ({', '.join(jurs)}) — merged as one case (e.g. AG opinion + Court judgment both indexed); verify in Step 4."
        ambiguity_log.append({"raw_label": name, "resolution": "merged, dual jurisdiction retained as note", "reasoning": note})
    primary_jur = jurs[-1] if "CJUE" in jurs or "CJCE" in jurs else jurs[0]
    # prefer CJUE/CJCE as primary display jurisdiction over AG when both present
    for pref in ("CJUE", "CJCE", "CourEDH", "BVerfGE", "ATF", "AG"):
        if pref in jurs:
            primary_jur = pref
            break
    distinct_cases.append({
        "id": slugify(name),
        "name": name,
        "jurisdiction": primary_jur,
        "jurisdiction_all_labels": jurs if len(jurs) > 1 else None,
        "citation": None,
        "citation_status": "unverified — needs Step 4 research",
        "categories": all_cat_slugs,
        "source": {
            "pages": sorted(set(r["page"] for r in rows)),
            "raw_keywords": [r["keywords"] for r in rows],
        },
        "ambiguity": note,
    })

print("TOTAL DISTINCT CASES:", len(distinct_cases))
print("ambiguity log entries:", len(ambiguity_log))

with open("/Users/Aron/Desktop/Casus/data/distinct_cases.json", "w", encoding="utf-8") as f:
    json.dump(distinct_cases, f, ensure_ascii=False, indent=2)
with open("/Users/Aron/Desktop/Casus/data/ambiguity_log.json", "w", encoding="utf-8") as f:
    json.dump(ambiguity_log, f, ensure_ascii=False, indent=2)
with open("/Users/Aron/Desktop/Casus/data/category_taxonomy.json", "w", encoding="utf-8") as f:
    json.dump([{"slug": s, "label_fr": n} for s, n in CATEGORY_SLUGS], f, ensure_ascii=False, indent=2)

# sanity: category coverage counts
from collections import Counter
cnt = Counter()
for c in distinct_cases:
    for cat in c["categories"]:
        cnt[cat] += 1
print("\ncase counts per category (post-dedup):")
for slug, name in CATEGORY_SLUGS:
    print(f"  {name:45} {cnt[slug]}")
