# Casus — Step 4 Progress

Last updated: 2026-07-23, in-session. Continuing in a fresh interactive session from the one that left off at 4/182 — confirmed via `ps`/`lsof` that the other live `claude` process on this machine has cwd `~`, not this repo, so no collision. Since then: added Grzelczyk, Åkerberg Fransson, Francovich, Mangold (8/182 new cases at full depth), completed the original-12 translation-parity pass (all 12 pre-existing cases now trilingual), completed an Italian language pass (site is now EN/FR/DE/IT quadrilingual across all 19 cases done before Mangold), and shipped a paragraph-precise citation-highlight upgrade (see "Citation-highlight upgrade" section below) — Mangold is the first case authored under the new tagging standard.

## Citation-highlight upgrade (user request, 2026-07-23) — mechanism shipped, retrofit COMPLETE (all 20 cases now tagged)
User asked for the highlight-to-see-source feature to: (1) also work in Intermediate mode, not just Detailed; (2) show the exact source paragraph, not a general case-wide reference; (3) auto-extend a partial selection to the whole "information unit" (all text drawn from one source paragraph); (4) split into separate citation cards when a selection spans two different source paragraphs.

**Data-model finding (reported before writing any UI code, per user's explicit request):** none of the 19 cases written before this point — not just the 4 the user asked about — had per-sentence paragraph tagging. The only structured citation data was a flat, case-level `citations[]` array (a list of quotable excerpts with a paragraph label), matched against user selections by fuzzy substring search, falling back to "show every citation for the case" whenever the exact substring wasn't found. Proved this concretely: neither of Simmenthal II's own two holding quotes (para 21, para 24) appears verbatim in its `detailed.rule` prose, so highlighting *either* paragraph's sentence today shows *both* citations — the exact failure mode the user's spec describes, already live in the site.

**Approved design:** inline `<cite data-para="key">...</cite>` spans wrapped directly around the specific clause a sentence paraphrases, embedded in the existing HTML template-literal prose (not a restructured segment-array schema — avoids fighting the flowing prose style and existing `<br><br>`/`<a class="case-link">` markup). Each citation object gets a new stable `key` field (e.g. `"p21"`, `"p24"`) alongside the existing human-readable `paragraphs` label. Mouseup handler: finds the `.citable` ancestor, checks for any `cite[data-para]` elements inside it — if none exist (legacy case), falls back to the original whole-case fuzzy match unchanged (no regression); if some exist, only responds to selections that intersect at least one tagged unit (`Range.intersectsNode`), extends the visible selection to cover the whole unit(s) touched, and shows one popup with one clearly-labeled card per distinct paragraph touched (reusing the existing multi-card popup layout — confirmed with the user that this satisfies "two separate citations, not merged," rather than needing two separately-positioned floating popups).

**Original retrofit decision (superseded — see reversal below):** initially deferred: do NOT retrofit the 19 cases written before this feature, tag only new cases going forward, revisit only if asked. That deferral held while the case queue and the Italian pass were in progress.

- **New standard, effective immediately, for every case from here on** (178 remaining + any further old-case work): `intermediate.rule`, `detailed.rule`, and `detailed.application`/`intermediate.application` (where a specific disposition paragraph exists) must carry inline `<cite data-para="key">` tags, in all four languages, authored at the same time as the prose itself — not bolted on later. Mangold (commit `a081e2e`) is the first case done this way and should be used as the reference example.

**Retrofit reversal (user's explicit new instruction, same day):** user asked to extend the tagging to all cases now ("can you extend this now to all cases?"), reversing the earlier defer. Retrofitting the 19 pre-Mangold cases in file order, one commit per case, same syntax-check/structural-check convention as new-case work. Since this prose was authored recently, source-paragraph mapping is done from existing session knowledge of each case's citations rather than fresh research.

**Retrofit progress (19 total, in file order):**
- [x] Costa v ENEL — key `p593` (commit `f5bb68b`)
- [x] Internationale Handelsgesellschaft — key `p4` (commit `c128a04`)
- [x] Melloni — key `p60` (commit `5bf13fa`)
- [x] Commission v Bavarian Lager — keys `p68`, `p78` (commit `bc7e8bb`)
- [x] Kadi I — keys `p281`, `p326` (commit `5f9b022`)
- [x] Kadi II — key `general` (commit `4113d5b`)
- [x] Van Gend en Loos — key `p12` (commit `3c821e2`)
- [x] Defrenne v Sabena (No 2) — keys `p21`, `p22` (commit `8d007da`)
- [x] Dominguez — keys `p17`, `p36` (commit `f255b7b`)
- [x] Opinion 2/13 — key `p191` (commit `6d0cef2`)
- [x] Stauder — key `p7` (commit `6b3c275`)
- [x] Konstantinidis — key `p16` (commit `adb6b69`)
- [x] Simmenthal II — keys `p21`, `p24` (commit `25b3b67`; also backfilled a missing `p21` citations[] entry in FR/DE for parity with EN/IT)
- [x] Marshall — keys `p48`, `p49` (commit `70166be`; also backfilled a missing `p49` citations[] entry in FR/DE for parity with EN/IT)
- [x] Solange I — key `leitsatz` (commit `15c26e8`)
- [x] Solange II — key `leitsatz2` (commit `5e6fa28`)
- [x] Grzelczyk — keys `p31`, `p44` (commit `006d239`)
- [x] Åkerberg Fransson — keys `p21`, `p35` (commit `1dca7ba`)
- [x] Francovich and Bonifaci v Italy — keys `p35`, `p40` (commit `601b847`)

**Retrofit complete:** all 19 pre-Mangold cases now carry `<cite data-para="key">` tagging in `intermediate.rule`/`detailed.rule` (and `application` where relevant), across EN/FR/DE/IT, with matching `key` fields on every affected `citations[]` entry. Combined with Mangold (the first case authored under the standard) and every case added since, **all 20 cases in Casus now use the paragraph-precise citation-highlight mechanism** — the legacy whole-case fuzzy-fallback path is no longer exercised by any case in the current dataset (it remains in the code as a safety net for any future case that's added without tagging). Two cases (Simmenthal II, Marshall) turned up a pre-existing asymmetry where FR/DE were missing a secondary citations[] entry that EN/IT had — backfilled during the retrofit so all four languages expose the same set of citation keys per case.

## Full-coverage citation tagging (user request, 2026-07-23) — IN PROGRESS

**User feedback after the retrofit above:** coverage was too narrow — only 2-3 tagged clauses per case, the rest of the Intermediate/Detailed prose (facts, procedural history, connective/analytical text) was not highlightable at all. User wants the ENTIRE case text highlightable at every level `.citable` is enabled on.

**New standard:** every sentence in `intermediate.issue/rule/application` and `detailed.issue/rule/application` must be inside a `<cite data-para="key">` span — no gaps. Two kinds of key:
- A specific `pXX` (or `leitsatz`/`leitsatz2` for BVerfG headnotes) wherever the text paraphrases one identifiable judgment paragraph — same convention as the original retrofit.
- A `"general"` key, with its own `citations[]` entry per language ("General case facts and reasoning (not a single specific paragraph)" + explanatory note), for background facts, procedural history, or connective/retrospective commentary that doesn't map to one specific paragraph. Never leave prose untagged.

**Key finding, user-prompted:** initially used "general" for ALL background text on Mangold (the pilot case). User asked "is it not possible to reveal where you got the general case facts from?" — tested EUR-Lex direct fetch again (it had failed consistently earlier this session) and it worked, returning real paragraph-by-paragraph structure. **User's explicit call: full paragraph precision everywhere, "general" only as a genuine last resort** when even research doesn't yield a specific paragraph (pre-1970s judgments without paragraph numbering, or judgments where EUR-Lex/secondary sources won't yield a clean number for that specific sentence).

**Per-case process:** (1) WebFetch EUR-Lex CELEX text for a paragraph-by-paragraph breakdown of facts/procedure/reasoning; if EUR-Lex returns empty (happens intermittently — succeeded for Mangold and Costa v ENEL, failed for Handelsgesellschaft), fall back to WebSearch + secondary sources for specific paragraph numbers; (2) map every sentence in the case's prose to a real paragraph where verifiable, add a matching `citations[]` entry per language with a note on how it was verified; (3) tag exhaustively — rule text that's one continuous quotation across a page range can just get one widened `pXX` span rather than being artificially split; (4) run the syntax + brace-balance + cite-key-consistency checks; (5) commit.

**Pre-1970s judgments (Costa v ENEL, Van Gend en Loos) are a known exception:** they predate paragraph numbering, and EUR-Lex's own page markers don't cleanly separate facts/procedure from reasoning the way later numbered paragraphs do (confirmed via direct fetch attempts) — so `general` legitimately remains the ceiling for their background text, clearly noted as such in the citation's own note field, not a shortcut.

**Progress (case order = file order, all cases already have SOME tagging from the original retrofit; this pass is about achieving full coverage + verified precision):**
- [x] Mangold — pilot case; keys `p20`, `p13`, `p31`, `p64`, `p59` (plus existing `p75`, `p77`), `general` only on one retrospective-commentary sentence per level (commits `0c02703`, `0eae83a`)
- [x] Costa v ENEL — key `p593` widened to cover the entire rule passage (one continuous quotation, pp. 593-594); `general` for facts/procedure/Lisbon-Treaty commentary (pre-numbering judgment, see exception above) (commit `55e0c32`)
- [x] Internationale Handelsgesellschaft — added key `p3` (primacy/independent-source-of-law reasoning, verified via secondary source after EUR-Lex fetch failed); `general` for facts/procedure/proportionality-outcome commentary (commit `a556d15`)
- [x] Melloni — added keys `p13` (facts), `p25` (referred questions), `p56` (Article 53 scope analysis), all EUR-Lex-verified; `general` only on one retrospective-commentary sentence (commit `6ecf8ef`)
- [x] Commission v Bavarian Lager — added keys `p19` (facts), `p1` (procedural history), `p59` (direct-referral reasoning), all EUR-Lex-verified; `general` only on one structural-commentary sentence (commit `938584f`)
- [x] Kadi I — added keys `p11` (facts), `p1` (procedural), `p334` (defence-rights violation), `p373` (deferred-effect ruling), all EUR-Lex-verified; upgraded p281's confidence note; `general` only on one retrospective sentence (commit `5e3f026`)
- [x] Kadi II — EUR-Lex failed repeatedly (3 attempts) and no new paragraph numbers found; consolidated into one continuous `general` span per field, fully honest about the verification gap (commit `bc1cade`)
- [x] Van Gend en Loos — key `p12` widened to cover the entire rule passage (one continuous quotation, ECR p. 12), same pattern as Costa v ENEL; `general` for facts/procedure/retrospective commentary (pre-numbering judgment, see exception above) (commit `e668850`)
- [x] Defrenne v Sabena (No 2) — retrieved full judgment text via CVCE-hosted ECR copy after EUR-Lex fetch failed; added keys `p1` (procedural, para 1), `p2` (facts, paras 2-3), `p39` (private-employer/horizontal-effect holding, paras 38-39), `p40` (reply to first question, para 40); existing `p21`/`p22` confirmed correct; `general` only for the pre-Law unnumbered facts (retirement age) and retrospective commentary (commit `3117444`)
- [x] Dominguez — EUR-Lex direct fetch succeeded (3 targeted fetches); added keys `p8` (national-law precondition, paras 8-9), `p10` (facts, paras 10-12), `p13` (procedural history, paras 13-14), `p34` (direct-effect criteria, paras 33-35), `p37` (no horizontal effect, para 37), `p38` (may rely against state in any capacity, para 38), `p40` (Foster emanation-of-state test + national court's task, paras 39-40), `p44` (full answer incl. Francovich fallback, paras 41-44 + operative part); corrected the pre-existing `p17` key to `p18` (exact quote is actually para 18, not 17 — verified via direct fetch); `p36` re-verified unchanged; no `general` needed — full paragraph precision achieved (commit `4985ac4`)
- [x] Opinion 2/13 — direct EUR-Lex fetch succeeded for the procedural background but truncated before the reasoning sections (a very long Opinion); fell back to WebSearch/secondary sources (Wikipedia structured summary + academic commentary, cross-checked) for the rest. Added keys `p1` (procedural background, paras 1-5/46-48), `p194` (mutual-trust-checking-would-undermine-autonomy, paras 194-195), `p199` (Protocol 16 risk to Art. 267 TFEU, paras 196-200), `p254` (CFSP jurisdiction gap, paras 249-257), `p258` (Court's conclusion + operative part); existing `p191` kept. `general` used sparingly for the Opinion-procedure framing, one transition sentence, and retrospective no-revised-agreement commentary (commit `2341582`)
- [x] Stauder — direct EUR-Lex fetch succeeded and returned the full eight-paragraph judgment verbatim (this 1969 judgment already uses numbered Grounds of Judgment). Added keys `p1` (procedural referral), `p2` (facts — Decision's coupon scheme), `p3` (multilingual-interpretation principle), `p4` (liberal-interpretation standard/purpose), `p6` (operative conclusion — number suffices); existing `p7` kept and re-verified. `general` used only for Stauder's personal war-victim/dignity narrative (unnumbered facts-section exception) and retrospective commentary (commit `a69298d`)
- [x] Konstantinidis — direct EUR-Lex fetch succeeded and returned a full paragraph-by-paragraph breakdown (paras. 1-17). Added keys `p1` (referral), `p3`/`p4`/`p6` (facts — occupation, 1983 marriage/ISO transliteration, objection), `p8` (referred questions), `p12` (Article 52 as fundamental provision), `p14` (transcription as such not precluded), `p15` (interference threshold), `p17` (operative ruling); existing `p16` kept and re-verified. New key `ag46` for the "civis europeus sum" passage — sourced from Advocate General Jacobs' separate Opinion (para. 46, via WebSearch), carefully distinguished from the Court's own numbered judgment. `general` used only for genuine retrospective/editorial commentary (commit `d308cef`)
- [ ] Simmenthal II
- [ ] Marshall
- [ ] Solange I
- [ ] Solange II
- [ ] Grzelczyk
- [ ] Åkerberg Fransson
- [ ] Francovich and Bonifaci v Italy

Remaining after this list: the 178-new-case queue (each authored with full-coverage tagging from the start, per the standard above, not as a later pass).

**Gotcha found during retrofit (not present in Mangold, which used backticks throughout):** whether a field is a double-quoted JS string (`rule:"..."`) or a backtick template literal (`` rule:`...` ``) determines whether the `<cite data-para="...">` attribute's double quotes must be escaped as `\"`. Double-quoted fields need `<cite data-para=\"key\">`; backtick fields use plain `<cite data-para="key">`. Missing this breaks the string and fails the syntax check immediately (caught both times it happened, before commit) — check each field's delimiter before inserting tags.

**Verification status:** user manually confirmed at `http://localhost:8934/casus.html` (local test server) that the split-popup behavior works correctly on Mangold — selecting across the "p75" and "p77" sentences produces two distinct, correctly-labeled citation cards. Feature confirmed working.

**Follow-up addition, same session:** every case (all 20, not just tagged ones) now also carries a case-level `sourceUrl` — the actual EUR-Lex CELEX page for CJEU/CJCE cases, or the bundesverfassungsgericht.de English page for Solange I/II — and the citation popup shows a localized "Read the full judgment" link beneath the card(s), for both the new precise path and the legacy fuzzy-fallback path. CELEX codes were constructed from each case's own citation number using the standard EUR-Lex pattern (`6` + case-number year + `CJ`/`CV` + case number, zero-padded to 4 digits) and spot-checked via search rather than assumed — confirmed correct for every case checked (10 of 20, spanning 1962–2013), no deviations found. **New standard going forward: every new case needs a `sourceUrl` field too**, alongside the `<cite data-para>` tagging requirement below.

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
- [x] Solange I — `4f7270e`
- [x] Solange II — `883e814`
- [x] Grzelczyk — `56367b7`
- [x] Åkerberg Fransson — `19ab253`
- [x] Francovich and Bonifaci v Italy — `6e96171` (authentic Italian citation text sourced and verified)

## Italian language pass — COMPLETE
All 19 cases now have a full `it:{}` translation block (all four IRAC levels, holistic, citations) — verified by script scanning every case in `CASES` for `it:{` presence, zero missing. Combined with the FR/DE work earlier this session, every case in `casus.html` is now fully quadrilingual (EN/FR/DE/IT). Order followed: file order (same as the parity pass), i.e. the order cases appear in `CASES`.

Resuming the 178-new-case queue now (see "Next up" section below) — new cases going forward will need EN/FR/DE/IT from the start, not EN/FR/DE followed by a later IT pass.

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
- Site is now quadrilingual (EN/FR/DE/IT) across all 20 cases currently live — see "Italian language pass" above. New cases from here on need all four languages, not three.
- Cases at full depth (4 levels x 4 languages, verified/flagged citations, per-paragraph `<cite>` tagging as of Mangold): **8 of 182**
  - [x] Simmenthal II (Case 106/77, CJCE) — `mise_en_oeuvre`, `ordre_juridique`
  - [x] Marshall (Case 152/84, CJCE) — `droit_derive`, `renvoi_prejudiciel`
  - [x] Solange I (BVerfGE 37, 271) — `droits_fondamentaux`, `identite_constitutionnelle`
  - [x] Solange II (BVerfGE 73, 339) — `droits_fondamentaux`, `identite_constitutionnelle`
  - [x] Grzelczyk (Case C-184/99, CJCE) — `citoyennete`, legacy tag `solidarity`
  - [x] Åkerberg Fransson (Case C-617/10, CJUE) — `droits_fondamentaux` (commit `e8020a3`)
  - [x] Francovich and Bonifaci v Italy (Joined Cases C-6/90 & C-9/90, CJCE) — `recours_manquement`, `responsabilite_extracontractuelle` (commit `417cc3c`)
  - [x] Mangold v Helm (Case C-144/04, CJCE) — `droit_derive`, `droits_fondamentaux`, `renvoi_prejudiciel`, legacy tag `non_discrimination` (commit `a081e2e`) — first case with `<cite data-para>` tagging; jurisdiction corrected CJUE→CJCE against TRACKING.md (decided 2005, pre-Lisbon)
- Note: Solange I and Solange II are both fully committed in commit `e32e5ca`, even though its message only names Solange I — the Edit that added them was a single combined change and both are present and correct in `casus.html`; this is just a commit-message labeling slip, not a content gap.
- Old 12 Casus cases: remapped onto the new taxonomy (themes[] swapped, jurisdiction added, legacyThemes added to Defrenne/Dominguez/Konstantinidis) AND now at full trilingual parity — see "Original-12 translation-parity pass" below, **complete as of this checkpoint**.
- 174 cases remaining, not started.

## Standing citation-verification convention (applies to all remaining cases)
Direct EUR-Lex fetches (`eur-lex.europa.eu/legal-content/.../TXT/HTML/...` and the plain `/TXT/` variant) have failed consistently — the page returns empty to WebFetch, likely JS-rendered. Per user decision, the fallback is:
1. Attempt EUR-Lex fetch once.
2. If it fails, use WebSearch to find the same paragraph-numbered quote corroborated by independent secondary sources (academic commentary, case-law databases).
3. Mark the citation's `note` field explicitly: "Verified via secondary source... primary EUR-Lex fetch failed" (English), with FR/DE/IT equivalents.
4. For non-English citation entries, translate the verified English quote myself and flag it explicitly as an unofficial translation not checked against the official-language EUR-Lex text — never present a FR/DE/IT quote as independently source-verified unless it actually was.
5. **Check the case's authentic procedural language first** (established during the FR/DE/IT passes): if the case's own language matches one of the site's four (e.g. an Italian case like Costa v ENEL, Simmenthal II, or Francovich; a French case like Grzelczyk or Defrenne; a German case like Handelsgesellschaft, Stauder, or Konstantinidis), try to source the actual judgment text in that language via WebSearch/WebFetch and use it as the verified primary citation in that language's translation block, rather than translating from English. This has consistently worked for Italian-language cases via secondary sources like giurcost.org even when EUR-Lex itself fails.

## Schema notes for future cases (Option 1, minimal-diff taxonomy integration)
- `jurisdiction: "CJCE"|"CJUE"|"CourEDH"|"BVerfGE"|"ATF"|"AG"` — required on every new case, renders as a visible badge next to the name/citation.
- `themes: [...]` — flat array of the 17 new canonical English strings (see `THEMES` const in casus.html). The establishes/illustrates/applies distinction per theme is captured in prose (Holistic + IRAC text), not a structured field — Option 2 (structured relations) was explicitly rejected by the user for now.
- `legacyThemes: [...]` (optional) — only for the 5 old substantive categories with no equivalent in the 17 (Non-discrimination, Market freedoms, Worker's rights, Collective action vs. economic liberty, Solidarity). Do not backfill this across all 182 cases — apply only where a case's actual holding genuinely turns on one of these.
- CJCE vs CJUE: date-based split at the Lisbon Treaty's entry into force (1 Dec 2009). Pre-Lisbon judgments are CJCE even if commonly cited by their later CJUE case number format.
- When adding a case, check `TRACKING.md`'s distinct-case list AND grep `casus.html` for `case-link-pending` with that case's name — several already-live cases (Costa v ENEL, Van Gend en Loos, Konstantinidis) have forward references to not-yet-added cases in their holistic text (Simmenthal, Foster v British Gas, Grzelczyk, Zhu and Chen, etc.). Converting a `case-link-pending` span to a real `<a class="case-link" onclick="jumpToCase('id')">` link is part of "adding" a case if it's referenced elsewhere. Some references (e.g. Marshall in Van Gend en Loos) were already coded as real `jumpToCase` links pointing at an id that didn't exist yet — these self-resolve once the case is added under that same id, no text edit needed, just confirm the id matches.
- **`translations` must now include `fr`, `de`, AND `it`** for every new case (as of the Italian language pass, 2026-07-23) — all four IRAC levels, holistic, and citations, same structure and rigor for each language. Write all three at once per case rather than doing a language in a separate later pass (that's what the original-12 parity pass and the Italian pass both had to clean up after the fact).
- **Citations need `<cite data-para="key">` inline tagging** for every new case (as of the citation-highlight upgrade, 2026-07-23) — see the dedicated section above for the full spec. Tag `intermediate.rule`/`detailed.rule` (and `application` where a specific disposition paragraph exists), give each citation object a stable `key` alongside its `paragraphs` label, same keys reused across all four languages. Mangold is the reference example — copy its pattern rather than re-deriving it.
- **Every case also needs a `sourceUrl`** — the EUR-Lex CELEX page (`https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:<code>`) for CJEU/CJCE judgments, or the appropriate national court's own site for non-EUR-Lex cases (e.g. bundesverfassungsgericht.de for BVerfGE decisions). Construct the CELEX code from the case's own citation number (year embedded in the case number, not the decision year — e.g. Case C-6/90 decided 1991 is CELEX `61990...`, not `61991...`) and spot-check it via search before trusting it; don't guess blind on cases you haven't verified at least once.

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
