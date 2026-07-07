# DiffSinger Local SVS Environment Configuration
To execute E2E phoneme-level singing voice synthesis via DiffSinger, ensure correct environment structure and dependencies:

## Checkpoint & Model Structure
Unzip pre-trained checkpoints into clean, isolated subdirectories under the `checkpoints/` folder. Do not extract raw content directly to the parent folder.
*   **Acoustic Shallow-Diffusion Model**: `checkpoints/0228_opencpop_ds100_rel/` (contains `config.yaml`, `model_ckpt_steps_160000.ckpt`).
*   **Vocoder (Universal NSF HiFi-GAN)**: `checkpoints/0109_hifigan_bigpopcs_hop128/` (contains `config.yaml`, `model_ckpt_steps_280000.ckpt`).
*   **Pitch Extractor**: `checkpoints/0102_xiaoma_pe/` (contains `config.yaml`, `model_ckpt_steps_60000.ckpt`).

## Dependency Repair & Package Invariants
Modern Python stacks require explicitly bypassing PEP virtualenv constraints using `--break-system-packages` in root/headless environments.
*   **Important Package Installs**: Ensure `pyyaml`, `h5py`, `tqdm`, `einops`, `pycwt`, `praat-parselmouth`, `scikit-image`, `webrtcvad`, `pyloudnorm`, and `pytorch_lightning` are present globally or in the active runner.
*   **SciPy Compatibility Patch**: SciPy 1.13+ removes `kaiser` from the top-level `scipy.signal` namespace. Modify imports in `modules/parallel_wavegan/layers/pqmf.py` to:
    ```python
    from scipy.signal.windows import kaiser
    ```

## Phonetic Segment and Syllable Alignment
When mapping Western vocal tracks (such as Balfolk or Folk lyrics) to the Chinese Opencpop-trained dictionary, use pinyin approximations:
*   **Syllable mapping**: Dutch "Een klein meisje ging eens wandelen" translates to pinyins: `en kuan mei xie jing en wan de leng`
*   **Note Alignment rule**: The input formatting expects phonetic arrays. Pinyins with multiple phoneme components (like "k uan" or "m ei") must duplicate their target MIDI pitch and note durations for *each* separated sub-phoneme inside the sequence. First sub-phoneme segment is a starting consonant (`is_slur_seq = 0`); any subsequent sub-segments are vowels (`is_slur_seq = 1`).
