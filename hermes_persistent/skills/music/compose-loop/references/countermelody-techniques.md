# Countermelody Techniques

## Method 032: Isorhythmic Talea-Color (ITCM)

Medieval technique adapted for algorithmic countermelody. Uses two independent cycles:

- **Talea**: rhythmic cycle (e.g., length 5)
- **Color**: pitch cycle (e.g., length 7)

When talea and color lengths are **coprime**, the combined pattern doesn't repeat until LCM(talea, color) notes. Example: 5×7 = 35 notes before cycling.

### Implementation Pattern

```python
# Talea: 5-note rhythmic cycle
TALEA = [QUARTER, EIGHTH, HALF, EIGHTH, QUARTER]

# Color: 7-note pitch cycle (descending arc)
COLOR_C = [64, 67, 69, 72, 71, 69, 67]  # E4 G4 A4 C5 B4 A4 G4
COLOR_G = [67, 69, 71, 74, 72, 71, 69]  # G4 A4 B4 D5 C5 B4 A4
COLOR_F = [65, 67, 69, 72, 71, 69, 67]  # F4 G4 A4 C5 B4 A4 G4

def build_countermelody(chord_name, section_offset, section_idx, section_name):
    events = []
    color = COLORS[chord_name]
    talea_pos = 0
    color_pos = (section_idx * 3) % len(color)  # Phase shift per section
    
    t = 0
    while t < SECTION:
        dur = TALEA[talea_pos % len(TALEA)]
        pitch = color[color_pos % len(color)]
        
        # Dynamic variation per section
        if section_name == 'Intro' or section_name == 'Outro':
            vol = 0  # Silent
        elif section_name.startswith('Ch'):
            vol = 85  # Forte in chorus
        elif section_name.startswith('V'):
            vol = 65 if section_idx >= 4 else 55  # V2 louder than V1
        
        if vol > 0 and t + dur <= SECTION:
            events.append(MusicEvent(pitch=pitch, volume=vol, 
                                    start_tick=t, end_tick=t + dur - 40))
        
        t += dur
        talea_pos += 1
        color_pos += 1
    
    pad_to_section(events)
    return MusicUnit(events=events)
```

### Key Parameters

- **Phase shift**: `(section_idx * 3) % len(color)` ensures each section starts at a different point in the color cycle
- **Duration subtraction**: `end_tick = t + dur - 40` creates slight separation between notes
- **Dynamic mapping**: Silent in intro/outro, moderate in verses, loud in chorus

### Why It Works

The coprime cycles create organic non-repetition. The phase shift per section prevents monotony across the composition. The technique produces countermelodies that feel independent yet harmonically coherent.
