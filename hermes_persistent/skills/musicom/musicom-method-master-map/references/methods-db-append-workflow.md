# Methods DB Append Workflow

## Context
The methods database lives at `/opt/data/projects/Research/CompositionMethods/methods_db.md` (4500+ lines). The daily research cron job appends one new method per run.

## Append Procedure
1. **Find last method number**: Read the master summary table (lines 9-55) to find the highest method ID. The table row format is `| **NNN** | Method Name | ...`.
2. **Read end of file**: Read last ~10 lines to confirm append point (after last detailed method section).
3. **Append detailed section**: Add full method documentation with these required sections:
   - `### **Source**` — origin/derivation of the method
   - `### **Description**` — what the method does
   - `### **Musical Elements Framework**` — PITCH, RHYTHM, HARMONY, STRUCTURE, TEXTURE
   - `### **UnitMatrix Integration (Voices & Sections)**` — Rows, Columns, Cells, Mapping Flow
   - `### **Pitfalls**` — numbered list of known issues
4. **Update master summary table**: Add a new row to the table at the top with all classification columns filled.
5. **Write standalone file**: Save full write-up (with Python implementation, extended math, references) to `/opt/data/projects/Research/CompositionMethods/method_NNN_<acronym>.md`

## Cron Delivery Pitfall
`hermes send --to telegram` is BLOCKED when the cron job's auto-delivery target is the same Telegram chat. The system refuses duplicate delivery. Solution: put the Axel notification content directly in the final response — cron auto-delivers it to Telegram.

## Method ID Sequence
Methods are numbered sequentially. As of 2026-08-01: last method is **043** (SATM — Strange Attractor Trajectory Mapping). Sound production methods use SP-NNN prefix.

## Standalone Method Files
Full standalone write-ups (with Python implementation code) are saved alongside the main DB at:
`/opt/data/projects/Research/CompositionMethods/method_NNN_<acronym>.md`
These are self-contained references with extended math, full code, pitfalls, and usage examples. The main `methods_db.md` contains a condensed version.
