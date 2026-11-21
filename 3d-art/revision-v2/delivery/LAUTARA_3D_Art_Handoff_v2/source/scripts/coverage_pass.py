"""Workbench object-colour coverage pass for measurable composition QA."""
import json
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

CATS = {
    "terrain": (0.0, 0.75, 0.0),
    "water": (0.0, 0.0, 0.8),
    "building": (0.8, 0.0, 0.0),
    "jetty": (0.9, 0.9, 0.0),
    "boat": (1.0, 0.45, 0.0),
    "vegetation": (0.0, 0.35, 0.0),
    "waterfx": (0.0, 0.8, 0.8),
    "section": (0.55, 0.0, 0.55),
    "backdrop": (0.95, 0.95, 0.95),
    "other": (0.45, 0.45, 0.45),
    "background": (1.0, 0.0, 1.0),
}


def category(ob):
    n = ob.name
    if n.startswith("ENV_Terrain"):
        return "terrain"
    if n.startswith("ENV_Water"):
        return "water"
    if n.startswith(("BLD_", "KIT_House")):
        return "building"
    if n.startswith("PROP_Jetty"):
        return "jetty"
    if n.startswith(("PROP_SurveyBoat", "PROP_LocalBoat")):
        return "boat"
    if n.startswith("VEG_"):
        return "vegetation"
    if n.startswith(("FX_", "SEC_Waterline")):
        return "waterfx"
    if n.startswith(("SEC_", "SECTION_")):
        return "backdrop" if n == "SEC_Backdrop" else "section"
    if n.startswith(("ENV_Lane", "ENV_Plaza", "PROP_Crate")):
        return "other"
    return "other"


def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    blend = args[0]
    outdir = args[1]
    slug = args[2]
    bpy.ops.wm.open_mainfile(filepath=blend)
    scene = bpy.context.scene
    for ob in scene.objects:
        cat = category(ob)
        ob.color = (*CATS[cat], 1.0)
        ob["qa_category"] = cat
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    sh = scene.display.shading
    sh.light = "FLAT"
    sh.color_type = "OBJECT"
    sh.show_shadows = False
    sh.show_cavity = False
    sh.background_type = "VIEWPORT"
    sh.background_color = CATS["background"]
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0
    os.makedirs(outdir, exist_ok=True)
    made = []
    for cam in ("COAST_OVERVIEW", "COAST_PLAN", "COAST_APPROACH", "COAST_DETAIL",
                "COAST_SECTION"):
        c = bpy.data.objects.get(cam)
        if not c:
            continue
        scene.camera = c
        if cam == "COAST_SECTION":
            for name in ("ENV_Land", "ENV_Water", "BLD_Village", "VEG_Scatter",
                         "PROP_Survey", "FX_Water", "GUIDE_Authoring"):
                cc = bpy.data.collections.get(name)
                if cc:
                    cc.hide_render = True
            for name in ("SEC_Section", "SEC_Stage"):
                cc = bpy.data.collections.get(name)
                if cc:
                    cc.hide_render = False
        else:
            for coll in bpy.data.collections:
                coll.hide_render = False
            for name in ("SEC_Section", "SEC_Stage"):
                cc = bpy.data.collections.get(name)
                if cc:
                    cc.hide_render = True
        path = os.path.join(outdir, "%s_%s.png" % (slug, cam))
        scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
        made.append({"camera": cam, "path": path})
    with open(os.path.join(outdir, "%s_coverage.json" % slug), "w", encoding="utf-8") as fh:
        json.dump({"blend": blend, "shots": made, "categories": CATS}, fh, indent=2)
    print("COVERAGE", json.dumps({"slug": slug, "shots": len(made)}))


if __name__ == "__main__":
    main()

