"""STEP 3: run every Openverse candidate through Earshot in ONE process (models load once).
For each candidate: description, calibrated match to the role description, measurements (clipping, silence, tail)."""
import json, sys
from earshot.describe import describe
from earshot.match import match
DESC = {
    'whoosh': ('a soft airy whoosh transition', ['an error buzz', 'a harsh noise burst']),
    'ping': ('a sonar ping with a soft echo', ['an alarm beep', 'a phone ringtone']),
    'tick': ('a soft short UI tick', ['a loud clap', 'a mechanical rattle']),
    'hollow': ('a low soft hollow impact', ['an explosion', 'a gunshot']),
    'click': ('a single mouse click', ['a double click', 'a keyboard typing run']),
    'paper': ('a paper sheet sliding on a desk', ['tearing paper', 'a plastic bag rustle']),
    'chime': ('a soft gentle confirmation chime', ['a church bell', 'an alarm']),
    'swell': ('a slow soft ambient swell', ['a guitar chord', 'an explosion']),
    'rain': ('a single small water drop', ['an explosion', 'a glass breaking']),
    'water': ('a small water splash', ['a toilet flush', 'heavy rain']),
    'riser': ('a slow soft rising tone', ['an alarm siren', 'a scream']),
}
cands = json.load(open('sfx/candidates/openverse.json'))
out = {}
for kind, lst in cands.items():
    q, alts = DESC[kind]
    for i, c in enumerate(lst):
        if 'wav' not in c:
            continue
        d = describe(c['wav'])
        m = match(c['wav'], q, alts=alts)
        meas = d.get('measurements', {})
        out[f'{kind}_{i}'] = {'kind': kind, 'title': c['title'], 'summary': d.get('summary', '')[:400],
                              'match': m, 'measurements': meas}
        z = None
        try:
            z = m['queries'][0]['z'] if 'queries' in m else m.get('z')
        except Exception:
            pass
        print(f"{kind}_{i:<2} z={z} dur={meas.get('duration')} peak={meas.get('peak_dbfs')} lufs={meas.get('lufs')} "
              f"atk={meas.get('attack_ms')} dec={meas.get('decay_ms')} sil={meas.get('digital_silence_frac')} | {c['title'][:40]}", flush=True)
json.dump(out, open('sfx/candidates/earshot_eval.json', 'w'), indent=1, default=str)
