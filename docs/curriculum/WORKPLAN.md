# Curriculum Upgrade — Workplan & Tracker

Source plan: [`PLAN.md`](PLAN.md) (copy of `CURRICULUM_UPGRADE_PLAN.md`, review of 2026-10-13).
Branch: **`curriculum-upgrade`** (local; not pushed, not deployed until the owner says so).

Status keys: `[ ]` todo · `[~]` in progress · `[x]` done (commit = task ID in `git log`) · `[!]` blocked (reason)

---

## RESUME HERE — recovery procedure (read first after any restart)

1. `cd C:\Users\Cyrille\Documents\Playground && git status && git branch --show-current`
   - Must be on `curriculum-upgrade`. If not: `git checkout curriculum-upgrade`.
   - Uncommitted changes = the task marked `[~]` below was interrupted. Run the tests (step 2); if green, commit it; if red, finish or `git stash` it.
2. `python manage.py test quiz` — must be green before starting the next task.
3. `git log --oneline -15` — every finished task is one commit whose message starts with its task ID (e.g. `B2.3:`). Cross-check with the boxes below; the commit log wins if they disagree.
4. Continue with the first `[ ]` / `[~]` task in the **Current phase**. Update this file in the same commit as the work.
5. Eyeball new pictures: `python manage.py preview_skills <slugs…> --lang fr --png preview.png` (headless Chrome screenshot of sample problems; write outputs outside the repo).
6. After adding skills: new data migration re-running the seed (copy `0020_*`), `python manage.py migrate`, add the slugs to `quiz/curriculum.py` (QC refs), tests in `quiz/test_curriculum_*.py`.

Session log (append one line per working session):

| Date | Session summary | Last commit |
|---|---|---|
| 2026-10-13 | Branch + workplan; Phase A done; WP2 + WP3 done (covered 57 → 97 of 236) | see git log |
| 2026-10-13 | WP4 done (covered → 129 of 236). **Full suite NOT re-run after WP4**: the run was killed (machine low on memory). `quiz.test_curriculum_plus` was green (35 tests). FIRST STEP next session: `python manage.py test quiz`. | B4 checkpoint |
| 2026-10-14 | Full suite (all modules at once) ran 24 min with no output and flat memory → looks like a hang, not low memory. Every test module passes when run alone (12/12). Suspect: a generator `while` loop that rarely never ends, depending on random state from earlier tests. Investigating with `-v 2`. | B4 checkpoint |
| 2026-10-14 | WP5 geometry done: 14 skills (C5.1–C5.14), solids/nets/grids/triangles/circles in `illustrations.py`, migration 0024, coverage 129 → 149 of 236 (geometry 29/40). `g2-grid-map` renamed `g3-grid-map` (no grade 2 domain yet). Next: finish the hang investigation, then WP6 (C6.1). | C5 checkpoint |

---

## Decisions (from PLAN.md §2)

| # | Decision | Status |
|---|---|---|
| D1 | Launch scope: grades 3–6 first, 1–2 afterwards | Adopted (recommendation) |
| D2 | Signed integers — grade-6-only domain, no arithmetic | **[!] Awaiting owner** — conflicts with the standing "no negatives anywhere" rule. WP9 + 4-quadrant item blocked until answered. |
| D3 | Beyond-primary content: cap grade-tagged skills; generic skills stay as challenge | Adopted |
| D4 | Typed answers at medium/hard for computation | Adopted |

---

## Conventions for every new skill (Definition of done)

- Generator in `quiz/generators/<module>.py`, levels easy/medium/hard, FR+EN prompt/hint/explanation, one language per session (labels as `(fr, en)` pairs).
- Wired in `GENERATORS`, `SKILL_MAP`, `TOPIC_GROUPS` (`quiz/generators/__init__.py`); seed migration; `quiz/curriculum.py` QC refs.
- Primary rules: no √, no negatives (until D2), audit number limits, fractions with related denominators in grade paths.
- Tests: 40 runs × 3 levels through the shared `_check`, plus a correctness test per skill where the answer can be recomputed.
- Seed: each batch adds a migration `00NN_seed_<batch>.py` calling `quiz.migrations.0020_curriculum_refs.seed_all` (seeds new skills + fills `curriculum_ref`).
- Wiring: new skills go in `quiz/generators/registry_plus.py` (PLUS_GENERATORS / PLUS_SKILL_MAP / PLUS_GROUPS); shared builders in `generators/kit.py` (mc/typed/ordering/match) and pictures in `quiz/illustrations.py`.
- Tests: add the module's correctness tests to `quiz/test_curriculum_plus.py` (the structural loop already covers every PLUS skill).
- Coverage: when a skill lands, add its QC entries to `docs/curriculum/coverage_upgrades.py`; `python docs/curriculum/coverage_map.py docs/curriculum/AUDIT_REFERENCE.md out.md` prints the live score.
- Coverage source of truth: `docs/curriculum/coverage_map.py` (status per QC entry) — update statuses when a skill lands; regenerate Appendix A with it in F4.
- New pictures use the generic `canvas` shape (`quiz/illustrations.py`) unless an existing renderer fits.

