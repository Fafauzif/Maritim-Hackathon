"""V2 export: editable packed source + clean glTF 2.0 GLBs + measured camera presets.

    blender -b --factory-startup --python export_v2.py -- \
        --run-root <run> --staging-root <bundle> --asset-id <id>
"""
import json
import math
import os
import struct
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

SITE_LOCATORS = {
    "kodingareng": (-5.14905, 119.26473),
    "tunda": (-5.81151, 106.27811),
    "amur": (43.32556, 131.80778),
}
REQUIRED_ANCHORS = ["COAST_ORIGIN", "ORBIT_SITE", "ORBIT_WATERFRONT", "TARGET_SURVEY",
                    "ANCHOR_JETTY", "ANCHOR_VESSEL", "SECTION_A", "SECTION_B"]


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = {}
    i = 0
    while i < len(argv):
        if argv[i] in ("--run-root", "--staging-root", "--asset-id"):
            out[argv[i][2:].replace("-", "_")] = argv[i + 1]; i += 2
        else:
            raise SystemExit("unknown arg " + argv[i])
    for k in ("run_root", "staging_root", "asset_id"):
        if k not in out:
            raise SystemExit("missing " + k)
    return out


def map_gltf(v):
    return [round(float(v[0]), 6), round(float(v[2]), 6), round(float(-v[1]), 6)]


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def glb_summary(path):
    with open(path, "rb") as fh:
        magic, version, length = struct.unpack("<4sII", fh.read(12))
        chunk_len, chunk_type = struct.unpack("<II", fh.read(8))
        json_bytes = fh.read(chunk_len)
    doc = json.loads(json_bytes.decode("utf-8").rstrip("\x00 "))
    nodes = doc.get("nodes", [])
    meshes = doc.get("meshes", [])
    materials = doc.get("materials", [])
    images = doc.get("images", [])
    buffers = doc.get("buffers", [])
    return {
        "magic": magic.decode("ascii", "replace"), "version": version,
        "declared_length": length, "actual_length": os.path.getsize(path),
        "generator": doc.get("asset", {}).get("generator"),
        "gltf_version": doc.get("asset", {}).get("version"),
        "nodes": [n.get("name") for n in nodes],
        "node_count": len(nodes), "mesh_count": len(meshes),
        "material_count": len(materials), "image_count": len(images),
        "texture_count": len(doc.get("textures", [])),
        "buffer_uris": [b.get("uri") for b in buffers],
        "image_uris": [i.get("uri") for i in images],
        "extensions_used": doc.get("extensionsUsed", []),
        "extensions_required": doc.get("extensionsRequired", []),
        "has_cameras": bool(doc.get("cameras")),
        "material_alpha_modes": {m.get("name"): m.get("alphaMode", "OPAQUE")
                                 for m in materials},
    }


def tri_count():
    tris = 0
    for ob in bpy.context.scene.objects:
        if ob.type == "MESH" and ob.data:
            tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
    return tris


def camera_presets(scene):
    presets = {}
    aspect = 16.0 / 9.0
    sensor_w = 36.0
    sensor_h = sensor_w / aspect
    for ob in scene.objects:
        if ob.type != "CAMERA":
            continue
        bpy.context.view_layer.update()
        mw = ob.matrix_world.copy()
        pos = mw.translation
        fwd = -(mw.to_3x3() @ Vector((0, 0, 1)))
        up = (mw.to_3x3() @ Vector((0, 1, 0)))
        target = pos + fwd * 80.0
        cam = ob.data
        p = {
            "projection": "orthographic" if cam.type == "ORTHO" else "perspective",
            "position": map_gltf(pos), "target": map_gltf(target),
            "up": [round(float(v), 6) for v in map_gltf(up)],
            "near": round(cam.clip_start, 4), "far": round(cam.clip_end, 2),
            "aspect": round(aspect, 6),
            "resolution": [3840, 2160],
            "sensorFit": "AUTO",
        }
        if cam.type == "ORTHO":
            p["orthoWidthM"] = round(cam.ortho_scale, 4)
            p["orthoHeightM"] = round(cam.ortho_scale / aspect, 4)
        else:
            vfov = 2.0 * math.atan(sensor_h / (2.0 * cam.lens))
            hfov = 2.0 * math.atan(sensor_w / (2.0 * cam.lens))
            p["lensMm"] = round(cam.lens, 3)
            p["verticalFovDeg"] = round(math.degrees(vfov), 4)
            p["horizontalFovDeg"] = round(math.degrees(hfov), 4)
            p["fitGuidance"] = ("Render at 16:9. For a narrower container keep the "
                                "vertical FOV and crop horizontally; for a wider "
                                "container keep vertical FOV and add side margin.")
        presets[ob.name] = p
    return presets


