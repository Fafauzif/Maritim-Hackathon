import bpy, os, hashlib
bpy.ops.wm.open_mainfile(filepath=r'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\checkpoints\coast-kodingareng.blend')
sc=bpy.context.scene
sc.render.engine='BLENDER_EEVEE'; sc.render.resolution_x=320; sc.render.resolution_y=180
sc.eevee.taa_render_samples=4
for coll in bpy.data.collections: coll.hide_render = coll.name in ('SEC_Section','SEC_Stage')
def shot(name, use_comp=True, frame=1):
    sc.render.use_compositing=use_comp
    sc.frame_set(frame)
    sc.camera=bpy.data.objects[name]
    p=r'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\tmp\ct2_'+name+('_f%d'%frame)+('_nc' if not use_comp else '')+'.png'
    sc.render.filepath=p
    bpy.ops.render.render(write_still=True)
    print('SHOT',name,'comp',use_comp,'frame',frame,'cam',sc.camera.name,hashlib.sha256(open(p,'rb').read()).hexdigest()[:12], [round(v,1) for v in sc.camera.matrix_world.translation])
shot('COAST_OVERVIEW',True,1)
shot('COAST_PLAN',True,1)
shot('COAST_APPROACH',True,1)
shot('COAST_PLAN',False,1)
shot('COAST_APPROACH',False,1)
shot('COAST_PLAN',True,2)
shot('COAST_APPROACH',True,2)
