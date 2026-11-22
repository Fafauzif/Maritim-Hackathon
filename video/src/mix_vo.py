import json, numpy as np, soundfile as sf, os, sys
sys.path.insert(0, 'src')
from timeline import build
tl = build(); SR = 48000
out = np.zeros(int(tl['total'] * SR) + SR)
for sid, t in tl['T'].items():
    a, sr = sf.read(f'audio/seg/{sid}.wav')
    a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
    i = int(t * SR); out[i:i + len(a)] += a
sf.write('audio/vo_raw.wav', out.astype(np.float32), SR)
