# Musicom Dashboard & Visualization Templates

## 1. Project Dashboard (index.html)
Use this template for single-project views. Requires a dark high-contrast aesthetic.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Project [ID]: [Name]</title>
    <style>
        :root { --bg: #020617; --card-bg: #0f172a; --primary: #22d3ee; --accent: #fb7185; }
        body { background: var(--bg); color: #f8fafc; font-family: sans-serif; padding: 2rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
        .card { background: var(--card-bg); border: 1px solid #1e293b; padding: 1.5rem; border-radius: 12px; }
    </style>
</head>
<body>
    <h1>Musicom Composition Agent</h1>
    <div class="grid">
        <!-- Visuals go here -->
    </div>
</body>
</html>
```

## 2. Visualization Logic (Matplotlib)

### Piano Roll
```python
import matplotlib.pyplot as plt
# Plot pitch vs time (quarterLength)
ax.add_patch(plt.Rectangle((offset, pitch), duration, 0.8, color='#22d3ee'))
```

### Volume Graph
```python
# Plot note velocity over time
plt.plot(times, velocities, color='#fb7185', linewidth=2)
plt.fill_between(times, velocities, color='#fb7185', alpha=0.2)
```

### Chroma Profile
```python
# Histogram of pitch classes (0-11)
plt.hist(pitches, bins=range(13), color='#22d3ee', rwidth=0.8)
```
