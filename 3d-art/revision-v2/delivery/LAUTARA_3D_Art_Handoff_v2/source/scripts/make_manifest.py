"""Build runtime/asset-manifest.json from the actual exported GLB bytes.

    python make_manifest.py --run-root <run> --staging-root <bundle>
"""
import argparse
import json
import math
import os
import struct

SITES = {
    "kodingareng": {
        "label": "Kodingareng Lompo",
        "locator": {"lat": -5.14905, "lon": 119.26473,
                    "role": "globe locator from project place board; scene origin is art-local"},
        "art": ("Compact low island with stilt and on-grade houses along connected lanes, "
                "a covered landing pavilion, a fixed jetty and a survey boat at the cut line. "
                "Illustrative; not a building census or surveyed shoreline."),
    },
    "tunda": {
        "label": "Pulau Tunda",
        "locator": {"lat": -5.81151, "lon": 106.27811,
                    "role": "globe locator from project place board; scene origin is art-local"},
        "art": ("Greener island with a sheltered cove landing, differentiated shoreline, "
                "mangrove fringe and roof clusters around the landing. Illustrative."),
    },
    "amur": {
        "label": "Razdolnaya mouth, northern Amur Bay",
        "locator": {"lat": 43.32556, "lon": 131.80778,
                    "role": "globe locator from project place board; scene origin is art-local"},
        "art": ("River-to-bay estuary with low asymmetric marsh banks, tidal creeks, reed "
                "bands and a compact working landing. Illustrative; no plume or bathymetry claim."),
    },
}


def read_glb(path):
    with open(path, "rb") as fh:
        magic, version, length = struct.unpack("<4sII", fh.read(12))
        if magic != b"glTF":
            raise ValueError("not a GLB: " + path)
        chunk_len, chunk_type = struct.unpack("<II", fh.read(8))
        doc = json.loads(fh.read(chunk_len).decode("utf-8").rstrip("\x00 "))
    return doc, version, length


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def node_matrix(node):
    if "matrix" in node:
        m = node["matrix"]
        return [[m[c * 4 + r] for c in range(4)] for r in range(4)]
    t = node.get("translation", [0, 0, 0])
    r = node.get("rotation", [0, 0, 0, 1])
    s = node.get("scale", [1, 1, 1])
    x, y, z, w = r
    rot = [
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w), 0],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w), 0],
        [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y), 0],
        [0, 0, 0, 1],
    ]
    for i in range(3):
        for j in range(3):
            rot[i][j] *= s[j]
    rot[0][3] = t[0]; rot[1][3] = t[1]; rot[2][3] = t[2]
    return rot


def xform(m, p):
    return [sum(m[i][j] * p[j] for j in range(3)) + m[i][3] for i in range(3)]


