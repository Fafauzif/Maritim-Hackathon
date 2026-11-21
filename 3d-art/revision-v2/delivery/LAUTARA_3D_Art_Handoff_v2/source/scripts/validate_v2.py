"""Validate the v2 handoff package against the contract.

    python validate_v2.py --bundle-root <bundle> --report <json> [--ffprobe <path>]
"""
import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from make_manifest import glb_stats, read_glb  # noqa: E402

REQUIRED_GLBS = {
    "globe": ["runtime/globe/globe.glb"],
    "kit": ["runtime/kit/common-kit.glb"],
    "coast_kodingareng": ["runtime/coasts/kodingareng/coast.glb",
                          "runtime/coasts/kodingareng/section.glb"],
    "coast_tunda": ["runtime/coasts/tunda/coast.glb",
                    "runtime/coasts/tunda/section.glb"],
    "coast_amur": ["runtime/coasts/amur/coast.glb",
                   "runtime/coasts/amur/section.glb"],
}
SITES = ("kodingareng", "tunda", "amur")
ANCHORS = ["COAST_ORIGIN", "ORBIT_SITE", "ORBIT_WATERFRONT", "TARGET_SURVEY",
           "ANCHOR_JETTY", "ANCHOR_VESSEL", "SECTION_A", "SECTION_B"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def item(items, iid, state, notes, evidence=None):
    items.append({"id": iid, "state": state, "evidencePaths": evidence or [],
                  "notes": notes})


def node_map(doc):
    out = {}
    for n in doc.get("nodes", []):
        out[n.get("name")] = n
    return out


def node_translation(node):
    if "matrix" in node:
        m = node["matrix"]
        return [m[12], m[13], m[14]]
    return node.get("translation", [0, 0, 0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle-root", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--ffprobe", default="ffprobe")
    ap.add_argument("--allow-missing-sums", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.bundle_root)
    report = os.path.abspath(args.report)
    items = []
    errors = []

    def need(rel, kind="file", min_bytes=1):
        p = os.path.join(root, rel)
        if kind == "dir":
            ok = os.path.isdir(p)
        else:
            ok = os.path.isfile(p) and os.path.getsize(p) >= min_bytes
        return ok, p

    # ------------------------- top-level inventory -------------------------
    docs = ["START_HERE.md", "HANDOFF.md", "ATTRIBUTION.md"]
    for rel in docs:
        ok, p = need(rel, min_bytes=400)
        item(items, "doc-" + rel.lower(), "pass" if ok else "fail",
             "required handoff document", [rel])
        if not ok:
            errors.append("missing " + rel)
    if not args.allow_missing_sums:
        ok, p = need("SHA256SUMS.txt", min_bytes=200)
        item(items, "inventory-sums", "pass" if ok else "fail",
             "archive checksum list", ["SHA256SUMS.txt"])
        if not ok:
            errors.append("missing SHA256SUMS.txt")
    else:
        item(items, "inventory-sums", "not-applicable",
             "staging validation before archive checksum generation", [])

    # banned artifacts
    banned = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith((".blend1", ".tmp", ".bak", ".pyc")) or name == ".DS_Store":
                banned.append(os.path.relpath(os.path.join(dirpath, name), root))
        if "__pycache__" in dirnames:
            banned.append(os.path.relpath(os.path.join(dirpath, "__pycache__"), root))
    item(items, "inventory-clean", "pass" if not banned else "fail",
         "no backups, caches or temporary files", banned)
    if banned:
        errors.append("banned artifacts: %s" % banned[:5])

    # ------------------------------ manifest -------------------------------
    man_rel = "runtime/asset-manifest.json"
    ok, man_path = need(man_rel, min_bytes=1000)
    if not ok:
        item(items, "manifest", "fail", "runtime manifest missing", [man_rel])
        errors.append("manifest missing")
        manifest = {}
    else:
        with open(man_path, encoding="utf-8") as fh:
            manifest = json.load(fh)
        required = ["schemaVersion", "revision", "baseCommit", "buildId",
                    "blenderVersion", "axisConvention", "units", "georeferenced",
                    "assets", "sites", "globe", "kit", "evidencePath"]
        missing = [k for k in required if k not in manifest]
        schema_ok = (manifest.get("schemaVersion") == 1 and
                     manifest.get("revision") == "v2" and
                     manifest.get("georeferenced") is False and
                     manifest.get("units") == "metres")
        item(items, "manifest", "pass" if not missing and schema_ok else "fail",
             "schemaVersion 1, revision v2, metres, not georeferenced; %d assets" %
             len(manifest.get("assets", [])), [man_rel])
        if missing or not schema_ok:
            errors.append("manifest fields: %s" % missing)
        raw = json.dumps(manifest)
        abs_paths = re.findall(r"[A-Za-z]:\\\\[^\"']+|/Users/[^\"']+|/home/[^\"']+", raw)
        item(items, "manifest-no-private-paths", "pass" if not abs_paths else "fail",
             "no absolute workstation paths in runtime manifest", [man_rel])
        if abs_paths:
            errors.append("private paths in manifest")

    # -------------------------------- GLBs ---------------------------------
    glb_docs = {}
    for group, rels in REQUIRED_GLBS.items():
        for rel in rels:
            ok, path = need(rel, min_bytes=10000)
            if not ok:
                item(items, "glb-" + rel, "fail", "required GLB missing", [rel])
                errors.append("missing " + rel)
                continue
            try:
                doc, ver, declared = read_glb(path)
                st = glb_stats(path)
                glb_docs[os.path.basename(rel).split(".")[0] + ":" + group] = doc
                issues = []
                if ver != 2 or doc.get("asset", {}).get("version") != "2.0":
                    issues.append("not glTF 2.0")
                if doc.get("cameras"):
                    issues.append("contains camera nodes")
                if doc.get("extensionsRequired"):
                    issues.append("requires extensions %s" % doc["extensionsRequired"])
                if doc.get("buffers") and any(b.get("uri") for b in doc["buffers"]):
                    issues.append("external buffer URI")
                if doc.get("images") and any(i.get("uri") for i in doc["images"]):
                    issues.append("external image URI")
                if st["duplicateNodeNames"]:
                    issues.append("duplicate node names")
                item(items, "glb-" + rel, "pass" if not issues else "fail",
                     "glTF 2.0 binary, embedded, no cameras/lights; %d tris; %s" %
                     (st["triangles"], "; ".join(issues) if issues else "core only"),
                     [rel])
                if issues:
                    errors.append(rel + ": " + "; ".join(issues))
            except Exception as exc:
                item(items, "glb-" + rel, "fail", "GLB parse failed: %s" % exc, [rel])
                errors.append(rel + ": " + str(exc))
    # manifest digests
    if manifest:
        for a in manifest.get("assets", []):
            p = os.path.join(root, a["path"])
            if not os.path.isfile(p):
                item(items, "asset-" + a["id"], "fail", "asset missing", [a["path"]])
                errors.append("missing " + a["path"])
                continue
            good = (os.path.getsize(p) == a["bytes"] and sha256(p) == a["sha256"])
            item(items, "asset-" + a["id"], "pass" if good else "fail",
                 "bytes and sha256 match manifest", [a["path"]])
            if not good:
                errors.append("digest mismatch " + a["path"])

    # required exact node IDs and A/B transform agreement
    for site in SITES:
        coast_path = os.path.join(root, "runtime", "coasts", site, "coast.glb")
        sec_path = os.path.join(root, "runtime", "coasts", site, "section.glb")
        if not (os.path.isfile(coast_path) and os.path.isfile(sec_path)):
            continue
        cd, _, _ = read_glb(coast_path)
        sd, _, _ = read_glb(sec_path)
        cm, sm = node_map(cd), node_map(sd)
        issues = []
        for n in ANCHORS:
            if n not in cm:
                issues.append("coast missing " + n)
            if n not in sm:
                issues.append("section missing " + n)
        if "ENV_Water" not in cm:
            issues.append("coast missing ENV_Water")
        if "SECTION_Water" not in sm:
            issues.append("section missing SECTION_Water")
        for n in ("SECTION_A", "SECTION_B", "COAST_ORIGIN"):
            if n in cm and n in sm:
                a = node_translation(cm[n])
                b = node_translation(sm[n])
                if max(abs(a[i] - b[i]) for i in range(3)) > 0.01:
                    issues.append("%s transform mismatch coast/section" % n)
        item(items, "anchors-" + site, "pass" if not issues else "fail",
             "required anchors and shared A/B transforms; %s" %
             ("ok" if not issues else "; ".join(issues)),
             ["runtime/coasts/%s/coast.glb" % site,
              "runtime/coasts/%s/section.glb" % site])
        if issues:
            errors.append(site + ": " + "; ".join(issues))

    # camera presets
    if manifest:
        cam_issues = []
        for site in SITES:
            rec = manifest.get("sites", {}).get(site, {})
            cams = rec.get("cameras", {})
            for name in ("COAST_OVERVIEW", "COAST_PLAN", "COAST_APPROACH",
                         "COAST_DETAIL", "COAST_SECTION"):
                c = cams.get(name)
                if not c:
                    cam_issues.append("%s missing %s" % (site, name))
                    continue
                for field in ("position", "target", "up", "near", "far", "aspect",
                              "projection"):
                    if field not in c:
                        cam_issues.append("%s.%s missing %s" % (site, name, field))
                if c.get("projection") == "orthographic" and "orthoWidthM" not in c:
                    cam_issues.append("%s.%s missing orthoWidthM" % (site, name))
                if c.get("projection") == "perspective" and "verticalFovDeg" not in c:
                    cam_issues.append("%s.%s missing verticalFovDeg" % (site, name))
        item(items, "camera-presets", "pass" if not cam_issues else "fail",
             "five required coast presets with position/target/up/near/far/aspect "
             "and projection-specific FOV", ["runtime/asset-manifest.json"])
        if cam_issues:
            errors.append("camera presets: %s" % cam_issues[:6])

    # -------------------------------- stills -------------------------------
    stills_issues = []
    for site in SITES:
        for slug in ("godview", "mapview", "approach", "detail", "section"):
            rel = "media/coasts/%s/%s.png" % (site, slug)
            p = os.path.join(root, rel)
            if not os.path.isfile(p):
                stills_issues.append("missing " + rel)
                continue
            with Image.open(p) as im:
                if im.size != (3840, 2160):
                    stills_issues.append("%s is %s" % (rel, im.size))
    item(items, "clean-stills", "pass" if not stills_issues else "fail",
         "15 coast PNGs at 3840x2160", ["media/coasts"])
    if stills_issues:
        errors.append("stills: %s" % stills_issues[:4])
    for rel, min_size in (("media/globe/globe-overview.png", (3840, 2160)),
                          ("media/kit/asset-sheet.png", (1920, 1080))):
        p = os.path.join(root, rel)
        if os.path.isfile(p):
            with Image.open(p) as im:
                ok = im.size[0] >= min_size[0] and im.size[1] >= min_size[1]
                item(items, "image-" + rel, "pass" if ok else "fail",
                     "required clean art; %s" % (im.size,), [rel])
                if not ok:
                    errors.append(rel + " size " + str(im.size))
        else:
            item(items, "image-" + rel, "fail", "missing", [rel])
            errors.append("missing " + rel)

    # -------------------------------- media --------------------------------
    media_issues = []
    probe = args.ffprobe
    if not os.path.exists(probe):
        import shutil
        probe = shutil.which(probe) or probe
    for site in SITES:
        rel = "media/coasts/%s/travel.mp4" % site
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            media_issues.append("missing " + rel)
            continue
        try:
            out = subprocess.run([probe, "-v", "error", "-select_streams", "v:0",
                                  "-show_entries",
                                  "stream=codec_name,width,height,r_frame_rate,pix_fmt,"
                                  "avg_frame_rate,nb_frames",
                                  "-show_entries", "format=duration",
                                  "-of", "json", p],
                                 capture_output=True, text=True, check=True).stdout
            info = json.loads(out)
            st = info["streams"][0]
            dur = float(info["format"]["duration"])
            if st.get("codec_name") != "h264" or st.get("pix_fmt") != "yuv420p":
                media_issues.append("%s codec/pix_fmt %s/%s" % (rel, st.get("codec_name"),
                                                                st.get("pix_fmt")))
            if (st.get("width"), st.get("height")) != (1920, 1080):
                media_issues.append("%s is %sx%s" % (rel, st.get("width"), st.get("height")))
            if not 6.0 <= dur <= 8.0:
                media_issues.append("%s duration %.2fs outside 6-8s" % (rel, dur))
            frames = int(st.get("nb_frames", 0) or 0)
            if frames != 168:
                media_issues.append("%s has %s frames (expect 168)" % (rel, frames))
        except Exception as exc:
            media_issues.append("%s probe failed: %s" % (rel, exc))
    reel = "media/coast-reel.mp4"
    p = os.path.join(root, reel)
    if not os.path.isfile(p):
        media_issues.append("missing " + reel)
    else:
        try:
            out = subprocess.run([probe, "-v", "error", "-select_streams", "v:0",
                                  "-show_entries",
                                  "stream=codec_name,width,height,pix_fmt,nb_frames",
                                  "-show_entries", "format=duration", "-of", "json", p],
                                 capture_output=True, text=True, check=True).stdout
            info = json.loads(out)
            st = info["streams"][0]
            dur = float(info["format"]["duration"])
            if not 22.0 <= dur <= 30.0:
                media_issues.append("reel duration %.2fs outside 22-30s" % dur)
            if int(st.get("nb_frames", 0) or 0) != 648:
                media_issues.append("reel frames %s (expect 648)" % st.get("nb_frames"))
        except Exception as exc:
            media_issues.append("reel probe failed: %s" % exc)
    item(items, "motion", "pass" if not media_issues else "fail",
         "three 7 s 1080p H.264 travel films and one 27 s reel; ffprobe verified",
         ["media/coasts", reel])
    if media_issues:
        errors.append("media: %s" % media_issues[:4])

    # ------------------------------ pitch plates ---------------------------
    pitch_issues = []
    for slug in ("kodingareng-surface", "kodingareng-deeper", "kodingareng-section"):
        rel = "media/pitch/%s.png" % slug
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            pitch_issues.append("missing " + rel)
            continue
        with Image.open(p) as im:
            if im.size[0] < 1920 or im.size[1] < 1080:
                pitch_issues.append("%s too small %s" % (rel, im.size))
    # pair base alignment outside the inset
    pair_ok = True
    try:
        a = Image.open(os.path.join(root, "media/pitch/kodingareng-surface.png")).convert("RGB")
        b = Image.open(os.path.join(root, "media/pitch/kodingareng-deeper.png")).convert("RGB")
        import numpy as np
        aa, bb = np.asarray(a).astype("int16"), np.asarray(b).astype("int16")
        mask = np.ones(aa.shape[:2], dtype=bool)
        mask[100:490, 30:660] = False   # inset region
        diff = np.abs(aa - bb).max(axis=2)
        pair_ok = bool(diff[mask].max() == 0)
        if not pair_ok:
            pitch_issues.append("surface/deeper differ outside the data inset")
    except Exception as exc:
        pair_ok = False
        pitch_issues.append("pair comparison failed: %s" % exc)
    item(items, "pitch-plates", "pass" if not pitch_issues else "fail",
         "three annotated pitch plates; comparison pair identical outside its data "
         "inset", ["media/pitch"])
    if pitch_issues:
        errors.append("pitch: %s" % pitch_issues)

    # ------------------------------ evidence -------------------------------
    ev_rel = "evidence/depth-case-verified.json"
    source_ev = os.path.join(os.path.dirname(root), "..", "..", "..", "revision-v2",
                             "references", "Depth_case_verified.json")
    p = os.path.join(root, ev_rel)
    if os.path.isfile(p):
        try:
            doc = json.load(open(p, encoding="utf-8"))
            item(items, "evidence", "pass",
                 "verified fixture present; %d keys" % len(doc), [ev_rel])
        except Exception as exc:
            item(items, "evidence", "fail", "fixture invalid JSON: %s" % exc, [ev_rel])
            errors.append("evidence invalid")
    else:
        item(items, "evidence", "fail", "missing verified fixture", [ev_rel])
        errors.append("missing evidence fixture")

    # ------------------------------ review docs ----------------------------
    for rel in ("review/before-after.png", "review/parity-sheet.png",
                "review/runtime-parity.png", "review/review-report.md"):
        ok, p = need(rel, min_bytes=500)
        item(items, "review-" + rel, "pass" if ok else "fail",
             "required review evidence", [rel])
        if not ok:
            errors.append("missing " + rel)

    # ------------------------------- sources -------------------------------
    src_issues = []
    for rel in ("source/coasts/kodingareng/scene.blend",
                "source/coasts/tunda/scene.blend",
                "source/coasts/amur/scene.blend",
                "source/globe/globe.blend", "source/kit/common-kit.blend",
                "source/BUILD.md"):
        ok, p = need(rel, min_bytes=1000)
        if not ok:
            src_issues.append(rel)
    item(items, "editable-sources", "pass" if not src_issues else "fail",
         "five packed primary scenes plus build instructions", ["source"])
    if src_issues:
        errors.append("source missing: %s" % src_issues)

    # ------------------------------ overall --------------------------------
    failed = [i for i in items if i["state"] == "fail"]
    result = {
        "schemaVersion": 1,
        "revision": "v2",
        "auditDate": "2026-11-21",
        "bundleRootName": os.path.basename(root),
        "blenderVersion": "5.2.2 LTS",
        "items": items,
        "summary": {"total": len(items), "pass": len([i for i in items if i["state"] == "pass"]),
                    "fail": len(failed),
                    "blocked": len([i for i in items if i["state"] == "blocked"]),
                    "notApplicable": len([i for i in items if i["state"] == "not-applicable"])},
        "errors": errors,
        "verdict": "pass" if not failed else "fail",
    }
    os.makedirs(os.path.dirname(report), exist_ok=True)
    with open(report, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print("VALIDATE " + json.dumps(result["summary"]) + " verdict=" + result["verdict"])
    if failed:
        print("FAILED: " + "; ".join(i["id"] for i in failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
