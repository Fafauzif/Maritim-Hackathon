"""Search Openverse (official API, anonymous) for each sound kind; download 3+ distinct CC0 candidates and record provenance."""
import json, subprocess, sys, time, urllib.parse, urllib.request
QUERIES_ALL = {
    'whoosh2': ['wind whoosh', 'air swoosh', 'swish'], 'ping': ['sonar ping'], 'tick': ['soft tick', 'ui tick'],
    'hollow': ['low boom', 'deep impact', 'sub drop'], 'click': ['mouse click'], 'paper': ['paper slide'],
    'chime': ['chime', 'bell ding', 'notification'], 'swell': ['soft swell', 'pad swell', 'drone', 'ambient swell'], 'rain': ['rain', 'drops', 'water drip'], 'water': ['water splash small'],
    'riser': ['soft riser', 'riser', 'rising tone'],
}
import sys as _s
QUERIES = {k: v for k, v in QUERIES_ALL.items() if len(_s.argv) < 2 or k in _s.argv[1].split(',')}
UA = {'User-Agent': 'lautara-video-sfx/1.0 (student competition video)'}
out = {}
for kind, qs in QUERIES.items():
    seen, picks = set(), []
    for q in qs:
        url = 'https://api.openverse.org/v1/audio/?' + urllib.parse.urlencode({'q': q, 'license': 'cc0', 'page_size': 12})
        d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))
        for r in d.get('results', []):
            dur = (r.get('duration') or 0) / 1000
            if r['id'] in seen or dur <= 0 or dur > (9 if kind in ('swell', 'rain', 'riser', 'hollow') else 3.5):
                continue
            seen.add(r['id'])
            picks.append({k: r.get(k) for k in ('id', 'title', 'creator', 'creator_url', 'url', 'foreign_landing_url', 'license', 'license_version', 'license_url', 'attribution', 'filetype', 'duration', 'provider', 'source')} | {'query': q})
        time.sleep(1.2)
    picks = picks[:6 if kind in ('whoosh', 'whoosh2', 'tick', 'ping', 'swell') else 4]
    for i, p in enumerate(picks):
        ext = (p.get('filetype') or 'mp3')
        fn = f'sfx/candidates/{kind}_{i}.{ext}'
        try:
            urllib.request.urlretrieve(p['url'], fn) if False else open(fn, 'wb').write(urllib.request.urlopen(urllib.request.Request(p['url'], headers=UA), timeout=60).read())
            wav = fn.rsplit('.', 1)[0] + '.wav'
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', fn, '-ar', '48000', '-ac', '2', wav], check=True)
            dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav]))
            p.update(file=fn, wav=wav, measured_duration=round(dur, 3), preview='/previews/' in p['url'])
        except Exception as e:
            p.update(error=str(e))
        time.sleep(0.6)
    out[kind] = picks
    print(kind, [(p.get('title'), p.get('measured_duration'), p.get('preview')) for p in picks], flush=True)
import os
prev = json.load(open('sfx/candidates/openverse.json')) if os.path.exists('sfx/candidates/openverse.json') else {}
prev.update({k: v for k, v in out.items() if v})
json.dump(prev, open('sfx/candidates/openverse.json', 'w'), indent=1)
