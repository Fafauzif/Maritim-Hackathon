"""Recreate the example and paired sign counts from the original archived daily model cells. Python 3."""
import csv
import io
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

folder = Path(__file__).resolve().parent
with ZipFile(folder / 'LAUTARA_Coastal_Sediment_Reproducibility.zip') as bundle:
    rows = csv.DictReader(io.StringIO(bundle.read('marine/glorys_daily.csv').decode()))
    pairs = defaultdict(dict)
    for row in rows:
        if row['site'].startswith('Kodingareng') and math.isclose(float(row['lat']), -5.166667, abs_tol=0.00001) and math.isclose(float(row['lon']),119.25,abs_tol=0.00001):
            depth = round(float(row['depth_m']), 3)
            assert depth not in pairs[row['utc_day']]
            pairs[row['utc_day']][depth] = row

def sign(value):
    return 'E' if value > 0 else 'W' if value < 0 else 'zero'

counts = Counter()
for day, layers in sorted(pairs.items()):
    assert set(layers) == {0.494, 9.573}
    counts[' / '.join(sign(float(layers[depth]['east_m_s'])) for depth in sorted(layers))] += 1
assert len(pairs) == 274
assert counts['W / E'] == 96
assert sum(n for key,n in counts.items() if key.startswith('E /')) == 139
assert sum(n for key,n in counts.items() if key.endswith('/ E')) == 230
day = '2020-04-16'
for row in pairs[day].values():
    u, v = (float(row[k]) for k in ('east_m_s', 'north_m_s'))
    assert math.isclose(math.hypot(u,v),float(row['speed_m_s']),abs_tol=0.000001)
    assert math.isclose(math.degrees(math.atan2(u,v)) % 360,float(row['towards_deg']),abs_tol=0.00001)
print(json.dumps({'source':'marine/glorys_daily.csv','days':len(pairs),'start':min(pairs),'end':max(pairs),'eastward_component_sign_surface_then_deeper':counts,'example':pairs[day]},indent=2))
