# Himalaya CLI (Email) Technical Notes

## Search & Query Syntax
The `himalaya` CLI version in this environment uses a specific query parser that requires spaces between keys and values, and does not support the `--limit` flag in all subcommands.

### Known Queries
- **List Inbox:** `himalaya envelope list`
- **Search Subject:** `himalaya envelope list "subject music"` (Note: `subject:music` fails; use space)
- **Search Body:** `himalaya envelope list "body music"`
- **Read Message:** `himalaya message read <ID>`
- **Switch Folder:** `himalaya envelope list -f <FOLDER_NAME>` (e.g., `Promotions`, `SocialNetworks`)

## Limitations & Pitfalls
- **No Search Command:** `himalaya envelope search` is not a valid subcommand; use `himalaya envelope list "<query>"` instead.
- **Permission Denied:** In this environment, `/opt/data/cron/jobs.json` is root-owned. Automation must be handled via background `terminal` loops or personal user-space cron if available.
- **Multipart Messages:** Some emails contain MIDI files as `<#part>` tags in the body.
