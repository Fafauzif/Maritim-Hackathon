import glob, json
from earshot.describe import describe
from earshot.match import match
Q = {'hollow': ('a low soft hollow impact', ['an explosion', 'a gunshot']), 'swell': ('a slow soft ambient swell', ['a guitar chord', 'fire crackling']),
     'riser': ('a slow soft rising tone', ['an alarm siren', 'a bubble pop']), 'chime': ('a soft gentle confirmation chime', ['a church bell', 'an alarm'])}
res = {}
for f in sorted(glob.glob('generated/syn_*.wav')):
    k = f.split('syn_')[1].split('_')[0].split('.')[0]
    m = match(f, Q[k][0], alts=Q[k][1]); d = describe(f); me = d.get('measurements', {})
    z = m['queries'][0]['z'] if 'queries' in m else m.get('z')
    res[f] = {'z': z, 'summary': d.get('summary', '')[:300], 'measurements': me}
    print(f, 'z=', z, 'dur', me.get('duration'), 'lufs', me.get('lufs'), '|', d.get('summary', '')[:160], flush=True)
json.dump(res, open('generated/earshot_eval_syn.json', 'w'), indent=1, default=str)
