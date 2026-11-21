"""Verify one GLB or BLEND in a fresh Blender process.

    blender -b --factory-startup --python verify_assets_v2.py -- \
        --bundle-root <bundle> --asset-id coast_kodingareng --report <json>
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def parse():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = {}
    i = 0
    while i < len(argv):
        if argv[i].startswith("--"):
            out[argv[i][2:].replace("-", "_")] = argv[i + 1]; i += 2
        else:
            i += 1
    return out


def gltf_to_blender(p):
    return [p[0], -p[2], p[1]]


def blender_to_gltf(p):
    return [p[0], p[2], -p[1]]


def world_bounds(objects):
    lo = Vector((1e18, 1e18, 1e18))
    hi = Vector((-1e18, -1e18, -1e18))
    n = 0
    for ob in objects:
        if ob.type != "MESH" or not ob.data:
            continue
        n += 1
        for c in ob.bound_box:
            w = ob.matrix_world @ Vector(c)
            for i in range(3):
                lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
    bl = {"blenderMin": [round(v, 4) for v in lo],
          "blenderMax": [round(v, 4) for v in hi], "meshes": n}
    # map all eight corners, then take min/max: glTF is (x, z, -y)
    g = []
    for x in (lo[0], hi[0]):
        for y in (lo[1], hi[1]):
            for z in (lo[2], hi[2]):
                g.append([x, z, -y])
    bl["gltfMin"] = [round(min(p[i] for p in g), 4) for i in range(3)]
    bl["gltfMax"] = [round(max(p[i] for p in g), 4) for i in range(3)]
    return bl


def setup_test_light():
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x = 900
    sc.render.resolution_y = 506
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "Khronos PBR Neutral"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = -0.35
    sc.view_settings.gamma = 1.0
    try:
        sc.eevee.taa_render_samples = 24
        sc.eevee.use_raytracing = True
    except Exception:
        pass
    if sc.world is None:
        sc.world = bpy.data.worlds.new("TEST_World")
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.84, 0.86, 0.88, 1.0)
        bg.inputs["Strength"].default_value = 0.55
    if not sc.objects.get("TEST_Sun"):
        d = bpy.data.lights.new("TEST_Sun", "SUN")
        d.energy = 3.8
        d.angle = math.radians(5)
        d.color = (1.0, 0.95, 0.88)
        ob = bpy.data.objects.new("TEST_Sun", d)
        ob.rotation_euler = (math.radians(48), math.radians(3), math.radians(218))
        sc.collection.objects.link(ob)
    if not sc.objects.get("TEST_Fill"):
        d = bpy.data.lights.new("TEST_Fill", "AREA")
        d.energy = 240.0
        d.size = 80.0
        d.color = (0.72, 0.84, 1.0)
        ob = bpy.data.objects.new("TEST_Fill", d)
        ob.location = (-30, -50, 60)
        sc.collection.objects.link(ob)
    # ground plane to read grounding and shadows
    if not sc.objects.get("TEST_Ground"):
        me = bpy.data.meshes.new("TEST_Ground")
        me.from_pydata([(-400, -400, -0.6), (400, -400, -0.6),
                        (400, 400, -0.6), (-400, 400, -0.6)], [], [(0, 1, 2, 3)])
        me.update()
        mat = bpy.data.materials.new("TEST_Ground_Mat")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
            0.72, 0.70, 0.64, 1.0)
        mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
        me.materials.append(mat)
        ob = bpy.data.objects.new("TEST_Ground", me)
        sc.collection.objects.link(ob)
    return sc


def camera_from_preset(scene, preset):
    cam_data = bpy.data.cameras.new("VERIFY_CAM")
    if preset.get("projection") == "orthographic":
        cam_data.type = "ORTHO"
        cam_data.ortho_scale = preset.get("orthoWidthM", 100.0)
    else:
        cam_data.lens = preset.get("lensMm", 50.0)
    cam_data.clip_start = 0.5
    cam_data.clip_end = 6000.0
    cam = bpy.data.objects.new("VERIFY_CAM", cam_data)
    scene.collection.objects.link(cam)
    pos = gltf_to_blender(preset["position"])
    tgt = gltf_to_blender(preset.get("target", [0, 0, 0]))
    cam.location = pos
    cam.rotation_euler = (Vector(tgt) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam
    return cam


def verify_glb(bundle, asset_id, manifest, run_root):
    rec = next(a for a in manifest["assets"] if a["id"] == asset_id)
    path = os.path.join(bundle, rec["path"])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    sc = setup_test_light()
    # extra backing plane only helps the loose kit components; it would occlude
    # section/coast water. Remove it for everything else.
    ground = sc.objects.get("TEST_Ground")
    if ground and not asset_id.startswith("kit"):
        bpy.data.objects.remove(ground, do_unlink=True)
    objects = list(sc.objects)
    meshes = [o for o in objects if o.type == "MESH"
              and not o.name.startswith("TEST_")]
    stats = {
        "assetId": asset_id, "path": rec["path"],
        "importedObjects": len(objects), "importedMeshes": len(meshes),
        "importedMaterials": len(bpy.data.materials),
        "importedImages": len(bpy.data.images),
        "unpackedImages": [i.name for i in bpy.data.images
                           if i.source == "FILE" and not i.packed_file],
        "cameras": len([o for o in objects if o.type == "CAMERA"]),
        "lights": len([o for o in objects if o.type == "LIGHT"]),
        "bounds": world_bounds(meshes),
        "nodeNames": sorted(o.name for o in objects),
    }
    required = []
    site = None
    for key, site_rec in manifest["sites"].items():
        if health_id(manifest, key, "coast") == asset_id or \
           health_id(manifest, key, "section") == asset_id:
            site = key
    if site:
        required = ["COAST_ORIGIN", "ORBIT_SITE", "ORBIT_WATERFRONT", "TARGET_SURVEY",
                    "ANCHOR_JETTY", "ANCHOR_VESSEL", "SECTION_A", "SECTION_B"]
        if "section" in asset_id:
            required += ["SECTION_Water", "SECTION_Land", "SECTION_Strata_A"]
        else:
            required += ["ENV_Water", "ENV_Terrain"]
    elif asset_id == "globe":
        required = ["Earth_Surface", "ANCHOR_kodingareng", "ANCHOR_tunda", "ANCHOR_amur"]
    elif asset_id == "kit":
        required = manifest["kit"]["components"]
    stats["requiredMissing"] = [n for n in required if not sc.objects.get(n)]
    stats["requiredPresent"] = len(required) - len(stats["requiredMissing"])
    # bounds agreement with the manifest's own GLB-derived bounds
    exp = rec.get("summary", {}).get("boundsGltf")
    if exp:
        got = stats["bounds"]
        diffs = [abs(got["gltfMin"][i] - exp["min"][i]) for i in range(3)] + \
                [abs(got["gltfMax"][i] - exp["max"][i]) for i in range(3)]
        stats["boundsMaxDeltaM"] = round(max(diffs), 4)
        stats["boundsAgree"] = bool(max(diffs) <= 0.02)
    # render with the published camera preset where applicable
    preset = None
    if site:
        site_rec = manifest["sites"][site]
        cam_key = "COAST_SECTION" if "section" in asset_id else "COAST_OVERVIEW"
        preset = site_rec["cameras"].get(cam_key)
    elif asset_id == "globe":
        preset = manifest["globe"]["cameras"].get("GLOBE_HOME")
    if preset:
        camera_from_preset(sc, preset)
    else:
        cam_data = bpy.data.cameras.new("VERIFY_CAM")
        cam_data.lens = 45.0
        cam = bpy.data.objects.new("VERIFY_CAM", cam_data)
        sc.collection.objects.link(cam)
        bmin, bmax = stats["bounds"]["blenderMin"], stats["bounds"]["blenderMax"]
        cx = 0.5 * (bmin[0] + bmax[0])
        cy = 0.5 * (bmin[1] + bmax[1])
        cz = 0.5 * (bmin[2] + bmax[2])
        span = max(bmax[i] - bmin[i] for i in range(3))
        dist = max(18.0, span * 1.35)
        cam.location = (cx + dist * 0.45, cy - dist * 1.05, cz + dist * 0.75)
        cam.rotation_euler = (Vector((cx, cy, cz)) - cam.location).to_track_quat(
            "-Z", "Y").to_euler()
        sc.camera = cam
    sc.render.filepath = os.path.join(run_root, "renders", "import-check",
                                      asset_id + ".png")
    os.makedirs(os.path.dirname(sc.render.filepath), exist_ok=True)
    bpy.ops.render.render(write_still=True)
    stats["render"] = sc.render.filepath
    stats["renderBytes"] = os.path.getsize(sc.render.filepath)
    return stats


def health_id(manifest, site, kind):
    rec = manifest["sites"][site]
    return rec["coastAssetId"] if kind == "coast" else rec["sectionAssetId"]


def verify_blend(bundle, asset_id, manifest, run_root):
    if asset_id.startswith("blend_coast_"):
        site = asset_id[len("blend_coast_"):]
        rel = "source/coasts/%s/scene.blend" % site
        cam = "COAST_OVERVIEW"
    elif asset_id == "blend_globe":
        rel = "source/globe/globe.blend"
        cam = "GLOBE_HOME"
    elif asset_id == "blend_kit":
        rel = "source/kit/common-kit.blend"
        cam = "KIT_SHEET_CAM"
    else:
        raise SystemExit("unknown blend asset " + asset_id)
    path = os.path.join(bundle, rel)
    bpy.ops.wm.open_mainfile(filepath=path)
    sc = bpy.context.scene
    objects = list(sc.objects)
    missing = []
    for img in bpy.data.images:
        if img.source == "FILE" and not img.packed_file and not os.path.exists(img.filepath):
            missing.append(img.filepath)
    stats = {
        "assetId": asset_id, "path": rel,
        "scene": sc.name, "objects": len(objects),
        "meshes": len([o for o in objects if o.type == "MESH"]),
        "materials": len(bpy.data.materials),
        "images": len(bpy.data.images),
        "missingImagePaths": missing,
        "cameras": sorted(o.name for o in objects if o.type == "CAMERA"),
        "lights": sorted(o.name for o in objects if o.type == "LIGHT"),
        "collections": sorted(c.name for c in bpy.data.collections),
        "hasWater": bool(sc.objects.get("ENV_Water") or sc.objects.get("Earth_Surface")),
        "hasSection": bool(sc.objects.get("SECTION_Water")),
        "world": sc.world.name if sc.world else None,
        "viewTransform": sc.view_settings.view_transform,
        "engine": sc.render.engine,
    }
    if bpy.data.objects.get("TRAVEL_CAM"):
        stats["travelCamera"] = "TRAVEL_CAM"
        stats["frameRange"] = [sc.frame_start, sc.frame_end]
    if cam not in sc.objects:
        raise RuntimeError("missing camera " + cam)
    sc.camera = bpy.data.objects[cam]
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x = 960
    sc.render.resolution_y = 540
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    try:
        sc.eevee.taa_render_samples = 24
    except Exception:
        pass
    sc.render.filepath = os.path.join(run_root, "renders", "import-check",
                                      asset_id + ".png")
    os.makedirs(os.path.dirname(sc.render.filepath), exist_ok=True)
    try:
        bpy.ops.render.render(write_still=True)
        stats["render"] = sc.render.filepath
        stats["renderBytes"] = os.path.getsize(sc.render.filepath)
    except Exception as exc:
        stats["renderError"] = str(exc)
    return stats


def main():
    a = parse()
    bundle = a["bundle_root"]
    asset_id = a["asset_id"]
    report_path = a["report"]
    run_root = a.get("run_root") or os.path.dirname(report_path)
    with open(os.path.join(bundle, "runtime", "asset-manifest.json"), encoding="utf-8") as fh:
        manifest = json.load(fh)
    if asset_id.startswith("blend_"):
        stats = verify_blend(bundle, asset_id, manifest, run_root)
    else:
        stats = verify_glb(bundle, asset_id, manifest, run_root)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2)
    print("VERIFY " + json.dumps({"asset": asset_id, "ok": not stats.get("requiredMissing"),
                                  "missing": stats.get("requiredMissing", [])}))


if __name__ == "__main__":
    main()

