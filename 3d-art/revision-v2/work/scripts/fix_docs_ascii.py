import os

base = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\delivery\LAUTARA_3D_Art_Handoff_v2"
for dirpath, _dirnames, filenames in os.walk(base):
    for name in filenames:
        if not name.endswith(".md"):
            continue
        p = os.path.join(dirpath, name)
        with open(p, encoding="utf-8") as fh:
            s = fh.read()
        s = s.replace("<= $ ", "<= ").replace(">= $ ", ">= ")
        s = s.replace("\ufffd", "")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(s)
        bad = [(i, line) for i, line in enumerate(s.splitlines(), 1)
               if "$ " in line and ("<= " in line or ">= " in line)]
        if bad:
            print("still bad", name, bad[:3])
print("done")
