# Casus — Step 4 Progress

Last updated: 2026-07-23, in-session. Continuing in a fresh interactive session from the one that left off at 4/182 — confirmed via `ps`/`lsof` that the other live `claude` process on this machine has cwd `~`, not this repo, so no collision. Since then: added Grzelczyk, Åkerberg Fransson, Francovich (7/182 new cases at full depth), completed the original-12 translation-parity pass (all 12 pre-existing cases now trilingual), and started an **Italian language pass** at the user's explicit request (add IT as a fourth site language, matching FR/DE exactly — see dedicated section below). Currently mid-way through the Italian pass; that's the active thread, not the new-case queue.

## Italian language pass (user request, 2026-07-23) — IN PROGRESS
User wants Italian added as a fourth site language, done exactly the same way as French and German — both the infrastructure (language switcher, theme-label dictionaries, citation-popup strings, fallback note) and per-case content (all four IRAC levels, holistic, citations) for every case currently in `casus.html`.

Infrastructure done first, one commit (`bb8e69c`): `THEME_LABELS_IT`, `LEGACY_THEME_LABELS_IT`, `it` branches in `themeLabel()`/`legacyThemeLabel()`, `['it','IT']` in the language switcher, `it:{...}` in the citation-popup `t` object, and an Italian fallback-note string. Same footprint as FR/DE — general UI chrome (tab labels, "Legal basis", etc.) stays English-only, matching precedent.

Per-case Italian translations: **19 cases total need an `it:{}` block** (all cases currently in `CASES`, i.e. the original 12 plus the 7 new ones added this session). One commit per case, same convention as before. Same authentic-language-checking discipline as the FR/DE work: verify whether the case's own procedural language is Italian (Costa v ENEL, Simmenthal II, Francovich all are — try to source the actual Italian judgment text for the primary citation) vs. translating from the verified English text with an honest "unofficial translation" flag (all other cases).

Progress (case → commit):
- [x] Costa v ENEL — `1a4f30b` (authentic Italian citation text sourced and verified)
- [x] Internationale Handelsgesellschaft — `ca1cbbd`
- [x] Melloni v Ministerio Fiscal — `04e3738`
- [x] Commission v Bavarian Lager — `21e4e7d`
- [x] Kadi I — `0d3bdc5`
- [x] Kadi II — `cc12efd`
- [x] Van Gend en Loos — `b9ba996`
- [x] Defrenne v Sabena (No 2) — `323fbf0`
- [x] Dominguez — `0636a3d`
- [x] Opinion 2/13 — `ded6d96`
- [x] Stauder v City of Ulm — `da4ef81`
- [x] Konstantinidis v Stadt Altensteig — `bb2d521` (original 12 now fully done in Italian)
- [x] Simmenthal II — `a014955` (authentic Italian citation text sourced and verified)
- [x] Marshall — `7aa6ea4`
- [ ] Solange I
- [ ] Solange II
- [ ] Grzelczyk
- [ ] Åkerberg Fransson
- [ ] Francovich and Bonifaci v Italy (Italian case — source authentic text)