---

## Phase A — Pre-launch hygiene (WP0)

- [x] A1 Typed answers at medium/hard for `add`, `subtract`, `multiply`, `divide`, `decimal-*`, `fraction-*` (D4)
- [x] A2 English number words in EN sessions: `write-number`, `read-decimal` (+ verify `read-number`, `g5-large-integer`)
- [x] A3 Scope caps: `read-decimal` ≤ thousandths; `decimal-multiply` product ≤ hundredths
- [x] A4 Wording fixes: plurals/articles (`fraction-collection`, `g5-probability-frac`), quantity-aware comparatives in `resolution.measurements`, `g5-data-table` duplicate table text, probability-0 answer
- [x] A5 "1re année" label for grade 1 in every grade picker
- [x] A6 `quiz/curriculum.py` (slug → QC refs) + migration filling `Skill.curriculum_ref`
- [x] A7 Generic `canvas` illustration type (`render_shape` + template) — infrastructure for B–E

## Phase B — Core grades 3–6 numbers (WP2, WP3, WP4)

WP2 Fractions
- [x] B2.1 `g3-fraction-words` (031, 040)
- [x] B2.2 `g3-numerator-denominator` (030)
- [x] B2.3 `g4-fraction-benchmark` (032)
- [x] B2.4 `g4-equivalent-fractions` (033, 113)
- [x] B2.5 `g5-fraction-meanings` (029)
- [x] B2.6 `g5-order-same-numerator` (037)
- [x] B2.7 `g6-order-related-denominators` (036)
- [x] B2.8 `g6-simplify-fraction` (114, 117)
- [x] B2.9 `g6-fraction-add-related` (115)
- [x] B2.10 `g6-whole-times-fraction` (116, 082)
- [x] B2.11 `fraction-shape` upgrade: circles + collections (027)

WP3 Decimals & percentages
- [x] B3.1 `g4-decimal-grid` (041, 042)
- [x] B3.2 `g4-decimal-equivalence` (044, 046)
- [x] B3.3 `g4-decimal-number-line` (047)
- [x] B3.4 `g6-decimal-number-line` (048)
- [x] B3.5 `g4-round-decimal` (050)
- [x] B3.6 `g5-times-power-of-ten` (122)
- [x] B3.7 `g5-estimate-decimal` (118, 119)
- [x] B3.8 `g5-decimal-story` (075–078)
- [x] B3.9 `g6-percent` (034, 053, 127–129, 131)
- [x] B3.10 `g6-choose-notation` (130)
- [x] B3.11 `fraction-to-decimal` hundredths (052)

WP4 Operations & calculation
- [x] B4.1 `g3-equality-true-false` (068)
- [x] B4.2 `g4-equivalent-expressions` (013)
- [x] B4.3 `g4-properties` (069, 070)
- [x] B4.4 `g6-distributive` (071)
- [x] B4.5 `g4-missing-factor` (100)
- [x] B4.6 `g4-division-remainder` (099)
- [x] B4.7 `g4-arrays` (095, 097, 067)
- [x] B4.8 `g3-story-meaning` (063–065)
- [x] B4.9 `g5-expression-for-story` (072)
- [x] B4.10 `g3-estimate-sum` (083)
- [x] B4.11 `g5-estimate-quotient` (084)
- [x] B4.12 `g6-divisibility` (103)
- [x] B4.13 `g6-prime-factors` (101)
- [x] B4.14 `g6-powers` (022, 025, 102)
- [x] B4.15 ×2 / square / triangular / growing sequences — delivered as new skill `g5-number-patterns` (legacy `number-sequence` untouched) (016, 107)
- [~] B4.16 Fact fluency: content done (`g4-times-tables`, typed, 10 s); **todo**: per-fact adaptive tracking in the practice view (087, 094, 096)
- [x] B4.17 `g6-write-large-number` (008) — added: writing numbers up to 999 999

## Phase C — Geometry & measurement (WP5, WP6)  ← current phase

