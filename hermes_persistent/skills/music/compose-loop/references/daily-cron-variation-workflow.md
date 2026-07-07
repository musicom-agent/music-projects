# Daily Cron Variation Workflow

Session-derived notes from scheduled music generation runs.

## Selection
- Pick one style folder from `/opt/data/projects/Styles/`.
- If no numbered project found in the selected style, fall back to another style that contains a numbered project.
- Use one numbered project folder as the working target.

## Analysis inputs
- Prefer project-local `README.md`, `unitmatrix.md`, `Analysis/*.md`, and existing MIDI analysis text when present.
- Extract a compact DNA summary across pitch center, rhythm, harmony, texture, form, and density.
- If a project has prior renders but no fresh source notes, use the most descriptive local analysis artifact available.

## Output contract
- Write files in the project root with the date-stamped naming convention requested by the job.
- Ensure the `daily_log.md` entry includes date, style, project, DNA summary, and file paths.
- Verify the appended log block by re-reading the exact inserted section.

## Reporting
- For cron-style runs, keep the final summary compact.
- If delivery is handled externally, do not call messaging tools from the job.
- If the run is silent, return `[SILENT]` exactly.

## Pitfall
- `search_files` may return truncated results; if so, narrow the path or increase offset before assuming a folder has no projects.