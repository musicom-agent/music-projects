# Bootstrap Toolchain Protocol (v1)

Context: Python 3.13 system environment is unstable for music libraries (basic-pitch, librosa, music21) due to removed legacy `pkg_resources` and `setuptools` build-meta issues.

## 1. Install Micromamba
Execute in `/opt/data/bin`:
`curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba`

## 2. Create Stable Environment
`micromamba create -n musicom -c conda-forge python=3.11 ffmpeg go pip -y -r /opt/data/micromamba`

## 3. Install Music Stack (Isolated)
Use specific version constraints to avoid build errors:
`PYTHONPATH="" micromamba run -n musicom pip install "setuptools<70" basic-pitch[tf] librosa music21 pretty-midi`

## 4. Execution
Always bypass system path:
`PYTHONPATH="" micromamba run -r /opt/data/micromamba -n musicom python <script.py>`
