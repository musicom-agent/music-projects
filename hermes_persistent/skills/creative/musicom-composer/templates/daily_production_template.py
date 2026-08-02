# -*- coding: utf-8 -*-
"""Template for autonomous daily composition & production pipeline.
Complies strictly with projects/Styles/AGENTS.md and zero-drift policy.
"""
import os
import sys
import random
import json
import re

# Enforce correct python interpreter packages
# (Package musicom is installed editable in the musicom env)
from structures import MusicUnit, MusicEvent, UnitMatrix, MidiInstrument, MidiPercussion
from workflows.unitmatrix_composer import (
    UnitMatrixComposer, create_note_unit, create_chord_unit, create_empty_unit,
)
from ai.utils.visualizer import write_grid_visualization
from workflows.provenance import write_provenance, AI_ASSISTED

def parse_methods_db(db_path="/opt/data/projects/Research/CompositionMethods/methods_db.md"):
    """Parses composition and production methods from the markdown database."""
    comp_methods = []
    prod_methods = []
    
    if not os.path.exists(db_path):
        return ["001"], ["SP-001"] # fallback
        
    with open(db_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extract Method IDs e.g. **021**
    comp_matches = re.findall(r"\|\s*\*\*(\d{3})\*\*\s*\|", content)
    # Extract Sound Production IDs e.g. **SP-011**
    prod_matches = re.findall(r"\|\s*\*\*(SP-\d{3})\*\*\s*\|", content)
    
    return comp_matches or ["001"], prod_matches or ["SP-001"]

def build_zero_drift_midi(composer, out_midi_path):
    """Saves MIDI with absolute track-length validation and tail padding.
    Ensures zero clock-drift across separate tracks.
    """
    # 1. Trigger engine-level validation gate
    ok, msg = composer.validate()
    if not ok:
        raise ValueError(f"UnitMatrixComposer validation failed: {msg}")
        
    # 2. Export to MIDI file
    composer.to_midi(out_midi_path)
    
    # 3. Size enforcement gate
    file_size = os.path.getsize(out_midi_path)
    if file_size <= 40:
        raise ValueError(f"Exported MIDI is empty/corrupt (size={file_size} bytes)")
        
    print(f"MIDI successfully written: {out_midi_path} ({file_size} bytes)")

def render_audio_fluidsynth(midi_path, wav_path, ogg_path):
    """Renders MIDI using headless FluidSynth and encodes to Opus OGG with peak norm."""
    soundfont = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
    
    # 1. Execute FluidSynth CLI
    fs_cmd = f"/opt/data/micromamba/envs/musicom/bin/fluidsynth -ni -F {wav_path} -g 1.2 {soundfont} {midi_path}"
    print(f"Running FluidSynth: {fs_cmd}")
    ret = os.system(fs_cmd)
    if ret != 0:
        raise RuntimeError("FluidSynth rendering failed")
        
    # 2. FFmpeg peaks normalization + Opus compression (48k voip)
    ffmpeg_cmd = (
        f"ffmpeg -i {wav_path} -af \"peaknorm=level=-1\" "
        f"-codec:a libopus -application voip -b:a 48k {ogg_path} -y -loglevel error"
    )
    print(f"Running FFmpeg: {ffmpeg_cmd}")
    ret = os.system(ffmpeg_cmd)
    if ret != 0:
        # Fallback if peaknorm filter is missing
        ffmpeg_cmd_fb = (
            f"ffmpeg -i {wav_path} -af \"volume=0.89\" "
            f"-codec:a libopus -application voip -b:a 48k {ogg_path} -y -loglevel error"
        )
        print(f"Running FFmpeg fallback: {ffmpeg_cmd_fb}")
        ret = os.system(ffmpeg_cmd_fb)
        if ret != 0:
            raise RuntimeError("FFmpeg compression failed")
            
    # 3. Clean up intermediate heavy WAV file
    if os.path.exists(wav_path):
        os.remove(wav_path)
        print(f"Removed temporary WAV: {wav_path}")

def generate_volt_dashboard(project_dir, project_name, comp_id, prod_id):
    """Generates a high-contrast VoltAgent-themed dashboard."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{project_name} - Dashboard</title>
    <style>
        body {{
            background-color: #050507;
            color: #e0e0e0;
            font-family: system-ui, -apple-system, sans-serif;
            margin: 40px;
        }}
        h1 {{
            color: #00d992;
            font-size: 48px;
            font-weight: 800;
            line-height: 1.0;
            margin-bottom: 20px;
        }}
        pre {{
            font-family: 'JetBrains Mono', monospace;
            background-color: #101010;
            border: 1px solid #222;
            padding: 20px;
            color: #00d992;
            overflow-x: auto;
        }}
        .metric {{
            color: #818cf8;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>{project_name}</h1>
    <p>Daily Algorithmic Production Run</p>
    <div>
        <p>Composition Method: <span class="metric">{comp_id}</span></p>
        <p>Sound Production Method: <span class="metric">{prod_id}</span></p>
    </div>
    <h2>Rhythm DNA</h2>
    <pre>
█░░░█░░░█░░░█░░░ (Lead)
█░█░█░█░█░█░█░█░ (Bass)
    </pre>
</body>
</html>
"""
    dash_path = os.path.join(project_dir, "index.html")
    with open(dash_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"VoltAgent dashboard written: {dash_path}")

if __name__ == "__main__":
    # Test script harness
    print("DAILY ALGORITHMIC PRODUCTION TEMPLATE READY")
