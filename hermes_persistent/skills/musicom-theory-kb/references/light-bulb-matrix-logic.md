# Logic of the Light Bulb Matrix (Pitch Class Dashboarding)

## Concept
The "Light Bulb" matrix is a pedagogical visualization tool designed to help composers see **Modal Interchange** as a discrete bit-flip in a 12-TET universe.

## Python Visualization Template (Matplotlib)
```python
import matplotlib.pyplot as plt
import numpy as np

def plot_bulb_matrix(chords, labels, title, save_path):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#020617')
    ax.set_facecolor('#020617')
    
    for i, chord in enumerate(chords):
        for pc in chord:
            # Check if note is 'borrowed' (not in base scale, e.g., C Major: [0,2,4,5,7,9,11])
            is_borrowed = pc not in [0, 2, 4, 5, 7, 9, 11] 
            color = '#fb7185' if is_borrowed else '#22d3ee'
            rect = plt.Rectangle((i, pc), 0.8, 0.8, color=color, alpha=0.9)
            ax.add_patch(rect)

    ax.set_ylim(-0.5, 12)
    ax.set_yticks(range(12))
    ax.set_yticklabels(labels, color='#94a3b8', fontname='monospace')
    ax.set_title(title, color='white')
    plt.savefig(save_path)
```

## Theory: Chromatic Gravity
1. **The #4 (Lydian)**: Creates an upward "bright" pull toward the 5th.
2. **The b6 (Minor Borrow)**: Creates a downward "dark" pull toward the 5th.
3. **The b7 (Mixolydian/Minor Borrow)**: Pulls away from the leading tone, softening the resolution.
