"""Independent descriptive decomposition of optical observation opportunities by rainfall."""
import argparse
import csv
from collections import defaultdict
from math import isnan
from pathlib import Path

def input_rows(path):
    with path.open() as f:
        return list(csv.DictReader(f))

def passes(rows, col):
    return sum(bool(int(r[col])) for r in rows)

def compare(rows, cutoff):
    wet=[r for r in rows if float(r["region_proxy_imerg_mm"])>=cutoff]
    dry=[r for r in rows if float(r["region_proxy_imerg_mm"])<cutoff]
    assert len(wet)+len(dry)==len(rows)
    if not wet or not dry:
        return None
    wet_acq, dry_acq = [passes(g,"either_acquired") for g in (wet,dry)]
    wet_pass, dry_pass = [passes(g,"either_pass") for g in (wet,dry)]
    assert wet_acq >= wet_pass and dry_acq >= dry_pass
    return dict(n_rain=len(wet), n_less_rain=len(dry), rain_acquired=wet_acq, less_rain_acquired=dry_acq,
        rain_pass=wet_pass,less_rain_pass=dry_pass,
        rain_acquired_pct=100*wet_acq/len(wet),
        less_rain_acquired_pct=100*dry_acq/len(dry),
        rain_pass_pct=100*wet_pass/len(wet),
        less_rain_pass_pct=100*dry_pass/len(dry),
        rain_pass_given_acquisition_pct=100*wet_pass/wet_acq if wet_acq else None,
        less_rain_pass_given_acquisition_pct=100*dry_pass/dry_acq if dry_acq else None)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("input",type=Path)
    p.add_argument("--out",type=Path,default=Path(__file__).resolve().parent/"rain_observation_decomposition.csv")
    a=p.parse_args()
    data=input_rows(a.input)
    assert len({(x["site"],x["date_utc"]) for x in data})==len(data)
    strata=defaultdict(list)
    for r in data:
        strata[(r['site'],r['date_utc'][:7])].append(r)
    output=[]
    for cutoff in (5,10,20):
        pooled=compare(data,cutoff)
        paired=[]
        for (site,month),obs in sorted(strata.items()):
            row=compare(obs,cutoff)
            if row is None:
                continue
            n1,n2=row["n_rain"],row["n_less_rain"]
            weight=n1*n2/(n1+n2)
            paired.append([weight,row["rain_pass_pct"]-row["less_rain_pass_pct"]])
            output.append(dict(threshold_mm=cutoff,site=site,month=month,**row))
        pdiff=pooled["rain_pass_pct"]-pooled["less_rain_pass_pct"]
        hold_month_site=sum(w*d for w,d in paired)/sum(w for w,_ in paired)
        print(f"{cutoff} mm: {pooled}; pooled risk difference {pdiff:.2f} percentage points; "
                f"paired descriptive difference {hold_month_site:.2f} percentage points across {len(paired)} site-month strata")
        output.append(dict(threshold_mm=cutoff,site="pooled",month="all",**pooled))
    with a.out.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)

if __name__=="__main__":
    main()
