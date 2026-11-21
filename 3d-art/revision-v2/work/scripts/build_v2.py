"""V2 build entry point.

    blender -b --factory-startup --python build_v2.py -- \
        --repo-root <root> --run-root <run> --target kodingareng [--proof]
"""
import json
import os
import sys
import time

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import v2sites as S
import v2scene as SC
import v2layout as LAY

SITE_LOCATORS = {
    "kodingareng": {"lat": -5.14905, "lon": 119.26473,
                    "role": "globe locator from project place board; art-local scene origin"},
    "tunda": {"lat": -5.81151, "lon": 106.27811,
              "role": "globe locator from project place board; art-local scene origin"},
    "amur": {"lat": 43.32556, "lon": 131.80778,
             "role": "globe locator from project place board; art-local scene origin"},
}


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = {"repo_root": None, "run_root": None, "target": None, "proof": False}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--repo-root":
            out["repo_root"] = argv[i + 1]; i += 2
        elif a == "--run-root":
            out["run_root"] = argv[i + 1]; i += 2
        elif a == "--target":
            out["target"] = argv[i + 1]; i += 2
        elif a == "--proof":
            out["proof"] = True; i += 1
        else:
            raise SystemExit("unknown arg " + a)
    if not out["repo_root"] or not out["run_root"] or not out["target"]:
        raise SystemExit("need --repo-root, --run-root, --target")
    return out


def world_bounds(exclude_collections=()):
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for ob in bpy.context.scene.objects:
        if ob.type != "MESH" or not ob.data:
            continue
        if any(c.name in exclude_collections for c in ob.users_collection):
            continue
        for corner in ob.bound_box:
            w = ob.matrix_world @ Vector(corner)
            lo.x = min(lo.x, w.x); lo.y = min(lo.y, w.y); lo.z = min(lo.z, w.z)
            hi.x = max(hi.x, w.x); hi.y = max(hi.y, w.y); hi.z = max(hi.z, w.z)
    # Blender -> glTF: X=x, Y=z, Z=-y
    g_lo = [round(lo.x, 4), round(lo.z, 4), round(-hi.y, 4)]
    g_hi = [round(hi.x, 4), round(hi.z, 4), round(-lo.y, 4)]
    return {"blender_min": [round(v, 4) for v in lo], "blender_max": [round(v, 4) for v in hi],
            "gltf_min": g_lo, "gltf_max": g_hi,
            "size_m": [round(hi.x - lo.x, 3), round(hi.y - lo.y, 3), round(hi.z - lo.z, 3)]}


def mesh_stats():
    tris = 0
    verts = 0
    meshes = 0
    for ob in bpy.context.scene.objects:
        if ob.type != "MESH" or not ob.data:
            continue
        meshes += 1
        verts += len(ob.data.vertices)
        tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
    return {"mesh_objects": meshes, "vertices": verts, "triangles": tris,
            "materials": len(bpy.data.materials)}


def project_objects(scene, cam_name, names, res=(3840, 2160)):
    from bpy_extras.object_utils import world_to_camera_view
    cam = bpy.data.objects.get(cam_name)
    if cam is None:
        return None
    old = scene.camera
    scene.camera = cam
    bpy.context.view_layer.update()
    out = {}
    W, H = res
    for name in names:
        ob = bpy.data.objects.get(name)
        if ob is None:
            continue
        pts = []
        if ob.type == "MESH" and ob.data:
            for corner in ob.bound_box:
                pts.append(ob.matrix_world @ Vector(corner))
        else:
            pts.append(ob.matrix_world.translation.copy())
        uv = [world_to_camera_view(scene, cam, p) for p in pts]
        xs = [p.x for p in uv]
        ys = [p.y for p in uv]
        zs = [p.z for p in uv]
        inside = sum(1 for p in uv if 0.0 <= p.x <= 1.0 and 0.0 <= p.y <= 1.0 and p.z > 0)
        px0, px1 = min(xs), max(xs)
        py0, py1 = min(ys), max(ys)
        out[name] = {
            "bbox_norm": [round(px0, 4), round(py0, 4), round(px1, 4), round(py1, 4)],
            "bbox_px": [round(px0 * W, 1), round(py0 * H, 1),
                        round((px1 - px0) * W, 1), round((py1 - py0) * H, 1)],
            "corners_inside": int(inside), "corners": len(pts),
            "fully_inside": bool(inside == len(pts) and px0 > 0.005 and px1 < 0.995
                                 and py0 > 0.005 and py1 < 0.995),
            "depth_min": round(min(zs), 3), "depth_max": round(max(zs), 3),
        }
    scene.camera = old
    return out


