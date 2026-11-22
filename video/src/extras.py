import sys; sys.path.insert(0, 'src')
from timeline import build
from script import SEGMENTS
tl = build(); T, D, S = tl['T'], tl['D'], tl['start']
def ts(x, sep=','):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'.replace('.', sep)
# subtitles: split long segments at sentence boundaries, timed by character share
import re
out, n = [], 1
for sc, sid, text, _ in SEGMENTS:
    parts = [p for p in re.split(r'(?<=[.?!:])\s+', text) if p]
    tot = sum(len(p) for p in parts); t = T[sid]
    for p in parts:
        d = D[sid] * len(p) / tot
        out.append(f'{n}\n{ts(t)} --> {ts(t + d)}\n{p}\n'); n += 1; t += d
open('out/LAUTARA_OceanHasFloors.en.srt', 'w').write('\n'.join(out))
cues = [
 (0.3, 'Scan sweeps across the globe', 'low air surge + soft sonar ping'),
 (T['o2'] - 0.8, 'Scan wipe: globe to Pulau Tunda descent', 'airy surge, wind ambience starts'),
 (T['o2'] + 3.6, '≈24,000 m³ reading written on', 'faint data tick'),
 (T['o3'] + 0.2, 'Archive timeline draws across', 'thin tonal sweep'),
 (T['o3'] + 0.9, 'Inspection marker (warm)', 'single sonar ping with two quiet echoes'),
 (T['o4'] + 1.4, '26 Oct scene frame', 'soft tick'),
 (T['o4'] + 3.0, '31 Oct scene frame', 'soft tick'),
 (T['o4'] + 5.6, 'Empty 27 Oct frame (hero)', 'hollow low tone, near-silence after'),
 (S['S2'] - 0.5, 'Camera move to the team', 'air surge'),
 (T['t1'], 'Four photo slots written on', 'four soft ticks, one per name'),
 (T['t2'] + 5.6, '“What we cannot see.”', 'leave empty: voice carries it'),
 (S['S3'] - 0.5, 'Move to the globe figure', 'air surge'),
 (T['g1'] + 1.0, '4–8 digits count up', 'light ticks'),
 (T['c1'] - 0.9, 'Pan down to the cloudy record', 'soft whoosh'),
 (T['c1'] + 6.0, 'Tunda row, one lit', 'tick run + one clean ping'),
 (T['c1'] + 12.6, 'Kodingareng row, none lit', 'tick run, no ping'),
 (T['c2'] + 0.6, '72 rainy days fill', 'rain-like tick run'),
 (S['S4'] - 0.5, 'Descent to Kodingareng Lompo', 'wind + low swell'),
 (T['d2'] - 0.6, 'Scan wipe to the overhead view', 'air surge'),
 (T['d2'] + 2.0, 'Dial appears', 'sonar ping'),
 (T['d3'] + 0.2, 'Depth slider, arrow turns W→NE (hero)', 'slow rising tone, 2.6 s'),
 (T['d4'] + 0.6, '96/274 reading', 'soft low pulse'),
 (S['S5'] - 0.7, 'Orbit into section A–B', 'long air surge'),
 (T['p2'] + 6.4, 'Sample depth marker drops to 9.6 m', 'descending soft blip'),
 (T['p4'] + 0.4, '+ Request field check (hero)', 'clean click'),
 (T['p4'] + 1.0, 'Field brief opens', 'paper swoosh'),
 (T['p4'] + 7.0, 'Supervisor signs', 'soft confirm tone'),
 (T['p4'] + 9.0, 'Readings return to the case (hero)', 'gentle water + swell'),
 (S['S6'] - 0.5, 'Descent to Amur Bay', 'wind ambience, colder'),
 (T['r2'] - 0.5, 'Scan wipe to the archive scene', 'air surge'),
 (T['r2'] + 8.2, 'Bars grow', 'two light ticks'),
 (T['r3'] + 0.8, '12 Jul bar', 'light tick'),
 (T['r4'] + 0.2, 'Three branches link the coasts (hero)', 'triple soft swell'),
 (S['S7'] - 0.5, 'Pull back to the planet', 'long low swell'),
 (T['e3'] + 4.6, 'Title written on (hero)', 'warm chord, let it ring'),
]
with open('out/SFX_CUES.md', 'w') as f:
    f.write('| # | Time | Moment | Suggested sound |\n|---|---|---|---|\n')
    for i, (t, m, s) in enumerate(cues, 1):
        f.write(f'| {i} | {int(t // 60)}:{t % 60:06.3f} | {m} | {s} |\n')
print(open('out/SFX_CUES.md').read())
