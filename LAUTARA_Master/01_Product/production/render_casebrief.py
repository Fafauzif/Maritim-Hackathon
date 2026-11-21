from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from PIL import Image
import fitz
P=Path(__file__).resolve().parent
for name, path in [('Body','open-sans/OpenSans-Regular'),('Bold','open-sans/OpenSans-Semibold'),('Title','liberation/LiberationSerif-Regular'),('Italic','liberation/LiberationSerif-Italic')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/'+path+'.ttf'))
W,H=612,792
c=canvas.Canvas(str(P/'layout.pdf'),pagesize=(W,H))
c.setTitle('The Ocean Has Floors | Coastal monitoring workspace'); c.setAuthor('LAUTARA team concept brief')
ink='#173837'; teal='#006D68'; quiet='#496664'; orange='#A64B20'; mist='#E5F0EB'; cream='#FAF8F1'; pale='#CBDCD4'
def rect(x,y,w,h,color):
    c.setFillColor(HexColor(color)); c.rect(x,H-y-h,w,h,stroke=0,fill=1)
def line(x,y,x2,y2,col=pale):
    c.setStrokeColor(HexColor(col)); c.setLineWidth(.7); c.line(x,H-y,x2,H-y2)
def label(x,y,s,size=9,col=teal,font='Bold'):
    c.setFont(font,size);c.setFillColor(HexColor(col));c.drawString(x,H-y-size,s)
def p(x,y,s,w=528,size=12.5,lead=18,font='Body',col=ink):
    obj=Paragraph(s,ParagraphStyle('a',fontName=font,fontSize=size,leading=lead,textColor=HexColor(col),splitLongWords=0))
    _,h=obj.wrap(w,999);obj.drawOn(c,x,H-y-h);return y+h
def start(n,section):
    rect(0,0,W,H,cream);label(42,26,'LAUTARA   /   THE OCEAN HAS FLOORS',9)
    label(435,26,'TEAM CONCEPT BRIEF',9);line(42,49,570,49)
    label(42,65,section.upper(),10,orange)
    line(42,751,570,751);label(42,762,'Coastal observation  /  Russia × Indonesia',8,quiet);label(543,760,f'{n} / 7',9,quiet)
def title(s):label(40,90,s,35,ink,'Title')
def end():c.showPage()
def anchor(url,name):return '<a href="'+url+'" color="#006D68"><u>'+name+'</u></a>'
def img(name,x,y,w,h):
    f=P.parent/(name+'.png'); c.drawImage(str(f),x,H-y-h,w,h,mask='auto')
art=anchor('https://chatgpt.com/library?file_id=libfile_a8a03db5ba0c81919c3c2cf5df53d7c5&amp;account_id=personal','Team research article, p. 7')
glory='https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description'
amur='https://doi.org/10.3390/jmse9090953'
tunda='https://doi.org/10.2478/cjf-2023-0009'
start(1,'The problem')
label(40,90,'The Ocean Has Floors',43,ink,'Title')
p(42,152,'A survey-planning workspace for government coastal monitoring teams',size=17,lead=23,font='Title')
p(42,207,'An officer reviewing proposed sand extraction needs a survey plan before work begins. In this internal 3D map, the officer inspects water currents at different depths, checks available observations and tells the crew where to sample, how deep to go and why.',size=14,lead=21)
rect(42,325,528,226,mist);label(62,346,'KODINGARENG  /  FEBRUARY–OCTOBER 2020',9)
p(62,371,'Days with an eastward component in the regional current model',488,14,19,'Bold')
for yy,depth,val,col in [(418,'Near surface · 0.5 m',139,'#4E9F98'),(475,'Deeper layer · 9.6 m',230,'#116862')]:
    label(63,yy,depth,10,ink);label(460,yy,f'{val} / 274 days',10,ink,'Bold')
    rect(63,yy+23,485,11,'#C8DAD2');rect(63,yy+23,485*val/274,11,col)
p(42,575,'Matching the two layers day by day reveals 96 days when the deeper layer had an eastward component and the surface layer had a westward one. A crew choosing a depth could be asking a materially different question about the same place.',size=13,lead=19)
p(42,657,'These daily counts describe one model cell roughly 9 km across. Testing whether sediment reached a particular reef would also require local observations and a dated record of the work.',size=10.5,lead=15,col=quiet)
p(42,716,art+'  ·  '+anchor(glory,'Copernicus GLORYS12 product'),size=9,lead=12)
end()
import math
back=next((P.parent/'generated_images').glob('exec-4fe3d289*'))
def dot(x,y,r,col):
 c.setFillColor(HexColor(col));c.circle(x,H-y,r,stroke=0,fill=1)
def arr(x,y,angle,length,col=ink,weight=2.5):
 a=math.radians(angle);dx=math.sin(a);dy=-math.cos(a);ex=x+dx*length;ey=y+dy*length
 c.setLineWidth(weight);c.setStrokeColor(HexColor(col));c.line(x,H-y,ex,H-ey)
 for sign in (-1,1):
  c.line(ex,H-ey,ex-dx*length*.30+sign*dy*length*.15,H-(ey-dy*length*.30-sign*dx*length*.15))
def mapview(x,y,w,h,depth=0,section=False):
 c.drawImage(str(back),x,H-y-h,w,h)
 def xy(a,b):return x+a*w,y+b*h
 def loop(points,col):
  c.setStrokeColor(HexColor(col));c.setLineWidth(1.3);c.setDash(3,2)
  ss=c.beginPath();xx,yy=xy(*points[0]);ss.moveTo(xx,H-yy)
  for a,b in points[1:]:
   xx,yy=xy(a,b);ss.lineTo(xx,H-yy)
  ss.close();c.drawPath(ss);c.setDash()
 loop([(.45,.86),(.64,.54),(.69,.34),(.60,.4),(.42,.79)],'#FFF8D6')
 loop([(.74,.23),(.91,.25),(.90,.42),(.76,.39)],'#FFC081')
 sx,sy=xy(.57,.59);dot(sx,sy,5.5,'#FFFFFF');dot(sx,sy,3,orange)
 rect(sx+7,sy-6,25,13,ink);label(sx+10,sy-5,'S-01',7,'#FFFFFF')
 if section:
  ax,ay=xy(.3,.66);bx,by=xy(.78,.52)
  line(ax,ay,bx,by,'#FFFFFF')
  for x1,y1,l in [(ax,ay,'A'),(bx,by,'B')]:
   dot(x1,y1,7.5,ink);label(x1-2.5,y1-4.8,l,7.5,'#FFFFFF')
 else:
  ax,ay=xy(.76,.73);dot(ax,ay,16,'#DFEFEB');arr(ax,ay,[264,45][depth],14,teal,2)
 label(x+w-21,y+4,'N',8,'#FFFFFF');arr(x+w-15,y+29,0,11,'#FFFFFF',1)
def btn(x,y,w,txt,on=True):
 rect(x,y,w,19,teal if on else mist);label(x+6,y+4,txt,8,'#FFFFFF' if on else ink)
start(2,'Proposed operator interface');title('The case opens on the coast')
p(42,141,'The officer opens a proposed works case and sees the whole area from above. Select a station, change the viewing depth, then decide what to ask the field crew to measure.',size=13,lead=18)
rect(34,211,544,332,'#E0E8E4');rect(35,212,542,31,ink)
label(46,221,'COASTAL MONITORING    /    Kodingareng',10,'#FFFFFF')
label(439,223,'Draft case  ·  KR-01',8.4,'#FFFFFF')
mapview(35,243,379,222)
rect(414,243,163,222,'#F2F4ED');label(424,252,'STATION  S-01',9)
label(424,274,'Viewing depth',11,ink,'Bold');btn(424,296,61,'0.5 m',True);btn(489,296,72,'9.6 m',False)
label(424,324,'Model date',8,quiet);label(424,339,'16 Apr 2020  ·  UTC',10,ink)
label(424,363,'GLORYS12  /  daily mean',8,quiet);label(424,380,'0.093 m/s   ·   264°',11,ink)
label(424,402,'Regional cell  ·  ~9 km',8,quiet)
btn(424,424,138,'+ Request field check')
rect(35,465,542,77,'#F5F4EE')
label(45,474,'MAP KEY',8,quiet);dot(112,481,3,orange);label(120,475,'Station',8,ink)
rect(171,474,25,12,'#237976');c.setDash(3,2);line(174,480,193,480,'#FFC081');c.setDash();label(197,475,'Proposed works',8,ink)
rect(286,474,24,12,'#237976');c.setDash(3,2);line(288,480,308,480,'#FFF8D6');c.setDash();label(312,475,'Reef outline',8,ink)
arr(397,483,45,9,teal,1.5);label(409,475,'Modeled current',8,ink)
label(45,507,'Overhead view',10,teal);label(157,507,'Draw section A–B',10,ink);label(303,507,'Compare depths',10,ink)
p(42,551,'Design mockup. The island, reef, station and work boundary illustrate the interface. The dated current reading is from the archived regional model.',528,9,13,col=quiet)
p(42,604,'What does “viewing depth” change?',size=21,lead=26,font='Title')
p(42,642,'The coast stays in place. Selecting a deeper layer shows how the water there was estimated to move on the chosen date. An officer can compare layers from above, then draw a section wherever the shape of the seabed matters to the sampling plan.',size=12,lead=17)
end()
start(3,'Two states of the same operator screen');title('Change the depth. Keep the date.')
p(42,141,'Kodingareng  ·  16 April 2020. Both views use the same camera, proposed station and regional model cell. The selected depth changes the current reading.',size=12.6,lead=18)
for i,x in enumerate((42,312)):
 rect(x,211,258,28,ink);label(x+9,219,'VIEWING DEPTH     '+['0.5 m','9.6 m'][i],9.4,'#FFFFFF')
 mapview(x,239,258,148,i)
 rect(x,387,258,98,mist)
 label(x+10,397,'MODELED CURRENT   /   DAILY MEAN',8,teal)
 label(x+10,417,['0.093 m/s   ·   264°','0.074 m/s   ·   045°'][i],17,ink,'Bold')
 label(x+10,448,['Toward the west','Toward the northeast'][i],11,ink)
p(42,506,'The surface estimate would point the officer west. At 9.6 m the estimate points northeast. To check whether this change occurs locally, select <b>Request field check</b> and ask for a current profile at S-01.',size=13,lead=19)
rect(42,598,528,107,'#E7EEEA')
# true geographic cell inset schematic, locate demo station relative to cell bounds
gx,gy=57,618;side=67
rect(gx,gy,side,side,'#CADCD5')
line(gx,gy+side/2,gx+side,gy+side/2,'#A0B4AB');line(gx+side/2,gy,gx+side/2,gy+side,'#A0B4AB')
dot(gx+side*(.5+.012/.083333),gy+side*(.5-.011667/.083333),3,orange)
label(60,688,'~9 km cell',8,quiet)
p(140,609,'How local is the arrow?',410,13,18,'Bold')
p(140,635,'One arrow summarizes the whole grid cell, centered at 5.1667° S, 119.2500° E. The dot marks the illustrative station inside it. A current profiler can test the model at the station.',410,10.6,15)
p(42,717,anchor('https://chatgpt.com/library?file_id=libfile_b8704091df1c819189fa17cf61011304&amp;account_id=personal','Source archive')+' · marine/glorys_daily.csv. Bearings are clockwise from north.',528,8.9,12,col=quiet)
end()
start(4,'Section view and field request');title('Take a slice through the station')
p(42,143,'Draw A–B through S-01. The camera turns along that line and keeps the jetty on the left. In section view, the officer sets a proposed sampling depth and saves it in the case.',size=12,lead=17)
mapview(42,210,256,146,section=True)
from PIL import ImageOps
from reportlab.lib.utils import ImageReader
cut=ImageOps.fit(Image.open(P.parent/'hero.png'),(1036,584));c.drawImage(ImageReader(cut),311,H-356,259,146)
rect(322,219,163,17,cream);label(328,222,'Proposed sample depth    9.6 m',8,ink)
for xx,lett in [(320,'A'),(555,'B')]:
 dot(xx,290,7.5,ink);label(xx-2.5,285,lett,7.5,'#FFFFFF')
label(42,365,'Overhead   /   Select section A–B',9)
label(311,365,'Section A–B   /   Set target depth',9)
p(42,391,'The two drawings show the proposed interaction. The section in the working app would use the selected line and a bathymetry grid to draw the seabed.',528,9,13,col=quiet)
p(42,442,'From model evidence to a field action',size=19,lead=23,font='Title')
p(42,699,'A current profiler records motion at depth. A bottle supplies water for sediment analysis. The requested instrument follows the question the officer needs to answer.',528,10.3,14,col=quiet)
end()
start(5,'Case handoff');title('What goes to the field crew?')
p(42,145,'A supervisor reviews the proposed station and issues a versioned brief. When the boat returns, the field lead attaches the readings and sample IDs to the same case.',size=12.5,lead=18)
rect(42,209,528,316,mist);label(57,224,'EXAMPLE FIELD BRIEF    /    DRAFT FOR REVIEW',9,teal)
p(57,248,'KR-01     Kodingareng baseline survey',491,18,23,'Title')
for yy,key,val in [
(288,'Station','S-01 · 5.1550° S, 119.2620° E (illustrative WGS84 waypoint).'),
(321,'When','Proposed pre-work visit, 08:00–10:00 WITA. Field lead confirms the date and local water depth before deployment.'),
(372,'Current check','Run a current profiler at S-01. Compare readings near 0.5 m and 9.6 m below surface where both depths are submerged.'),
(424,'Sediment baseline','Collect paired water bottles at the two target depths if feasible. Log actual depth, time and sample ID for each bottle.'),
(475,'Review and return','Coastal monitoring supervisor reviews the plan. Field lead returns the profile and lab results to case KR-01.')]:
 p(57,yy,key,104,10.2,14,'Bold');p(168,yy,val,385,10.2,14)
p(42,539,'Planning example only. Coordinates and field instructions illustrate the handoff. Model evidence attached: GLORYS12 daily mean, 16 April 2020, reference cell on page 3.',528,9,13,col=quiet)
p(42,599,'How two offices could use the same workflow',size=19,lead=24,font='Title')
p(42,638,'An Indonesian reviewer could share the Kodingareng plan. An Amur Bay reviewer could compare its depth choices with a published local survey that sampled near the surface and above the bed. Each office records what it would change and why. Tunda offers a further case for planning a reef baseline before proposed work.',528,11.2,16)
p(42,721,anchor(tunda,'Tunda reef survey')+'  ·  '+anchor(amur,'Amur Bay sampling methods'),528,8.8,12)
end()
start(6,'Suggested web architecture');title('How the browser experience works')
p(42,148,'Prepare dated coastal layers in advance for fast inspection. Keep case records and review decisions in an access-controlled service. The map and case file share the selected station, depth and source.',size=13,lead=19)
def table(y,rows):
    for h,t,b in rows:
        line(42,y,570,y);p(42,y+10,t,164,11.4,15,'Bold');p(225,y+10,b,344,11.1,15.2);y+=h
    return y
table(223,[(76,'Web interface<br/>React + TypeScript','Display the case, station, date, evidence and draft plan. Offer both the cable gesture and keyboard depth entry.'),(80,'3D scene<br/>Three.js + React Three Fiber','Switch depth layers in the overhead view. Pivot around A–B, clip the water and draw the exposed section, with the boat anchored to its map position.'),(87,'Art assets<br/>Blender → glTF / GLB','Model low-detail boats, jetties and buildings. Optional Blender MCP support helps artists place or revise objects during production. Export approved meshes to the web app.'),(82,'Scientific processing<br/>Python + Xarray + Rasterio','Keep native grid cells and depth levels. Convert selected model dates, local terrain and image masks into compact assets with source and units attached.'),(76,'Case records<br/>FastAPI + PostgreSQL','Use agency sign-in and role-based access. Version survey plans, record sign-off, attach field results and export the issued brief with its evidence sources.')])
rect(42,646,528,68,mist);p(56,657,'First build test',490,11,14,'Bold');p(56,675,'Can a colleague open an issued brief, recover its exact source and depths, and attach measured results to the correct station?',492,10.4,14.5)
p(42,729,anchor('https://r3f.docs.pmnd.rs/getting-started/introduction','React Three Fiber')+'   ·   '+anchor('https://github.com/ahujasid/mcp-for-blender','Community Blender MCP integration'),size=8.6,lead=11)
end()
start(7,'Implementation reference');title('The datasets behind the scene')
p(42,145,'Fetch public data when preparing the case layers. Bundle the source ID, acquisition date, units, grid size, quality flags and access terms with each layer. Linked documentation below is the starting point for integration.',size=12,lead=17)
cop='https://help.marine.copernicus.eu/en/articles/8283072-copernicus-marine-toolbox-api-subset'
cdse='https://documentation.dataspace.copernicus.eu/APIs/STAC.html'
usgs='https://www.usgs.gov/landsat-missions/spatiotemporal-asset-catalog-stac'
rows=[
(79,'Currents by depth',anchor(cop,'Copernicus Marine Toolbox subset API')+' · GLORYS12 daily means. Select uo and vo (m/s) by time, depth and bounding box. Dataset: cmems_mod_glo_phy_my_0.083deg_P1D-m.'),
(78,'Seabed and habitat',anchor('https://big.go.id/en/content/product/demnas','BIG BATNAS')+' · Indonesian bathymetry, 6 arc-seconds. '+anchor('https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2025-grid','GEBCO 2025')+' · bilateral terrain, 15 arc-seconds. Use '+anchor('https://allencoralatlas.org/methods/','Allen Coral Atlas')+' mapped reef extent where coverage permits. Check depth datum before joining layers.'),
(70,'Satellite surface view',anchor(cdse,'Copernicus Data Space STAC')+' for Sentinel-2 and '+anchor(usgs,'USGS Landsat STAC')+' for Landsat 8/9. Search the reef footprint and date, then screen cloud, shadow and glint over that footprint.'),
(76,'Local measurements',anchor('https://www.ncei.noaa.gov/access/world-ocean-database-select/dbsearch.html','NOAA WODselect')+' for profiles and '+anchor('https://www.ncei.noaa.gov/access/search/datasets/standard-product-global-ocean-currents-database/','NOAA GOCD')+' for acoustic current records. Match variable, coordinates, depth and date. Raw turbidity profiles from the Amur survey still need verification.'),
(75,'Rain, runoff and waves',anchor('https://gpm.nasa.gov/data/imerg','NASA GPM IMERG')+' via '+anchor('https://earthaccess.readthedocs.io/en/latest/','earthaccess')+' for catchment rain. Compare '+anchor('https://ewds.climate.copernicus.eu/datasets/cems-glofas-historical?tab=overview','GloFAS discharge')+' where the river is represented and '+anchor('https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels','ERA5 wind and waves')+' to investigate other explanations for surface brightness.')]
yy=225
for h,t,b in rows:
    line(42,yy,570,yy);p(42,yy+11,t,124,11.5,15,'Bold');p(177,yy+9,b,393,10.5,15);yy+=h
rect(42,624,528,98,mist);label(56,635,'FIRST DATA CHECK',9)
p(56,654,'Pick one Kodingareng day and two wet model depths. Reproduce both current vectors from the source file. Then query for a nearby current profile and record the match or the gap. This gives the team one complete, traceable scene to build around.',496,11.2,16)
end();c.save()
doc=fitz.open(P/'layout.pdf');flow=fitz.open(P/'flow.pdf')
doc[3].show_pdf_page(fitz.Rect(122,473,490,687),flow,0)
out=Path('/mnt/data/The_Ocean_Has_Floors.pdf');doc.save(out,garbage=4,deflate=True)