def anchors(scene):
    out = {}
    for name in REQUIRED_ANCHORS:
        ob = scene.objects.get(name)
        if ob:
            out[name] = map_gltf(ob.matrix_world.translation)
    return out


def main():
    args = parse_args()
    run = args["run_root"]
    staging = args["staging_root"]
    asset = args["asset_id"]
    logs = os.path.join(run, "logs")
    os.makedirs(logs, exist_ok=True)
    report = {"asset_id": asset, "staging": staging}
    if asset in SITE_LOCATORS:
        site = asset
        bpy.ops.wm.open_mainfile(filepath=os.path.join(run, "checkpoints",
                                                       "coast-%s.blend" % site))
        scene = bpy.context.scene
        try:
            bpy.ops.file.pack_all()
        except Exception as exc:
            report["pack_error"] = str(exc)
        src_dir = os.path.join(staging, "source", "coasts", site)
        os.makedirs(src_dir, exist_ok=True)
        src_path = os.path.join(src_dir, "scene.blend")
        bpy.ops.wm.save_as_mainfile(filepath=src_path)
        report["source"] = {"path": "source/coasts/%s/scene.blend" % site,
                            "bytes": os.path.getsize(src_path),
                            "sha256": sha256(src_path)}
        # camera + anchor metadata
        presets = camera_presets(scene)
        anc = anchors(scene)
        report["cameras"] = presets
        report["anchors_gltf"] = anc
        sec_cam = presets.get("COAST_SECTION", {})
        look = [sec_cam["target"][i] - sec_cam["position"][i] for i in range(3)] if sec_cam else [0, 0, -1]
        norm = math.sqrt(sum(v * v for v in look)) or 1.0
        report["section"] = {
            "fromNode": "SECTION_A", "toNode": "SECTION_B",
            "lookDirectionGltf": [round(v / norm, 6) for v in look],
            "verticalExaggeration": float(scene.get("section_exag", 3.0)),
            "verticalPivotUpM": 0.0, "illustrative": True,
            "mutuallyExclusiveWithCoast": True,
        }
        # COAST GLB
        export_objs = []
        for coll_name in ("ENV_Land", "ENV_Water", "BLD_Village", "PROP_Survey",
                          "VEG_Scatter", "FX_Water"):
            coll = bpy.data.collections.get(coll_name)
            if coll:
                export_objs.extend([o for o in coll.all_objects if o.type == "MESH"])
        export_objs.extend([o for o in scene.objects if o.type == "EMPTY"])
        for ob in scene.objects:
            ob.select_set(False)
        for ob in export_objs:
            ob.select_set(True)
        bpy.context.view_layer.objects.active = export_objs[0]
        out_dir = os.path.join(staging, "runtime", "coasts", site)
        os.makedirs(out_dir, exist_ok=True)
        glb_path = os.path.join(out_dir, "coast.glb")
        kwargs = dict(filepath=glb_path, export_format="GLB", use_selection=True,
                      export_cameras=False, export_lights=False, export_apply=True,
                      export_yup=True, export_extras=True)
        try:
            bpy.ops.export_scene.gltf(**kwargs, export_vertex_color="ACTIVE")
        except TypeError:
            bpy.ops.export_scene.gltf(**kwargs)
        report["coast"] = {"path": "runtime/coasts/%s/coast.glb" % site,
                           "bytes": os.path.getsize(glb_path),
                           "sha256": sha256(glb_path),
                           "glb": glb_summary(glb_path),
                           "triangles": tri_count(),
                           "export_objects": len(export_objs)}
        # SECTION GLB
        for ob in scene.objects:
            ob.select_set(False)
        sec_coll = bpy.data.collections.get("SEC_Section")
        sec_objs = [o for o in sec_coll.all_objects if o.type == "MESH"] if sec_coll else []
        sec_objs += [o for o in scene.objects if o.type == "EMPTY"]
        for ob in sec_objs:
            ob.select_set(True)
        if sec_objs:
            bpy.context.view_layer.objects.active = sec_objs[0]
        sec_path = os.path.join(out_dir, "section.glb")
        kwargs["filepath"] = sec_path
        try:
            bpy.ops.export_scene.gltf(**kwargs, export_vertex_color="ACTIVE")
        except TypeError:
            bpy.ops.export_scene.gltf(**kwargs)
        report["section_glb"] = {"path": "runtime/coasts/%s/section.glb" % site,
                                 "bytes": os.path.getsize(sec_path),
                                 "sha256": sha256(sec_path),
                                 "glb": glb_summary(sec_path),
                                 "triangles": tri_count(),
                                 "export_objects": len(sec_objs)}
        report["siteLocatorWgs84"] = {"lat": SITE_LOCATORS[site][0],
                                      "lon": SITE_LOCATORS[site][1],
                                      "role": "globe locator from project place board"}
    elif asset == "kit":
        bpy.ops.wm.open_mainfile(filepath=os.path.join(run, "checkpoints", "kit.blend"))
        scene = bpy.context.scene
        try:
            bpy.ops.file.pack_all()
        except Exception as exc:
            report["pack_error"] = str(exc)
        src_dir = os.path.join(staging, "source", "kit")
        os.makedirs(src_dir, exist_ok=True)
        src_path = os.path.join(src_dir, "common-kit.blend")
        bpy.ops.wm.save_as_mainfile(filepath=src_path)
        report["source"] = {"path": "source/kit/common-kit.blend",
                            "bytes": os.path.getsize(src_path),
                            "sha256": sha256(src_path)}
        used = [o for o in scene.objects if o.type == "MESH"
                and o.name.startswith("KIT_") and not o.name.startswith("KIT_Ground")
                and not o.name.startswith("KIT_Backdrop")]
        for ob in scene.objects:
            ob.select_set(False)
        for ob in used:
            ob.select_set(True)
        bpy.context.view_layer.objects.active = used[0]
        out_dir = os.path.join(staging, "runtime", "kit")
        os.makedirs(out_dir, exist_ok=True)
        glb_path = os.path.join(out_dir, "common-kit.glb")
        kwargs = dict(filepath=glb_path, export_format="GLB", use_selection=True,
                      export_cameras=False, export_lights=False, export_apply=True,
                      export_yup=True, export_extras=True)
        try:
            bpy.ops.export_scene.gltf(**kwargs, export_vertex_color="ACTIVE")
        except TypeError:
            bpy.ops.export_scene.gltf(**kwargs)
        report["kit"] = {"path": "runtime/kit/common-kit.glb",
                         "bytes": os.path.getsize(glb_path),
                         "sha256": sha256(glb_path),
                         "glb": glb_summary(glb_path),
                         "triangles": tri_count(),
                         "components": [o.name for o in used]}
    elif asset == "globe":
        bpy.ops.wm.open_mainfile(filepath=os.path.join(run, "checkpoints", "globe.blend"))
        scene = bpy.context.scene
        try:
            bpy.ops.file.pack_all()
        except Exception as exc:
            report["pack_error"] = str(exc)
        src_dir = os.path.join(staging, "source", "globe")
        os.makedirs(src_dir, exist_ok=True)
        src_path = os.path.join(src_dir, "globe.blend")
        bpy.ops.wm.save_as_mainfile(filepath=src_path)
        report["source"] = {"path": "source/globe/globe.blend",
                            "bytes": os.path.getsize(src_path),
                            "sha256": sha256(src_path)}
        used = [o for o in scene.objects
                if o.name.startswith(("Earth_Surface", "MK_", "ANCHOR_"))]
        for ob in scene.objects:
            ob.select_set(False)
        for ob in used:
            ob.select_set(True)
        bpy.context.view_layer.objects.active = used[0]
        out_dir = os.path.join(staging, "runtime", "globe")
        os.makedirs(out_dir, exist_ok=True)
        glb_path = os.path.join(out_dir, "globe.glb")
        kwargs = dict(filepath=glb_path, export_format="GLB", use_selection=True,
                      export_cameras=False, export_lights=False, export_apply=True,
                      export_yup=True, export_extras=True)
        try:
            bpy.ops.export_scene.gltf(**kwargs, export_vertex_color="ACTIVE")
        except TypeError:
            bpy.ops.export_scene.gltf(**kwargs)
        globe_anchors = {}
        for k in ("kodingareng", "tunda", "amur"):
            ob = scene.objects.get("ANCHOR_" + k)
            if ob:
                globe_anchors[k] = {"position": map_gltf(ob.matrix_world.translation),
                              "lat": float(ob.get("lat", 0.0)),
                              "lon": float(ob.get("lon", 0.0))}
        report["globe"] = {"path": "runtime/globe/globe.glb",
                           "bytes": os.path.getsize(glb_path),
                           "sha256": sha256(glb_path),
                           "glb": glb_summary(glb_path),
                           "anchors": globe_anchors,
                           "radiusArtUnits": float(scene.objects["Earth_Surface"].get("radius", 10.0)),
                           "cameras": camera_presets(scene)}
    else:
        raise SystemExit("unsupported asset id " + asset)
    with open(os.path.join(logs, "export-%s.json" % asset), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print("EXPORTED " + json.dumps({"asset": asset,
                                    "coast_bytes": report.get("coast", {}).get("bytes"),
                                    "section_bytes": report.get("section_glb", {}).get("bytes")}))


if __name__ == "__main__":
    main()