Order followed: file order (same as the parity pass), i.e. the order cases appear in `CASES`. **This pass takes priority over the 178-new-case queue right now** — resume the new-case queue only after all 19 have an `it:{}` block. If picking this up cold: check the box list above against `grep -c 'it:{' casus.html` per case id to confirm actual state before assuming the list is current (update it as you go, don't trust it blindly after a context compaction).

## IMPORTANT: overnight automation did NOT run the batch — read before resuming
`casus_overnight.sh` was actually launched by the user in a separate terminal tonight (session 1 ~2 AM, session 2 at the 4 AM resume — see `overnight_run.log`, `session1_output.json`, `session2_output.json`, left in place untouched, not part of the project content). Both headless runs correctly detected this interactive session was already live and editing the same branch/files, declined to touch anything to avoid corrupting concurrent writes, and asked the user for direction (which went unanswered since the user wasn't watching). **All Step 4 progress so far has come from this one interactive session, not from the overnight script.** If resuming later via `casus_overnight.sh` again, first confirm no other session is already live on this branch (check for a running `claude` process and recent commits) before letting it write.

## MANDATORY per-case step, added after tonight's blank-page bug (read before writing another case)
Marshall's German translation broke the entire site: an opening German quote „ (U+201E) got closed with a straight ASCII `"` instead of the correct `"` (U+201C) in a double-quoted JS string field, which prematurely terminated the string and turned the rest of the file into unparseable garbage — silent blank page, no console error until parse time. `node` is not installed in this environment; use macOS's built-in JS engine instead. **Before committing any case from now on, run:**
```
python3 -c "
import re
html = open('casus.html', encoding='utf-8').read()
blocks = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
open('/tmp/casus_app.js','w',encoding='utf-8').write(blocks[-1])
"
osascript -l JavaScript -e "$(cat /tmp/casus_app.js)" 2>&1 | head -5
```
Expect either a clean run or `ReferenceError: Can't find variable: document` (that's fine — this engine has no DOM, it means parsing succeeded and execution started). Anything that says `SyntaxError` is a real, blocking bug — find and fix it before committing, the same way the Marshall fix was done (`git log` commit `8cd56e2`). This applies to `casus_overnight.sh` runs too, not just this interactive session — if you're an agent picking this up cold, run the check now against the current `casus.html` before writing anything, and again before every commit after that.

This exact bug recurred during the original-12 translation-parity pass (Kadi I's German `application` field, fixed before commit `947789b`) — it's an easy typo to make since „ and " look almost identical while typing German quotes fast. Faster than waiting for the JS engine to catch it: before running the check above, `grep -n '„[^“]*"' casus.html` — flags any „ opening quote whose *next* quote-like character is a straight `"` instead of the correct closing `"` (U+201C). This over-flags: matches inside backtick-delimited fields (`rule`, `holistic`) are harmless, since a stray `"` there doesn't end the string — only check hits inside plain double-quoted fields (`issue`, `application`, and sometimes `rule`) are real bugs. Skim the matches with that in mind rather than assuming every hit is broken.

## Status
- Distinct case count: **182** (confirmed final by user — no further merges).
- Taxonomy: 17 categories live in `casus.html` (Option 1, minimal-diff), 5 legacy substantive tags as a secondary layer. See `TRACKING.md` for full rationale.
- Cases at full depth (4 levels x 3 languages, verified/flagged citations): **7 of 182**
  - [x] Simmenthal II (Case 106/77, CJCE) — `mise_en_oeuvre`, `ordre_juridique`
  - [x] Marshall (Case 152/84, CJCE) — `droit_derive`, `renvoi_prejudiciel`
  - [x] Solange I (BVerfGE 37, 271) — `droits_fondamentaux`, `identite_constitutionnelle`
  - [x] Solange II (BVerfGE 73, 339) — `droits_fondamentaux`, `identite_constitutionnelle`
  - [x] Grzelczyk (Case C-184/99, CJCE) — `citoyennete`, legacy tag `solidarity`
  - [x] Åkerberg Fransson (Case C-617/10, CJUE) — `droits_fondamentaux` (commit `e8020a3`)
  - [x] Francovich and Bonifaci v Italy (Joined Cases C-6/90 & C-9/90, CJCE) — `recours_manquement`, `responsabilite_extracontractuelle` (commit `417cc3c`)
- Note: Solange I and Solange II are both fully committed in commit `e32e5ca`, even though its message only names Solange I — the Edit that added them was a single combined change and both are present and correct in `casus.html`; this is just a commit-message labeling slip, not a content gap.
- Old 12 Casus cases: remapped onto the new taxonomy (themes[] swapped, jurisdiction added, legacyThemes added to Defrenne/Dominguez/Konstantinidis) AND now at full trilingual parity — see "Original-12 translation-parity pass" below, **complete as of this checkpoint**.
- 175 cases remaining, not started.

## Standing citation-verification convention (applies to all remaining cases)
Direct EUR-Lex fetches (`eur-lex.europa.eu/legal-content/.../TXT/HTML/...` and the plain `/TXT/` variant) have failed twice in a row — the page returns empty to WebFetch, likely JS-rendered. Per user decision, the fallback is:
1. Attempt EUR-Lex fetch once.
2. If it fails, use WebSearch to find the same paragraph-numbered quote corroborated by independent secondary sources (academic commentary, case-law databases).
3. Mark the citation's `note` field explicitly: "Verified via secondary source... primary EUR-Lex fetch failed" (English), with FR/DE equivalents.
4. For non-English citation entries, translate the verified English quote myself and flag it explicitly as an unofficial translation not checked against the official-language EUR-Lex text — never present a FR/DE quote as independently source-verified unless it actually was.

## Schema notes for future cases (Option 1, minimal-diff taxonomy integration)
- `jurisdiction: "CJCE"|"CJUE"|"CourEDH"|"BVerfGE"|"ATF"|"AG"` — required on every new case, renders as a visible badge next to the name/citation.
- `themes: [...]` — flat array of the 17 new canonical English strings (see `THEMES` const in casus.html). The establishes/illustrates/applies distinction per theme is captured in prose (Holistic + IRAC text), not a structured field — Option 2 (structured relations) was explicitly rejected by the user for now.
- `legacyThemes: [...]` (optional) — only for the 5 old substantive categories with no equivalent in the 17 (Non-discrimination, Market freedoms, Worker's rights, Collective action vs. economic liberty, Solidarity). Do not backfill this across all 182 cases — apply only where a case's actual holding genuinely turns on one of these.
- CJCE vs CJUE: date-based split at the Lisbon Treaty's entry into force (1 Dec 2009). Pre-Lisbon judgments are CJCE even if commonly cited by their later CJUE case number format.
- When adding a case, check `TRACKING.md`'s distinct-case list AND grep `casus.html` for `case-link-pending` with that case's name — several already-live cases (Costa v ENEL, Van Gend en Loos, Konstantinidis) have forward references to not-yet-added cases in their holistic text (Simmenthal, Foster v British Gas, Grzelczyk, Zhu and Chen, etc.). Converting a `case-link-pending` span to a real `<a class="case-link" onclick="jumpToCase('id')">` link is part of "adding" a case if it's referenced elsewhere. Some references (e.g. Marshall in Van Gend en Loos) were already coded as real `jumpToCase` links pointing at an id that didn't exist yet — these self-resolve once the case is added under that same id, no text edit needed, just confirm the id matches.

## Original-12 translation-parity pass — COMPLETE (user request, 2026-07-23)
All 11 non-Costa cases now have full FR/DE translations (all four IRAC levels, holistic, citations), verified by script: every one of the 12 shows `fr:{` and `de:{` present in its `translations` block. Details of the pass kept below for reference.

User asked for the 12 pre-existing Casus cases to be brought up to the same 4-level x 3-language standard as the newly authored cases, before/alongside the 178 new-case batch. Assessment (via a script parsing `CASES` for level keys, `translations:` presence, and citation-block counts):
- **Costa v ENEL: already complete** — full FR/DE translations, done earlier as the trilingual proof of concept. No work needed.
- **11 others (Handelsgesellschaft, Melloni, Bavarian Lager, Kadi I, Kadi II, Van Gend en Loos, Defrenne, Dominguez, Opinion 2/13, Stauder, Konstantinidis): all already have full 4-level English content (abstract/intermediate/detailed/holistic) and an English `citations` array with verification notes following the same convention as the new cases (a couple — Kadi I, Kadi II — are already honestly flagged as lower-confidence, unconfirmed paragraph numbers; that's pre-existing and correct, not something to silently upgrade to "verified"). What's missing across all 11 is the `translations` block entirely: no French, no German.**
- Taxonomy (17-category themes, jurisdiction, legacy substantive tags) was checked against `TRACKING.md`'s remap table for all 12 and already matches live `casus.html` exactly, including the flagged mismatches (Bavarian Lager's old tag dropped as a mistagging with no legacy substitute, Defrenne/Dominguez/Konstantinidis legacy tags applied). No taxonomy work needed on any of the 12.

**Decision (logged, not re-asked): doing this as its own sequential pass, first, ahead of the 178 new cases**, because (a) it's bounded — 11 cases, not 178 — so worth clearing to get the site internally consistent before opening a second, much larger front; (b) it's cheaper per case than new-case authoring, since the facts/holding/citations already exist and are already verified — the actual work is high-quality FR/DE translation of existing content, not fresh legal research; (c) running one track at a time (all old-case backfill, then all new cases) is less error-prone for checkpointing than interleaving two different kinds of edits to the same file.

Order (as they appear in `casus.html` / TRACKING.md's remap table): Handelsgesellschaft (`6f4fa37`) → Melloni (`6cb0661`) → Bavarian Lager (`7219779`) → Kadi I (`947789b`) → Kadi II (`6cd1363`) → Van Gend en Loos (`207f557`) → Defrenne (`b06f0d9`) → Dominguez (`fc71a86`) → Opinion 2/13 (`4d22147`) → Stauder (`5d6df96`) → Konstantinidis (`cbe0a8e`). One commit per case, same as new-case convention. **All 11 done — pass complete.** Also fixed some pre-existing small gaps found along the way: two stale `case-link-pending` spans that should already have been real links (Kadi I → Opinion 2/13), and Opinion 2/13's holistic text had plain-text mentions of Costa v ENEL/Van Gend en Loos instead of jumpToCase links.

Note: Defrenne and Dominguez both contain real (non-pending) `jumpToCase('mangold')` links — intentional, per the existing schema note above (Mangold is on the 182-case list, not yet written; these self-resolve once it's added, no text edit needed then).

Translation note for this pass: for each case, checked whether the case's authentic procedural language is English (Bavarian Lager — UK party) vs. something else the English citation is itself already a translation of (Handelsgesellschaft — German proceedings; Melloni — Spanish proceedings). Flagged FR/DE citation notes accordingly: "unofficial translation of the authentic English text" for Bavarian Lager, vs. "unofficial translation of the verified English text, neither the authentic-language original nor the official FR/DE Recueil text checked this session" for the other two. Same distinction to apply going forward for Kadi I/II (English), Van Gend en Loos (Dutch), Defrenne (French), Dominguez (French), Opinion 2/13 (n/a — Court's own request), Stauder (German), Konstantinidis (German, per originalName).

## Next up (priority queue, in order)
Continuing through the 182-case list by category coverage (aiming to touch all 17 categories reasonably early rather than clearing one category at a time) — no more already-referenced pending links left to prioritize right now; pick the next case using TRACKING.md's untouched-case list and cross-reference density with what's already live.

Francovich (CJCE) done this checkpoint (commit `417cc3c`) — added Directive 80/987/EEC and Article 4(3) TEU entries to ARTICLES. Left a forward `case-link-pending` to "Brasserie du Pêcheur and Factortame III". Flag for whoever adds that case: TRACKING.md lists **"Brasserie du pêcheur"** (row 134) and **"Factortame"** (row 168) as two separate distinct-case entries, but they were in fact decided together as one joined judgment (Joined Cases C-46/93 and C-48/93) — same situation as the Solange I/Solange II commit-message slip noted above, just not yet resolved. When adding, decide whether to write one combined case entry (matching the real judgment) with a single id, or two separate entries per TRACKING.md's row-level ground truth, and update TRACKING.md's row count/rationale accordingly either way — don't silently pick one without a note.

Fransson (CJUE) done earlier (commit `e8020a3`) — was referenced pending in Melloni (all 3 languages), now real `jumpToCase('fransson')` links. Added Charter Article 51 and Article 50 entries to ARTICLES.

Grzelczyk (CJCE) done earlier — was referenced pending in Konstantinidis, now a real `jumpToCase('grzelczyk')` link. Still pending in Grzelczyk's own holistic text: `Zhu and Chen` (id will be `chen` — see TRACKING.md row 138) — convert that span when Chen is added. Same for Konstantinidis's own pending reference to `Zhu and Chen`.

## Flags for later review (not blocking, logged and continuing per standing instruction)
- Dominguez: PDF-derived jurisdiction read "CJCE" but the case is from 2012 (post-Lisbon) — used "CJUE" instead based on date, flagged in the Step 4 infra commit.
- Konstantinidis: the PDF index specifically tags this row under "AG" (Advocate General opinion) rather than the Court's judgment — likely because Jacobs AG's opinion (the "civis europeus sum" passage) is the more famous/quoted part of this case. Used "CJCE" for the badge since the site cites the Court's 1993 judgment (C-168/91), which the existing holistic text already discusses correctly alongside the AG opinion.
- Van Gend en Loos's PDF-derived categories include `competences` alongside `ordre_juridique` — unexpected for the direct-effect classic. Kept as document ground truth; worth a second look if time allows, not blocking.
- EUR-Lex access failure is systemic, not case-specific — expect this flag to recur on nearly every case going forward. Not re-flagging as a "new" problem each time; see the standing convention above.

## Session mechanics
- Working on branch `casus-jurisprudence-batch-2026-07-23`, not `main`.
- `.claude/settings.local.json` pre-approves only Read/Edit/WebFetch/WebSearch; Bash requires per-call approval in principle, though the session's actual permission mode has been auto-approving Bash without a visible prompt (flagged to user earlier in-session; user decided to proceed relying on the deny-list backstop rather than resolve the mode mismatch).
- Checkpointing every 1-3 cases: one commit per case (per original instruction), PROGRESS.md updated at each checkpoint.
- Continuing to the next cases now without further check-ins, per standing instruction.
