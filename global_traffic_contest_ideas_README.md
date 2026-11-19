# Global Traffic Innovation Contest Ideas (2023–2026)
**Snapshot:** 2026-11-19 · **Language:** Vietnamese · **Coverage:** 121 sourced idea/project entries, 21 competition/program groups, 27 public source pages.

## Files
- `global_traffic_contest_ideas_2023_2026.xlsx` — recommended Excel workbook (10 sheets)
- `global_traffic_contest_ideas_2023_2026.csv` — flat machine-readable 121-row idea table
- `global_traffic_contest_ideas_2023_2026.json` — structured version of the same idea table

## Excel workbook structure
1. `IDEAS`: 121 sourced idea records. The first **23 columns match** the previous Vietnamese contest dataset's names and order, facilitating comparison and joins. Nine additional columns contain international information.
2. `NGUON`: 27 source references (URLs and source notes).
3. `BAO_PHU`: competition/program group coverage.
4. `RUBRIC`: published judging-related information vs **clearly labeled non-official** research rubric; do not confuse.
5. `DATA_DICTIONARY`: definitions and interpretation rules for all columns.
6. `NHAN_DANH`: outcome-label dictionary.
7. `DOI_CHIEU`: within-competition comparisons for studying differences in publicly disclosed outcomes.
8. `CHU_DE_2026`: mapping to Vietnam's 2026 themes (researcher's classification; not organizer-approved).
9. `THONG_KE`: summary formulas; 39 A-priority, 18 B-priority, 64 C-priority records.
10. `FOCUS_15`: 15 prompts for further research, **not validated winning ideas**.

## Outcome labels — treat as distinct
- `AWARDED` = a published award, in the specific competition/program and year.
- `SELECTED_PILOT` = selected for municipal pilot/support (e.g. RAPTOR), **not** ranked national/international first prize.
- `FINALIST_NO_CATEGORY_AWARD` = published finalist not listed as a category awardee in checked award recap; **not** proof of failure or rejection.
- `SHORTLISTED` = named in published shortlist; position/status may remain unknown.
- `RANKED_FINALIST` = named in a ranked/final round but technical description or final award may be unavailable.
- `FINALIST` = reported finalist, no reliably comparable award level.

## Methods and provenance
- Per-record `entry_evidence_url` and, where available, `award_evidence_url` point to contest organizers, government, or reputable coverage.
- `mechanism_evidence` and `evidence_depth` distinguish grounded descriptions from title-only records.
- `similarity_priority_inferred` grades **research priority**: A resembles Vietnamese motorcycle/mixed traffic context or is directly transferable; B selectively transferable; C novelty/variety control. This is a qualitative labeling heuristic, not a measured traffic similarity score.
- Country fields can represent participant/team origin or site of innovation. **Do not** assume all are deployment countries.
- Award labels are observed historical outcomes. They must not be treated as ground-truth measures of innovation quality or as causal features for predicting winners: selection/reporting bias and cross-contest non-comparability are severe.
- `GT-xx` mappings are suggested future joins to Vietnam traffic datasets, not validation against those data.
- Descriptions reproduce **claims made by sources**; phrases like "aims to reduce" are not independently proven impact.
- Do not count omitted entries as rejected. The collection is **not exhaustive** of all applications worldwide, or all finalists in each contest.
- Check licences and privacy constraints prior to downloading/reusing primary traffic data.

## Recommended workflow for research agent
1. Audit sources and re-open URLs; record 404, retractions, corrections, and date of access.
2. Deduplicate repeated products that appear at multiple contests, preserving each separate contest appearance.
3. Build prior-art clusters by *mechanism*, not keywords ("AI", "smart", "traffic").
4. Cross-match clusters against Vietnamese `GT-01` to `GT-22` datasets and identify **empirical** problem evidence.
5. Rank novel research questions by evidence strength, contextual transfer, practical feasibility, and meaningful technical distinction; do not infer judge preferences without judging comments or scores.
6. Use the `DOI_CHIEU` sheet as prompts for **comparative analysis only**, not as evidence of why a team won or lost.

**Critical:** This database includes 2026 projects public before or on 2026-11-19, not all projects from the full 2026 calendar year.
