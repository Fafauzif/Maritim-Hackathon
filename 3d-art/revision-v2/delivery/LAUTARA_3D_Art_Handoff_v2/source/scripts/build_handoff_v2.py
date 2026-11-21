"""Package the v2 handoff ZIP and prove a fresh extraction.

    python build_handoff_v2.py --staging-root <bundle> --out <zip> --verify-extract <dir>
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import zipfile

BANNED = (".blend1", ".tmp", ".bak", ".pyc", ".DS_Store")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def list_files(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace("\\", "/")
            out.append(rel)
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--staging-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--verify-extract", required=True)
    ap.add_argument("--root-name", default="LAUTARA_3D_Art_Handoff_v2")
    args = ap.parse_args()
    stage = os.path.abspath(args.staging_root)
    out_zip = os.path.abspath(args.out)
    verify_dir = os.path.abspath(args.verify_extract)
    report = {"staging": stage, "out": out_zip, "verifyExtract": verify_dir}
    # clean banned artifacts
    removed = []
    for dirpath, dirnames, filenames in os.walk(stage):
        for name in filenames:
            if name.endswith(BANNED):
                p = os.path.join(dirpath, name)
                os.remove(p)
                removed.append(os.path.relpath(p, stage))
    report["removedArtifacts"] = removed
    files = list_files(stage)
    required = [
        "START_HERE.md", "HANDOFF.md", "ATTRIBUTION.md",
        "runtime/asset-manifest.json",
        "runtime/globe/globe.glb", "runtime/kit/common-kit.glb",
        "runtime/coasts/kodingareng/coast.glb",
        "runtime/coasts/kodingareng/section.glb",
        "runtime/coasts/tunda/coast.glb", "runtime/coasts/tunda/section.glb",
        "runtime/coasts/amur/coast.glb", "runtime/coasts/amur/section.glb",
        "source/globe/globe.blend", "source/kit/common-kit.blend",
        "source/coasts/kodingareng/scene.blend",
        "source/coasts/tunda/scene.blend", "source/coasts/amur/scene.blend",
        "source/BUILD.md",
        "media/globe/globe-overview.png", "media/kit/asset-sheet.png",
        "media/coast-reel.mp4",
        "media/pitch/kodingareng-surface.png",
        "media/pitch/kodingareng-deeper.png",
        "media/pitch/kodingareng-section.png",
        "evidence/depth-case-verified.json",
        "review/before-after.png", "review/parity-sheet.png",
        "review/runtime-parity.png", "review/review-report.md",
        "review/validation.json",
    ]
    for site in ("kodingareng", "tunda", "amur"):
        for slug in ("godview", "mapview", "approach", "detail", "section"):
            required.append("media/coasts/%s/%s.png" % (site, slug))
        required.append("media/coasts/%s/travel.mp4" % site)
    missing = [r for r in required if r not in files]
    report["missingRequired"] = missing
    if missing:
        print("PACKAGE FAIL missing: %s" % missing[:10])
        sys.exit(1)
    # checksum list
    sums_path = os.path.join(stage, "SHA256SUMS.txt")
    lines = []
    for rel in files:
        if rel == "SHA256SUMS.txt":
            continue
        lines.append("%s  %s" % (sha256(os.path.join(stage, rel)), rel))
    lines.sort(key=lambda s: s.split("  ", 1)[1])
    with open(sums_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    files = list_files(stage)
    report["fileCount"] = len(files)
    report["payloadBytes"] = sum(os.path.getsize(os.path.join(stage, f)) for f in files)
    # build archive atomically
    os.makedirs(os.path.dirname(out_zip), exist_ok=True)
    tmp_zip = out_zip + ".tmp"
    if os.path.exists(tmp_zip):
        os.remove(tmp_zip)
    with zipfile.ZipFile(tmp_zip, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=6) as zf:
        for rel in files:
            zf.write(os.path.join(stage, rel), arcname=args.root_name + "/" + rel)
    os.replace(tmp_zip, out_zip)
    report["zipBytes"] = os.path.getsize(out_zip)
    report["zipSha256"] = sha256(out_zip)
    # fresh extraction
    if os.path.exists(verify_dir):
        if os.listdir(verify_dir):
            raise SystemExit("verify-extract directory is not empty: " + verify_dir)
    os.makedirs(verify_dir, exist_ok=True)
    extract_problems = []
    with zipfile.ZipFile(out_zip, "r") as zf:
        names = zf.namelist()
        for n in names:
            if n.startswith("/") or ".." in n.split("/") or ":" in n.split("/")[0]:
                extract_problems.append("unsafe path " + n)
        zf.extractall(verify_dir)
    report["extractProblems"] = extract_problems
    extracted_root = os.path.join(verify_dir, args.root_name)
    extracted_files = list_files(extracted_root)
    report["extractedFileCount"] = len(extracted_files)
    report["nameSetEqual"] = bool(sorted(extracted_files) ==
                                  sorted(files))
    if not report["nameSetEqual"]:
        extract_problems.append("extracted name set differs")
        only_src = sorted(set(files) - set(extracted_files))
        only_ext = sorted(set(extracted_files) - set(files))
        report["onlyInStaging"] = only_src
        report["onlyInExtract"] = only_ext
    # checksums
    bad = []
    with open(os.path.join(extracted_root, "SHA256SUMS.txt"), encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            digest, rel = line.split("  ", 1)
            p = os.path.join(extracted_root, rel.replace("/", os.sep))
            if not os.path.isfile(p) or sha256(p) != digest:
                bad.append(rel)
    report["badChecksums"] = bad
    if bad:
        extract_problems.append("bad checksums: %s" % bad[:8])
    # manifest and embedded-resource sanity from the extracted copy
    try:
        man = json.load(open(os.path.join(extracted_root, "runtime",
                                          "asset-manifest.json"), encoding="utf-8"))
        report["manifestAssets"] = len(man.get("assets", []))
        raw = json.dumps(man)
        report["manifestAbsolutePaths"] = bool(
            __import__("re").search(r"[A-Za-z]:\\\\|/Users/|/home/", raw))
    except Exception as exc:
        extract_problems.append("manifest read failed: %s" % exc)
    report["verdict"] = "pass" if not extract_problems else "fail"
    report["errors"] = extract_problems
    log_dir = os.path.join(os.path.dirname(os.path.dirname(out_zip)), "..", "work", "runs")
    # write next to the archive's sibling review folder for a stable record
    report_path = os.path.join(verify_dir, "package-report.json")
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print("PACKAGE " + json.dumps({"zip": out_zip, "bytes": report["zipBytes"],
                                    "files": report["fileCount"],
                                    "extracted": report["extractedFileCount"],
                                    "verdict": report["verdict"]}))
    if extract_problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
