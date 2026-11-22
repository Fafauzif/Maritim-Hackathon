"""STEP 1 + 4: the moment list from the project's own timeline, the chosen sound per moment, the skipped moments."""
import json, sys
sys.path.insert(0, 'src')
from timeline import build
tl = build(); T, D, S = tl['T'], tl['D'], tl['start']
V = '/Users/danferdiansyah/Development/Maritim-Hackathon/video'
C = lambda n: f'{V}/sfx/candidates/{n}.wav'
G = lambda n: f'{V}/sfx/generated/{n}.wav'
out_t = T['e3'] + D['e3'] + 0.6
cues = [  # (t, label, file, role, extra)
 (0.30, 'scan sweeps across the globe', C('whoosh_3'), 'whoosh', {'gain_db': -7, 'anchor': 'start'}),
 (T['o2'] - 0.8, 'scan wipe: globe to Pulau Tunda', C('whoosh_5'), 'whoosh', {'gain_db': -3}),
 (T['o3'] + 1.15, 'inspection marker appears (warm)', C('ping_0'), 'chime', {'gain_db': -4, 'anchor': 'start'}),
 (T['o4'] + 1.4, '26 Oct scene frame', C('tick_4'), 'click', {'gain_db': 0}),
 (T['o4'] + 3.0, '31 Oct scene frame', C('tick_2'), 'click', {'gain_db': -2}),
 (T['o4'] + 5.6, 'empty 27 Oct frame (hero)', G('syn_hollow'), 'hit', {'gain_db': -9, 'anchor': 'start'}),
 (S['S2'] - 0.5, 'camera move to the title and team', C('whoosh_4'), 'whoosh', {'gain_db': -4}),
 (T['t2'] - 0.4, 'the answer frame opens (hero)', G('gen_swell_pad'), 'riser', {'gain_db': -4, 'anchor': 'start', 'max_dur': 4.0}),
 (S['S3'] - 0.3, 'scan rewrites the frame to the globe figure', C('ping_1'), 'chime', {'gain_db': -9, 'anchor': 'start', 'max_dur': 1.4}),
 (T['c1'] + 6.0 + 13 * 0.05, 'the one clear Tunda date lights', C('rain_0'), 'pop', {'gain_db': 0, 'anchor': 'start'}),
 (T['c2'] + 0.6 + 41 * 0.03, 'the one usable rainy day lights', C('rain_3'), 'pop', {'gain_db': 4, 'anchor': 'start', 'pitch': -2}),
 (S['S4'] - 0.5, 'descent to Kodingareng Lompo', C('whoosh_3'), 'whoosh', {'gain_db': -8, 'anchor': 'start', 'pitch': -3}),
 (T['d2'] - 0.6, 'scan wipe to the overhead view', C('ping_2'), 'chime', {'gain_db': -12, 'anchor': 'start', 'max_dur': 1.8}),
 (T['d2'] + 2.0, 'current dial appears', C('ping_3'), 'chime', {'gain_db': -8, 'anchor': 'start', 'max_dur': 1.6}),
 (T['d3'] + 0.2, 'depth slider; arrow turns W to NE (hero)', G('syn_riser'), 'riser', {'gain_db': 1, 'anchor': 'start'}),
 (T['d4'] + 0.6, '96/274 reading', C('tick_0'), 'click', {'gain_db': -1, 'max_dur': 0.2}),
 (S['S5'] - 0.7, 'orbit into section A-B', C('whoosh_2'), 'whoosh', {'gain_db': -6, 'pitch': -4, 'fit_dur': 0.8}),
 (T['p2'] + 6.4, 'sample-depth marker drops to 9.6 m', C('rain_3'), 'pop', {'gain_db': 3, 'anchor': 'start', 'pitch': -5}),
 (T['p4'] + 0.4, '+ Request field check (hero)', C('click_3'), 'click', {'gain_db': 6, 'slice': 'first'}),
 (T['p4'] + 1.0, 'field brief opens', C('paper_0'), 'paper', {'gain_db': 3}),
 (T['p4'] + 7.0, 'supervisor signs', G('gen_chime'), 'chime', {'gain_db': -6}),
 (T['p4'] + 9.0, 'readings return to the case (hero)', C('water_1'), 'foley', {'gain_db': 3}),
 (S['S6'] - 0.5, 'descent to Amur Bay', C('whoosh2_5'), 'whoosh', {'gain_db': -7, 'pitch': -3}),
 (T['r2'] - 0.5, 'scan wipe to the archive scene', C('ping_1'), 'chime', {'gain_db': -8, 'anchor': 'start', 'max_dur': 1.4, 'pitch': -2}),
 (T['r2'] + 8.2, 'Sentinel-2 bar grows', C('tick_4'), 'click', {'gain_db': -1}),
 (T['r2'] + 8.7, 'Landsat 9 bar grows', C('tick_2'), 'click', {'gain_db': -3, 'pitch': -2}),
 (T['r3'] + 0.8, '12 Jul bar grows', C('tick_0'), 'click', {'gain_db': 4, 'pitch': -2, 'max_dur': 0.2}),
 (T['r4'] + 0.2, 'three branches link the coasts (hero)', G('gen_swell_pad'), 'riser', {'gain_db': -6, 'anchor': 'start', 'max_dur': 3.5, 'pitch': 2}),
 (S['S7'] - 0.45, 'pull back to the planet', G('syn_swell'), 'riser', {'gain_db': -1, 'anchor': 'start', 'max_dur': 3.2}),
 (out_t + 0.6, 'title written on (hero)', C('ping_0'), 'chime', {'gain_db': -6, 'anchor': 'start'}),
]
skipped = [
 (T['o2'] + 3.6, '≈24,000 m³ reading', 'the voice says the number at the same moment'),
 (T['o3'] + 0.2, 'archive timeline draws', '0.7 s before the inspection ping, which carries the moment'),
 (S['S2'] + 0.4, 'film title written on', '0.9 s after the camera-move whoosh; a second sound would crowd it'),
 (T['t1'], 'four photo slots, one per name', 'the voice speaks each name as its slot appears'),
 (T['t2'] + 5.6, '"A blind spot." written on', 'the voice carries the line; the swell already marks the frame'),
 (T['g1'] + 1.0, '4–8 digits count up', 'the voice says the figure'),
 (T['c1'] + 12.6, 'Kodingareng row, none lit', 'silence is the point: nothing is seen'),
 (T['c1'] - 0.9, 'pan down to the cloudy record', 'a small in-shot pan under continuous voice; a ninth whoosh would repeat the pool'),
 (T['p3'] + 1.6, 'MODELLED / MEASURED / MISSING labels', 'the voice reads the three labels'),
 (T['r4'] + 0.6, 'case-review panel', '0.4 s after the branch swell (0.5 s rule)'),
 (S['S8'] - 0.4, 'move to the end card', 'credits; the title ping and its tail close the film'),
]
cues.sort(key=lambda c: c[0])
for a, b in zip(cues, cues[1:]):
    assert b[0] - a[0] >= 0.5, (a[1], b[1], b[0] - a[0])
