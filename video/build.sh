#!/bin/sh
# Rebuild the film from source. Usage: sh build.sh [tts]   (pass "tts" to regenerate the narration first)
set -e
cd "$(dirname "$0")"
PY=.venv/bin/python
RS=${REAL_SFX:-tools/real-sfx}          # the Real SFX skill folder (github.com/Clipwing/skills, skills/real-sfx)
[ "$1" = "tts" ] && $PY src/tts.py
$PY src/timeline.py
$PY src/mix_vo.py
ffmpeg -y -v error -i audio/vo_raw.wav -af "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=7" -ar 48000 audio/vo_master.wav
rm -rf out/chunks && $PY src/film.py render
ffmpeg -y -v error -i out/silent.mp4 -i audio/vo_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 21 -maxrate 5M -bufsize 10M \
  -tune animation -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out/picture_with_voice.mp4
$PY src/sfx_cues.py
mkdir -p sfx/result
HERE=$(pwd)
(cd "$RS" && "$HERE/$PY" scripts/mix.py "$HERE/sfx/work/cues.json" --out "$HERE/sfx/result/final_sfx.mp4" --voice-safe --target-lufs -14)
cp sfx/result/final_sfx.mp4 out/LAUTARA_OceanHasFloors_FINAL.mp4
cp sfx/result/final_sfx_sfx_track_in_mix_level.wav out/LAUTARA_OceanHasFloors_SFX_only.wav
$PY src/extras.py > /dev/null
echo "done: out/LAUTARA_OceanHasFloors_FINAL.mp4"
