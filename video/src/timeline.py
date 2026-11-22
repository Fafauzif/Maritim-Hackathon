"""Builds the shot timeline from the real voice-over segment durations."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from script import SEGMENTS
import soundfile as sf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD = 2.2        # globe fades up from black before the first line
GAP = 1.1         # extra camera-flight time between scenes
S7_TAIL = 4.0     # title lock-up after the last line
ENDCARD = 10.0

def build():
    T, D, scenes = {}, {}, {}
    t, prev = LEAD, None
    for scene, sid, text, pause in SEGMENTS:
        if prev and scene != prev:
            t += GAP
        d = sf.info(f'{ROOT}/audio/seg/{sid}.wav').duration
        T[sid], D[sid] = t, d
        scenes.setdefault(scene, [t, t + d])
        scenes[scene][1] = t + d
        t += d + pause
        prev = scene
    names = list(scenes)
    start = {n: (0.0 if i == 0 else scenes[n][0] - GAP * 0.6) for i, n in enumerate(names)}
    end = {n: (start[names[i + 1]] if i + 1 < len(names) else t + S7_TAIL) for i, n in enumerate(names)}
    start['S8'] = end['S7']; end['S8'] = end['S7'] + ENDCARD
    return dict(T=T, D=D, start=start, end=end, total=end['S8'])

if __name__ == '__main__':
    tl = build()
    os.makedirs(f'{ROOT}/out', exist_ok=True)
    json.dump(tl, open(f'{ROOT}/out/timeline.json', 'w'), indent=1)
    for k in tl['start']: print(k, round(tl['start'][k], 2), round(tl['end'][k], 2))
    print('total', round(tl['total'], 2))
