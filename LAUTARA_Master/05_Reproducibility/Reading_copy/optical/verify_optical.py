#!/usr/bin/env python3
"""Verify dates, percentages and headline opportunity calculations from final tables."""
from pathlib import Path
import pandas as pd
from summarize import row_summary

p=Path(__file__).resolve().parent
s=pd.read_csv(p/"sentinel_longitudinal.csv",parse_dates=["date"])
l=pd.read_csv(p/"landsat_longitudinal.csv",parse_dates=["date"])
assert len(s)==1178 and s.status.eq("ok").sum()==1177
assert len(l)==799 and l.status.eq("ok").sum()==799
assert not s.duplicated(["site","date"]).any()
assert not l.duplicated(["site","id"]).any()
for d in (s,l):
    q=d[d.status.eq("ok")]
    assert q.clear_pct.between(0,100).all()
    assert q.water_pct.between(0,100).all()
    assert q.clear_pct.ge(q.water_pct).all()
    assert q.n_pixels.gt(0).all()
    assert q.date.between("2019-01-01","2026-10-31").all()
    assert q.groupby(d.site).apply(lambda z:z.date.lt('2025-01-01').any(),include_groups=False).all()
old=pd.read_csv(p/"sentinel_pilot_input.csv",parse_dates=["date"])
overlap=s.merge(old,on=["site","date"],suffixes=("_full","_prior"))
assert len(overlap)==len(old)==116
assert overlap.clear_pct_full.sub(overlap.clear_pct_prior).abs().max()<0.000001
assert overlap.water_pct_full.sub(overlap.water_pct_prior).abs().max()<0.000001
br=row_summary(pd.concat([s,l],ignore_index=True))
v=br[(br.window=="all_matched")&(br.threshold==90)&(br.metric=="clear_pct")].set_index("site")
assert v.loc["Tunda","landsat_added"]==15
assert v.loc["Kodingareng Lompo","landsat_added"]==25
assert v.loc["Tunda","combined_max_unqualified_run_days"]==131
assert v.loc["Kodingareng Lompo","combined_max_unqualified_run_days"]==158
r=s[s.site=="Tunda"]
assert (r.clear_pct.ge(90) & r.reef_clear_pct.lt(90)).sum()==10
assert (r.clear_pct.lt(90) & r.reef_clear_pct.ge(90)).sum()==24
print("PASS all site, date, raster, prior-audit, cross-sensor and habitat checks")
print("1177/1178 Sentinel-2 date quality masks; 799/799 Landsat products; 116 prior audited site-dates reproduced")
