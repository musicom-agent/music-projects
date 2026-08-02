---
name: musicom-agent-assessment
description: "Evidence-first review of the Musicom companion agent + codebase: verify claims with real tool output (imports, install, tests, git, doc-vs-code drift), produce SWOT, then a flash-executable improvement plan."
version: 1.0.0
author: "Musicom Agent"
metadata:
  hermes:
    tags: [music, assessment, audit, review, codebase, planning, verification]
---

# Musicom Agent Assessment

Class of task: "review / evaluate / assess the goal, setup and state of the Musicom agent and its repos, then plan improvements." Also applies to any request to hand a plan to a cheaper/faster model (e.g. Gemini-flash) for execution.

## Core principle: verify, do not trust docs
READMEs, QUICK_REFERENCE, and skill claims drift from reality. NEVER write a SWOT from documentation alone. Run real probes first and quote the actual output. Doc-vs-code drift is itself a top finding.

## Workflow
1. **Read the intent layer**: load `music-companion-role-spec` (mission/loop/gates) + any `*-plan` skills + repo `README.md`, `DOC.md`, `plans/architecture-review.md`.
2. **Probe live state** — run `scripts/verify_state.sh` (or the checks inline). Capture real output for each row of the state table.
3. **Map ecosystem**: `ls /opt/data/repos/` — flag which repo is canonical vs sprawl/duplication.
4. **Confirm one real workflow end-to-end**: actually import the composer and construct a UnitMatrix; do not assume it works.
5. **Write SWOT** grounded in probe output. Every weakness cites a verified fact.
6. **Emit a flash-executable plan** (see below).
7. **Write full report** to `/opt/data/projects/Research/<area>/agent_assessment_<date>.md`; deliver a compact table summary to chat.

## State table — the checks that matter (learned this session)
| Check | Command | Why |
|---|---|---|
| import shell | `python -c "import musicom"` | passes even when package is an empty namespace shell |
| real export | `python -c "from musicom import UnitMatrix"` | catches "imports OK but nothing exported" |
| submodule | `python -c "from musicom.workflows... import ..."` | catches missing/uninstalled subpackages |
| installed? | `pip show musicom` | path hacks hide that `pip install -e .` was never run |
| example import style | grep `^(import|from)` in examples/ | reveals `sys.path` hacks + bare `from workflows` (competing layout) |
| tests | `python -m pytest tests/ -q` | pytest often absent from env → coverage claims unverifiable |
| git | `git status -s` + `git log --oneline -5` | uncommitted WIP = loss risk finding |
| doc drift | compare README/QUICK_REF API names vs `structures/unit.py` | phantom API (Note/Chord/Sequence vs MusicEvent/MusicUnit) misleads any model |
| render chain | check outputs/ for MIDI+WAV+OGG triplets | proves pipeline actually runs |

## Flash-executable plan format (for Gemini-flash or similar)
The plan is the deliverable; make it runnable by a fast, low-reasoning model:
- Ordered phases, Phase 0 = stabilize foundation (install/import/commit) BEFORE anything else.
- Each task = exact path + exact command + explicit **Verify** command with expected exit/output.
- Bug fixes: one edit + one test each.
- Include an **execution contract**: one task at a time; run Verify; paste real output; on fail STOP and report, never fabricate; outputs to `/opt/data/projects/Research/<project>/`; commit per phase.

## Pitfalls
- **"import musicom OK" is a false positive.** It can be a namespace package with zero exports. Always follow with a concrete `from musicom import <Class>`.
- **Two competing import layouts** (namespaced `musicom.x` vs flat `structures/`,`workflows/` with `sys.path` hacks) are the #1 fragility. Pick one in the plan; don't leave both.
- **Do not report a blocker as fixed.** If a probe fails (pytest missing, package not installed) that is a Phase-0 task for the plan, not a defect to paper over.
- **Deliver via file, summarize in chat.** Full SWOT+plan to a dated Research file; chat gets the compact table + phase list + the MEDIA path.
- Keep style caveman: short technical fragments, high-contrast tables, no filler.

## Scripts
- [verify_state.sh](scripts/verify_state.sh) — run this FIRST; re-runnable probe covering all 9 state-table checks. `bash scripts/verify_state.sh [REPO] [PY]`.

## References
- [assessment-2026-07-20.md](references/assessment-2026-07-20.md) — worked example: full findings + 6-phase plan from the first assessment run.