sheet = {'video': f'{V}/out/picture_with_voice.mp4', 'keep_audio': 'yes',
         'cues': [{'t': round(t, 3), 'label': lab, 'file': f, 'role': r, **x} for t, lab, f, r, x in cues]}
os.makedirs('sfx/work', exist_ok=True) if 'os' in dir() else None
import os; os.makedirs('sfx/work', exist_ok=True)
json.dump(sheet, open('sfx/work/cues.json', 'w'), indent=1)
json.dump([{'t': round(t, 3), 'moment': m, 'why_skipped': w} for t, m, w in skipped], open('sfx/work/skipped.json', 'w'), indent=1)
# sync evidence (optional): nearest picture moment found by real-sfx find_moments for every cue
import os
if not os.path.exists('sfx/work/moments/moments.json'):
    print(f'{len(cues)} cues, {len(skipped)} skipped (run real-sfx find_moments.py for the sync evidence)'); sys.exit(0)
mom = json.load(open('sfx/work/moments/moments.json'))
mts = sorted(m['t'] for m in (mom['moments'] if isinstance(mom, dict) else mom))
near = [min(mts, key=lambda m: abs(m - c[0])) - c[0] for c in cues]
hit = sum(abs(d) <= 0.25 for d in near)
print(f'{len(cues)} cues, {len(skipped)} skipped; {hit}/{len(cues)} cues have a find_moments picture event within 0.25 s')
for c, d in zip(cues, near):
    if abs(d) > 0.25: print(f'  no picture event within 0.25 s: {c[0]:.2f} {c[1]} (nearest {d:+.2f} s)')
