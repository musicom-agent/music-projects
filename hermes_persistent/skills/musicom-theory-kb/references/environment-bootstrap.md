# User-Space Environment Bootstrap

In restricted environments (no root/apt), maintain the toolchain in `/opt/data/micromamba`.

## 1. Micromamba Bootstrap
```bash
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
mv bin/micromamba /opt/data/bin/micromamba
```

## 2. Python 3.11 Workspace (Fixing 3.13 Build Errors)
Music AI libraries often fail on Python 3.13 due to `setuptools` conflicts. Use Python 3.11.

```bash
/opt/data/bin/micromamba create -n musicom -c conda-forge python=3.11 ffmpeg go -y -r /opt/data/micromamba
# Essential: Downgrade setuptools for basic-pitch/librosa builds
/opt/data/bin/micromamba run -r /opt/data/micromamba -n musicom pip install "setuptools<70" basic-pitch
```

## 3. Tool Execution
Always bypass system paths:
```bash
export PYTHONPATH=""
/opt/data/bin/micromamba run -r /opt/data/micromamba -n musicom <command>
```
