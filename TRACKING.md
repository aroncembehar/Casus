# Casus — Jurisprudence UE Tracking File

Source: `IUR I/Droit européen/jurisprudence UE.pdf` — 284 rows across 17 category tables, extracted via `pdfplumber` table extraction (not text scraping). Document self-reports 176 distinct cases.

**Distinct cases identified after dedup: 182** (document's own estimate: 176; honest working range discussed with user: 169-176). This run landed at 182, above that range — see "Count reconciliation" below for why, and it needs your sign-off before Step 4 sizing.

## Status

- [x] PDF table extraction (284/284 rows, all 17 category counts verified against document header claims)
- [x] Deduplication + category union per distinct case
- [x] Ambiguous grouped-row resolution (see Ambiguity Log)
- [x] 17-category taxonomy adopted, old 10-theme cases remapped
- [x] Dual-taxonomy resolution: 5 legacy substantive themes kept as a secondary tag layer
- [ ] Case-by-case content development (Step 4) — NOT STARTED, 0/182 cases at full depth

## Count reconciliation

Exact case-name-string grouping of the 284 rows gives 171 distinct labels. Ten of those labels are the ambiguous bundled/duplicated rows you flagged (or that showed inconsistent jurisdiction/aussi cross-referencing on inspection) — splitting them into their real sub-cases adds 11, for 182 total. The document's self-reported 176 likely just didn't split all of these the same way. Nothing was forced to hit a target number — see the Ambiguity Log for the reasoning behind every split. If you disagree with a split, flag it and I'll merge it back.

## 17-category taxonomy (replacing the old 10-theme list)

- `cedh` — **CEDH / Droits CEDH** (13 cases)
- `citoyennete` — **Citoyenneté / libre circulation** (14 cases)
- `competences` — **Compétences / base juridique** (20 cases)
- `droit_derive` — **Droit dérivé / actes juridiques** (29 cases)
- `droits_fondamentaux` — **Droits fondamentaux** (31 cases)
- `identite_constitutionnelle` — **Identité constitutionnelle nationale** (10 cases)
- `jurisprudence_nationale` — **Jurisprudence nationale (BVerfGE / ATF)** (3 cases)
- `mise_en_oeuvre` — **Mise en œuvre / autonomie procédurale** (22 cases)
- `ordre_juridique` — **Ordre juridique / primauté / effet direct** (24 cases)
- `procedures_legislatives` — **Procédures législatives** (7 cases)
- `recours_annulation` — **Recours en annulation** (21 cases)
- `recours_manquement` — **Recours en manquement** (12 cases)
- `relations_exterieures` — **Relations extérieures / DI** (24 cases)
- `renvoi_prejudiciel` — **Renvoi préjudiciel** (30 cases)
- `responsabilite_extracontractuelle` — **Responsabilité extracontractuelle** (16 cases)
- `revision_traites` — **Révision des traités / Kompetenz** (6 cases)
- `equilibre_institutionnel` — **Équilibre institutionnel** (14 cases)

**Structural note:** this taxonomy classifies cases by institutional/procedural doctrine (primacy, competences, judicial-review channels, external relations, institutional balance, etc.) — the same axis as a droit constitutionnel européen course. It does **not** include the old taxonomy's substantive-law categories: *Non-discrimination, Market freedoms, Worker's rights, Collective action vs. economic liberty, Solidarity*. Resolved as a **dual-taxonomy structure** (see next section) rather than dropping those categories or forcing them into the 17.

## Secondary taxonomy layer (legacy substantive themes)

The 17 categories above are primary/structural. The 5 old substantive categories that don't fit that axis are kept as a **secondary tag layer**, applied only where they genuinely describe the case — not backfilled across all 182 cases, just applied where Step 4 research (or this remap) confirms the fit. Starting set:

- `non_discrimination` — **Non-discrimination** (2 cases tagged so far)
- `market_freedoms` — **Market freedoms** (1 cases tagged so far)
- `workers_rights` — **Worker's rights** (1 cases tagged so far)
- `collective_action_vs_economic_liberty` — **Collective action vs. economic liberty** (0 cases tagged so far)
- `solidarity` — **Solidarity** (0 cases tagged so far)

## Old Casus cases (12, not 10) remapped onto the new taxonomy

Note: the current site has **12** case entries, not 10 (10 is the old *theme* count). All 12 were found in the PDF index itself, so the mapping below uses the document's own category tags as ground truth rather than my guessing, where a match exists.

| Case | Old theme(s) | New primary categories | Secondary (legacy) tags | Note |
|---|---|---|---|---|
| Costa v ENEL | Primacy of EU law | `ordre_juridique` | — |  |
| Internationale Handelsgesellschaft | Primacy of EU law; Fundamental rights | `droits_fondamentaux`, `identite_constitutionnelle`, `ordre_juridique` | — |  |
| Melloni v Ministerio Fiscal | Primacy of EU law; Fundamental rights | `droits_fondamentaux`, `identite_constitutionnelle`, `ordre_juridique` | — |  |
| Commission v Bavarian Lager | Primacy of EU law | `equilibre_institutionnel` | *(none)* | Old tag was a **mistagging**, not a taxonomy gap — case is about transparency/data-protection balance (Reg 1049/2001 vs Reg 45/2001), not primacy, and none of the 5 legacy substantive tags apply either. No secondary tag added; the old theme is simply dropped as incorrect. |
| Kadi I | Primacy of EU law; EU legal order | `droits_fondamentaux`, `ordre_juridique`, `relations_exterieures` | — |  |
| Kadi II | Primacy of EU law; EU legal order | `ordre_juridique`, `relations_exterieures` | — |  |
| Van Gend en Loos | Direct effect of EU law; EU legal order | `competences`, `ordre_juridique` | — | PDF tags it partly under `competences` — unexpected for the direct-effect classic; kept as document ground truth, worth a sanity check in Step 4. |
| Defrenne v Sabena (No 2) | Direct effect of EU law; Non-discrimination | `droits_fondamentaux`, `ordre_juridique` | `non_discrimination` | Legacy tag restores the old theme via the secondary layer. |
| Dominguez | Direct effect of EU law; Non-discrimination; Worker's rights | `citoyennete`, `droit_derive` | `non_discrimination`, `workers_rights` | Both legacy tags restored; `citoyennete` as primary is still a loose fit for a working-time-directive case, worth a second look in Step 4. |
| Opinion 2/13 | EU legal order | `cedh`, `ordre_juridique`, `relations_exterieures` | — |  |
| Stauder v City of Ulm | Fundamental rights | `droits_fondamentaux` | — |  |
| Konstantinidis v Stadt Altensteig | Fundamental rights; Market freedoms | `citoyennete`, `droits_fondamentaux` | `market_freedoms` | Legacy tag restores the old theme via the secondary layer. |

## Ambiguity log (grouped/duplicated rows requiring judgment)

- **Dhabib ; Schipani ; Arlewin** — split into 3 cases
  - Single bundled row citing three separate CourEDH applicants under one label (study-notes shorthand). Dhahbi v Italy and Schipani and Others v Italy both concern a domestic court's duty to give reasons when declining an Art. 267 TFEU preliminary reference (Art. 6 ECHR fair trial); Arlewin v Sweden concerns extraterritorial jurisdiction over defamation. Distinct facts, likely distinct holdings -> split into 3, sharing the row's category set (cannot subdivide categories per sub-case from the source alone).
- **Rottmann** — merged, dual jurisdiction retained as note
  - Same case cited under multiple jurisdiction labels across rows (AG, CJUE) — merged as one case (e.g. AG opinion + Court judgment both indexed); verify in Step 4.
- **Tas-Hagen ; Morgan & Bucher** — split into 2 cases
  - Semicolon separates two distinct citizenship cases: Tas-Hagen and Tas (C-192/05), and the joined case Morgan and Bucher (C-11/06 & C-12/06) — the ampersand here is part of that joined case's conventional shorthand, not a further split.
- **Parlement c. Conseil** — split into 2 cases (discovered via aussi cross-reference inconsistency, not in original flagged list)
  - Same case-name label reused for two unrelated CJCE/AG matters. Rows in Compétences/base juridique, Procédures législatives and Équilibre institutionnel mutually cross-reference each other via 'aussi' (consistent triangle) and share identical keyword text ('double base juridique') -> one case. The Révision des traités/Kompetenz row (AG opinion) has no aussi links to the others and describes an unrelated subject (customary-law treaty revision) -> a second, different case. Exact citations for both need Step 4 verification (many 'Parlement c. Conseil' cases exist in CJCE case law, e.g. Chernobyl C-70/88, Bangladesh aid C-181/91, GSP C-45/86).
- **Publicité sur le tabac (I et II)** — split into 2 cases
  - Two distinct CJUE judgments, Germany v Parliament and Council (2000 and 2006), on tobacco-advertising directive competence.
- **Kolpinghuis et Adeneler** — split into 2 cases
  - Two distinct judgments on different (though related) doctrines: Kolpinghuis Nijmegen (80/86, no direct effect of an unimplemented directive against an individual in criminal proceedings) and Adeneler (C-212/04, consistent-interpretation / indirect-effect duty).
- **Solange I et Solange II** — split into 2 cases
  - Explicitly two BVerfGE judgments (1974 and 1986) forming a well-known doctrinal pair; not a single case.
- **Aranyosi et Caldararu et Poplawski** — split into 2 cases
  - Aranyosi and Caldararu (joined cases C-404/15 & C-659/15 PPU) is itself a single joined judgment. Poplawski is a separate later case (either Poplawski I, C-579/15, or Poplawski II, C-573/17 — citation to be confirmed) on the same EAW/primacy theme. Split into 2, not 3.
- **Conseil c. Commission** — split into 2 cases (discovered via aussi cross-reference inconsistency, not in original flagged list)
  - Two 'Équilibre institutionnel' rows exist for this name label with different keyword phrasing and different jurisdictions (CJCE vs CJUE); only one of them cross-references the Procédures législatives row via 'aussi'. Read together this looks like two different loyal-cooperation cases decided years apart rather than one case appearing three times. Citations to be confirmed in Step 4.
- **Unibet ; Avis 1/09** — split into 2 cases
  - Semicolon separates two unrelated matters: Unibet (C-432/05, effective judicial protection) and Opinion 1/09 (draft unified patent litigation agreement).
- **Holtz & Willemsen et Bergaderm** — split into 2 cases
  - 'Holtz & Willemsen' is itself a single case's proper name (153/73, the ampersand is part of the applicant company name, not a bundling marker). 'et Bergaderm' adds a second, later case (C-352/98 P) aligning non-contractual EU liability with the Member State liability standard. Split into 2.

## Distinct case checklist (182)

Format: `- [ ] name — jurisdiction — categories [+ legacy tags]`. Citations are all unverified pending Step 4 research (the source PDF is a keyword index, not a citation list — none were invented).

- [ ] **AETR** — CJCE — Compétences / base juridique, Recours en annulation, Relations extérieures / DI
- [ ] **AETR (objet)** — CJUE — Recours en annulation
- [ ] **AKZO** — CJCE — Équilibre institutionnel
- [ ] **ATF 123 I 152** — ATF — Jurisprudence nationale (BVerfGE / ATF)
- [ ] **ATF 129 III 335** — ATF — Jurisprudence nationale (BVerfGE / ATF)
- [ ] **ATF 137 III 487 ; ATF 137 II 199** — ATF — Jurisprudence nationale (BVerfGE / ATF)
- [ ] **Achmea** — CJUE — Relations extérieures / DI, Renvoi préjudiciel
- [ ] **Adeneler e.a.** — CJUE — Droit dérivé / actes juridiques, Mise en œuvre / autonomie procédurale, Renvoi préjudiciel ⚠️
- [ ] **Affaire dioxyde de titane (Commission c. Conseil)** — CJCE — Compétences / base juridique, Procédures législatives
- [ ] **Ahokainen** — AG — Compétences / base juridique
- [ ] **Alimanovic** — CJUE — Citoyenneté / libre circulation
- [ ] **Allemagne c. Commission + British American Tobacco** — CJCE — Droit dérivé / actes juridiques
- [ ] **Aranyosi et Caldararu** — CJUE — Mise en œuvre / autonomie procédurale ⚠️
- [ ] **Arcelor** — AG — Identité constitutionnelle nationale
- [ ] **Arcor** — CJCE — Droit dérivé / actes juridiques
- [ ] **Arlewin c. Suède** — CourEDH — CEDH / Droits CEDH, Renvoi préjudiciel ⚠️
- [ ] **Associacao Sindical dos Juizes Portugueses** — CJUE — Droits fondamentaux, Mise en œuvre / autonomie procédurale
- [ ] **Audiolux** — CJUE — Droits fondamentaux, Ordre juridique / primauté / effet direct
- [ ] **Avis 1/09** — AG — Équilibre institutionnel, Renvoi préjudiciel ⚠️
- [ ] **Avis 1/76** — CJCE — Compétences / base juridique, Relations extérieures / DI
- [ ] **Avis 1/91** — CJCE — Ordre juridique / primauté / effet direct, Relations extérieures / DI
- [ ] **Avis 2/13** — CJUE — CEDH / Droits CEDH, Ordre juridique / primauté / effet direct, Relations extérieures / DI
- [ ] **Avis 2/25** — CJUE — Compétences / base juridique, Relations extérieures / DI
- [ ] **Avis 2/94** — CJCE — CEDH / Droits CEDH, Compétences / base juridique, Révision des traités / Kompetenz
- [ ] **Avis ciel ouvert** — CJCE — Compétences / base juridique, Relations extérieures / DI
- [ ] **BASF** — CJCE — Droit dérivé / actes juridiques, Recours en annulation
- [ ] **BECTU** — CJCE — Droits fondamentaux
- [ ] **Bavaria** — CJCE — Recours en annulation
- [ ] **Bavarian Lager** — CJUE — Équilibre institutionnel
- [ ] **Becker et Grosskrotzenburg** — CJCE — Droit dérivé / actes juridiques, Ordre juridique / primauté / effet direct
- [ ] **Bergaderm et Goupil c. Commission** — CJUE — Responsabilité extracontractuelle ⚠️
- [ ] **Biocides & Commission c. Conseil et Parlement** — CJUE — Droit dérivé / actes juridiques
- [ ] **Bosman** — CJCE — Renvoi préjudiciel
- [ ] **Bosphorus** — CourEDH — CEDH / Droits CEDH, Droits fondamentaux
- [ ] **Brasserie du pêcheur** — CJUE — Recours en manquement, Responsabilité extracontractuelle
- [ ] **CILFIT (283/81)** — CJCE — Renvoi préjudiciel
- [ ] **CLIFIT** — CJCE — Droit dérivé / actes juridiques, Renvoi préjudiciel
- [ ] **Chemiefarma** — CJCE — Procédures législatives
- [ ] **Chen** — CJCE — Citoyenneté / libre circulation
- [ ] **Commission c. Belgique** — CJUE — Droit dérivé / actes juridiques, Mise en œuvre / autonomie procédurale
- [ ] **Commission c. Conseil (AETR étendu)** — CJUE — Compétences / base juridique, Relations extérieures / DI
- [ ] **Commission c. Espagne** — CJCE — Recours en manquement
- [ ] **Commission c. Espagne (manquement judiciaire)** — CJUE — Recours en manquement, Responsabilité extracontractuelle
- [ ] **Commission c. Finlande** — CJCE — Relations extérieures / DI
- [ ] **Commission c. Grèce** — CJCE — Recours en manquement
- [ ] **Commission c. Italie** — CJCE — Ordre juridique / primauté / effet direct, Recours en manquement
- [ ] **Commission c. Portugal** — CJCE — Recours en manquement
- [ ] **Conseil c. Commission (coopération loyale — accords interinstitutionnels)** — CJUE — Équilibre institutionnel ⚠️
- [ ] **Conseil c. Commission (coopération loyale — répartition des attributions)** — CJCE — Procédures législatives, Équilibre institutionnel ⚠️
- [ ] **Cordoniu** — CJCE — Recours en annulation
- [ ] **Costa c. ENEL (1964)** — CJCE — Ordre juridique / primauté / effet direct
- [ ] **D'Hoop** — CJCE — Citoyenneté / libre circulation
- [ ] **Daichii Sankyo** — CJUE — Relations extérieures / DI
- [ ] **Dano** — CJUE — Citoyenneté / libre circulation
- [ ] **Defrenne I** — CJCE — Révision des traités / Kompetenz
- [ ] **Defrenne II** — CJCE — Droits fondamentaux, Ordre juridique / primauté / effet direct [legacy: Non-discrimination]
- [ ] **Defrenne III** — CJCE — Droits fondamentaux, Ordre juridique / primauté / effet direct
- [ ] **Demirel** — CJCE — Relations extérieures / DI
- [ ] **Deutsche Milchkontor** — CJCE — Mise en œuvre / autonomie procédurale
- [ ] **Deutsche Telekom** — CJCE — Recours en manquement
- [ ] **Deutz** — CJCE — Droit dérivé / actes juridiques
- [ ] **Dhahbi v Italie** — CourEDH — CEDH / Droits CEDH, Renvoi préjudiciel ⚠️
- [ ] **Digital Rights** — CJUE — Droits fondamentaux, Recours en annulation
- [ ] **Dillenkofer** — CJUE — Recours en manquement, Responsabilité extracontractuelle
- [ ] **Dorsch Consult** — CJCE — Renvoi préjudiciel
- [ ] **ERT** — CJCE — Droits fondamentaux, Mise en œuvre / autonomie procédurale
- [ ] **Elchinov** — CJCE — Ordre juridique / primauté / effet direct, Renvoi préjudiciel
- [ ] **Faccini Dori** — CJCE — Droit dérivé / actes juridiques, Renvoi préjudiciel
- [ ] **Factortame** — CJCE — Mise en œuvre / autonomie procédurale, Ordre juridique / primauté / effet direct, Responsabilité extracontractuelle
- [ ] **Ferreira da Silva** — CJUE — Recours en manquement, Renvoi préjudiciel, Responsabilité extracontractuelle
- [ ] **Firma A. Racke** — CJCE — Droit dérivé / actes juridiques
- [ ] **Foto-Frost** — CJCE — Renvoi préjudiciel
- [ ] **Francovich** — CJCE — Recours en manquement, Responsabilité extracontractuelle
- [ ] **Fransson** — CJUE — Droits fondamentaux
- [ ] **Franz Grad** — CJCE — Droit dérivé / actes juridiques, Ordre juridique / primauté / effet direct
- [ ] **Front Polisario** — CJUE — Recours en annulation, Relations extérieures / DI
- [ ] **Fédéchar** — CJCE — Compétences / base juridique
- [ ] **Gauweiler (C-62/14)** — AG — Identité constitutionnelle nationale, Renvoi préjudiciel
- [ ] **Gennaro Curra** — CJUE — Relations extérieures / DI
- [ ] **Giordano** — CJUE — Responsabilité extracontractuelle
- [ ] **Glatzel** — CJUE — Droit dérivé / actes juridiques, Relations extérieures / DI
- [ ] **Global Starnet** — CJUE — Renvoi préjudiciel
- [ ] **Goodwin** — CourEDH — CEDH / Droits CEDH
- [ ] **Grimaldi** — CJUE — Droit dérivé / actes juridiques
- [ ] **Grzelczyk** — CJCE — Citoyenneté / libre circulation
- [ ] **Haegeman et Opel Austria** — CJCE — Relations extérieures / DI
- [ ] **Handelsgesellschaft** — CJCE — Droits fondamentaux, Identité constitutionnelle nationale, Ordre juridique / primauté / effet direct
- [ ] **Holtz & Willemsen** — CJCE — Responsabilité extracontractuelle ⚠️
- [ ] **IATA** — CJCE — Équilibre institutionnel, Renvoi préjudiciel
- [ ] **IBM** — CJCE — Recours en annulation
- [ ] **International Fruits** — CJCE — Relations extérieures / DI
- [ ] **Inuit** — CJUE — Recours en annulation
- [ ] **Isoglucose** — CJCE — Équilibre institutionnel, Procédures législatives
- [ ] **James Elliott** — CJUE — Droit dérivé / actes juridiques, Équilibre institutionnel
- [ ] **Kadi I** — CJCE — Droits fondamentaux, Ordre juridique / primauté / effet direct, Relations extérieures / DI
- [ ] **Kadi II** — CJUE — Ordre juridique / primauté / effet direct, Relations extérieures / DI
- [ ] **Kampffmeyer** — CJCE — Responsabilité extracontractuelle
- [ ] **Kempter (C-2/06)** — CJCE — Renvoi préjudiciel
- [ ] **Kolpinghuis Nijmegen** — CJCE — Droit dérivé / actes juridiques, Mise en œuvre / autonomie procédurale, Renvoi préjudiciel ⚠️
- [ ] **Konstantinidis** — AG — Citoyenneté / libre circulation, Droits fondamentaux [legacy: Market freedoms]
- [ ] **Köbler** — CJUE — Recours en manquement, Renvoi préjudiciel, Responsabilité extracontractuelle
- [ ] **Kücükdeveci** — CJUE — Droit dérivé / actes juridiques, Droits fondamentaux, Renvoi préjudiciel
- [ ] **Kühne et Heitz** — CJCE — Mise en œuvre / autonomie procédurale, Renvoi préjudiciel
- [ ] **Laval** — CJCE — Compétences / base juridique, Droits fondamentaux
- [ ] **Les Verts** — CJCE — Équilibre institutionnel, Ordre juridique / primauté / effet direct, Recours en annulation
- [ ] **Lissabonsvertrag** — BVerfGE — Identité constitutionnelle nationale, Révision des traités / Kompetenz
- [ ] **Lord Bruce of Donington** — CJCE — Équilibre institutionnel
- [ ] **Lucchini** — CJCE — Mise en œuvre / autonomie procédurale, Ordre juridique / primauté / effet direct
- [ ] **M.S.S.** — CourEDH — CEDH / Droits CEDH
- [ ] **Mangold** — CJUE — Droit dérivé / actes juridiques, Droits fondamentaux, Renvoi préjudiciel
- [ ] **Marcin Bonda** — AG — Droits fondamentaux
- [ ] **Maribel Dominguez** — CJCE — Citoyenneté / libre circulation, Droit dérivé / actes juridiques [legacy: Non-discrimination, Worker's rights]
- [ ] **Marleasing** — CJCE — Droit dérivé / actes juridiques, Ordre juridique / primauté / effet direct
- [ ] **Marshall** — CJCE — Droit dérivé / actes juridiques, Renvoi préjudiciel
- [ ] **Martinez Sala** — CJCE — Citoyenneté / libre circulation
- [ ] **Matthews** — CourEDH — CEDH / Droits CEDH, Relations extérieures / DI
- [ ] **Melloni** — CJCE — Droits fondamentaux, Identité constitutionnelle nationale, Ordre juridique / primauté / effet direct
- [ ] **Meroni** — CJCE — Équilibre institutionnel, Recours en annulation
- [ ] **Michaniki** — AG — Identité constitutionnelle nationale
- [ ] **Michaud** — CourEDH — CEDH / Droits CEDH
- [ ] **Micheletti** — CJCE — Citoyenneté / libre circulation
- [ ] **Microban** — CJUE — Recours en annulation
- [ ] **Morgan et Bucher** — CJUE — Citoyenneté / libre circulation ⚠️
- [ ] **Mox** — CJCE — Recours en manquement, Relations extérieures / DI
- [ ] **Nold** — CJCE — Droits fondamentaux
- [ ] **OMT** — BVerfGE — Identité constitutionnelle nationale, Révision des traités / Kompetenz
- [ ] **Omega** — CJCE — Compétences / base juridique, Droits fondamentaux
- [ ] **Otis** — CJUE — Droits fondamentaux
- [ ] **Palmisani** — CJCE — Mise en œuvre / autonomie procédurale, Responsabilité extracontractuelle
- [ ] **Parlement c. Conseil (double base juridique)** — CJCE — Compétences / base juridique, Procédures législatives, Équilibre institutionnel ⚠️
- [ ] **Parlement c. Conseil (révision par voie coutumière)** — AG — Révision des traités / Kompetenz ⚠️
- [ ] **Peterbroeck** — CJCE — Renvoi préjudiciel
- [ ] **Plaumann** — CJCE — Recours en annulation
- [ ] **Poirrez** — CourEDH — CEDH / Droits CEDH
- [ ] **Poplawski** — CJUE — Mise en œuvre / autonomie procédurale ⚠️
- [ ] **Poulsen et Opel Austria** — CJCE — Relations extérieures / DI
- [ ] **Preston** — CJCE — Mise en œuvre / autonomie procédurale
- [ ] **Pringle** — CJUE — Compétences / base juridique, Révision des traités / Kompetenz
- [ ] **Promusica et T ; Arcelor** — CJCE — Droits fondamentaux, Mise en œuvre / autonomie procédurale
- [ ] **Publicité sur le tabac I (Allemagne c. Parlement et Conseil)** — CJUE — Compétences / base juridique, Recours en annulation ⚠️
- [ ] **Publicité sur le tabac II (Allemagne c. Parlement et Conseil)** — CJUE — Compétences / base juridique, Recours en annulation ⚠️
- [ ] **Pupino** — CJCE — Droit dérivé / actes juridiques, Ordre juridique / primauté / effet direct
- [ ] **Racke** — CJCE — Relations extérieures / DI
- [ ] **Ratti** — CJCE — Droit dérivé / actes juridiques, Renvoi préjudiciel
- [ ] **Razzouk** — CJUE — Recours en annulation
- [ ] **Rewe-Zentralfinanz** — CJCE — Mise en œuvre / autonomie procédurale
- [ ] **Roquette** — CJCE — Équilibre institutionnel, Procédures législatives
- [ ] **Rottmann** — CJUE — Citoyenneté / libre circulation ⚠️
- [ ] **Royaume-Uni c. Parlement et Conseil** — CJCE — Compétences / base juridique
- [ ] **Rutili** — CJCE — CEDH / Droits CEDH, Droits fondamentaux
- [ ] **République Slovaque / Hongrie c. Conseil** — CJUE — Compétences / base juridique, Relations extérieures / DI
- [ ] **Sayn-Wittgenstein** — CJUE — Citoyenneté / libre circulation, Identité constitutionnelle nationale
- [ ] **Schipani et autres c. Italie** — CourEDH — CEDH / Droits CEDH, Renvoi préjudiciel ⚠️
- [ ] **Schmidberger** — CJCE — Compétences / base juridique, Droits fondamentaux
- [ ] **Schneider Electric** — CJUE — Responsabilité extracontractuelle
- [ ] **Schrems** — CJUE — Droits fondamentaux, Recours en annulation
- [ ] **Sevince** — CJCE — Droit dérivé / actes juridiques, Relations extérieures / DI
- [ ] **Simmenthal II** — CJCE — Mise en œuvre / autonomie procédurale, Ordre juridique / primauté / effet direct
- [ ] **Solange I** — BVerfGE — Droits fondamentaux, Identité constitutionnelle nationale ⚠️
- [ ] **Solange II** — BVerfGE — Droits fondamentaux, Identité constitutionnelle nationale ⚠️
- [ ] **Stauder** — CJCE — Droits fondamentaux
- [ ] **T-Mobile et Vodafone** — CJCE — Droit dérivé / actes juridiques, Renvoi préjudiciel
- [ ] **TWD I** — CJCE — Procédures législatives, Recours en annulation
- [ ] **Taricco II** — CJUE — Droits fondamentaux, Mise en œuvre / autonomie procédurale
- [ ] **Tas-Hagen et Tas** — CJUE — Citoyenneté / libre circulation ⚠️
- [ ] **Test-Achats** — CJUE — Droits fondamentaux, Recours en annulation
- [ ] **Transportes Urbanos** — CJUE — Mise en œuvre / autonomie procédurale, Responsabilité extracontractuelle
- [ ] **Trubowest** — CJUE — Responsabilité extracontractuelle
- [ ] **Tyrer** — CourEDH — CEDH / Droits CEDH
- [ ] **Unibet** — CJUE — Équilibre institutionnel, Renvoi préjudiciel ⚠️
- [ ] **Van Duyn** — CJCE — Droit dérivé / actes juridiques, Ordre juridique / primauté / effet direct, Renvoi préjudiciel
- [ ] **Van Gend & Loos (26/62, 1963)** — CJCE — Compétences / base juridique, Ordre juridique / primauté / effet direct
- [ ] **Van Landewyck** — CJCE — Recours en annulation
- [ ] **Variola** — CJCE — Droit dérivé / actes juridiques, Ordre juridique / primauté / effet direct
- [ ] **Viking Line** — CJCE — Compétences / base juridique, Droits fondamentaux
- [ ] **Von Colson** — CJCE — Droit dérivé / actes juridiques, Mise en œuvre / autonomie procédurale
- [ ] **Wachauf** — CJCE — Droits fondamentaux, Mise en œuvre / autonomie procédurale
- [ ] **Walonie** — CJCE — Droit dérivé / actes juridiques, Mise en œuvre / autonomie procédurale
- [ ] **Winner Wetten** — CJUE — Mise en œuvre / autonomie procédurale, Renvoi préjudiciel
- [ ] **Zambrano** — CJUE — Citoyenneté / libre circulation
- [ ] **Zuckerfabrik** — CJCE — Recours en annulation, Responsabilité extracontractuelle
- [ ] **van Delft** — CJUE — Ordre juridique / primauté / effet direct