I want to start a fresh batch job building out Casus case content, using the
attached case index (jurisprudence_UE.pdf) as the authoritative source list.
Please follow this exact order and don't skip the confirmation step.

STEP 1 — SAFE SETUP
- Create a new branch for this work. Do not touch main.
- Configure yourself to run with only Read, Edit, WebFetch, and WebSearch
  pre-approved. Do not pre-approve push, delete, or any destructive command.
- Set a sensible turn limit and a hard budget cap so this can't run away
  unattended.

STEP 2 — CONFIRM BEFORE ANYTHING RUNS
- Show me the literal contents of the permissions/settings file from Step 1.
- Tell me exactly what you're about to do first, so I can confirm before
  it starts.

STEP 3 — EXTRACT AND DEDUPLICATE THE CASE LIST
- The case index is at Desktop>IUR I>Droit européen/jurisprudence_UE.pdf.
- Parse it using its table structure (it has real tables, not flowed text —
  use a PDF table-extraction library, not plain text scraping, or you'll
  misparse wrapped rows).
- The document lists 284 rows across 17 category tables, but many rows are
  the SAME case appearing under multiple categories (the "aussi :" field
  confirms this). The document states 176 distinct cases total.
- Build ONE case record per distinct case (not one per row), collecting
  the FULL set of categories each case belongs to across all its row-
  appearances and "aussi :" cross-references. A case genuinely belonging
  to 4 categories should end up tagged with all 4, not just 1.
- Watch for ambiguous grouped rows that may be 2-3 distinct cases bundled
  into one (e.g. "Dhabib ; Schipani ; Arlewin", "Solange I et Solange II",
  "Publicité sur le tabac (I et II)", "Tas-Hagen ; Morgan & Bucher",
  "Aranyosi et Caldararu et Poplawski", "Unibet ; Avis 1/09",
  "Kolpinghuis et Adeneler", "Holtz & Willemsen et Bergaderm"). Use your
  judgment, flag your reasoning per case in the tracking file, and don't
  force the count to hit exactly 176 — 169-176 is the honest range.
- ADOPT ALL 17 of the document's categories as the new Casus theme
  taxonomy, replacing the current 10-theme list. Map each existing case
  already in Casus (the original 10) onto this new 17-category set as
  part of this step, so the whole site uses one consistent taxonomy going
  forward. Flag any of the original 10 cases whose old theme doesn't
  cleanly map to one of the 17.
- Output a tracking file (markdown checklist or JSON) with one entry per
  distinct case: name, jurisdiction (CJCE/CJUE, CourEDH, BVerfGE, ATF, or
  AG opinion), full citation if available, and the complete list of
  categories/themes it belongs to. This file must survive across sessions.
- IMPORTANT: this document is an index of names and keyword topics, not
  case content. You still need to research each case's actual facts,
  holding, and reasoning from real sources before writing anything.

STEP 4 — THE ACTUAL WORK
1. Process in batches of ~15 distinct cases (not rows). For each case,
   develop it to full depth before moving to the next batch — all four
   levels: Abstract, Intermediate, Detailed (with verified paragraph
   citations), and Holistic — in all three languages (English, French,
   German). Do not leave any case at partial depth; every case gets the
   same full treatment.
2. A case's content — especially Holistic and any theme-tagging — must
   reflect its actual relationship to EACH theme it's tagged under, which
   may differ by theme (e.g. "establishes" primacy but merely "illustrates"
   or "applies" direct effect). Do this per case per theme, not once per
   case overall — this matters for later quiz-question generation.
3. Use Costa v ENEL and Van Gend en Loos as the style reference for tone
   and sentence length, in every language, at every level.
4. Verified citations only — flag anything you can't confirm rather than
   inventing it. CourEDH/BVerfGE/ATF citation formats differ from CJUE
   conventions — use the correct format for each court, and tag
   jurisdiction visibly for site users, not just internal metadata.
5. Commit one case at a time, not in one giant batch commit.
6. If you're getting close to a turn or budget limit, stop cleanly, commit
   what's done, and update PROGRESS.md rather than continuing.
7. Write a PROGRESS.md summary when you stop or finish: which cases
   reached full depth, which are incomplete, any citation flags, and the
   final distinct-case count with a note on how the ambiguous grouped
   rows were resolved.

