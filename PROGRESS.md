# Casus — Step 4 Progress

Last updated: 2026-07-23 ~09:55 local time, in-session (checkpoint after 4 cases).

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

## Status
- Distinct case count: **182** (confirmed final by user — no further merges).
- Taxonomy: 17 categories live in `casus.html` (Option 1, minimal-diff), 5 legacy substantive tags as a secondary layer. See `TRACKING.md` for full rationale.
- Cases at full depth (4 levels x 3 languages, verified/flagged citations): **4 of 182**
  - [x] Simmenthal II (Case 106/77, CJCE) — `mise_en_oeuvre`, `ordre_juridique`
  - [x] Marshall (Case 152/84, CJCE) — `droit_derive`, `renvoi_prejudiciel`
  - [x] Solange I (BVerfGE 37, 271) — `droits_fondamentaux`, `identite_constitutionnelle`
  - [x] Solange II (BVerfGE 73, 339) — `droits_fondamentaux`, `identite_constitutionnelle`
- Note: Solange I and Solange II are both fully committed in commit `e32e5ca`, even though its message only names Solange I — the Edit that added them was a single combined change and both are present and correct in `casus.html`; this is just a commit-message labeling slip, not a content gap.
- Old 12 Casus cases: remapped onto the new taxonomy (themes[] swapped, jurisdiction added, legacyThemes added to Defrenne/Dominguez/Konstantinidis). Not rewritten at full depth beyond that — their existing IRAC/holistic content is untouched.
- 178 cases remaining, not started.

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

## Next up (priority queue, in order)
Chosen for cross-reference density with existing content and to close out already-referenced pending links first:
1. Grzelczyk (CJCE) — referenced pending in Konstantinidis
2. Fransson / Åkerberg Fransson (CJUE)
3. Francovich (CJCE)
4. Then continuing through the 182-case list by category coverage (aiming to touch all 17 categories reasonably early rather than clearing one category at a time).

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
