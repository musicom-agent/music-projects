# Official SKILL.md Standards (from NousResearch/hermes-agent)

Based on analysis of 7 official skills from the Hermes Agent repo (songwriting-and-ai-music, architecture-diagram, test-driven-development, github-pr-workflow, linear, openhue, blogwatcher).

## Required Frontmatter

```yaml
---
name: skill-name                    # lowercase, hyphens/underscores, max 64 chars
description: "One-line summary."    # present tense, what it does
version: 1.0.0                      # SEMVER
author: Author Name                 # or "community"
license: MIT
platforms: [linux, macos, windows]  # omit if platform-specific
dependencies:                       # external tools needed
  - some-tool
prerequisites:                      # env vars, commands
  env_vars: [TOKEN]
  commands: [command]
triggers:                           # auto-activation keywords
  - trigger phrase
  - another trigger
metadata:
  hermes:
    tags: [tag1, tag2]
    related_skills: [sibling-skill]
---
```

## Required Sections (in order)

1. **Header** — `# Skill Name` + one-liner
2. **When to Use / Scope** — when to apply, when to delegate elsewhere
3. **Installation & Prerequisites** — how to get tools, not just "check what's available"
4. **Quick Start** — 3-line example or minimal working case
5. **Core Workflow** — numbered steps with code/command examples
6. **Reference** — tables, formulas, lookup data
7. **Output Specifications** — where files go, what formats, how to verify
8. **Notes** — pitfalls, edge cases, version caveats, performance tips

## Key Patterns Across All Skills

- **Explicit failure modes**: Every skill documents what can go wrong and how to recover
- **Platform variants**: When commands differ by OS, show both (gh vs git+curl)
- **Minimal first**: Quick start shows the simplest case; advanced usage follows
- **Related skills**: Always link sibling skills in metadata for discoverability
- **Versioned**: Every file has `version` in frontmatter; changes tracked in version history
