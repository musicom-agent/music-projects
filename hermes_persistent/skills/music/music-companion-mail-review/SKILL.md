---
name: music-companion-mail-review
description: "Weekly mail review workflow for Musicom: read inbox, extract music/AI workflow signals, and turn them into product/spec ideas."
version: 1.0.0
author: "Musicom Agent"
metadata:
  hermes:
    tags: [email, music, ai-music, workflow, spec, review]
---

# Music Companion Mail Review

## Trigger
Use when the user asks to read mail for useful music-companion signals or wants the inbox turned into product ideas/specs.

## Goal
Turn newsletter and inbox noise into a small set of actionable product signals for a transparent music companion.

## Inputs
- IMAP credentials from `/opt/data/.env.mail`
- Focus on AI music, DAW workflows, creator tooling, distribution, royalties, rights, metadata, provenance, and artist workflow

## Procedure
1. Read recent mail and identify messages with product-relevant music signals.
2. Prefer newsletter content and industry updates over ordinary personal mail.
3. Extract only durable signals:
   - workflow patterns
   - user pain points
   - provenance / credits / rights concerns
   - DAW integration ideas
   - review/approval behavior
   - metadata and release tooling
4. Convert signals into proposed spec changes.
5. Keep output short, technical, and caveat any uncertainty.

## Output Format
Use this structure:
- `Useful signals`
- `Product implications`
- `Proposed specs`

## Spec Style
Each proposed spec should be phrased as:
- feature name
- what it does
- why it matters
- human gate if needed

## Constraints
- Do not dump full newsletters unless asked.
- Do not invent certainty from noisy marketing copy.
- Prefer repeatable product lessons over one-off headlines.
- Keep language caveman-short and technically accurate.

## Verification
If mail access fails, say so plainly.
If nothing useful is found, say that too.
