"""Headless render passes for phases 04-05.

Called by the orchestration job, never by the interactive session:

    blender -b 03-kodingareng.blend --python render_pass.py -- stills kodingareng
    blender -b 03-kodingareng.blend --python render_pass.py -- beforeafter kodingareng
    blender -b 04-globe.blend        --python render_pass.py -- globe
    blender -b 04-globe.blend        --python render_pass.py -- reel

Everything writes to `work/renders/` (and `work/reviews/before|after`), so a
failed pass never leaves a half-deliverable in `output/`.
"""
import os
import sys

import bpy

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
SCRIPTS = os.path.join(ART, 'work', 'scripts')
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

RENDERS = os.path.join(ART, 'work', 'renders')
REVIEWS = os.path.join(ART, 'work', 'reviews')

BEAUTY_HIDE = ('SEC_Section',)
SECTION_HIDE = ('ENV_Land', 'ENV_Water', 'BLD_Village', 'VEG_Scatter')

STILLS = [
    ('COAST_OVERVIEW', 'godview', BEAUTY_HIDE),
    ('COAST_PLAN', 'mapview', BEAUTY_HIDE),
    ('COAST_SECTION', 'section', SECTION_HIDE),
]


def render(scene, camera_name, path, res, samples, hide):
    import scene_build as SC
    return SC.render_still(scene, camera_name, path, res=res,
                           engine='BLENDER_EEVEE', samples=samples, hide=hide)


def stills(site):
    scene = bpy.context.scene
    out_dir = os.path.join(RENDERS, 'final-4k')
    os.makedirs(out_dir, exist_ok=True)
    made = []
    for cam, slug, hide in STILLS:
        path = os.path.join(out_dir, '%s_%s.png' % (site, slug))
        info = render(scene, cam, path, (3840, 2160), 48, hide)
        made.append({'camera': cam, 'path': path, 'bytes': info['bytes'],
                     'resolution': info['resolution'], 'engine': info['engine']})
    return made


def beforeafter(site):
    """One real before/after pair per coast, each isolating a fixed defect.

    before/overview = the old colour pipeline (AgX + exposure 0.1 + Hue/Sat 0.92)
    after/overview  = the measured rig in look_rig.py
    before/section  = the cut with its strata hidden (the hollow-cut defect)
    after/section   = the solid cut
    """
    import look_rig
    scene = bpy.context.scene
    before = os.path.join(REVIEWS, 'before')
    after = os.path.join(REVIEWS, 'after')
    os.makedirs(before, exist_ok=True)
    os.makedirs(after, exist_ok=True)
    made = []

    nov = os.path.join(after, '%s_overview.png' % site)
    made.append({'tag': 'after_overview',
                 **render(scene, 'COAST_OVERVIEW', nov, (1280, 720), 32, BEAUTY_HIDE)})

    old = {'view_transform': 'AgX', 'look': 'AgX - Medium High Contrast',
           'exposure': 0.10, 'sun': 4.6, 'fill': 320.0, 'world': 0.62, 'grade_sat': 0.92}
    look_rig.apply(scene, old)
    bov = os.path.join(before, '%s_overview_oldrig.png' % site)
    made.append({'tag': 'before_overview',
                 **render(scene, 'COAST_OVERVIEW', bov, (1280, 720), 32, BEAUTY_HIDE)})
    look_rig.apply(scene)

    sec = os.path.join(after, '%s_section.png' % site)
    made.append({'tag': 'after_section',
                 **render(scene, 'COAST_SECTION', sec, (1600, 900), 32, SECTION_HIDE)})

    hidden = list(SECTION_HIDE) + ['SEC_Section']
    # temporarily reveal only the shallow band: hide the solid block and strata
    for name in ('SEC_BedCut', 'SEC_Stratum_A', 'SEC_Grass'):
        ob = bpy.data.objects.get(name)
        if ob:
            ob.hide_render = True
    bsec = os.path.join(before, '%s_section_hollow.png' % site)
    made.append({'tag': 'before_section',
                 **render(scene, 'COAST_SECTION', bsec, (1600, 900), 32, SECTION_HIDE)})
    for name in ('SEC_BedCut', 'SEC_Stratum_A', 'SEC_Grass'):
        ob = bpy.data.objects.get(name)
        if ob:
            ob.hide_render = False
    return made


def globe():
    scene = bpy.context.scene
    out_dir = os.path.join(RENDERS, 'final-4k')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'globe_overview.png')
    info = render(scene, 'GLOBE_HOME', path, (3840, 2160), 64, ())
    reg = []
    for site in ('kodingareng', 'tunda', 'amur'):
        rp = os.path.join(RENDERS, 'globe', 'globe-region-%s-4k.png' % site)
        reg.append(render(scene, 'GLOBE_REGION_' + site, rp, (1920, 1080), 32, ()))
    return {'overview': info, 'regions': reg}


def reel():
    scene = bpy.context.scene
    out_dir = os.path.join(RENDERS, 'globe-reel')
    os.makedirs(out_dir, exist_ok=True)
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.engine = 'BLENDER_EEVEE'
    try:
        scene.eevee.taa_render_samples = 24
    except Exception:
        pass
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = os.path.join(out_dir, 'frame_')
    scene.frame_start = 1
    scene.frame_end = 72
    scene.render.fps = 24
    bpy.ops.render.render(animation=True)
    return {'frames_dir': out_dir, 'count': 72}


def travel(site):
    """Two-pass film render: travel shot, then the cutaway shot.

    Collection visibility cannot be keyframed in 5.2, so each shot is rendered
    with its own fixed visibility instead of switching mid-animation. The frames
    keep their real numbers (1-108 then 109-132), so the sequence stays one film.
    """
    scene = bpy.context.scene
    out_dir = os.path.join(RENDERS, 'travel-frames', site)
    os.makedirs(out_dir, exist_ok=True)
    scene.render.filepath = os.path.join(out_dir, 'frame_')

    surface = ['ENV_Land', 'ENV_Water', 'BLD_Village', 'VEG_Scatter']
    for name in surface:
        coll = bpy.data.collections.get(name)
        if coll:
            coll.hide_render = False
    sec = bpy.data.collections.get('SEC_Section')
    if sec:
        sec.hide_render = True
    scene.frame_start = 1
    scene.frame_end = 108
    bpy.ops.render.render(animation=True)

    for name in surface:
        coll = bpy.data.collections.get(name)
        if coll:
            coll.hide_render = True
    if sec:
        sec.hide_render = False
    scene.frame_start = 109
    scene.frame_end = 132
    bpy.ops.render.render(animation=True)
    return {'frames_dir': out_dir, 'range': [1, 132]}


def main():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    if not argv:
        raise SystemExit('need a mode: stills|beforeafter|globe|reel [site]')
    mode = argv[0]
    site = argv[1] if len(argv) > 1 else None
    if mode == 'stills':
        made = stills(site)
        print('STILLS', site, [m['path'] for m in made])
    elif mode == 'beforeafter':
        made = beforeafter(site)
        print('BEFOREAFTER', site, [(m['tag'], m.get('path')) for m in made])
    elif mode == 'globe':
        info = globe()
        print('GLOBE', info['overview']['path'], info['overview']['bytes'])
    elif mode == 'reel':
        print('REEL', reel())
    else:
        raise SystemExit('unknown mode %s' % mode)


if __name__ == '__main__':
    main()
