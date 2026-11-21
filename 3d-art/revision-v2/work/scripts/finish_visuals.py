"""Finish the visual-fix pass: section stills + the only changed travel frames."""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import v2scene as SC

SURFACE = ("ENV_Land", "ENV_Water", "BLD_Village", "PROP_Survey", "VEG_Scatter",
           "FX_Water", "GUIDE_Authoring")
SECTION_HIDE = ("ENV_Land", "ENV_Water", "BLD_Village", "VEG_Scatter",
                "PROP_Survey", "FX_Water", "GUIDE_Authoring")


def main():
    run = sys.argv[sys.argv.index("--") + 1]
    for site in ("kodingareng", "tunda", "amur"):
        bpy.ops.wm.open_mainfile(filepath=os.path.join(run, "checkpoints",
                                                       "coast-%s.blend" % site))
        scene = bpy.context.scene
        # 4K section still + review preview
        SC.render_still(scene, "COAST_SECTION",
                        os.path.join(run, "renders", "final-4k", site, "section.png"),
                        res=(3840, 2160), samples=48, hide=SECTION_HIDE,
                        show=("SEC_Section", "SEC_Stage"))
        SC.render_still(scene, "COAST_SECTION",
                        os.path.join(run, "renders", "previews", site, "section.png"),
                        res=(1280, 720), samples=24, hide=SECTION_HIDE,
                        show=("SEC_Section", "SEC_Stage"))
        # only the overview segment and the cutaway hold changed
        scene.render.engine = "BLENDER_EEVEE"
        scene.eevee.taa_render_samples = 8
        scene.eevee.use_raytracing = False
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1080
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = "PNG"
        scene.render.fps = 24
        prefix = os.path.join(run, "renders", "travel", site, "frame_")
        scene.render.filepath = prefix
        scene.camera = bpy.data.objects["TRAVEL_CAM"]
        SC.set_visibility(show=("ENV_Land", "ENV_Water", "BLD_Village", "PROP_Survey",
                                "VEG_Scatter", "FX_Water", "GUIDE_Authoring"),
                          hide=("SEC_Section", "SEC_Stage"))
        scene.frame_start, scene.frame_end = 1, 61
        bpy.ops.render.render(animation=True)
        scene.camera = bpy.data.objects["COAST_SECTION"]
        SC.set_visibility(show=("SEC_Section", "SEC_Stage"), hide=SECTION_HIDE)
        scene.frame_start, scene.frame_end = 133, 168
        bpy.ops.render.render(animation=True)
        print("FINISH", site, "ok")


if __name__ == "__main__":
    main()
