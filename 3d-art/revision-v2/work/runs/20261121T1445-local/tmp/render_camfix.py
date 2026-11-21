import bpy, os, hashlib, sys
sys.path.insert(0, r'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\scripts')
import v2scene as SC
bpy.ops.wm.open_mainfile(filepath=r'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\checkpoints\coast-kodingareng.blend')
sc=bpy.context.scene
for cam in ['COAST_OVERVIEW','COAST_PLAN','COAST_APPROACH','COAST_DETAIL','COAST_SECTION']:
    hide=('SEC_Section','SEC_Stage') if cam!='COAST_SECTION' else ('ENV_Land','ENV_Water','BLD_Village','VEG_Scatter','PROP_Survey','FX_Water','GUIDE_Authoring')
    show=('SEC_Section','SEC_Stage') if cam=='COAST_SECTION' else ()
    info=SC.render_still(sc,cam,r'C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\tmp\fix_'+cam+'.png',res=(480,270),samples=6,hide=hide,show=show)
    print('FIX',cam,os.path.getsize(info['path']),hashlib.sha256(open(info['path'],'rb').read()).hexdigest()[:12])
