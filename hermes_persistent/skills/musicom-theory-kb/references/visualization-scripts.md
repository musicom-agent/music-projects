# Music Visualization Scripts

These scripts provide the core logic for the "Play & See" pipeline in the Musicom Composition Platform.

## 1. Piano Roll Generator
Uses `music21` and `matplotlib` to create a dark-themed piano roll with cyan bars.

```python
import sys
import os
import matplotlib.pyplot as plt
from music21 import converter, note, chord

def generate_piano_roll(midi_path, output_path):
    score = converter.parse(midi_path)
    notes, times, pitches, durations = [], [], [], []
    
    for part in score.parts:
        for element in part.flatten().notes:
            if isinstance(element, note.Note):
                notes.append(element)
                times.append(element.offset)
                pitches.append(element.pitch.ps)
                durations.append(element.quarterLength)
            elif isinstance(element, chord.Chord):
                for n in element:
                    notes.append(n)
                    times.append(element.offset)
                    pitches.append(n.pitch.ps)
                    durations.append(element.quarterLength)

    plt.figure(figsize=(12, 6), facecolor='#1e1e1e')
    ax = plt.gca()
    ax.set_facecolor('#1e1e1e')
    for t, p, d in zip(times, pitches, durations):
        ax.add_patch(plt.Rectangle((t, p), d, 0.8, color='#58C4DD', alpha=0.8))
    
    plt.xlim(0, max(times) + 5 if times else 10)
    plt.ylim(min(pitches) - 5 if pitches else 40, max(pitches) + 5 if pitches else 80)
    plt.grid(True, linestyle='--', alpha=0.2, color='white')
    plt.savefig(output_path, dpi=150)
    plt.close()
```

## 2. Dynamics/Volume Graph
Visualizes the "shape" of the composition by plotting velocity over time.

```python
import matplotlib.pyplot as plt
from music21 import note, chord

def plot_dynamics(score, output_path):
    times, velocities = [], []
    for element in score.flatten().notes:
        times.append(element.offset)
        if isinstance(element, note.Note):
            velocities.append(element.volume.velocity or 64)
        else:
            velocities.append(element[0].volume.velocity or 64)

    plt.figure(figsize=(10, 4), facecolor='#1e1e1e')
    plt.plot(times, velocities, color='#fb7185', linewidth=2)
    plt.fill_between(times, velocities, color='#fb7185', alpha=0.2)
    plt.savefig(output_path)
```