def glb_stats(path):
    doc, version, length = read_glb(path)
    accessors = doc.get("accessors", [])
    meshes = doc.get("meshes", [])
    scene = (doc.get("scenes") or [{}])[0]
    roots = scene.get("nodes", list(range(len(doc.get("nodes", [])))))
    nodes = doc.get("nodes", [])
    tri = 0
    verts = 0
    lo = [1e18, 1e18, 1e18]
    hi = [-1e18, -1e18, -1e18]
    mesh_instances = 0
    color0 = 0

    def visit(idx, parent):
        nonlocal tri, verts, lo, hi, mesh_instances, color0
        node = nodes[idx]
        world = mat_mul(parent, node_matrix(node))
        if "mesh" in node:
            mesh = meshes[node["mesh"]]
            mesh_instances += 1
            for prim in mesh.get("primitives", []):
                pos = accessors[prim["attributes"]["POSITION"]]
                minv, maxv = pos.get("min"), pos.get("max")
                if minv and maxv:
                    for cx in (minv[0], maxv[0]):
                        for cy in (minv[1], maxv[1]):
                            for cz in (minv[2], maxv[2]):
                                p = xform(world, [cx, cy, cz])
                                for k in range(3):
                                    lo[k] = min(lo[k], p[k])
                                    hi[k] = max(hi[k], p[k])
                verts += pos.get("count", 0)
                if "indices" in prim:
                    tri += accessors[prim["indices"]].get("count", 0) // 3
                else:
                    tri += pos.get("count", 0) // 3
                if "COLOR_0" in prim.get("attributes", {}):
                    color0 += 1
        for ch in node.get("children", []):
            visit(ch, world)

    ident = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    for r in roots:
        visit(r, ident)
    node_names = [n.get("name") for n in nodes]
    dup = sorted({n for n in node_names if node_names.count(n) > 1})
    return {
        "gltfVersion": doc.get("asset", {}).get("version"),
        "generator": doc.get("asset", {}).get("generator"),
        "declaredBytes": length,
        "actualBytes": os.path.getsize(path),
        "nodes": len(nodes),
        "meshInstances": mesh_instances,
        "meshData": len(meshes),
        "materials": len(doc.get("materials", [])),
        "textures": len(doc.get("textures", [])),
        "images": len(doc.get("images", [])),
        "triangles": tri,
        "vertices": verts,
        "boundsGltf": {"min": [round(v, 4) for v in lo], "max": [round(v, 4) for v in hi],
                       "size": [round(hi[i] - lo[i], 3) for i in range(3)]},
        "nodeNames": node_names,
        "duplicateNodeNames": dup,
        "hasCameras": bool(doc.get("cameras")),
        "hasLights": any("KHR_lights_punctual" in (n.get("extensions", {}) or {}) for n in nodes),
        "extensionsUsed": doc.get("extensionsUsed", []),
        "extensionsRequired": doc.get("extensionsRequired", []),
        "externalBufferUris": [b.get("uri") for b in doc.get("buffers", []) if b.get("uri")],
        "externalImageUris": [i.get("uri") for i in doc.get("images", []) if i.get("uri")],
        "vertexColorPrimitives": color0,
        "materialAlphaModes": {m.get("name"): m.get("alphaMode", "OPAQUE")
                               for m in doc.get("materials", [])},
    }


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--staging-root", required=True)
    args = ap.parse_args()
    run, staging = args.run_root, args.staging_root
    exports = {}
    for name in os.listdir(os.path.join(run, "logs")):
        if name.startswith("export-") and name.endswith(".json"):
            with open(os.path.join(run, "logs", name), encoding="utf-8") as fh:
                report = json.load(fh)
            exports[report["asset_id"]] = report
    build_id = os.path.basename(os.path.abspath(run))
    base_commit = "e07093ef34118bc3e686257accbbfe6246595153"
    assets = []
    asset_index = {}
    for asset_id, rel, kind in (
            ("globe", "runtime/globe/globe.glb", "globe"),
            ("kit", "runtime/kit/common-kit.glb", "kit")):
        path = os.path.join(staging, rel)
        st = glb_stats(path)
        entry = {"id": asset_id, "path": rel, "kind": kind,
                 "bytes": os.path.getsize(path), "sha256": sha256(path),
                 "summary": {k: st[k] for k in ("nodes", "meshInstances", "meshData",
                                                "materials", "textures", "images",
                                                "triangles", "vertices", "boundsGltf")}}
        assets.append(entry)
        asset_index[asset_id] = st
    sites_manifest = {}
    for site in SITES:
        ids = {}
        for kind, rel in (("coast", "runtime/coasts/%s/coast.glb" % site),
                          ("section", "runtime/coasts/%s/section.glb" % site)):
            path = os.path.join(staging, rel)
            st = glb_stats(path)
            aid = "%s_%s" % (kind, site)
            assets.append({"id": aid, "path": rel, "kind": kind,
                           "bytes": os.path.getsize(path), "sha256": sha256(path),
                           "summary": {k: st[k] for k in ("nodes", "meshInstances",
                                                        "meshData", "materials",
                                                        "textures", "images", "triangles",
                                                        "vertices", "boundsGltf")}})
            asset_index[aid] = st
            ids[kind] = aid
        er = exports.get(site, {})
        section_report = er.get("section", {})
        sites_manifest[site] = {
            "label": SITES[site]["label"],
            "coastAssetId": ids["coast"],
            "sectionAssetId": ids["section"],
            "sourcePath": "source/coasts/%s/scene.blend" % site,
            "siteLocatorWgs84": SITES[site]["locator"],
            "originGltf": [0.0, 0.0, 0.0],
            "waterlineUpM": 0.0,
            "waterNode": "ENV_Water",
            "sectionWaterNode": "SECTION_Water",
            "anchorsGltf": er.get("anchors_gltf", {}),
            "cameras": er.get("cameras", {}),
            "section": dict(section_report, fromNode="SECTION_A", toNode="SECTION_B",
                            verticalPivotUpM=0.0, illustrative=True,
                            mutuallyExclusiveWithCoast=True),
            "cleanStills": {
                "godview": "media/coasts/%s/godview.png" % site,
                "mapview": "media/coasts/%s/mapview.png" % site,
                "approach": "media/coasts/%s/approach.png" % site,
                "detail": "media/coasts/%s/detail.png" % site,
                "section": "media/coasts/%s/section.png" % site,
            },
            "film": "media/coasts/%s/travel.mp4" % site,
            "artNotes": SITES[site]["art"],
        }
    globe_export = exports.get("globe", {})
    globe_stats = asset_index["globe"]
    globe_markers = {}
    for site in SITES:
        marker = (globe_export.get("globe", {}).get("anchors", {}) or {}).get(site, {})
        globe_markers[site] = {
            "label": SITES[site]["label"],
            "wgs84": SITES[site]["locator"],
            "node": "ANCHOR_" + site,
            "positionGltf": marker.get("position", [0, 0, 0]),
            "role": "globe locator; not a scene transform",
        }
    manifest = {
        "schemaVersion": 1,
        "revision": "v2",
        "baseCommit": base_commit,
        "buildId": build_id,
        "blenderVersion": "5.2.2 LTS",
        "axisConvention": ("Blender +X east, +Y north, +Z up, waterline Z=0, 1 unit = 1 m. "
                           "glTF +X east, +Y up, -Z north. Map Blender [x,y,z] to glTF [x,z,-y]."),
        "units": "metres",
        "georeferenced": False,
        "assets": assets,
        "sites": sites_manifest,
        "globe": {
            "assetId": "globe",
            "radiusArtUnits": 10.0,
            "projection": "natural-earth equirectangular UV on a UV sphere; +Y north after export",
            "markers": globe_markers,
            "cameras": globe_export.get("globe", {}).get("cameras", {}),
            "assetBounds": globe_stats["boundsGltf"],
        },
        "kit": {
            "assetId": "kit",
            "components": exports.get("kit", {}).get("kit", {}).get("components", []),
            "originRules": ("Each component has its own authored pivot at ground/waterline; "
                            "place on Z=0 for waterline assets and on sampled terrain for land assets. "
                            "Instance repeated parts; do not normalise component sizes."),
        },
        "evidencePath": "evidence/depth-case-verified.json",
        "media": {
            "globeOverview": "media/globe/globe-overview.png",
            "kitSheet": "media/kit/asset-sheet.png",
            "coastReel": "media/coast-reel.mp4",
            "pitchPlates": ["media/pitch/kodingareng-surface.png",
                            "media/pitch/kodingareng-deeper.png",
                            "media/pitch/kodingareng-section.png"],
        },
        "integrationNotes": [
            "Load one coast.glb at a time; hide coast.glb before showing its section.glb.",
            "Both variants share the same world origin and A/B anchor transforms.",
            "ENV_Water and SECTION_Water are independent selectable water nodes.",
            "Runtime meshes carry no evidence figures, arrows, labels or statutory boundaries.",
            "Use the annotated pitch plates for the case story; do not bake them into runtime art.",
        ],
    }
    out = os.path.join(staging, "runtime", "asset-manifest.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    os.replace(tmp, out)
    report = {"manifest": out, "assets": len(assets),
              "sites": len(sites_manifest),
              "sha256": sha256(out),
              "bytes": os.path.getsize(out),
              "assetStats": {a["id"]: {k: asset_index[a["id"]][k] for k in
                                       ("nodes", "triangles", "materials", "boundsGltf")}
                             for a in assets}}
    with open(os.path.join(run, "logs", "manifest-build.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print("MANIFEST " + json.dumps({"assets": len(assets), "bytes": report["bytes"],
                                    "sha256": report["sha256"]}))


if __name__ == "__main__":
    main()
