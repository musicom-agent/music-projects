# Disco Density Analysis (v1 → v2 → v3)

## v1: Classic Disco (Manual Patterns)
```
Drums   : ████████████████ (100%)
Bass    : ████████████████ (100%)
Strings : █░█░█░█░█░█░█░█░ (50%)  ← sparse
Brass   : █░░░░░░░█░░░░░░░ (12%)  ← very sparse
```
**Problem**: Strings and brass too sparse. Staccato feel.

## v2: Euclidean Groove (Method 011)
```
Drums   : ███░███░███░███░ (75%)
Bass    : █░░░█░░░█░░░█░░░ (25%)  ← WORSE
Strings : ░█░░░█░░░█░░░█░░ (25%)  ← WORSE
Brass   : █░█░█░█░█░█░█░█░ (50%)  ← better
```
**Problem**: Euclidean patterns alone create MORE gaps. Bass and strings dropped to 25%.

## v3: Euclidean + DPSM Hybrid (Method 011 + 026)
```
Drums   : ███░███░███░███░ (75%)
Bass    : ████████████████ (100%)  ← FIXED (added walking fills)
Arpeggios: ████████████████ (100%) ← NEW (DPSM 3-phase)
Strings : ████████████████ (100%)  ← FIXED (sustained pad)
Brass   : █░░░░░░░█░░░░░░░ (12%)  ← intentional sparse (accent role)
```
**Solution**: Hybrid approach fills gaps while preserving rhythmic interest.

## Key Insight

**Sparse patterns (Euclidean) are for RHYTHMIC structure, not harmonic content.**

For dance genres, you need:
1. Sparse rhythmic foundation (drums/bass with Euclidean)
2. Continuous harmonic layer (arps/pads with DPSM or sustained)
3. Intentional sparse accents (brass/stabs for punctuation)

Density by role:
- **Rhythmic** (drums): 75-100% — drives the groove
- **Harmonic** (bass, arps, pads): 100% — provides continuous flow
- **Accent** (brass, stabs): 12-50% — adds punctuation, not foundation
