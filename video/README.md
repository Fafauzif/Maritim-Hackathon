# The Ocean Has Floors · LAUTARA 2026 first-round video

A 4 min 46 s documentary-style film (1920×1080, 24 fps, English narration) answering the competition question
*"What do you think is the most important challenge facing maritime affairs today, and why?"*

**Deliverables** (in `out/`):

| File | What it is |
|---|---|
| `LAUTARA_OceanHasFloors_FINAL.mp4` | The film: H.264 + AAC, narration + sound effects, −14 LUFS |
| `LAUTARA_OceanHasFloors_SFX_only.wav` | The sound-effects track alone, at its level in the film |
| `LAUTARA_OceanHasFloors.en.srt` | English captions (upload to YouTube as CC) |
| `SFX_TABLE.md` | Every placed sound: time, purpose, source, creator, licence; skipped moments |

## Fill in before submitting

1. `src/scenes.py`: `TEAM_NAME`, `INSTITUTION`.
2. Team photos: `assets/team/01.jpg … 04.jpg` (Daniel Ferdiansyah, Daniel Angger, Salwa Alifia, Fauzi Fadhlurohman). Portrait crops work best; they are cropped to the slot automatically.
3. Run `sh build.sh` (about 8 minutes on an M4).

## Rebuild from source

Requirements: macOS or Linux, `ffmpeg`, `uv`, Python 3.11, the 3D art delivery at
`../3d-art/revision-v2/delivery/LAUTARA_3D_Art_Handoff_v2/` and the research pack at `../LAUTARA_Master/`.

```sh
uv venv -p 3.11 .venv
uv pip install -p .venv/bin/python kokoro soundfile numpy pillow opencv-python-headless pyloudnorm "misaki[en]" skia-python scipy
uv pip install -p .venv/bin/python https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl   # Kokoro's English G2P; a uv venv has no pip to fetch it itself
sh tools/fetch_fonts.sh                      # Montserrat (OFL) into fonts/montserrat
curl -sL -o assets/countries50.geojson https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson
git clone --depth 1 https://github.com/Clipwing/skills /tmp/clipwing && cp -R /tmp/clipwing/skills/real-sfx tools/real-sfx
sh build.sh tts                              # "tts" regenerates the narration (Kokoro, voice bm_lewis)
```

Stills for checking a moment: `.venv/bin/python src/film.py stills 12.5,66,145` → `out/stills/`.

## How it is made

| Part | File |
|---|---|
| Narration text (every fact sourced in `LAUTARA_Master`) | `src/script.py` |
| Narration audio, pronunciation overrides | `src/tts.py` |
| Timing: every picture event is keyed to the narration | `src/timeline.py` |
| Shots S1–S8 (documentary treatment) | `src/shots.py` (+ helpers in `src/scenes.py`) |
| Type, palette, scan-written text, footage reader | `src/gfx.py` |
| Camera, faces, render | `src/film.py` |
| Sound: cue list, skipped moments, Openverse search, Earshot listening, synthesis | `src/sfx_cues.py`, `src/ov_search.py`, `src/ear_eval.py`, `src/ear_rank.py`, `src/synth_sfx.py` |

Data rules kept everywhere: each number on screen carries MODELLED, MEASURED or DESIGN CONCEPT; no vessel, company or person is
named as a culprit; no dredging, plume or extraction polygon is drawn; the 27 Oct 2023 frame is empty because the archive searched
has no scene that day. The Kodingareng vectors are read from `LAUTARA_Master/05_Reproducibility/Depth_case_verified.json`.

## Asset record

| Asset (path) | Role | Origin / creator | Licence or basis | Changes |
|---|---|---|---|---|
| `../3d-art/revision-v2/delivery/.../media/coast-reel.mp4`, `coasts/*/travel.mp4` | Moving footage: globe, three descents | Team, Blender 3D art delivery v2 | Team work | Cold monochrome grade, slowed, scan-revealed |
| `.../coasts/*/{godview,mapview,section,detail}.png`, `globe/globe-overview.png` | Shot backgrounds | Team, Blender | Team work | Cold grade |
| `assets/amur_optical_counterexample.png` | Amur Bay 6 Sep 2023 panel | Team archive figure from Sentinel-2 L2A | Contains modified Copernicus Sentinel data 2023 | Cropped, slightly desaturated |
| `assets/countries50.geojson` | Map outlines | Natural Earth | Public domain | Drawn as coastlines |
| `fonts/montserrat/*.ttf` | All type | Montserrat Project (J. Ulanovsky et al.) | SIL OFL 1.1 | None |
| `audio/seg/*.wav` | Narration | Kokoro-82M TTS (hexgrad), voice `bm_lewis`, team script | Apache-2.0 model; AI voice disclosed in the end card | Loudness-normalised |
| `sfx/candidates/*` | Sound effects (15 creators) | Openverse → Freesound previews | CC0 1.0 (per file in `out/SFX_TABLE.md`) | Trimmed, pitched, levelled |
| `sfx/generated/gen_*.wav` | Chime, pad swell | Earshot 1.0.0 `make` | Earshot: sounds are yours to use; MIT code | Levelled |
| `sfx/generated/syn_*.wav` | Hollow tone, riser, pull-back swell | Team, `src/synth_sfx.py` (seeded numpy synthesis) | Team work | — |
| `tools/real-sfx` | Placement and mix workflow | Clipwing, github.com/Clipwing/skills | See its LICENSE | Used unmodified |

## Known limits

- The narration is synthetic (Kokoro). The end card says so. A team member reading `src/script.py` would serve the
  English-communication criterion better; drop a `audio/vo_raw.wav` recording in and run the mix steps of `build.sh`.
- Openverse supplied Freesound **preview** MP3s (~128 kbps), not the original uploads.
- Real SFX `look.py` needs an ffmpeg with `drawtext`; the Homebrew build here lacks it, so frames were checked with the
  sync sheets instead.
