import bpy
bpy.ops.wm.open_mainfile(filepath=r'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\checkpoints\coast-kodingareng.blend')
sc=bpy.context.scene
for name in ['COAST_OVERVIEW','COAST_PLAN','COAST_APPROACH','COAST_DETAIL']:
    o=bpy.data.objects[name]
    print('OBJ',name,id(o),o.type,[round(v,2) for v in o.location],[(c.type,getattr(c,'target',None).name if getattr(c,'target',None) else None) for c in o.constraints])
for name in ['COAST_OVERVIEW','COAST_PLAN']:
    o=bpy.data.objects[name]
    sc.camera=o
    print('SET',name,'->',sc.camera.name,[round(v,2) for v in sc.camera.location])
