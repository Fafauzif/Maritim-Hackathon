import json
import os

run = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local"
zip_path = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\delivery\LAUTARA_3D_Art_Handoff_v2.zip"

import hashlib
zip_sha = hashlib.sha256(open(zip_path, "rb").read()).hexdigest()
zip_size = os.path.getsize(zip_path)

progress = {
    "schemaVersion": 1,
    "runId": "20261121T1445-local",
    "baseCommit": "e07093ef34118bc3e686257accbbfe6246595153",
    "blenderVersion": "5.2.2 LTS",
    "toolingEvidence": "logs/toolchain.json",
    "activeCheckpoint": "validated delivery ZIP",
    "phaseStatus": {"0": "pass", "1": "pass", "2": "pass", "3": "pass",
                    "4": "pass", "5": "pass", "6": "pass", "7": "pass"},
    "siteStatus": {"kodingareng": "pass", "tunda": "pass", "amur": "pass"},
    "assetStatus": {
        "globe": "pass", "kit": "pass",
        "kodingareng_coast": "pass", "kodingareng_section": "pass",
        "tunda_coast": "pass", "tunda_section": "pass",
        "amur_coast": "pass", "amur_section": "pass",
    },
    "renderJobs": [
        {"id": "stills-4k", "profile": "final", "status": "done",
         "resolution": [3840, 2160], "count": 16,
         "output": "renders/final-4k"},
        {"id": "travel", "profile": "final", "status": "done",
         "frameRange": [1, 168], "fps": 24, "resolution": [1920, 1080],
         "count": 504, "output": "renders/travel"},
        {"id": "globe-reel", "profile": "final", "status": "done",
         "frameRange": [1, 144], "fps": 24, "resolution": [1920, 1080],
         "count": 144, "output": "renders/globe-reel"},
    ],
    "gateEvidence": {
        "preflight": "logs/preflight.md",
        "lookProof": "proofs/look/decision.md",
        "coverage": "logs/coverage-shares.json",
        "palette": "logs/final-still-stats.json",
        "builds": ["logs/build-kodingareng.json", "logs/build-tunda.json",
                   "logs/build-amur.json", "logs/build-kit.json", "logs/build-globe.json"],
        "manifest": "logs/manifest-build.json",
        "encode": "logs/encode-report.json",
        "verification": "logs/finalverify-*.json",
        "validation": "logs/validation-final.json",
        "package": "logs/package-final.json",
    },
    "validation": {"total": 38, "pass": 38, "fail": 0, "blocked": 0},
    "delivery": {
        "zip": zip_path,
        "bytes": zip_size,
        "sha256": zip_sha,
        "files": 72,
        "cleanExtraction": True,
        "extractedValidation": "38/38 pass",
    },
    "blockers": [],
    "limits": [
        "Illustrative terrain, section and prop placement; not surveyed.",
        "Human playback of the three films and reel remains recommended.",
        "Water is a single alpha plane; replace with opaque material if the target renderer sorts alpha badly.",
    ],
    "nextAction": "Hand the validated ZIP to the teammate; play the films once for human sign-off.",
}
tmp = os.path.join(run, "progress.json.tmp")
with open(tmp, "w", encoding="utf-8") as fh:
    json.dump(progress, fh, indent=2)
os.replace(tmp, os.path.join(run, "progress.json"))
print("progress written", zip_sha[:16], zip_size)
