# Musicom Toolchain Bootstrap (Restricted Environment)

Recipe for establishing technical autonomy in sandboxes with Python 3.13+ and no root access.

## 1. Core Bootstrap (Micromamba)
```bash
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
mkdir -p /opt/data/bin && mv bin/micromamba /opt/data/bin/micromamba
```

## 2. Environment Creation (Python 3.11 for ML/Music compatibility)
```bash
/opt/data/bin/micromamba create -n musicom -c conda-forge python=3.11 ffmpeg go pip -y -r /opt/data/micromamba
```

## 3. Stability Fixes (setuptools/pkg_resources)
Older music libraries (resampy, basic-pitch) break on Python 3.13 or newer setuptools.
```bash
/opt/data/bin/micromamba run -r /opt/data/micromamba -n musicom pip install "setuptools<70"
```

## 4. Primary Tooling
```bash
/opt/data/bin/micromamba run -r /opt/data/micromamba -n musicom pip install basic-pitch[tf] pretty-midi librosa music21
```

## 5. Execution Protocol
Always clear `PYTHONPATH` to prevent system libraries from leaking into the 3.11 environment:
```bash
PYTHONPATH="" /opt/data/bin/micromamba run -r /opt/data/micromamba -n musicom <command>
```
