"""One-off: correct the reel duration and travel-camera description in the handoff."""
p = r'3d-art\output\review\handoff.md'
with open(p, encoding='utf-8') as fh:
    s = fh.read()

before = s
s = s.replace('Earth to each coast and back, 22.5 s, 1920x1080 24 fps',
              'Earth to each coast and back, 20.5 s, 1920x1080 24 fps')
s = s.replace('the film path (16 mm for the reel? no: 58 mm, animated)',
              'animated film path: overview -> approach -> lateral -> push')
with open(p, 'w', encoding='utf-8') as fh:
    fh.write(s)
print('changed' if s != before else 'NO CHANGE')
for line in s.splitlines():
    if '20.5 s' in line or 'TRAVEL_CAM' in line:
        print(line)
