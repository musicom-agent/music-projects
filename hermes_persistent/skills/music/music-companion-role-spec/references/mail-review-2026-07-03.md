# Mail Review 2026-07-03

Condensed signals extracted from weekly mail review used to update `music-companion-role-spec`.

## Signals
- **Conversational DAW Assist:** User wants talk-first workflow; no menus first; iterate live; exportable material for other DAWs; flow mode vs review mode split.
- **Provenance and AI Labels:** Platforms care about monetization, impersonation, and rights; companion must tag outputs and warn on policy risk.
- **Distribution and Rights Awareness:** AI music value now depends on rights and distribution, not generation alone; surface platform restrictions, impersonation risk, missing credits/metadata.
- **Project-Level Metadata and Release Support:** Companion must help with orchestration: idea → draft → metadata → release → promo; keep versioned exports, inspectable project state, release notes and metadata drafts.
- **Companion Feedback Loop:** User wants iterative composition with visible results; propose → adjust → approve; compare-select-feedback loop; keep transparent reasoning.

## Product Implications
- Generation is becoming infrastructure; orchestration and metadata are the differentiators.
- Rights and provenance are now first-class concerns for any release.
- Conversational, preview/approve workflows are expected by users.

## Changes Made to `music-companion-role-spec`
- Added "Pitfalls & Learned Constraints" section capturing empty/corrupt file regenerate, MIDI meta insertion order, soundfont availability fallback, DAW-native conversational workflow, rights and provenance awareness, and project-level metadata/release support.
- Added "References" pointer to this file.

## Next Steps
- Implement flow/review modes in companion runtime.
- Add provenance tagging and rights warnings.
- Build metadata/release export pipeline.
