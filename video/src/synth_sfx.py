"""Reproducible synthesis for moments Openverse and Earshot's catalogue could not cover (seeded, no samples)."""
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR = 48000
rng = np.random.default_rng(7)
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def t_(d): return np.arange(int(d * SR)) / SR
def norm(x, peak=-3): return x / np.abs(x).max() * 10 ** (peak / 20)
def fade(x, a=0.01, b=0.05):
    n = len(x); e = np.ones(n); na, nb = int(a * SR), int(b * SR)
    e[:na] = np.linspace(0, 1, na); e[n - nb:] = np.linspace(1, 0, nb); return x * e
# hollow: a struck low body (65 Hz + 2.3x partial), soft felt attack, 1.4 s ring, a breath of noise
t = t_(1.6)
env = (1 - np.exp(-t / 0.012)) * np.exp(-t / 0.45)
body = np.sin(2 * np.pi * 65 * t) + 0.35 * np.sin(2 * np.pi * 150 * t) * np.exp(-t / 0.2)
air = lp(rng.normal(0, 1, len(t)), 400) * np.exp(-t / 0.08) * 0.4
sf.write('generated/syn_hollow.wav', fade(norm((body * env + air)), 0.002, 0.3), SR)
# swell: a warm low pad (A1 + E2 + A2), slow 2.2 s rise, filtered air on top
t = t_(4.5)
env = np.clip(t / 2.2, 0, 1) ** 2 * np.exp(-np.clip(t - 2.6, 0, None) / 0.8)
pad = sum(a * np.sin(2 * np.pi * f * t + p) for f, a, p in ((55, 1, 0), (82.4, .6, 1), (110, .5, 2), (110.6, .4, 0.5)))
air = bp(rng.normal(0, 1, len(t)), 300, 1800) * 0.25
sf.write('generated/syn_swell.wav', fade(norm(pad * env + air * env, -4), 0.05, 0.6), SR)
# riser: a soft tone gliding up a fifth over 2.6 s, filtered noise rising with it
t = t_(2.8)
f = 220 * 2 ** ((7 / 12) * np.clip(t / 2.6, 0, 1))
ph = 2 * np.pi * np.cumsum(f) / SR
env = np.clip(t / 2.6, 0, 1) ** 1.5 * np.exp(-np.clip(t - 2.6, 0, None) / 0.12)
tone = np.sin(ph) + 0.3 * np.sin(2 * ph)
air = bp(rng.normal(0, 1, len(t)), 800, 4000) * 0.35 * env
sf.write('generated/syn_riser.wav', fade(norm(tone * env + air, -4), 0.05, 0.1), SR)
print('ok')
