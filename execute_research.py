import json
import os

# research goal: 'Serialism' (Twelve-Tone Technique) - fits matrix perfectly.

method = {
    "name": "Twelve-Tone Technique (Serialism)",
    "category": "Algorithmic / Traditional",
    "description": "A method of composition devised by Arnold Schoenberg where all 12 notes of the chromatic scale are sounded as often as one another in a piece of music, preventing the emphasis of any one note. It uses a 'Tone Row' as the fundamental DNA.",
    "elements": {
        "PITCH": "Defined by the Tone Row (Prime, Retrograde, Inversion, Retrograde-Inversion). No note repetition until row is complete.",
        "RHYTHM": "Independent of pitch row. Often complex, using non-standard subdivisions or total serialism (serialized durations).",
        "HARMONY": "Resultant from vertical stacking of row segments or multiple row iterations in parallel voices.",
        "STRUCTURE": "Strict permutations of the Tone Row. Geometric logic (inversion, retrograde).",
        "TEXTURE": "Ranges from monophonic pointillism to dense polyphonic webs of row permutations."
    },
    "unit_matrix": {
        "VOICES": "Each voice typically carries a unique transformation of the row (e.g., Voice 1: P0, Voice 2: I5).",
        "SECTIONS": "Sections are defined by full row completions or transitions between different row sets (matrices)."
    }
}

db_path = "/opt/data/projects/Research/CompositionMethods/methods_db.md"

with open(db_path, "a") as f:
    f.write(f"\n## {method['name']}\n")
    f.write(f"- **Category**: {method['category']}\n")
    f.write(f"- **Description**: {method['description']}\n")
    f.write("\n### Musical Elements Framework\n")
    for k, v in method['elements'].items():
        f.write(f"- **{k}**: {v}\n")
    f.write("\n### UnitMatrix (Voices & Sections)\n")
    f.write(f"- **Voices**: {method['unit_matrix']['VOICES']}\n")
    f.write(f"- **Sections**: {method['unit_matrix']['SECTIONS']}\n")
    f.write("\n---\n")

print("SUCCESS: Method added to DB.")
