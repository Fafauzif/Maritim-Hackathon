"""V2 render passes: 4K stills, travel film frames, globe stills and reel frames.

    blender -b --factory-startup --python render_v2.py -- --run-root <run> --mode stills --target kodingareng
"""
import json
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import v2scene as SC

SURFACE = ("ENV_Land", "ENV_Water", "BLD_Village", "PROP_Survey", "VEG_Scatter",
           "FX_Water")
SECTION_HIDE = SURFACE + ("GUIDE_Authoring",)
STILLS = [
    ("COAST_OVERVIEW", "godview"),
    ("COAST_PLAN", "mapview"),
    ("COAST_APPROACH", "approach"),
    ("COAST_DETAIL", "detail"),
]


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


def stills(run, site):
    bpy.ops.wm.open_mainfile(filepath=os.path.join(run, "checkpoints",
                                                   "coast-%s.blend" % site))
    scene = bpy.context.scene
    outdir = os.path.join(run, "renders", "final-4k", site)
    os.makedirs(outdir, exist_ok=True)
    made = []
    for cam, slug in STILLS:
        made.append(SC.render_still(scene, cam, os.path.join(outdir, slug + ".png"),
                                    res=(3840, 2160), samples=48,
                                    hide=("SEC_Section", "SEC_Stage")))
    made.append(SC.render_still(
        scene, "COAST_SECTION", os.path.join(outdir, "section.png"),
        res=(3840, 2160), samples=48, hide=SECTION_HIDE,
        show=("SEC_Section", "SEC_Stage")))
    # previews for review sheets
    prev = os.path.join(run, "renders", "previews", site)
    os.makedirs(prev, exist_ok=True)
    for cam, slug in STILLS:
        SC.render_still(scene, cam, os.path.join(prev, slug + ".png"),
                        res=(1280, 720), samples=24,
                        hide=("SEC_Section", "SEC_Stage"))
    SC.render_still(scene, "COAST_SECTION", os.path.join(prev, "section.png"),
                    res=(1280, 720), samples=24, hide=SECTION_HIDE,
                    show=("SEC_Section", "SEC_Stage"))
    return made


def travel(run, site):
    bpy.ops.wm.open_mainfile(filepath=os.path.join(run, "checkpoints",
                                                   "coast-%s.blend" % site))
    scene = bpy.context.scene
    outdir = os.path.join(run, "renders", "travel", site)
    os.makedirs(outdir, exist_ok=True)
    prefix = os.path.join(outdir, "frame_")
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 8
    try:
        scene.eevee.use_raytracing = False
    except Exception:
        pass
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.fps = 24
    scene.camera = bpy.data.objects["TRAVEL_CAM"]
    SC.set_visibility(show=SURFACE + ("GUIDE_Authoring",),
                      hide=("SEC_Section", "SEC_Stage"))
    scene.render.filepath = prefix
    scene.frame_start, scene.frame_end = 1, 132
    bpy.ops.render.render(animation=True)
    scene.camera = bpy.data.objects["COAST_SECTION"]
    SC.set_visibility(show=("SEC_Section", "SEC_Stage"), hide=SECTION_HIDE)
    scene.frame_start, scene.frame_end = 133, 168
    bpy.ops.render.render(animation=True)
    return {"frames": 168, "dir": outdir}


def globe(run):
    bpy.ops.wm.open_mainfile(filepath=os.path.join(run, "checkpoints", "globe.blend"))
    scene = bpy.context.scene
    outdir = os.path.join(run, "renders", "final-4k", "globe")
    os.makedirs(outdir, exist_ok=True)
    made = [SC.render_still(scene, "GLOBE_HOME", os.path.join(outdir, "globe-overview.png"),
                            res=(3840, 2160), samples=64)]
    prev = os.path.join(run, "renders", "previews", "globe")
    os.makedirs(prev, exist_ok=True)
    SC.render_still(scene, "GLOBE_HOME", os.path.join(prev, "globe-overview.png"),
                    res=(1280, 720), samples=32)
    for site in ("kodingareng", "tunda", "amur"):
        SC.render_still(scene, "GLOBE_REGION_" + site,
                        os.path.join(prev, "region-%s.png" % site),
                        res=(1280, 720), samples=32)
    return made


def globe_reel(run):
    bpy.ops.wm.open_mainfile(filepath=os.path.join(run, "checkpoints", "globe.blend"))
    scene = bpy.context.scene
    outdir = os.path.join(run, "renders", "globe-reel")
    os.makedirs(outdir, exist_ok=True)
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 8
    try:
        scene.eevee.use_raytracing = False
    except Exception:
        pass
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.fps = 24
    scene.camera = bpy.data.objects["GLOBE_REEL"]
    scene.render.filepath = os.path.join(outdir, "frame_")
    scene.frame_start, scene.frame_end = 1, 144
    bpy.ops.render.render(animation=True)
    return {"frames": 144, "dir": outdir}


def main():
    a = parse()
    run = a["run_root"]
    mode = a["mode"]
    target = a.get("target")
    if mode == "stills":
        made = stills(run, target)
    elif mode == "travel":
        made = travel(run, target)
    elif mode == "globe":
        made = globe(run)
    elif mode == "globe-reel":
        made = globe_reel(run)
    else:
        raise SystemExit("unknown mode " + mode)
    print("RENDER " + json.dumps({"mode": mode, "target": target,
                                  "made": made if isinstance(made, dict) else len(made)}))


if __name__ == "__main__":
    main()


