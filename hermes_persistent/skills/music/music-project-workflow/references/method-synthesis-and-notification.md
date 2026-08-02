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
7. If running as a scheduled cron job, do not attempt to invoke any direct outbound messaging platforms (e.g. `send_message`, `hermes send`). The scheduled job runner automatically captures your final assistant response and delivers it to the designated recipient's inbox. Put all intended communication directly in the final response and bypass manual gateway sends.
8. If runtime Telegram env is missing, report delivery unavailable and avoid guessing a destination.

## Pitfalls
- Duplicate headings are a failure.
- A valid bot token does not imply a usable chat id.
- Shell env and gateway runtime env can differ.

## Verified pattern from this session
- Runtime env lacked `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`, so notification had to be reported as unavailable.
- The method inserted was `WCS` / `Wavefront Constraint Sequencing` and the heading was verified in the file before attempting delivery.
- Added **Method 024: Additive Mass LFO Synthesis** based on Melatonin's Sine Machine (Vienna, July 2026), demonstrating continuous-time additive LFO synthesis structures inside the UnitMatrix.
- Added **Method 028: Chaotically Modulated Cellular Grains (CMCG)**, demonstrating nature-led, discrete-time chaotic maps (Hénon, Ikeda) modulating granular synthesis engines inside the UnitMatrix.
- Added **Method 029: Continuous Polyphonic Portamento Glide (CPPG)** based on kota kato's *Puntone* (July 2026), demonstrating polyphonic portamento / chordal frequency-morphing trajectories inside the UnitMatrix.
- Confirmed that in the cron session, `HERMES_CRON_AUTO_DELIVER_PLATFORM=telegram` and `HERMES_CRON_AUTO_DELIVER_CHAT_ID=8684633270` are populated, meaning the final response is automatically delivered to Axel on Telegram. No manual Telegram commands or direct sends are needed.
- Produced high-accuracy telegraphic report matching the `caveman` style standard and bypassed manual `send_message` commands.