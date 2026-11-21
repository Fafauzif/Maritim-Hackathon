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
p(42,207,'A coastal monitoring officer is reviewing proposed sand extraction near a reef. Before work starts, the field crew needs a baseline. A map pin tells the skipper where to stop. It leaves the crew to guess which depth to sample and why.',size=14,lead=21)
rect(42,325,528,226,mist);label(62,346,'KODINGARENG  /  FEBRUARY–OCTOBER 2020',9)
p(62,371,'Days with an eastward component in the regional current model',488,14,19,'Bold')
for yy,depth,val,col in [(418,'Near surface · 0.5 m',139,'#4E9F98'),(475,'Deeper layer · 9.6 m',230,'#116862')]:
    label(63,yy,depth,10,ink);label(460,yy,f'{val} / 274 days',10,ink,'Bold')
    rect(63,yy+23,485,11,'#C8DAD2');rect(63,yy+23,485*val/274,11,col)
p(42,575,'On at least 91 of those days, the deeper layer had an eastward component while the surface layer did not. A crew choosing a depth could be asking a materially different question about the same place.',size=13,lead=19)
p(42,657,'These daily counts describe one model cell roughly 9 km across. Testing whether sediment reached a particular reef would also require local observations and a dated record of the work.',size=10.5,lead=15,col=quiet)
p(42,716,art+'  ·  '+anchor(glory,'Copernicus GLORYS12 product'),size=9,lead=12)
end()
start(2,'The internal workspace');title('Open a case. Inspect the water.')
p(42,148,'Open a coastal works case, select the reef, and draw a line through the proposed station. The map tilts along that line. The boat stays in view as the officer inspects the water beneath it.',size=13,lead=19)
img('hero',42,237,528,352)
rect(51,247,237,44,cream);label(60,253,'EXAMPLE CASE  /  DRAFT SURVEY PLAN',8);label(60,267,'Kodingareng · Pre-work baseline',12,ink)
p(42,595,'Illustrative case view · The waterfront and seabed are concept artwork.',size=8.5,lead=12,col=quiet)
p(42,631,'The bottle cable is the depth control.',size=22,lead=27,font='Title')
p(42,672,'Drag it to a model depth to see the dated current estimate. Select a second depth to compare, then add a proposed sample to the case. The officer records the reason for the request.',size=12.5,lead=18)
end()
start(3,'A day in the monitoring office');title('From a case file to a crew brief')
p(42,145,'In this example, the field lead has one scheduled visit. The officer wants comparable sediment samples at two depths before work begins. Here is how they prepare the request.',size=13,lead=19)
img('walk',42,210,528,352)
for x,h,s in [(42,'Place the pin','Choose the site and date. Trace a line through the proposed station.'),(222,'Turn the coast','Tilt along the line. Keep the boat in sight as the seabed comes into view.'),(402,'Lower the bottle','Select the two target depths. Attach the dated model view to the request.')]:
    p(x,572,h,164,13,16,'Bold');p(x,594,s,164,10,14)
rect(42,660,528,74,mist);label(56,671,'EXAMPLE FIELD BRIEF  /  PROPOSED SAMPLING',8.5)
p(56,690,'Field lead: collect paired surface and near-bed samples at the selected reef station before work. Log depths, times and sample IDs. Return suspended-sediment results to the case reviewer.',500,10.5,15)
end()
start(4,'The evidence flow');title('When does the crew need a sample?')
p(42,148,'Start with a question and a dated model layer. The next step depends on whether someone measured the same thing close enough in place, depth and time.',size=13,lead=19)
# TikZ diagram is embedded as vector art after page composition.
p(42,593,'What counts as a match?',size=20,lead=25,font='Title')
p(42,631,'A current profiler can test a current estimate. A water bottle can test suspended sediment if the sample is analyzed. The brief records the instrument, units, time and distance from the planned station so a second reviewer can judge the comparison.',size=12.5,lead=18)
end()
start(5,'Internal review and handoff');title('What the next reviewer inherits')
p(42,145,'A colleague reopening the case should see the evidence available at the time, the officer’s reasoning, and the field results that came back.',size=13,lead=19)
for y,a,b in [(211,'Depth comparison','Pin two dated layers. See the direction and speed at each depth, alongside the actual model cell that supplied each arrow.'),(277,'Survey design','Compare two depths at one station or two stations at the same depth. Choose the design that answers the case question.'),(343,'Plan comparison','Save a draft baseline plan alongside an alternative. A supervisor can review the differences and record which plan to issue.'),(409,'Peer review','Indonesian and Russian teams could exchange selected case briefs, apply the same evidence rules and document disagreements.')]:
    line(42,y-8,570,y-8);p(42,y,a,150,12.3,17,'Bold');p(202,y,b,368,11.4,15.5)
rect(42,483,528,242,mist);label(58,498,'THREE REFERENCE CASES',9)
for y,h,s in [(525,'Kodingareng, Indonesia','Find dates when regional currents differ by depth. Choose a measurement that could check the model.'),(586,'Tunda, Indonesia','Plan a survey before proposed work near a mapped reef. Choose a baseline station and a backup if clouds cover it.'),(648,'Amur Bay, Russia','Use a published surface-and-bottom survey as a reference for paired sampling. Check the underlying records before attaching a measured value.')]:
    p(58,y,h,493,11,14,'Bold');p(58,y+17,s,495,10.4,14)
p(42,731,anchor(tunda,'Tunda reef survey')+'   ·   '+anchor(amur,'Amur Bay field methods, August 2007'),size=8.4,lead=10)
end()
start(6,'Suggested web architecture');title('How the browser experience works')
p(42,148,'Prepare dated coastal layers in advance for fast inspection. Keep case records and review decisions in an access-controlled service. The map and case file share the selected station, depth and source.',size=13,lead=19)
def table(y,rows):
    for h,t,b in rows:
        line(42,y,570,y);p(42,y+10,t,164,11.4,15,'Bold');p(225,y+10,b,344,11.1,15.2);y+=h
    return y
table(223,[(76,'Web interface<br/>React + TypeScript','Display the case, station, date, evidence and draft plan. Offer both the cable gesture and keyboard depth entry.'),(80,'3D scene<br/>Three.js + React Three Fiber','Orbit the scene around the selected line. Clip the water and draw the exposed section, with the boat anchored to its map position.'),(87,'Art assets<br/>Blender → glTF / GLB','Model low-detail boats, jetties and buildings. Optional Blender MCP support helps artists place or revise objects during production. Export approved meshes to the web app.'),(82,'Scientific processing<br/>Python + Xarray + Rasterio','Keep native grid cells and depth levels. Convert selected model dates, local terrain and image masks into compact assets with source and units attached.'),(76,'Case records<br/>FastAPI + PostgreSQL','Use agency sign-in and role-based access. Version survey plans, record sign-off, attach field results and export the issued brief with its evidence sources.')])
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
doc[3].show_pdf_page(fitz.Rect(80,228,532,568),flow,0)
out=Path('/mnt/data/The_Ocean_Has_Floors.pdf');doc.save(out,garbage=4,deflate=True)
