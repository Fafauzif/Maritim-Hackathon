"""Render the phase-01 blockout proofs and phase-02/03 beauty proofs for a site.

    import render_proofs; render_proofs.run("kodingareng", which="blockout")
"""
import os
import sys

import bpy

HERE = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\work\scripts"
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import scene_build as SC

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
RENDERS = os.path.join(ART, "work", "renders")

MAIN_HIDE = ('SEC_Section',)
SECTION_HIDE = ('ENV_Land', 'ENV_Water', 'BLD_Village', 'VEG_Scatter')


def run(site, which='blockout', res=(960, 540)):
    out = []
    scene = bpy.context.scene
    cul = os.path.join(RENDERS, 'blockout' if which == 'blockout' else 'coast')
    os.makedirs(cul, exist_ok=True)
    engine = 'BLENDER_WORKBENCH' if which == 'blockout' else 'BLENDER_EEVEE'

    out.append(SC.render_still(scene, 'COAST_OVERVIEW',
                               os.path.join(cul, '%s_overview.png' % site),
                               res=res, engine=engine, samples=32, hide=MAIN_HIDE))
    out.append(SC.render_still(scene, 'COAST_SECTION',
                               os.path.join(cul, '%s_section.png' % site),
                               res=res, engine=engine, samples=32, hide=SECTION_HIDE))
    if which != 'blockout':
        out.append(SC.render_still(scene, 'COAST_PLAN',
                                   os.path.join(cul, '%s_plan.png' % site),
                                   res=res, engine=engine, samples=32, hide=MAIN_HIDE))
        out.append(SC.render_still(scene, 'COAST_APPROACH',
                                   os.path.join(cul, '%s_approach.png' % site),
                                   res=res, engine=engine, samples=32, hide=MAIN_HIDE))
    return {'site': site, 'which': which, 'engine': engine,
            'shots': out, 'render_dir': cul}
