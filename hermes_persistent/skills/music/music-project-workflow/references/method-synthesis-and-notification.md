# Method Synthesis and Notification

Use when appending a new composition method to `methods_db.md` and notifying a human contact.

## Stable flow
1. Pick a genuinely new method class; do not duplicate an existing heading.
2. Write the method in the database's stable template:
   - Source
   - Workflow
   - Description
   - Filling the Elements
   - UnitMatrix Mapping
   - Best Use
3. Cover all five Musical Elements explicitly: PITCH, RHYTHM, HARMONY, STRUCTURE, TEXTURE.
4. Include a Voices × Sections explanation. Prefer section constraints first, voice realization second.
5. Re-read the exact inserted block and confirm the heading before any notification.
6. For Telegram, keep the message compact: method name, source, UnitMatrix fit, file path.
7. If runtime Telegram env is missing, report delivery unavailable and avoid guessing a destination.

## Pitfalls
- Duplicate headings are a failure.
- A valid bot token does not imply a usable chat id.
- Shell env and gateway runtime env can differ.

## Verified pattern from this session
- Runtime env lacked `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`, so notification had to be reported as unavailable.
- The method inserted was `WCS` / `Wavefront Constraint Sequencing` and the heading was verified in the file before attempting delivery.