# MusicMatrix Reserved Semantics

Session learning from Project 014 genre education.

## Source repo

Use `axelwiertz/musicom` as Musicom core KB.

Local path:

```text
/opt/data/repos/musicom
```

Core file:

```text
structures/matrix.py
```

Core class:

```python
class UnitMatrix:
    """
    Basic 2D matrix for MusicUnit objects:
    - horizontal rows are voices in pitch space
    - vertical columns are sections in time space
    """
```

## Reserved vocabulary

`MusicMatrix` / `UnitMatrix` is reserved for the actual Musicom composition structure.

Do not use it as a generic table name.

Canonical axes:

```text
Rows    = voices / pitch-space layers
Columns = measures or sections / time-space segments
Cells   = MusicUnit material
```

## Genre matrix relation

Genre matrices fit perfectly *inside* this structure as semantic annotation layers.

Correct relationship:

```text
MusicMatrix / UnitMatrix = structural grid
Genre Pattern Matrix     = semantic education layer over the grid
```

Example mapping:

```text
MusicMatrix row      Genre tag
Percussion voice  -> Rhythm DNA
Bass voice        -> Bass DNA
Harmony voice     -> Harmony DNA
Lead voice        -> Melody DNA
Pad/counterline   -> Timbre/Form support
```

## Teaching/composition rule

When educating about genres:

1. Define the actual MusicMatrix rows (voices) and columns (bars/sections).
2. Attach genre DNA labels to rows/cells.
3. Show which row changes when moving between genre versions.
4. Keep most rows stable when making hybrids; transform only one or two rows to preserve identity.

Example:

```text
Balfolk -> Hybrid Jazz
Keep: rhythm row, bass row, folk lead row
Change: harmony row from modal triads to Dm9/Cmaj7/G13
Optional: timbre row from accordion/guitar to piano color
```
