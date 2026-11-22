import glob
from earshot import rank
sets = {
  'hollow (empty 27 Oct frame)': (sorted(glob.glob('candidates/hollow_*.wav')) + ['generated/gen_hollow.wav', 'generated/gen_hollow_deep.wav', 'generated/syn_hollow.wav'], 'a soft sub bass drop'),
  'riser (depth slider)': (sorted(glob.glob('candidates/riser_*.wav')) + ['generated/gen_riser_breath.wav', 'generated/syn_riser.wav'], 'a slow uplifter sweep'),
  'swell (three coasts / final title)': (sorted(glob.glob('candidates/swell_*.wav')) + ['generated/gen_swell_pad.wav', 'generated/gen_swell_drone.wav', 'generated/syn_swell.wav'], 'a warm ambient synth pad swell'),
}
for name, (paths, q) in sets.items():
    r = rank(paths, q)
    rows = r.get('ranked') or r.get('results') or r
    print(f'== {name}: "{q}"')
    for x in rows[:6]:
        print('  ', {k: x.get(k) for k in ('path', 'file', 'z', 'score', 'verdict') if k in x})