- [x] C5.1 `g3-solid-picture` (141, 143)
- [x] C5.2 `g3-prism-or-pyramid` (145, 152)
- [x] C5.3 `g3-net-match` (146, 147, 150)
- [x] C5.4 `g4-net-pyramid` (148)
- [x] C5.5 `g6-polyhedron-net` (149)
- [x] C5.6 `g3-convex` (157)
- [x] C5.7 `g6-triangle-type` (162, 163, 165)
- [x] C5.8 `g6-circle-parts` (164, 165)
- [x] C5.9 `g3-symmetry-axis` (168, 170)
- [x] C5.10 `g6-translation` (169, 171)
- [x] C5.11 `g3-frieze` (167–169)
- [x] C5.12 `g3-grid-map` (133) — slug changed from g2- (lives in grade 3 until WP1 adds grade 2)
- [x] C5.13 `cartesian-place-point` (135)
- [x] C5.14 `g3-congruent` (166) — added: congruent figures
- [ ] C6.1 `g3-ruler-mm` (176)
- [ ] C6.2 `g5-estimate-length` (177)
- [ ] C6.3 `g3-area-count-squares` (184, 186)
- [ ] C6.4 `g5-area-units` (185, 187)
- [ ] C6.5 `g3-volume-count-cubes` (188)
- [ ] C6.6 `g6-volume-units` (191)
- [ ] C6.7 `g4-compare-angles` (192)
- [ ] C6.8 `g6-protractor` (194, 195)
- [ ] C6.9 `g3-balance-scale` (200, 201)
- [ ] C6.10 `g3-capacity-estimate` (196, 197)
- [ ] C6.11 `g3-thermometer` grades 3–4 (208)

## Phase D — Statistics, probability, integers (WP7, WP8, WP9)

- [ ] D7.1 `g3-pictograph` (212)
- [ ] D7.2 `g4-line-graph` (213, 219)
- [ ] D7.3 `g3-tally-table` (211)
- [ ] D7.4 `g3-build-chart` (215, 216)
- [ ] D7.5 `g4-survey-question` (210)
- [ ] D8.1 `g3-equally-likely` (222)
- [ ] D8.2 `g4-compare-likelihood` (226, 231)
- [ ] D8.3 `g4-independence` (223)
- [ ] D8.4 `g4-variability` (221)
- [ ] D8.5 `g5-probability-line` (232)
- [ ] D8.6 `g5-tree-diagram` (230)
- [ ] D8.7 `g5-simulation` (224, 227, 228, 234, 235)
- [ ] D8.8 `g2-list-outcomes` (229)
- [!] D9.1–D9.4 Integers domain — blocked on D2

## Phase E — Grades 1–2 (WP1)

- [ ] E0 Read-aloud button (Web Speech API, FR/EN) for prompts
- [ ] E1.1 `g1-count-objects` · [ ] E1.2 `g1-count-on` · [ ] E1.3 `g1-skip-count` · [ ] E1.4 `g1-estimate-collection`
- [ ] E1.5 `g2-tens-ones-picture` · [ ] E1.6 `g2-hundred-chart` · [ ] E1.7 `g1-compare` · [ ] E1.8 `g2-order`
- [ ] E1.9 `g1-add-facts` · [ ] E1.10 `g1-sub-facts` · [ ] E1.11 `g1-fact-strategies` · [ ] E1.12 `g2-add-sub-2digit`
- [ ] E1.13 `g1-story-add-sub` · [ ] E1.14 `g2-equal-groups` · [ ] E1.15 `g1-true-equality` · [ ] E1.16 `g1-missing-number`
- [ ] E1.17 `g1-shape-pattern` · [ ] E1.18 `g1-name-shape` · [ ] E1.19 `g1-open-closed-lines` · [ ] E1.20 `g1-solid-objects`
- [ ] E1.21 `g1-position-words` · [ ] E1.22 `g1-same-shape-size` · [ ] E1.23 `g1-compare-lengths` · [ ] E1.24 `g1-measure-units`
- [ ] E1.25 `g2-ruler-cm` · [ ] E1.26 `g1-clock-hour-half` · [ ] E1.27 `g1-calendar` · [ ] E1.28 `g1-half-third-quarter`
- [ ] E1.29 `g1-pictograph` · [ ] E1.30 `g1-certain-possible-impossible`

## Phase F — Cross-cutting (WP10)

- [ ] F1 Vocabulary matching skill per domain (term ↔ picture/symbol)
- [ ] F2 "Who is right?" reasoning items (≥ 1 per domain)
- [ ] F3 Resolution level for new skills where it makes sense
- [ ] F4 Re-score Appendix A of PLAN.md with the new skills; final coverage numbers

## Release checklist (owner-triggered, not done automatically)

- [ ] Full test suite green · [ ] manual click-through of each new domain (FR + EN, mobile width)
- [ ] Merge `curriculum-upgrade` → `master`, push, deploy per DEBUG.md, `migrate`, `ai_enrich_skills`
