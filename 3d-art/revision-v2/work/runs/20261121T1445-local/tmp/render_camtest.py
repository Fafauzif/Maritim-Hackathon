import bpy, os, hashlib
bpy.ops.wm.open_mainfile(filepath=r'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\checkpoints\coast-kodingareng.blend')
sc=bpy.context.scene
sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=640; sc.render.resolution_y=360
sc.render.image_settings.file_format='PNG'
sc.eevee.taa_render_samples=8
for coll in bpy.data.collections:
    coll.hide_render = coll.name in ('SEC_Section','SEC_Stage')
for cam in ['COAST_OVERVIEW','COAST_PLAN','COAST_APPROACH','COAST_DETAIL']:
    sc.camera=bpy.data.objects[cam]
    p=r'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\tmp\camtest_'+cam+'.png'
    sc.render.filepath=p
    bpy.ops.render.render(write_still=True)
    print('RENDERED',cam,os.path.getsize(p),hashlib.sha256(open(p,'rb').read()).hexdigest()[:16], [round(v,2) for v in sc.camera.location])
