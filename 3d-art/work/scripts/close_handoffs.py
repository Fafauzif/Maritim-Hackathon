"""One-off: close out the earlier handoff notes now that phases 05-06 finished."""
import io

updates = {
    r'3d-art\work\handoffs\phase-03.md': (
        'Status: **in progress — proofs equivalent across the three sites at 960×540; before/after review and 4K stills still open.**',
        'Status: **complete.** Superseded by phase-05.md (4K stills, parity sheet) and phase-06.md (export).'),
    r'3d-art\work\handoffs\phase-04.md': (
        "Status: **globe and camera rigs complete; films rendering when this note was written.**",
        'Status: **complete.** Globe still, three travel films and the connecting reel are delivered; see phase-06.md.'),
}

for path, (old, new) in updates.items():
    with io.open(path, encoding='utf-8') as fh:
        text = fh.read()
    if old not in text:
        print('ANCHOR MISSING', path)
        continue
    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(text.replace(old, new))
    print('updated', path)
