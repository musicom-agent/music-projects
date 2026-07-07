# Promoting a generated draft into a numbered Musicom project

Session pattern from project 016 (`016-electric-folk-d-major`).

## Trigger
User has a generated MIDI/audio draft in `/tmp/hermes/songs/...` and asks to put all results into a new numbered project.

## Canonical repo
Use `~/projects/music-projects` as local clone of `musicom-agent/music-projects`.
If missing, clone:

```bash
mkdir -p ~/projects
git clone https://github.com/musicom-agent/music-projects.git ~/projects/music-projects
```

Verify remote/branch before edits:

```bash
cd ~/projects/music-projects
git remote -v
git branch --show-current
```

Expected remote may normalize to SSH (`git@github.com:musicom-agent/music-projects.git`) from existing credentials. Preserve working credentials.

## Folder shape for generated drafts
Use the newer Musicom composer project shape, not only the legacy BandLab template:

```text
NNN-project-name/
├── README.md
├── index.html
├── MIDI/
├── Audio/
├── Renders/
├── Analysis/
├── Notes/
├── Scripts/
├── BandLab/
└── Stems/
```

For each generated draft:
- Copy `.mid` to `MIDI/v1_<slug>.mid`.
- Copy `.ogg` to `Audio/v1_<slug>.ogg` for Telegram/listening.
- Copy `.wav` to `Renders/v1_<slug>.wav` if full render should be preserved.
- Copy generator script to `Scripts/generate_v1.py` if reproducibility matters.
- Write `Analysis/v1_dna.txt` and/or `Analysis/v1_analysis.md` with rhythm/harmony/pitch DNA.
- Write `Notes/concept.md` with production questions and next-step decisions.
- Write `index.html` dashboard with audio player, MIDI link, and high-contrast rhythm DNA (`█`/`░`).
- Write `BandLab/link.md` placeholder if no cloud DAW URL yet.

## Commit protocol
Use the Musicom Agent identity:

```bash
git config user.name 'Musicom Agent'
git config user.email 'musicom@wiertz.tech'
git add NNN-project-name
git commit -m 'NNN: add <project-name> project'
git push origin main
git status --short
```

Report commit hash, push target, working-tree status, project path, and next workflow step.

## Next workflow step after v1 generation
Usually: DAW/BandLab production pass.

1. Import MIDI into DAW/BandLab.
2. Replace GM/synthetic sounds with realistic or chosen production sounds.
3. Balance core engine (kick+bass, snare backbeat, rhythm guitar drive, lead hooks, vocal room).
4. Export v2 audio + MIDI.
5. Analyze v2 against v1 and update `Analysis/`, `README.md`, `index.html`, then commit `NNN: add v2 production pass`.
