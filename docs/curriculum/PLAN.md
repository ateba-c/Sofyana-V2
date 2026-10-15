# Sofyana — Primary Math Coverage Review & Upgrade Plan

*Review date: 2026-10-13 · Reference: `Sofyana_Audit_Mathematique_Quebec.md` (236 entries, grades 1–6), used as a general primary-math checklist · Code reviewed at `f1020ed`*

## 1. Verdict

**Sofyana is not yet complete enough to claim "all of primary-school math".** Its strength is **grades 3–6 number work**: place value, comparing and ordering, the four operations, time, unit conversions, order of operations, the mean, and pie charts. It falls short in four areas:

1. **Grades 1–2 have no content at all.** No skill is tagged grade 1 or 2, and the sign-up grade picker only offers grades 3–6, because the list of grades comes from the content. 85 of the 236 entries are active in grade 1 or 2.
2. **Geometry is about half missing**: triangles, circles, nets, symmetry and translations, convex polygons, and spatial relations.
3. **Probability and statistics stop at the basics**: no pictographs, line graphs, building a chart, equally likely outcomes, tree diagrams or experiments.
4. **Fractions and decimals are partial**: no equivalent fractions, simplifying, whole number × fraction, decimals on a number line, rounding decimals, ×/÷ 10/100/1000, or percentages as a skill of their own.

### Scorecard

| Field | Entries | Covered | Partial | Missing | Off-screen | Decision |
|---|---|---|---|---|---|---|
| Arithmetic | 131 | 27 | 66 | 29 | 3 | 6 |
| Geometry | 40 | 9 | 9 | 20 | 1 | 1 |
| Measurement | 38 | 16 | 10 | 11 | 1 | 0 |
| Statistics | 11 | 3 | 3 | 5 | 0 | 0 |
| Probability | 16 | 2 | 5 | 9 | 0 | 0 |
| **Total** | **236** | **57 (24 %)** | **93 (39 %)** | **74 (31 %)** | **5** | **7** |

Status definitions follow the audit's own rule: an entry is **Covered** only when the verb, the representation, the number limits and the level of independence all match. A multiple-choice recognition item does **not** cover a "construct / measure / explain" objective.
- **Partial**: the topic exists, but with the wrong representation (text instead of a picture), outside the number limits, only at another grade, or only as multiple choice.
- **Off-screen**: building physical rulers or solids, or using a calculator.
- **Decision**: signed integers, which conflict with the current "no negatives" rule.

**How this was checked.** The audit matrix was mapped against all 134 skills in the registry. Every skill was run at every level (two samples each, 635 sample lines) to check real output, not just skill names. The full table for each entry is in **Appendix A**.

## 2. Decisions needed before work starts

