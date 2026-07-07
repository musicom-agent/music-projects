# Canonical Local Project Workspace Correction

Session learning: a numbered project was first created in `/root/projects/music-projects` after cloning `musicom-agent/music-projects`. The user corrected that the real project folder on disk is `/opt/data/projects/`, and that this folder is mirrored to the `music-projects` repo.

## Rule

Use `/opt/data/projects/` as the canonical local workspace for numbered Musicom composition projects.

## Correct workflow

```bash
cd /opt/data/projects
mkdir -p 016-electric-folk-d-major/{MIDI,Audio,Analysis,Notes,Scripts,Renders,BandLab,Stems,Scores}
```

Add or update project assets there first:

- `MIDI/` for editable DAW files
- `Audio/` for OGG/Opus listening renders
- `Renders/` for WAV/full production renders
- `Analysis/` for DNA, MIDI/audio analysis, grids
- `Notes/` for concept and iteration notes
- `Scripts/` for project-local generators
- `index.html` dashboard at project root

## If project content lands in the wrong clone

1. Verify canonical destination does not already exist:
   ```bash
   test -e /opt/data/projects/<NNN-project-name> && echo DEST_EXISTS
   ```
2. Move the project folder:
   ```bash
   mv /root/projects/music-projects/<NNN-project-name> /opt/data/projects/<NNN-project-name>
   ```
3. Verify files:
   ```bash
   find /opt/data/projects/<NNN-project-name> -type f | sort
   ```
4. Remove or reset the stray clone so future work does not continue there:
   ```bash
   rm -rf /root/projects/music-projects
   ```

## Pitfall

Do not infer canonical local path from GitHub repo name. `musicom-agent/music-projects` is the remote repository identity; `/opt/data/projects/` is the user's mounted/mirrored local workspace.
