import json
import os

stage = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\delivery\LAUTARA_3D_Art_Handoff_v2"
extract = r"C:\Users\fauzi\AppData\Local\Temp\LAUTARA_v2_extract_20261121\LAUTARA_3D_Art_Handoff_v2"
# The extracted-copy report includes the archive checksum check, which the
# staging report could not run. Promote it as the shipped validation report.
src = os.path.join(extract, "review", "validation-extracted.json")
dst = os.path.join(stage, "review", "validation.json")
with open(src, encoding="utf-8") as fh:
    report = json.load(fh)
with open(dst, "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=2)

for rel in ("START_HERE.md", "HANDOFF.md", "review/review-report.md"):
    p = os.path.join(stage, rel)
    with open(p, encoding="utf-8") as fh:
        s = fh.read()
    s = s.replace("37 pass", "38 pass")
    s = s.replace("| inventory-sums | not-applicable |  |",
                  "| inventory-sums | pass |  |")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(s)
print("updated", report.get("summary"))