| # | Decision | Options | Recommendation |
|---|---|---|---|
| D1 | **Launch scope** | (a) Launch now as "Grades 3–6", with grades 1–2 marked coming soon. (b) Hold the launch until grades 1–2 ship. | **(a)**. Grades 3–6 are credible after Phase A+B. Grades 1–2 need new picture-based renderers and read-aloud, which is a project of its own. |
| D2 | **Signed integers** (QC-056→061, QC-136; grades 5–6) | (a) Keep "no negatives anywhere" and document 7 entries as a deliberate exclusion. (b) Allow negatives **only** in a grade-6 "Integers" domain: thermometer below 0 °C, number line, compare and order, 4-quadrant plane. **No arithmetic on negatives** (the audit doesn't ask for it). | **(b)**. The rule was meant to stop negative *results* from appearing in younger grades. A walled-off grade-6 domain keeps that promise. |
| D3 | **Generic skills that go beyond primary** (`fraction-divide`, unrelated-denominator fraction +/−, decimal × decimal to thousandths, `mg`/`kL`, ten-thousandths in `read-decimal`) | Keep as is / tag as "Enrichment" / cap to primary limits | **Cap the grade-tagged paths, keep the generic skills labelled "Challenge".** |
| D4 | **Multiple choice for computation** (generic add/subtract/multiply/divide and decimal ops) | Keep MC / typed answers at medium and hard | **Typed at medium and hard**, MC kept at easy. Typed-answer checking (`quiz/answers.py`) already exists. |

## 3. Quality issues found in existing content (WP0, do before launch)

These came up while running every generator. All are small.

| Issue | Where | Fix |
|---|---|---|
| English sessions see **French number words** ("Write in digits: **sept cent dix-huit**"). This breaks the one-language-per-session rule. | `write-number`, `read-decimal` (prompt words); `read-number` has `label_en` but check it shows | Generate English words when the session is EN |
| Out-of-scope numbers in grade-tagged paths | `read-decimal` hard (64.5712), `decimal-multiply` hard (62.64 × 2.9 = 181.656), `convert-mass` (mg), `convert-volume` (kL), `fraction-subtract` hard (3/4 − 4/9) | Cap per D3 |
| Computation answered by multiple choice, so it can be guessed | `add`, `subtract`, `multiply`, `divide`, `decimal-*`, `fraction-*` | Per D4 |
| Grammar: "1 tulips", "1 cars", "a orange marble" | `fraction-collection`, `g5-probability-frac` | Plural/article helper |
| Wrong comparative: "Hugo's road is 56 km **shorter**" for suitcases (kg) and flour (g) | `resolution.measurements` (used by `g4-order-numbers`, `g4-before-after`, `order-numbers`) | Pick the word by quantity: lighter/heavier, less/more |
| Data table text appears twice in the prompt ("Table: Apple: 3 … Table of favourite fruits: Apple: 3, …") | `g5-data-table` | Show it once, ideally as a rendered table |
| Probability-0 answer written as `0/1` | `g5-probability-forms` resolution | Accept and display `0` |
| `{{ g }}e année` would display "1e année" for grade 1 | `register.html`, other grade pickers | Use "1re" for grade 1 (needed for WP1) |
| `Skill.curriculum_ref` is empty | admin | Fill it with QC IDs from Appendix A. Coverage can then be tracked in admin, and AI search gets better metadata |

## 4. Upgrade plan: work packages

Each package lists proposed skills, using the existing slug conventions. The **Format** column says what the item needs: MC, typed, ordering, matching, or a new illustration (🖼) or interaction (🖐). QC references link back to the audit.

### Shared infrastructure (build once, used by WP1, WP5–WP8)

The existing renderers are clock, number line, fraction bar/number line, bar chart, pie chart, thermometer, grid point, polygons, angles and line pairs. To add:

| Renderer / widget | Used by |
|---|---|
| 🖼 Object collection (countable emojis/icons, optionally grouped in tens) | WP1 counting, equal groups, pictograph |
| 🖼 Base-10 blocks & hundred chart | WP1 place value |
| 🖼 Ruler (cm/mm) and protractor | WP6 |
| 🖼 Balance scale, measuring jug | WP6 |
| 🖼 Isometric solids (sphere, cone, cube, cylinder, prism, pyramid) and cube stacks | WP5, WP6 volume |
| 🖼 Nets of prisms and pyramids | WP5 |
| 🖼 Square grid with a figure (area counting, symmetry, translation, map squares) | WP5, WP6 |
| 🖼 Triangle with tick marks and right-angle marks; circle with radius/diameter | WP5 |
| 🖼 Pictograph with key; line graph | WP7 |
| 🖼 Spinner, die, tree diagram; 10×10 decimal grid | WP8, WP3 |
| 🖐 Tap to place a point on a number line or grid (MC first, then real tap) | WP3, WP5, WP8 |
| 🖐 Bar chart builder (tap to set bar heights) | WP7 |
| 🖐 Simulation runner (spin or roll N times, tally, compare with theory) | WP8 |
| 🔊 Read-aloud of prompts (Web Speech API, FR/EN) | WP1, a requirement for 6–7-year-olds |

### WP1: Grades 1–2 foundation · *L · ~28 skills · new domains "1re année" / "2e année"*

| Skill (proposed slug) | Grade | Format | QC |
|---|---|---|---|
| `g1-count-objects`: how many? (≤20, then ≤100) | 1 | typed + 🖼 collection | 004, 006, 009 |
| `g1-count-on`: count on from a number | 1 | typed | 001, 005 |
| `g1-skip-count`: by 2, 5, 10 (<100), forwards and backwards | 1–2 | typed | 002, 003 |
| `g1-estimate-collection`: about how many? | 1–2 | MC + 🖼 | 021 |
| `g2-tens-ones-picture`: base-10 blocks → number, and back | 2 | typed/MC + 🖼 | 010, 012 |
| `g2-hundred-chart`: missing number in a hundred chart | 1–2 | typed + 🖼 | 017 |
| `g1-compare`, `g2-order` (<100 / <1000, <, >, =) | 1–2 | typed / ordering | 014, 015 |
| `g1-add-facts`, `g1-sub-facts` (0+0 … 10+10, timed option) | 1–2 | typed | 085, 087 |
| `g1-fact-strategies`: doubles, make 10, near doubles | 1–2 | MC | 086 |
| `g2-add-sub-2digit`: with number line or blocks picture | 2 | typed + 🖼 | 088, 090 |
| `g1-story-add-sub`: join / separate / compare stories | 1–2 | typed + 🖼 | 062, 063 |
| `g2-equal-groups`: groups and sharing pictures (× ÷ meaning) | 2 | typed + 🖼 | 066 |
| `g1-true-equality`: is 3 + 2 = 6 − 1 true? | 1–2 | MC | 068, 069 |
| `g1-missing-number`: □ + 4 = 9 in all six forms | 1–2 | typed | 093 |
| `g1-shape-pattern`: what comes next (shapes, colours) | 1 | MC + 🖼 | 105, 167 |
| `g1-name-shape`: square, rectangle, triangle, rhombus, circle | 1–2 | MC + 🖼 | 154, 155 |
| `g1-open-closed-lines`: open/closed, curved/broken | 1 | MC + 🖼 | 153 |
| `g1-solid-objects`: ball → sphere, can → cylinder… | 1–2 | MC + 🖼 | 139, 141, 142 |
| `g1-position-words`: left/right, above/below, in front/behind | 1 | MC + 🖼 | 132 |
| `g1-same-shape-size`: congruent figures | 1–2 | MC + 🖼 | 166 |
| `g1-compare-lengths`: longer/shorter, order 3 objects | 1 | MC + 🖼 | 172 |
| `g1-measure-units`: how many paper clips long? | 1 | typed + 🖼 | 174 |
| `g2-ruler-cm`: read a length in cm | 2 | typed + 🖼 ruler | 175 |
| `g1-clock-hour-half`: o'clock and half past | 1–2 | MC + 🖼 clock | 204, 206 |
| `g1-calendar`: days, months, seasons, yesterday/tomorrow | 1–2 | MC | 207 |
| `g1-half-third-quarter`: everyday fractions plus the words | 1–2 | MC + 🖼 | 026, 039 |
| `g1-pictograph`: read and answer | 1–2 | typed + 🖼 | 212, 218 |
| `g1-certain-possible-impossible`: picture version of `probability-vocab` | 1–2 | MC + 🖼 | 225, 229 |

Also needed: add grades 1–2 to the grade picker (automatic once domains exist), fix the "1re" label, and turn on read-aloud for these domains.

### WP2: Fractions · *M · ~10 skills*

| Skill | Grade | Format | QC |
|---|---|---|---|
| `g3-fraction-words`: "three quarters" ↔ 3/4 | 3–4 | typed / match | 031, 040 |
| `g3-numerator-denominator`: what each part means | 3–4 | MC + 🖼 | 030 |
| `g4-fraction-benchmark`: compare to 0, ½, 1 | 4 | MC | 032 |
| `g4-equivalent-fractions`: shaded bars, then numbers | 4–6 | MC/typed + 🖼 | 033, 113 |
| `g5-fraction-meanings`: sharing, division (3 ÷ 4 = 3/4), ratio | 5–6 | MC | 029 |
| `g5-order-same-numerator` / `g6-order-related-denominators` | 5–6 | ordering | 036, 037 |
| `g6-simplify-fraction` | 6 | typed | 114, 117 |
| `g6-fraction-add-related`: 1/2 + 3/8 (one denominator a multiple of the other) | 6 | typed | 115 |
| `g6-whole-times-fraction`: 3 × 2/5, ⅓ of 12 | 6 | typed | 116, 082 |
| Upgrade `fraction-shape`: add circles and sets of objects | 3 | 🖼 | 027 |

### WP3: Decimals & percentages · *M · ~10 skills*

| Skill | Grade | Format | QC |
|---|---|---|---|
| `g4-decimal-grid`: 10×10 grid / money ↔ decimal | 4 | MC + 🖼 | 041, 042 |
| `g4-decimal-equivalence`: 0.5 = 0.50, 12 tenths = 1.2 | 4–6 | match | 044, 046 |
| `g4-decimal-number-line`: between two whole numbers | 4 | MC → 🖐 | 047 |
| `g6-decimal-number-line`: between two decimals | 6 | MC → 🖐 | 048 |
| `g4-round-decimal`: round / truncate | 4–6 | typed | 050 |
| `g5-times-power-of-ten`: × and ÷ by 10, 100, 1000 | 5–6 | typed | 122 |
| `g5-estimate-decimal`: estimate sums, products, quotients | 4–6 | MC | 118, 119 |
| `g5-decimal-story`: +/−/×/÷ stories with decimals | 4–6 | typed | 075–078 |
| `g6-percent`: fraction ↔ decimal ↔ %, 100-grid | 6 | typed / match | 034, 053, 127–129, 131 |
| `g6-choose-notation`: which form fits the context | 6 | MC | 130 |
| Fix `fraction-to-decimal` to include hundredths | 4 | — | 052 |

### WP4: Operations & calculation · *M · ~14 skills + 1 feature*

| Skill | Grade | Format | QC |
|---|---|---|---|
| `g3-equality-true-false`, `g4-equivalent-expressions` | 3–6 | MC | 013, 068 |
| `g4-properties`: commutative, associative, fact families for +/− | 3–4 | MC | 069, 070 |
| `g6-distributive`: 7 × 12 = 7 × 10 + 7 × 2 | 5–6 | MC/typed | 071 |
| `g4-missing-factor`: a × □ = c, □ ÷ b = c | 4–6 | typed | 100 |
| `g4-division-remainder`: quotient and remainder | 4–6 | typed (2 fields) | 099 |
| `g4-arrays`: arrays and multiplication strategies | 3–4 | MC + 🖼 | 095, 097, 067 |
| `g3-story-meaning`: join / separate / compare, bar model | 3–6 | MC + 🖼 | 063–065 |
| `g5-expression-for-story`: pick the operation chain | 5–6 | MC | 072 |
| `g3-estimate-sum`, `g5-estimate-quotient` | 3–6 | MC | 083, 084 |
| `g6-divisibility`: by 2, 3, 4, 5, 6, 8, 9, 10 | 6 | MC | 103 |
| `g6-prime-factors`: factor tree | 5–6 | typed + 🖼 | 101 |
| `g6-powers`: 2³, square and cube, exponent words | 5–6 | typed | 022, 025, 102 |
| Upgrade `number-sequence`: ×2, square and triangular sequences, "describe the rule" | 3–6 | typed/MC | 016, 107 |
| **Feature:** timed fact-fluency mode for + and × tables, with per-fact mastery tracking | 1–5 | — | 087, 094, 096 |

### WP5: Geometry · *L · ~14 skills (heaviest renderer work)*

| Skill | Grade | Format | QC |
|---|---|---|---|
| `g3-solid-picture`: name the solid from an isometric drawing | 3 | MC + 🖼 | 141, 143 |
| `g3-prism-or-pyramid`: classify, name by base | 3–4 | MC + 🖼 | 145, 152 |
| `g3-net-match`: net ↔ prism; `g4-net-pyramid`; `g6-polyhedron-net` | 3–6 | MC + 🖼 nets | 146–150 |
| `g3-convex`: convex or non-convex polygon | 3–4 | MC + 🖼 | 157 |
| `g6-triangle-type`: by sides and by angles | 5–6 | MC + 🖼 | 162, 163, 165 |
| `g6-circle-parts`: radius, diameter, circumference, central angle (d = 2r) | 5–6 | MC/typed + 🖼 | 164, 165 |
| `g3-symmetry-axis`: is this a line of symmetry? Complete the figure | 3–4 | MC + 🖼 grid | 168, 170 |
| `g6-translation`: which image is the translation? Follow the arrow | 5–6 | MC + 🖼 grid | 169, 171 |
| `g3-frieze`: which transformation built this frieze or tiling | 3–6 | MC + 🖼 | 167–169 |
| `g3-grid-map`: square B3, follow directions on a plan | 1–4 | MC + 🖼 | 133 |
| `cartesian-place-point`: place (3, 5) | 3–4 | 🖐 | 135 |
| Integers domain: 4-quadrant plane (only if D2 = b) | 6 | 🖐 | 136 |

### WP6: Measurement · *M · ~10 skills*

| Skill | Grade | Format | QC |
|---|---|---|---|
| `g3-ruler-mm`, `g5-estimate-length` (incl. km) | 3–6 | typed + 🖼 | 176, 177 |
| `g3-area-count-squares` | 3 | typed + 🖼 grid | 184, 186 |
| `g5-area-units`: cm², dm², m², with units in the answer | 5–6 | typed | 185, 187 |
| `g3-volume-count-cubes` | 3 | typed + 🖼 cube stacks | 188 |
| `g6-volume-units`: cm³, dm³, 1 dm³ = 1 L | 5–6 | typed | 191 |
| `g4-compare-angles` | 3–4 | MC + 🖼 | 192 |
| `g6-protractor`: read / estimate an angle in degrees | 5–6 | typed + 🖼 | 194, 195 |
| `g3-balance-scale`, `g3-mass-estimate` | 3–6 | MC + 🖼 | 200, 201 |
| `g3-capacity-estimate`: how many cups fill the jug | 3–5 | MC + 🖼 | 196, 197 |
| Thermometer for grades 3–4 (with negatives only if D2 = b) | 3–6 | typed + 🖼 | 208 |

### WP7: Statistics · *M · ~5 skills*

| Skill | Grade | Format | QC |
|---|---|---|---|
| `g3-pictograph`: with key (one picture = 2) | 1–4 | typed + 🖼 | 212 |
| `g4-line-graph`: read and compare | 3–6 | typed/MC + 🖼 | 213, 219 |
| `g3-tally-table`: organise raw data into a table | 1–6 | typed | 211 |
| `g3-build-chart`: build the bar chart for this table (MC "which chart matches", then 🖐 builder) | 1–6 | MC → 🖐 | 215, 216 |
| `g4-survey-question`: which question can a survey answer | 1–6 | MC | 210 |

### WP8: Probability · *M · ~8 skills + simulation widget*

| Skill | Grade | Format | QC |
|---|---|---|---|
| `g3-equally-likely`: fair die, spinner with equal sectors | 1–6 | MC + 🖼 | 222 |
| `g4-compare-likelihood`: more / less / equally likely (spinners) | 3–6 | MC + 🖼 | 226, 231 |
| `g4-independence`: "4 heads in a row; next toss?" | 1–6 | MC | 223 |
| `g4-variability`: will everyone get the same result? | 1–6 | MC | 221 |
| `g5-probability-line`: place an event on a 0–1 line | 5–6 | MC → 🖐 | 232 |
| `g5-tree-diagram`: read and complete | 3–6 | typed + 🖼 | 230 |
| `g5-simulation`: run 20 spins, tally, prediction vs result, experimental vs theoretical | 1–6 | 🖐 simulation | 224, 227, 228, 234, 235 |
| `g2-list-outcomes`: list outcomes of a simple experiment | 1–2 | MC | 229 |

### WP9: Integers (only if D2 = b) · *S · 4 skills, grade-6 domain*

`g6-integer-thermometer`, `g6-integer-number-line`, `g6-integer-compare`, `g6-integer-order` (QC-056→061, plus the 4-quadrant plane in WP5). No addition or subtraction of negatives.

### WP10: Cross-cutting skills (problem solving, reasoning, vocabulary) · *M, ongoing*

The audit's cross-cutting section asks for problem solving, reasoning, communication and feedback on errors.
- **Problem-solving level**: 69 of 134 skills have the 4th "Résolution" level today. Make it part of done for every new skill, and extend `scenarios.py` / `resolution*.py` families.
- **Reasoning items**: "Who is right?" error-analysis items (e.g. *Léo says 0.25 > 0.3 because 25 > 3*), and "pick the justification" MC. At least one per domain.
- **Vocabulary**: one term ↔ picture/symbol matching item per domain. This closes the ~15 "Vocabulaire" entries that are Partial (QC-023/024, 073/074, 112, 137, 156, 161, 181, 186, 218, 236…).
- **Multi-step and missing/irrelevant information**: extend the `g6-relevant-info` pattern to grades 3–5.

## 5. Sequencing

| Phase | Content | Exit criterion |
|---|---|---|
| **A: Pre-launch hygiene** | WP0, decisions D1–D4, `curriculum_ref` filled | No language leaks, no out-of-scope numbers in grade paths, computation typed at medium and hard |
| **B: Core grades 3–6 numbers** | WP2, WP3, WP4 (no new renderers except 10×10 grid and arrays) | Grade 3–6 Arithmetic entries ≥ 85 % Covered/Partial-with-plan |
| **C: Renderers + geometry and measurement** | Shared renderers, WP5, WP6 | Geometry and Measurement Missing count ≤ 3 |
| **D: Statistics, probability, integers** | WP7, WP8, WP9 | Simulation widget live |
| **E: Grades 1–2** | Read-aloud, WP1 | Grades 1 and 2 selectable at sign-up; 85 grade-1/2 entries Covered/Partial |
| **Ongoing** | WP10 on every new skill | — |

Phase E can run in parallel with C and D if there is capacity. It reuses the collection, ruler, clock and pictograph renderers from C and D.

## 6. Definition of done for each new skill

Same pattern as the grade-4 and grade-6 rollouts:
1. Generator in `quiz/generators/gN_*.py` with easy/medium/hard and a FR/EN prompt, hint and step explanation. One language per session.
2. Register in `GENERATORS`, `SKILL_MAP`, `TOPIC_GROUPS`, and add a data migration that re-runs the idempotent seed (copy `0012_seed_grade4_skills.py`).
3. Set `curriculum_ref` = QC IDs and `answer_type`, then run `manage.py ai_enrich_skills` after deploy.
4. Respect the primary rules: no √, no negatives outside the WP9 domain, the audit's number limits, and fractions only with related denominators in grade-tagged paths.
5. Add a resolution-level family where it makes sense.
6. Tests in `quiz/test_gN_generators.py`: every level generates ~200 problems without errors, answers are within limits, and the correct answer is among the choices.
7. Update the status in Appendix A.

---

## Appendix A: Coverage for each entry

> **Re-scored 2026-10-14 (task F4):** after WP0–WP8, WP1 and WP10 the score is **214 covered, 10 partial, 0 missing, 5 off-screen, 7 awaiting decision D2** (was 57 covered). The live per-entry table is `docs/curriculum/COVERAGE.md`, regenerated with `python docs/curriculum/coverage_map.py docs/curriculum/AUDIT_REFERENCE.md docs/curriculum/COVERAGE.md`. The table below is the original October 13 baseline, kept for comparison.

Grade columns follow the audit: **A** = taught with support, **M** = independent by end of year, **R** = reused, **·** = no milestone.

| ID | Objective | 1 2 3 4 5 6 | Status | Sofyana skills | Gap / action |
|---|---|---|---|---|---|
| | **Sens et écriture des nombres / A. Nombres naturels inférieurs à…** | | | | |
| QC-001 | 1. Compter ou réciter la comptine des nombres naturels / a. par ordre croissant à partir d’un nombre donné | `A M · · · ·` | Partial | g4-before-after, number-sequence | No G1–2 counting (<100) — WP1 |
| QC-002 | 1. Compter ou réciter la comptine des nombres naturels / b. par ordre croissant ou décroissant | `A M A M A M` | Partial | number-sequence, g4-skip-sequence | Descending only at hard; nothing for G1–2 — WP1 |
| QC-003 | 1. Compter ou réciter la comptine des nombres naturels / c. par bonds | `A M A M A M` | Covered | number-sequence, g4-skip-sequence | Add G1–2 range (by 2, 5, 10 under 100) — WP1 |
| QC-004 | 2. Dénombrer des collections réelles ou dessinées / a. coordonner le geste et le nombre correspondant (mot); reconnaître l’aspect cardinal d… | `M · · · · ·` | Missing | — | Count a drawn collection (tap/type) — WP1 |
| QC-005 | 2. Dénombrer des collections réelles ou dessinées / b. dénombrer à partir d’un nombre donné | `A M · · · ·` | Missing | — | Count on from a given number — WP1 |
| QC-006 | 2. Dénombrer des collections réelles ou dessinées / c. dénombrer une collection en groupant ou en regroupant | `A M A M A M` | Partial | count-groups | Text only; needs drawn groups of 10 — WP1 |
| QC-007 | 2. Dénombrer des collections réelles ou dessinées / d. dénombrer une collection déjà groupée | `· · A M A M` | Covered | count-groups, g4-grouping-problem, g6-count-groups |  |
| QC-008 | 3. Lire et écrire tout nombre naturel | `A M A M A M` | Partial | read-number, write-number, g5-large-integer | Writing stops at 9 999; G5–6 need typed up to 999 999. EN sessions show French number words — WP0 |
| QC-009 | 4. Représenter des nombres naturels de différentes façons ou associer un nombre à un ensemble d’objets ou à des dessins / a. accent mis sur… | `A M · · · ·` | Missing | — | Visual grouped objects (bags of 10) — WP1 |
| QC-010 | 4. Représenter des nombres naturels de différentes façons ou associer un nombre à un ensemble d’objets ou à des dessins / b. accent mis sur… | `· A A M · ·` | Partial | base10-match, build-number | Text "3 centaines…", no base-10 block picture — WP1 |
| QC-011 | 4. Représenter des nombres naturels de différentes façons ou associer un nombre à un ensemble d’objets ou à des dessins / c. accent mis sur… | `· · A A A M` | Partial | money-match, g6-symbol-form | No abacus picture — WP1 |
| QC-012 | 5. Composer et décomposer un nombre naturel de différentes façons (ex. : 123 = 100 + 23 123 = 100 + 20 + 3 123 = 50 + 50 + 20 + 3 123 = 2 ×… | `A M A M A M` | Covered | expanded-form, decomposition-match, g4-expanded-form, g6-additive-form, g6-symbol-form, g6-multiplicative-form | Add non-standard splits (123 = 50+50+23) — WP4 |
| QC-013 | 6. Reconnaître des expressions équivalentes (ex. : 52 = 40 + 12, 25 + 27 = 40 + 12, 52 = 104 ÷ 2) | `A M A M A M` | Missing | — | Equivalent expressions (52 = 40+12 = 104÷2) — WP4 |
| QC-014 | 7. Comparer entre eux des nombres naturels | `A M A M A M` | Covered | compare-int, g4-compare, g6-compare | Add G1–2 range — WP1 |
| QC-015 | 8. Ordonner des nombres naturels par ordre croissant ou décroissant | `A M A M A M` | Covered | order-numbers, g4-order-numbers, g6-order, g6-extreme |  |
| QC-016 | 9. Décrire dans ses mots et avec un vocabulaire mathématique approprié des régularités numériques (ex. : nombres pairs, nombres impairs, nom… | `A M A M A M` | Partial | even-odd, squares, primes, number-classify | No triangular numbers; no "describe the rule" — WP4 |
| QC-017 | 10. Situer des nombres naturels à l’aide de différents supports (ex. : grille de nombres, bande de nombres, axe de nombres [droite numérique… | `A M A M A M` | Partial | g4-number-line-point, g5-number-line | No hundred chart — WP1 |
| QC-018 | 11. Reconnaître les propriétés des nombres naturels / a. nombre pair ou impair | `A M R R R R` | Covered | even-odd, number-classify |  |
| QC-019 | 11. Reconnaître les propriétés des nombres naturels / b. nombre carré, premier ou composé | `· · A M R R` | Covered | squares, primes, number-classify |  |
| QC-020 | 12. Classifier des nombres naturels de différentes façons selon leurs propriétés (ex. : nombres pairs, nombres composés) | `A M A M A M` | Covered | number-classify, primes (match) |  |
| QC-021 | 13. Faire une approximation d’une collection réelle ou dessinée (estimer, arrondir à un ordre de grandeur donné, etc.) | `A M A M A M` | Partial | round-ten, round-hundred | Rounding yes; estimating a drawn collection no — WP1 |
| QC-022 | 14. Représenter la puissance d’un nombre naturel | `· · · · A M` | Partial | squares (N²) | No cubes / exponent notation 2³ — WP4 |
| QC-023 | Vocabulaire Groupement, chiffre, nombre, unité, dizaine, centaine Nombre naturel, nombre pair, nombre impair Est égal à; est plus grand que… | `A M R R R R` | Partial | compare-int, digit-position | Vocabulary used, never assessed — WP10 |
| QC-024 | Vocabulaire Base dix, position, valeur de position, millier, unité de mille, dizaine de mille Est différent de; est supérieur à; est inférie… | `· · A M R R` | Partial | digit-position, g4-digit-position, primes | No ≠ symbol — WP10 |
| QC-025 | Vocabulaire Centaine de mille, million Exposant, puissance, carré de (le), cube de (le) Parenthèse Symboles ( ), nombres écrits en chiffres,… | `· · · · A M` | Partial | g6-digit-position, squares | No exponent/cube vocabulary — WP4 |
| | **Sens et écriture des nombres / B. Fractions (à l’aide de matériel concret ou de schémas)** | | | | |
| QC-026 | 1. Reconnaître des fractions se rapportant à des éléments du quotidien (représentations concrètes ou imagées) | `A M · · · ·` | Partial | fraction-shape | G3 skill; no G1–2 half/third/quarter of everyday objects — WP1 |
| QC-027 | 2. Représenter une fraction de différentes façons à partir d’un tout ou d’une collection | `A A A A A M` | Covered | fraction-shape, fraction-collection | Only bar pictures; add circles, sets — WP2 |
| QC-028 | 3. Associer une fraction à une partie d’un tout (parties isométriques ou parties équivalentes) ou d’un groupe d’objets et vice versa | `· · A M R R` | Covered | fraction-shape, fraction-collection |  |
| QC-029 | 4. Reconnaître différents sens de la fraction (partage, division, rapport) | `· · A A A A` | Missing | — | Senses of a fraction (sharing, division 3÷4 = 3/4, ratio) — WP2 |
| QC-030 | 5. Distinguer le rôle du numérateur de celui du dénominateur | `· · A M R R` | Partial | fraction-shape (distractor feedback) | Needs explicit numerator/denominator items — WP2 |
| QC-031 | 6. Lire et écrire une fraction | `· · A M R R` | Missing | — | Read/write "trois quarts" ↔ 3/4 — WP2 |
| QC-032 | 7. Comparer une fraction à 0, à ½ ou à 1 | `· · A M R R` | Partial | compare-fraction (vs 1) | No comparing to 0 or to ½ — WP2 |
| QC-033 | 8. Vérifier l’équivalence de deux fractions | `· · A A A M` | Missing | — | Equivalent fractions (visual, then numeric) — WP2 |
| QC-034 | 9. Associer un nombre décimal ou un pourcentage à une fraction | `· · · A A M` | Partial | fraction-to-decimal (tenths), g5-probability-forms | No hundredths, no percentages in context — WP3 |
| QC-035 | 10. Ordonner des fractions ayant un même dénominateur | `· · · A M R` | Covered | g6-fraction-order |  |
| QC-036 | 11. Ordonner des fractions, le dénominateur de l’une étant un multiple de l’autre (ou des autres) | `· · · · A M` | Partial | compare-fraction | Not limited to "one denominator a multiple of the other" — WP2 |
| QC-037 | 12. Ordonner des fractions ayant un même numérateur | `· · · · A M` | Partial | compare-fraction (hard) | Not a dedicated same-numerator item — WP2 |
| QC-038 | 13. Situer des fractions sur un axe de nombres (droite numérique) | `· · · · A M` | Covered | g6-fraction-on-line, g6-fraction-between |  |
| QC-039 | Vocabulaire Fraction, demi, tiers, quart | `A M R R R R` | Partial | fraction-shape | No demi/tiers/quart vocabulary item — WP2 |
| QC-040 | Vocabulaire Numérateur, dénominateur Entier, partie équivalente, fraction équivalente Symbole Notation fractionnaire | `· · A M R R` | Partial | — | Numerator/denominator, equivalent fraction vocabulary — WP2 |
| | **Sens et écriture des nombres / C. Nombres décimaux jusqu’à l’ordre des…** | | | | |
| QC-041 | 1. Représenter des nombres décimaux de différentes façons (concrètes ou imagées) | `· · A M A M` | Partial | g5-decimal-forms | No pictures (10×10 grid, money) — WP3 |
| QC-042 | 2. Reconnaître des représentations équivalentes (concrètes ou imagées) | `· · A M A M` | Partial | g5-decimal-forms | Text only — WP3 |
| QC-043 | 3. Lire et écrire des nombres écrits en notation décimale | `· · A M A M` | Covered | read-decimal, g5-decimal-write | read-decimal goes to ten-thousandths (out of scope) — WP0 |
| QC-044 | 4. Comprendre le rôle de la virgule | `· · A M · ·` | Partial | g5-decimal-write | No item on the role of the decimal point — WP3 |
| QC-045 | 5. Composer et décomposer un nombre décimal écrit en notation décimale | `· · A M A M` | Covered | g5-decimal-write |  |
| QC-046 | 6. Reconnaître des expressions équivalentes (ex. : 12 dixièmes est équivalent à 1 unité et 2 dixièmes; 0,5 est équivalent à 0,50) | `· · A M A M` | Partial | g5-decimal-forms | No 12 tenths = 1.2 or 0.5 = 0.50 items — WP3 |
| QC-047 | 7. Situer des nombres décimaux sur un axe de nombres (droite numérique) / a. entre deux nombres naturels consécutifs | `· · A M A M` | Missing | — | Decimals on a number line between two whole numbers — WP3 |
| QC-048 | 7. Situer des nombres décimaux sur un axe de nombres (droite numérique) / b. entre deux nombres décimaux | `· · · A A M` | Missing | — | Decimals on a number line between two decimals — WP3 |
| QC-049 | 8. Comparer entre eux des nombres décimaux | `· · A M A M` | Covered | compare-decimal |  |
| QC-050 | 9. Faire une approximation (estimer, arrondir à un ordre de grandeur donné, tronquer, etc.) | `· · A M A M` | Missing | — | Round / truncate decimals — WP3 |
| QC-051 | 10. Ordonner des nombres décimaux par ordre croissant ou décroissant | `· · A M A M` | Covered | compare-decimal (sort) |  |
| QC-052 | 11. Associer / a. une fraction à un nombre décimal | `· · A M R R` | Partial | fraction-to-decimal | Tenths only — WP3 |
| QC-053 | 11. Associer / b. une fraction ou un pourcentage à un nombre décimal | `· · · · A M` | Partial | g5-probability-forms | Only inside probability — WP3 |
| QC-054 | Vocabulaire Nombre décimal, dixième, centième Symbole Notation décimale | `· · A M R R` | Partial | g5-decimal-write | Vocabulary not assessed — WP10 |
| QC-055 | Vocabulaire Millième Symbole Notation décimale | `· · · · A M` | Covered | g5-decimal-write (hard) |  |
| | **Sens et écriture des nombres / D. Nombres entiers** | | | | |
| QC-056 | 1. Représenter des nombres entiers de différentes façons (concrètes ou imagées) (ex. : jetons de deux couleurs différentes, droite numérique… | `· · · A A M` | Decision needed | — | Conflicts with the "no negatives" rule — WP9 |
| QC-057 | 2. Lire et écrire des nombres entiers | `· · · · A M` | Decision needed | — | WP9 |
| QC-058 | 3. Situer des nombres entiers sur un axe de nombres (droite numérique, plan cartésien) | `· · · · A M` | Decision needed | cartesian-coord (1st quadrant only) | WP9 |
| QC-059 | 4. Comparer entre eux des nombres entiers | `· · · · A M` | Decision needed | g5-temperature (positive only) | WP9 |
| QC-060 | 5. Ordonner des nombres entiers par ordre croissant ou décroissant | `· · · · A M` | Decision needed | — | WP9 |
| QC-061 | Vocabulaire Nombre entier Nombre négatif, nombre positif Symboles Notation d’un nombre entier, touche +/– sur la calculatrice | `· · · · A M` | Decision needed | — | WP9 |
| | **Sens des opérations / A. Nombres naturels inférieurs à…** | | | | |
| QC-062 | 1. Reconnaître l’opération ou les opérations à effectuer dans une situation | `A M A M A M` | Covered | choose-operation, multiply-context, word-problem | Add G1–2 range — WP1 |
| QC-063 | 2. Traduire une situation à l’aide de matériel concret, de schémas ou d’équations et vice versa (exploitation des différents sens de l’addit… | `A M A M A M` | Partial | word-problem, missing-addend (resolution) | Meanings of +/− (join, separate, compare) not distinguished; no schemas — WP4 |
| QC-064 | 2. Traduire une situation à l’aide de matériel concret, de schémas ou d’équations et vice versa (exploitation des différents sens de l’addit… | `· · A M A M` | Partial | word-problem | Same as above — WP4 |
| QC-065 | 2. Traduire une situation à l’aide de matériel concret, de schémas ou d’équations et vice versa (exploitation des différents sens de l’addit… | `· · · · A M` | Partial | g6-comparative-phrase | Comparison meaning only — WP4 |
| QC-066 | 3. Traduire une situation à l’aide de matériel concret, de schémas ou d’équations et vice versa (exploitation des différents sens de la mult… | `A M · · · ·` | Missing | — | G1–2 equal groups / sharing pictures — WP1 |
| QC-067 | 3. Traduire une situation à l’aide de matériel concret, de schémas ou d’équations et vice versa (exploitation des différents sens de la mult… | `· · A M A M` | Covered | multiply-context, repeated-addition, division-sharing | Add "how many groups" division and arrays — WP4 |
| QC-068 | 4. Établir la relation d’égalité entre des expressions numériques (ex. : 3 + 2 = 6 – 1) | `A M A M A M` | Missing | — | True/false equalities (3 + 2 = 6 − 1) — WP4 |
| QC-069 | 5. Déterminer des équivalences numériques à l’aide de relations entre / a. les opérations (addition et soustraction) et la commutativité de… | `A M · · · ·` | Partial | fact-family | Multiplication only; need +/− fact families — WP4 |
| QC-070 | 5. Déterminer des équivalences numériques à l’aide de relations entre / b. les opérations (les 4 opérations), la commutativité de l’addition… | `· · A M · ·` | Partial | fact-family | No commutativity/associativity items — WP4 |
| QC-071 | 5. Déterminer des équivalences numériques à l’aide de relations entre / c. les opérations (les 4 opérations), la commutativité de l’addition… | `· · · · A M` | Missing | — | Distributivity (7 × 12 = 7 × 10 + 7 × 2) — WP4 |
| QC-072 | 6. Traduire une situation à l’aide d’une chaîne d’opérations en respectant la priorité des opérations | `· · · · A M` | Partial | g5-decimal-mult (resolution: "one expression") | Need "pick the expression for this story" — WP4 |
| QC-073 | Vocabulaire Plus, moins, de moins, de plus Addition, soustraction, somme, différence Symboles +, – | `A M R R R R` | Partial | choose-operation | Vocabulary not assessed — WP10 |
| QC-074 | Vocabulaire Au moins, au plus, terme, terme manquant Multiplication, facteur, produit Division, diviseur, dividende, quotient, reste, partag… | `· · A M R R` | Partial | fact-family | Factor/product/quotient/remainder vocabulary — WP10 |
| | **Sens des opérations / B. Nombres décimaux jusqu’à l’ordre des…** | | | | |
| QC-075 | 1. Traduire une situation à l’aide de matériel concret, de schémas ou d’équations et vice versa (exploitation des différents sens de l’addit… | `· · A M A M` | Partial | g5 resolution (money) | Decimal +/− stories not a dedicated skill — WP3 |
| QC-076 | 1. Traduire une situation à l’aide de matériel concret, de schémas ou d’équations et vice versa (exploitation des différents sens de l’addit… | `· · A M A M` | Partial | g5 resolution (money) | WP3 |
| QC-077 | 1. Traduire une situation à l’aide de matériel concret, de schémas ou d’équations et vice versa (exploitation des différents sens de l’addit… | `· · · · A M` | Partial | g5 resolution (money) | WP3 |
| QC-078 | 2. Traduire une situation à l’aide de matériel concret, de schémas ou d’équations et vice versa (exploitation des différents sens de la mult… | `· · A M A M` | Partial | g5-order-ops resolution (unit price) | WP3 |
| QC-079 | 3. Déterminer des équivalences numériques à l’aide / a. de la relation entre les opérations (addition et soustraction), la commutativité de… | `· · A M · ·` | Missing | — | Decimal equivalences via properties — WP3 |
| QC-080 | 3. Déterminer des équivalences numériques à l’aide / b. des relations entre les opérations (les 4 opérations), la commutativité de l’additio… | `· · · · A M` | Missing | — | WP3 |
| QC-081 | 4. Traduire une situation à l’aide d’une chaîne d’opérations en respectant la priorité des opérations | `· · · · A M` | Partial | g5-order-ops | Natural numbers only — WP3 |
| | **Sens des opérations / C. Fractions** | | | | |
| QC-082 | 1. Traduire une situation à l’aide de matériel concret, de schémas ou par une opération et vice versa (exploitation des différents sens de l… | `· · · · A M` | Partial | fraction-shape/-collection resolution | Stories of a fraction of a quantity only — WP2 |
| | **Calcul / A. Nombres naturels (selon les balises de chaque cycle)** | | | | |
| QC-083 | 1. Faire une approximation du résultat / a. d’une addition ou d’une soustraction de nombres naturels | `A M R R R R` | Partial | round-ten/round-hundred resolution | No "estimate this sum" item — WP4 |
| QC-084 | 1. Faire une approximation du résultat / b. de l’une ou l’autre des opérations sur des nombres naturels | `· · A A A M` | Partial | g6-estimate-product, g6-rate-problem | No division estimate — WP4 |
| QC-085 | 2. Développer le répertoire mémorisé de l’addition et de la soustraction / a. Construire les faits numériques de l’addition (0 + 0 à 10 + 10… | `A M · · · ·` | Partial | add/subtract (easy) | Not restricted to 0+0…10+10; no G1–2 fact skill — WP1 |
| QC-086 | 2. Développer le répertoire mémorisé de l’addition et de la soustraction / b. Développer diverses stratégies favorisant la maîtrise des fait… | `A A M R R R` | Missing | — | Strategies (doubles, make-10) — WP1 |
| QC-087 | 2. Développer le répertoire mémorisé de l’addition et de la soustraction / c. Maîtriser l’ensemble des faits numériques de l’addition (0 + 0… | `A A M R R R` | Partial | add/subtract (easy) | No timed fluency mode — WP4 |
| QC-088 | 3. Développer des processus de calcul mental / a. À l’aide de processus personnels, déterminer la somme ou la différence de deux nombres nat… | `A M R R R R` | Partial | add/subtract | Multiple choice; no mental-math framing — WP0/WP4 |
| QC-089 | 3. Développer des processus de calcul mental / b. À l’aide de processus personnels, déterminer le produit ou le quotient de deux nombres nat… | `· · A A A M` | Partial | multiply/divide | Multiple choice — WP0 |
| QC-090 | 4. Développer des processus de calcul écrit (addition et soustraction) / a. À l’aide de processus personnels, en utilisant du matériel ou de… | `A M · · · ·` | Missing | — | G1–2 add/sub with drawings (number line, base-10) — WP1 |
| QC-091 | 4. Développer des processus de calcul écrit (addition et soustraction) / b. À l’aide de processus conventionnels, déterminer la somme de deu… | `· · A M R R` | Partial | add (hard) | Multiple choice; no column layout — WP0/WP4 |
| QC-092 | 4. Développer des processus de calcul écrit (addition et soustraction) / c. À l’aide de processus conventionnels, déterminer la différence d… | `· · A M R R` | Partial | subtract (hard) | Multiple choice; no column layout — WP0/WP4 |
| QC-093 | 5. Déterminer un terme manquant dans une équation (relations entre les opérations) : a + b = □, a + □ = c, □ + b = c, a – b = □, a – □ = c,… | `A M R R R R` | Covered | missing-addend, missing-subtrahend | Lacks □ + b = c and □ − b = c forms — WP4 |
| QC-094 | 6. Développer le répertoire mémorisé de la multiplication et de la division / a. Construire les faits numériques de la multiplication (0 × 0… | `· · A M · ·` | Partial | multiply/divide (easy), fact-family | Not restricted to 0×0…10×10 tables — WP4 |
| QC-095 | 6. Développer le répertoire mémorisé de la multiplication et de la division / b. Développer diverses stratégies favorisant la maîtrise des f… | `· · A A M R` | Missing | — | Multiplication strategies (doubling, ×5 = ×10 ÷ 2) — WP4 |
| QC-096 | 6. Développer le répertoire mémorisé de la multiplication et de la division / c. Maîtriser l’ensemble des faits numériques de la multiplicat… | `· · A A M R` | Partial | multiply (easy) | No timed tables mode — WP4 |
| QC-097 | 7. Développer des processus de calcul écrit (multiplication et division) / a. À l’aide de processus personnels, en utilisant du matériel ou… | `· · A M · ·` | Partial | repeated-addition, division-sharing | No arrays/drawings — WP4 |
| QC-098 | 7. Développer des processus de calcul écrit (multiplication et division) / b. À l’aide de processus conventionnels, déterminer le produit d’… | `· · · · A M` | Covered | g6-multiply, g6-partial-products |  |
| QC-099 | 7. Développer des processus de calcul écrit (multiplication et division) / c. À l’aide de processus conventionnels, déterminer le quotient d… | `· · · · A M` | Partial | divide (hard) | Multiple choice; no long-division steps; remainders only in resolution — WP4 |
| QC-100 | 8. Déterminer un terme manquant dans une équation (relations entre les opérations) : a × b = □, a × □ = c, □ × b = c, a ÷ b = □, a ÷ □ = c,… | `· · A A A M` | Missing | — | Missing factor/divisor (a × □ = c) — WP4 |
| QC-101 | 9. Décomposer un nombre en facteurs premiers | `· · · A A M` | Missing | — | Prime factorisation (factor tree) — WP4 |
| QC-102 | 10. Calculer la puissance d’un nombre | `· · · · A M` | Partial | squares (N²) | No powers beyond squares — WP4 |
| QC-103 | 11. Déterminer la divisibilité d’un nombre par 2, 3, 4, 5, 6, 8, 9, 10 | `· · · · A M` | Missing | — | Divisibility by 2, 3, 4, 5, 6, 8, 9, 10 — WP4 |
| QC-104 | 12. Effectuer une chaîne d’opérations en respectant la priorité des opérations | `· · · · A M` | Covered | g5-order-ops |  |
| QC-105 | 13. Décrire, dans ses mots et à l’aide du langage mathématique propre à son cycle, / a. des régularités non numériques (ex. : suite de coule… | `A M R R R R` | Missing | — | Non-numeric patterns (shapes/colours) — WP1 |
| QC-106 | 13. Décrire, dans ses mots et à l’aide du langage mathématique propre à son cycle, / b. des régularités numériques (ex. : comptine des nombr… | `A M R R R R` | Covered | number-sequence, g4-skip-sequence |  |
| QC-107 | 13. Décrire, dans ses mots et à l’aide du langage mathématique propre à son cycle, / c. des suites de nombres et famille d’opérations | `A A A A A M` | Partial | number-sequence | Only +/− constant steps; no ×2, square or triangular sequences — WP4 |
| QC-108 | 14. Ajouter de nouveaux termes à une suite dont au moins les 3 premiers termes sont donnés | `A A A A A M` | Covered | number-sequence, g4-skip-sequence |  |
| QC-109 | 15. Utiliser la calculatrice en / a. s’appropriant les fonctions simples de la calculatrice (+, –, =, touches numériques de 0 à 9, touches d… | `A M R R R R` | Off-screen | — | Calculator use — out of scope (optional on-screen calculator) |
| QC-110 | 15. Utiliser la calculatrice en / b. s’appropriant les fonctions × et ÷ de la calculatrice | `· · A M R R` | Off-screen | — | Calculator |
| QC-111 | 15. Utiliser la calculatrice en / c. s’appropriant les touches pour les mémoires et pour le changement de signe (+/–) | `· · · · A M` | Off-screen | — | Calculator |
| QC-112 | Vocabulaire Régularité, suite Symboles Touches de la calculatrice | `A M R R R R` | Partial | number-sequence | Vocabulary — WP10 |
| | **Calcul / B. Fractions (à l’aide de matériel concret ou de schémas)** | | | | |
| QC-113 | 1. Construire un ensemble de fractions équivalentes | `· · A A A M` | Missing | — | Build equivalent fractions — WP2 |
| QC-114 | 2. Réduire une fraction à sa plus simple expression | `· · · · A M` | Missing | — | Simplify a fraction (dedicated skill) — WP2 |
| QC-115 | 3. Additionner et soustraire des fractions dont le dénominateur de l’une est un multiple de l’autre | `· · · · A M` | Partial | fraction-add, fraction-subtract | Generators exceed scope (unrelated denominators); need a scoped G6 skill — WP2 |
| QC-116 | 4. Multiplier un nombre naturel par une fraction | `· · · · A M` | Missing | fraction-multiply is fraction × fraction | Whole number × fraction (3 × 2/5, ⅓ of 12) — WP2 |
| QC-117 | Vocabulaire Fraction irréductible | `· · · · A M` | Missing | — | Simplest-form vocabulary — WP2 |
| | **Calcul / C. Nombres décimaux** | | | | |
| QC-118 | 1. Faire une approximation / a. du résultat d’une addition ou d’une soustraction | `· · A A A M` | Missing | — | Estimate a decimal sum/difference — WP3 |
| QC-119 | 1. Faire une approximation / b. du résultat d’une multiplication ou d’une division | `· · · · A M` | Missing | — | Estimate a decimal product/quotient — WP3 |
| QC-120 | 2. Développer des processus de calcul mental / a. Additionner et soustraire des nombres décimaux | `· · A A A M` | Partial | decimal-add, decimal-subtract | Multiple choice — WP0 |
| QC-121 | 2. Développer des processus de calcul mental / b. Effectuer des opérations sur des nombres décimaux (multiplication, division par un nombre… | `· · · · A M` | Partial | g5-decimal-mult, g5-decimal-div |  |
| QC-122 | 2. Développer des processus de calcul mental / c. Multiplier et diviser par 10, 100, 1000 | `· · · · A M` | Partial | decimal-divide (÷10) | No ×10/100/1000 or ÷100/1000 skill — WP3 |
| QC-123 | 3. Développer des processus de calcul écrit / a. Additionner et soustraire des nombres décimaux dont le résultat ne dépasse pas la position… | `· · A M R R` | Covered | decimal-add, decimal-subtract | Switch to typed answers — WP0 |
| QC-124 | 3. Développer des processus de calcul écrit / b. Multiplier des nombres décimaux dont le produit ne dépasse pas la position des centièmes | `· · · · A M` | Partial | decimal-multiply | Hard goes to thousandths (out of scope); g5-decimal-mult covers decimal × whole only — WP0/WP3 |
| QC-125 | 3. Développer des processus de calcul écrit / c. Diviser un nombre décimal par un nombre naturel inférieur à 11 | `· · · · A M` | Covered | g5-decimal-div, decimal-divide |  |
| QC-126 | Symboles $, ¢ | `· · A M R R` | Covered | money-change, money-match |  |
| | **Calcul / D. Utilisation des nombres** | | | | |
| QC-127 | 1. Exprimer en notation fractionnaire un nombre exprimé en notation décimale et vice versa | `· · · · A M` | Partial | fraction-to-decimal, g5-decimal-forms | Decimal → fraction direction weak — WP3 |
| QC-128 | 2. Exprimer par un pourcentage un nombre exprimé en notation décimale et vice versa | `· · · · A M` | Partial | g5-probability-forms | Only as matching inside probability — WP3 |
| QC-129 | 3. Exprimer par un pourcentage un nombre exprimé en notation fractionnaire et vice versa | `· · · · A M` | Partial | g5-probability-forms | WP3 |
| QC-130 | 4. Choisir une forme d’écriture appropriée selon le contexte | `· · · · A M` | Missing | — | Choose the right notation for the context — WP3 |
| QC-131 | Vocabulaire Pourcentage Symbole % | `· · · · A M` | Partial | g5-pie-chart | Percentage never taught on its own — WP3 |
| | **Géométrie / A. Espace** | | | | |
| QC-132 | 1. Se repérer et repérer des objets dans l’espace (relations spatiales) | `A M · · · ·` | Missing | — | Spatial relations (left/right, above/below) — WP5 |
| QC-133 | 2. Effectuer des activités de repérage dans un plan | `A A A M · ·` | Missing | — | Locate on a map/grid (B3, routes) — WP5 |
| QC-134 | 3. Effectuer des activités de repérage sur un axe (selon les types de nombres à l’étude) | `A M A M A M` | Covered | g4-number-line-point, g5-number-line, g6-fraction-on-line |  |
| QC-135 | 4. Repérer des points dans le plan cartésien / a. dans le 1er quadrant | `A A A M · ·` | Covered | cartesian-coord | Ask to place a point too, not only read — WP5 |
| QC-136 | 4. Repérer des points dans le plan cartésien / b. dans les 4 quadrants | `· · · · A M` | Decision needed | — | Four quadrants need negatives — WP9 |
| QC-137 | Vocabulaire Système de repérage, plan, plan cartésien, couple | `A A A M R R` | Partial | cartesian-coord | WP10 |
| QC-138 | Symboles Écriture d’un couple (a, b) | `A A A A A M` | Covered | cartesian-coord (hard) |  |
| | **Géométrie / B. Solides** | | | | |
| QC-139 | 1. Comparer des objets ou des parties d’objets de l’environnement aux solides à l’étude (boule, cône, cube, cylindre, prisme, pyramide) | `A M R R R R` | Missing | — | Match everyday objects to solids (ball → sphere) — WP5 |
| QC-140 | 2. Comparer et construire des solides (boule, cône, cube, cylindre, prisme, pyramide) | `A M · · · ·` | Off-screen | — | Building solids is physical; offer a guided activity |
| QC-141 | 3. Identifier les principaux solides (boule, cône, cube, cylindre, prisme, pyramide) | `A M R R R R` | Partial | identify-solid | Matches text descriptions; no pictures of the solids — WP5 |
| QC-142 | Vocabulaire Solide, base d’un solide, face, surface plane, surface courbe Boule, cône, cube, cylindre, prisme, pyramide | `A M R R R R` | Partial | identify-solid | Flat/curved surface vocabulary — WP5 |
| QC-143 | 4. Identifier et représenter les différentes faces d’un prisme ou d’une pyramide | `A M R R R R` | Partial | identify-solid, g5-solid-counts | No "which faces does this prism have" item — WP5 |
| QC-144 | 5. Décrire des prismes et des pyramides à l’aide de faces, de sommets, d’arêtes | `· · A M R R` | Covered | identify-solid, g5-solid-counts |  |
| QC-145 | 6. Classifier des prismes et des pyramides | `· · A M R R` | Missing | — | Classify prisms vs pyramids — WP5 |
| QC-146 | 7. Développer un prisme ou une pyramide | `· · A M R R` | Missing | — | Nets — WP5 |
| QC-147 | 8. Associer le développement de la surface / a. d’un prisme au prisme correspondant et vice versa | `· A A M · ·` | Missing | — | Match prism ↔ net — WP5 |
| QC-148 | 8. Associer le développement de la surface / b. d’une pyramide à la pyramide correspondante et vice versa | `· A A M · ·` | Missing | — | Match pyramid ↔ net — WP5 |
| QC-149 | 8. Associer le développement de la surface / c. d’un polyèdre convexe au polyèdre convexe correspondant | `· · · · A M` | Missing | — | Convex polyhedron ↔ net — WP5 |
| QC-150 | Vocabulaire Sommet, arête, développement d’un solide | `· · A M R R` | Partial | g5-solid-counts | Net vocabulary missing — WP5 |
| QC-151 | 9. Expérimenter la relation d’Euler sur des polyèdres convexes | `· · · · A M` | Covered | g5-euler |  |
| QC-152 | Vocabulaire Polyèdre, polyèdre convexe | `· · · · A M` | Partial | g5-euler | Polyhedron/convex not taught — WP5 |
| | **Géométrie / C. Figures planes** | | | | |
| QC-153 | 1. Comparer et construire des figures composées de lignes courbes fermées ou de lignes brisées fermées | `A M · · · ·` | Missing | — | Open/closed, curved/broken lines — WP1 |
| QC-154 | 2. Identifier des figures planes : carré, rectangle, triangle, losange, cercle | `A M R R R R` | Partial | name-polygon, g4-quadrilateral-name | No circle or rhombus at G1–2 level — WP1 |
| QC-155 | 3. Décrire des figures planes : carré, rectangle, triangle, losange | `A M R R R R` | Covered | g4-quadrilateral-riddle, count-sides |  |
| QC-156 | Vocabulaire Ligne brisée, ligne brisée fermée, ligne courbe Figure plane, côté Carré, cercle, rectangle, triangle, losange | `A M R R R R` | Partial | name-polygon | WP10 |
| QC-157 | 4. Décrire des polygones convexes et non convexes | `· · A M R R` | Missing | — | Convex / non-convex polygons — WP5 |
| QC-158 | 5. Identifier et construire des droites parallèles et des droites perpendiculaires | `· · A M R R` | Covered | parallel-perp, g4-lines | Identify only (construction off-screen) |
| QC-159 | 6. Décrire des quadrilatères (parallélisme, perpendicularité, angle droit, angle aigu, angle obtus, etc.) | `· · A M R R` | Covered | g4-quadrilateral-riddle, g4-quadrilateral-count, g4-quadrilateral-match |  |
| QC-160 | 7. Classifier des quadrilatères | `· · A M R R` | Covered | g4-quadrilateral-name, g4-quadrilateral-match |  |
| QC-161 | Vocabulaire Quadrilatère, parallélogramme, trapèze, polygone Polygone convexe, polygone non convexe, segment Est parallèle à; est perpendicu… | `· · A M R R` | Partial | g4-quadrilateral-* | No ⊥ // symbols — WP10 |
| QC-162 | 8. Décrire des triangles : triangle scalène, triangle rectangle, triangle isocèle, triangle équilatéral | `· · · · A M` | Missing | — | Triangles: scalene/isosceles/equilateral/right — WP5 |
| QC-163 | 9. Classifier des triangles | `· · · · A M` | Missing | — | Classify triangles — WP5 |
| QC-164 | 10. Décrire le cercle | `· · · · A M` | Missing | — | Circle: radius, diameter, circumference, central angle — WP5 |
| QC-165 | Vocabulaire Triangle équilatéral, triangle isocèle, triangle rectangle, triangle scalène Disque, angle au centre, diamètre, rayon, circonfér… | `· · · · A M` | Missing | — | WP5 |
| | **Géométrie / D. Frises et dallages** | | | | |
| QC-166 | 1. Identifier des figures isométriques | `A M R R R R` | Missing | — | Congruent (isometric) figures — WP5 |
| QC-167 | 2. Observer et produire des régularités à l’aide de figures géométriques | `A A A M · ·` | Missing | — | Geometric patterns — WP1/WP5 |
| QC-168 | 3. Observer et produire des frises et des dallages / a. à l’aide de la réflexion | `· · A M R R` | Missing | — | Reflection / line of symmetry — WP5 |
| QC-169 | 3. Observer et produire des frises et des dallages / b. à l’aide de la translation | `· · · · A M` | Missing | — | Translation — WP5 |
| QC-170 | Vocabulaire Frise, dallage Réflexion, axe de réflexion, figure symétrique | `· · A M R R` | Missing | — | WP5 |
| QC-171 | Vocabulaire Translation, flèche de translation | `· · · · A M` | Missing | — | WP5 |
| | **Mesure / A. Longueurs** | | | | |
| QC-172 | 1. Comparer des longueurs | `A M · · · ·` | Missing | — | Compare lengths (pictures) — WP1 |
| QC-173 | 2. Construire des règles | `A M · · · ·` | Off-screen | — | Building rulers is physical |
| QC-174 | 3. Estimer et mesurer les dimensions d’un objet à l’aide d’unités non conventionnelles | `A M · · · ·` | Missing | — | Measure with non-standard units (paper clips) — WP1 |
| QC-175 | 4. Estimer et mesurer les dimensions d’un objet à l’aide d’unités conventionnelles / a. mètre, décimètre et centimètre | `A M · · · ·` | Missing | — | Read a ruler (cm) — WP6 |
| QC-176 | 4. Estimer et mesurer les dimensions d’un objet à l’aide d’unités conventionnelles / b. mètre, décimètre, centimètre et millimètre | `· · A M · ·` | Missing | measure-unit (choose unit) | Read a ruler in mm — WP6 |
| QC-177 | 4. Estimer et mesurer les dimensions d’un objet à l’aide d’unités conventionnelles / c. mètre, décimètre, centimètre, millimètre et kilomètr… | `· · · · A M` | Partial | measure-unit | Estimating km — WP6 |
| QC-178 | 5. Établir des relations entre les unités de mesure de longueur / a. mètre, décimètre, centimètre et millimètre | `· · A M · ·` | Covered | convert-length | Generic skill includes units outside the list — WP0 |
| QC-179 | 5. Établir des relations entre les unités de mesure de longueur / b. mètre, décimètre, centimètre, millimètre et kilomètre | `· · · · A M` | Covered | convert-length |  |
| QC-180 | 6. Calculer le périmètre de figures planes | `· · A M R R` | Covered | perimeter-labeled, geometry-perimeter |  |
| QC-181 | Vocabulaire Largeur, longueur, hauteur, profondeur Unité de mesure, centimètre, décimètre, mètre Symboles m, dm, cm | `A M R R R R` | Partial | measure-unit | WP10 |
| QC-182 | Vocabulaire Périmètre, millimètre Symbole mm | `· · A M R R` | Covered | perimeter-labeled, convert-length |  |
| QC-183 | Vocabulaire Kilomètre Symbole km | `· · · · A M` | Covered | measure-unit, convert-length |  |
| | **Mesure / B. Surfaces** | | | | |
| QC-184 | 1. Estimer et mesurer l’aire de surfaces / a. à l’aide d’unités non conventionnelles | `· · A M · ·` | Missing | — | Area by counting squares — WP6 |
| QC-185 | 1. Estimer et mesurer l’aire de surfaces / b. à l’aide d’unités conventionnelles | `· · · · A M` | Partial | geometry-area | Formula only, unitless; no cm²/m² — WP6 |
| QC-186 | Vocabulaire Surface, aire | `· · A M R R` | Partial | geometry-area | WP10 |
| QC-187 | Vocabulaire Centimètre carré, décimètre carré, mètre carré Symboles m2, dm2, cm2 | `· · · · A M` | Missing | — | cm², dm², m² — WP6 |
| | **Mesure / C. Volumes** | | | | |
| QC-188 | 1. Estimer et mesurer des volumes / a. à l’aide d’unités non conventionnelles | `· · A M · ·` | Missing | — | Volume by counting cubes — WP6 |
| QC-189 | 1. Estimer et mesurer des volumes / b. à l’aide d’unités conventionnelles | `· · · · A M` | Covered | g5-volume |  |
| QC-190 | Vocabulaire Volume | `· · A M R R` | Covered | g5-volume |  |
| QC-191 | Vocabulaire Centimètre cube, décimètre cube, mètre cube Symboles m3, dm3, cm3 | `· · · · A M` | Partial | g5-volume | No dm³ or cm³ ↔ L — WP6 |
| | **Mesure / D. Angles** | | | | |
| QC-192 | 1. Comparer des angles | `· · A M R R` | Partial | identify-angle | Classifies one angle; no comparing two — WP6 |
| QC-193 | Vocabulaire Angle, angle droit, angle aigu, angle obtus | `· · A M R R` | Covered | identify-angle |  |
| QC-194 | 2. Estimer et mesurer des angles en degrés | `· · · · A M` | Missing | — | Estimate/measure angles in degrees (on-screen protractor) — WP6 |
| QC-195 | Vocabulaire Degré, rapporteur d’angles Symboles ∠, ° | `· · · · A M` | Missing | — | WP6 |
| | **Mesure / E. Capacités** | | | | |
| QC-196 | 1. Estimer et mesurer des capacités à l’aide d’unités non conventionnelles | `· · A A M R` | Missing | — | Non-standard capacity (how many cups fill the jug) — WP6 |
| QC-197 | 2. Estimer et mesurer des capacités à l’aide d’unités conventionnelles | `· · A A M R` | Partial | unit-by-quantity | Unit choice only; no estimating amounts — WP6 |
| QC-198 | 3. Établir des relations entre les unités de mesure (ex. : 1 L = 1000 mL, ½ L = 500 mL) | `· · · · M R` | Covered | g5-capacity-convert, convert-volume |  |
| QC-199 | Vocabulaire Capacité, litre, millilitre | `· · · A M R` | Covered | unit-by-quantity, g5-capacity-convert |  |
| | **Mesure / F. Masses** | | | | |
| QC-200 | 1. Estimer et mesurer des masses à l’aide d’unités non conventionnelles | `· · A A A M` | Missing | — | Balance scales — WP6 |
| QC-201 | 2. Estimer et mesurer des masses à l’aide d’unités conventionnelles | `· · A A A M` | Partial | unit-by-quantity | No estimating or reading a scale — WP6 |
| QC-202 | 3. Établir des relations entre les unités de mesure (ex. : 1 kg = 1000 g, ½ kg = 500 g) | `· · · · A M` | Covered | g5-mass-convert, convert-mass |  |
| QC-203 | Vocabulaire Masse, gramme, kilogramme Symboles g, kg | `· · · · A M` | Covered | g5-mass-convert |  |
| | **Mesure / G. Temps** | | | | |
| QC-204 | 1. Estimer et mesurer le temps à l’aide d’unités conventionnelles | `A A A M R R` | Covered | read-clock, g4-elapsed-time, g4-end-time, clock skills | No G1–2 o’clock/half-past skill — WP1 |
| QC-205 | 2. Établir des relations entre les unités de mesure | `A A A A A M` | Covered | time-convert, g4-time-units |  |
| QC-206 | Vocabulaire Jour, heure, minute, seconde Symboles h, min, s, codage de l’heure : 3 h, 3 h 25 min, 03 : 25 | `A M R R R R` | Covered | read-clock, g4-clock-24h |  |
| QC-207 | Vocabulaire Cycle quotidien, cycle hebdomadaire, cycle annuel | `A A A M R R` | Partial | time-convert | No calendar, days of the week, months or seasons — WP1/WP6 |
| | **Mesure / H. Températures** | | | | |
| QC-208 | 1. Estimer et mesurer des températures à l’aide d’unités conventionnelles | `A A A A A M` | Partial | g5-thermometer, g5-temperature | Positive only (see WP9); nothing below G5 — WP6 |
| QC-209 | Vocabulaire Degré Celsius Symbole °C | `A M R R R R` | Covered | g5-thermometer |  |
| | **Statistique /** | | | | |
| QC-210 | 1. Formuler des questions d’enquête (selon les sujets appropriés à la maturité de l’élève, l’évolution des apprentissages en français, etc.) | `A A A A A M` | Missing | — | Pick a good survey question — WP7 |
| QC-211 | 2. Collecter, décrire et organiser des données (classifier ou catégoriser) à l’aide de tableaux | `A A A A A M` | Partial | g5-data-table | Read only; no tallying/organising — WP7 |
| QC-212 | 3. Interpréter des données à l’aide / a. d’un tableau, d’un diagramme à bandes et d’un diagramme à pictogrammes | `A M · · · ·` | Partial | read-bar-chart | No pictograph — WP7 |
| QC-213 | 3. Interpréter des données à l’aide / b. d’un tableau, d’un diagramme à bandes, d’un diagramme à pictogrammes et d’un diagramme à ligne bris… | `· · A M · ·` | Missing | — | Line graph — WP7 |
| QC-214 | 3. Interpréter des données à l’aide / c. d’un tableau, d’un diagramme à bandes, d’un diagramme à pictogrammes, d’un diagramme à ligne brisée… | `· · · · A M` | Covered | g5-pie-chart, read-bar-chart, g5-data-table |  |
| QC-215 | 4. Représenter des données à l’aide / a. d’un tableau, d’un diagramme à bandes, d’un diagramme à pictogrammes | `A M · · · ·` | Missing | — | Build a bar chart/pictograph (interactive) — WP7 |
| QC-216 | 4. Représenter des données à l’aide / b. d’un tableau, d’un diagramme à bandes, d’un diagramme à pictogrammes et d’un diagramme à ligne bris… | `· · A M R R` | Missing | — | Build bar chart/line graph — WP7 |
| QC-217 | 5. Comprendre et calculer la moyenne arithmétique | `· · · · A M` | Covered | g5-arithmetic-mean |  |
| QC-218 | Vocabulaire Enquête, tableau Diagramme à bandes, diagramme à pictogrammes | `M R R R R R` | Partial | read-bar-chart | WP10 |
| QC-219 | Vocabulaire Diagramme à ligne brisée | `· · A M R R` | Missing | — | WP7 |
| QC-220 | Vocabulaire Diagramme circulaire, moyenne arithmétique | `· · · · A M` | Covered | g5-pie-chart, g5-arithmetic-mean |  |
| | **Probabilité /** | | | | |
| QC-221 | 1. Reconnaître, quand elle s’applique, la variabilité des résultats possibles (incertitude) | `A A A A A M` | Missing | — | Variability of outcomes — WP8 |
| QC-222 | 2. Reconnaître, quand elle s’applique, l’équiprobabilité (ex. : quantité, symétrie d’un objet [cube]) | `A A A A A M` | Missing | — | Equally likely (fair die, spinner) — WP8 |
| QC-223 | 3. Prendre conscience, quand elle s’applique, de l’indépendance entre les tours lors d’une expérimentation | `A A A A A M` | Missing | — | Independence of trials ("after 3 heads…") — WP8 |
| QC-224 | 4. Expérimenter des activités liées au hasard en utilisant du matériel varié (ex. : roulettes, prismes à base rectangulaire, verres, billes,… | `A A A A A M` | Missing | — | Virtual experiments (dice, spinners) — WP8 |
| QC-225 | 5. Prédire qualitativement un résultat ou plusieurs événements en utilisant, entre autres, une droite des probabilités / a. résultat certain… | `A A A A A M` | Covered | probability-vocab |  |
| QC-226 | 5. Prédire qualitativement un résultat ou plusieurs événements en utilisant, entre autres, une droite des probabilités / b. événement plus p… | `· · A A A M` | Partial | probability-vocab | No "equally likely" or comparing two events — WP8 |
| QC-227 | 6. Distinguer la prédiction du résultat obtenu | `A A A A A M` | Missing | — | Prediction vs result — WP8 |
| QC-228 | 7. Utiliser des tableaux ou des diagrammes pour colliger et mettre en évidence les résultats de l’expérimentation | `A A A A A M` | Missing | — | Record results in a table — WP8 |
| QC-229 | 8. Dénombrer les résultats possibles / a. d’une expérience aléatoire simple | `A M · · · ·` | Partial | g5-count-outcomes | G5 only; G1–2 simple listing missing — WP8 |
| QC-230 | 8. Dénombrer les résultats possibles / b. d’une expérience aléatoire à l’aide d’un tableau, d’un diagramme en arbre | `· · A A A M` | Partial | g5-count-outcomes | Multiplication only; no tree diagram picture — WP8 |
| QC-231 | 9. Comparer qualitativement la probabilité théorique ou fréquentielle que des événements se produisent | `· · A A A M` | Missing | — | Theoretical vs experimental probability — WP8 |
| QC-232 | 10. Reconnaître qu’une probabilité se situe entre 0 et 1 | `· · · · A M` | Partial | g5-probability-frac | No 0–1 probability line — WP8 |
| QC-233 | 11. Utiliser la notation fractionnaire, la notation décimale ou le pourcentage pour quantifier une probabilité | `· · · · A M` | Covered | g5-probability-frac, g5-probability-forms |  |
| QC-234 | 12. Comparer des résultats d’une expérience aléatoire aux résultats théoriques connus | `· · · · A M` | Missing | — | Compare experiment with theory — WP8 |
| QC-235 | 13. Simuler des expériences aléatoires avec ou sans l’aide de la technologie | `· · A A A M` | Missing | — | Simulation — WP8 |
| QC-236 | Vocabulaire Hasard, expérience aléatoire, chance, dénombrement, diagramme en arbre Résultat certain, résultat possible, résultat impossible… | `A A A M R R` | Partial | probability-vocab | WP10 |
