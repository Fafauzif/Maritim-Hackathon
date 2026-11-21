import bpy, time, os
bpy.ops.wm.open_mainfile(filepath=r'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\checkpoints\coast-kodingareng.blend')
sc=bpy.context.scene
sc.render.engine='BLENDER_EEVEE'
sc.eevee.taa_render_samples=10
sc.eevee.use_raytracing=False
sc.render.resolution_x=1920; sc.render.resolution_y=1080
sc.render.image_settings.file_format='PNG'
sc.camera=bpy.data.objects['TRAVEL_CAM']
sc.frame_set(30)
sc.render.filepath=r'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\tmp\anim-timing.png'
t=time.time(); bpy.ops.render.render(write_still=True)
print('ANIMTIMING', round(time.time()-t,3))