def main():
    args = parse_args()
    target = args["target"]
    if target not in S.SITES:
        raise SystemExit("unknown site target %s" % target)
    t0 = time.time()
    scene, stats = LAY.build_site(target)
    site = S.SITES[target]
    # scene metadata used by export/manifest
    scene["site_key"] = target
    scene["site_label"] = site["label"]
    scene["revision"] = "v2"
    scene["axis_convention"] = "+X east, +Y north, +Z up; waterline Z=0; 1 unit = 1 m"
    scene["site_locator_wgs84"] = json.dumps(SITE_LOCATORS[target])
    scene["georeferenced"] = False
    scene["art_note"] = ("Illustrative coastal miniature. Site-art values, prop "
                         "placement and section geometry are art, not surveyed data.")
    scene["section_exag"] = float(site["section_exag"])
    scene["section_pivot_z"] = 0.0
    scene["waterline_z"] = 0.0
    bpy.context.view_layer.update()

    stats["mesh"] = mesh_stats()
    stats["bounds_all"] = world_bounds()
    stats["bounds_export"] = world_bounds(exclude_collections=("SEC_Section", "SEC_Stage"))
    stats["build_seconds"] = round(time.time() - t0, 2)
    stats["cameras_detail"] = {}
    for cam in [o for o in scene.objects if o.type == "CAMERA"]:
        mw = cam.matrix_world
        fwd = -(mw.to_3x3() @ Vector((0, 0, 1)))
        stats["cameras_detail"][cam.name] = {
            "blender_pos": [round(v, 4) for v in mw.translation],
            "blender_forward": [round(v, 5) for v in fwd],
            "lens": round(cam.data.lens, 3),
            "type": cam.data.type,
            "ortho_scale": round(cam.data.ortho_scale, 3) if cam.data.type == "ORTHO" else None,
        }
    # frame audit: do the story objects read inside every required view?
    key_objs = ["PROP_SurveyBoat", "PROP_Jetty"]
    for ob in scene.objects:
        if ob.name.startswith(("BLD_Landing", "BLD_WorkingLanding", "BLD_CommunityHall")):
            key_objs.append(ob.name)
    for ob in list(scene.objects):
        if ob.name.startswith("BLD_House_") and "_Pad" not in ob.name and len(key_objs) < 12:
            key_objs.append(ob.name)
    stats["frame_audit"] = {}
    for cam_name in ("COAST_OVERVIEW", "COAST_PLAN", "COAST_APPROACH",
                     "COAST_DETAIL", "COAST_SECTION"):
        stats["frame_audit"][cam_name] = project_objects(scene, cam_name, key_objs)

    ckpt_dir = os.path.join(args["run_root"], "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)
    path = os.path.join(ckpt_dir, "coast-%s.blend" % target)
    bpy.ops.wm.save_as_mainfile(filepath=path)

    logs = os.path.join(args["run_root"], "logs")
    os.makedirs(logs, exist_ok=True)
    with open(os.path.join(logs, "build-%s.json" % target), "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2)

    if args["proof"]:
        proof_dir = os.path.join(args["run_root"], "proofs", "look")
        os.makedirs(proof_dir, exist_ok=True)
        proofs = {}
        for cam, slug in (("COAST_OVERVIEW", "godview"), ("COAST_PLAN", "mapview"),
                          ("COAST_APPROACH", "approach"), ("COAST_DETAIL", "detail")):
            proofs[cam] = SC.render_still(
                scene, cam, os.path.join(proof_dir, "%s_%s.png" % (target, slug)),
                res=(960, 540), samples=20, hide=("SEC_Section", "SEC_Stage"))
        proofs["COAST_SECTION"] = SC.render_still(
            scene, "COAST_SECTION",
            os.path.join(proof_dir, "%s_section.png" % target),
            res=(960, 540), samples=20,
            hide=("ENV_Land", "ENV_Water", "BLD_Village", "VEG_Scatter",
                  "PROP_Survey", "FX_Water", "GUIDE_Authoring"),
            show=("SEC_Section", "SEC_Stage"))
        stats["proofs"] = {k: {"path": v["path"], "bytes": v["bytes"]} for k, v in proofs.items()}
        with open(os.path.join(logs, "build-%s.json" % target), "w", encoding="utf-8") as fh:
            json.dump(stats, fh, indent=2)
        # keep the saved file camera state clean
        scene.camera = bpy.data.objects["COAST_OVERVIEW"]
        bpy.ops.wm.save_as_mainfile(filepath=path)

    print("BUILD " + json.dumps({"target": target, "checkpoint": path,
                                 "objects": stats["objects"],
                                 "houses": stats["houses"],
                                 "triangles": stats["mesh"]["triangles"],
                                 "seconds": stats["build_seconds"]}))


if __name__ == "__main__":
    main()
