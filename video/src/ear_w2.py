import glob
from earshot import rank
from earshot.describe import describe
paths = sorted(glob.glob('sfx/candidates/whoosh2_*.wav')) + ['sfx/candidates/whoosh_%d.wav' % i for i in (2, 3, 4, 5)]
for x in rank(paths, 'a soft airy whoosh transition').get('ranked', []):
    d = describe(x['path']); m = d.get('measurements', {})
    print(x['path'].split('/')[-1], x['z'], x['verdict'], 'dur', m.get('duration'), 'lufs', m.get('lufs'), 'sil', m.get('digital_silence_frac'), '|', d['summary'][:110])
