"""Fixed-page research-article layout for the LAUTARA report."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
FIG=ROOT/'figures'
W,H=A4
L=47
CW=W-2*L
INK='#132c35'
TXT='#2c4850'
TEAL='#13786f'
DARK='#102e35'
MUTED='#506a72'
RULE='#cfdddc'
PALE='#eaf3f0'
GOLD='#9b5426'
SAND='#f9efe1'
for short,file in [('Text','OpenSans-Regular.ttf'),('Bold','OpenSans-Bold.ttf'),('Italic','OpenSans-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(short,'/usr/share/fonts/truetype/open-sans/'+file))
pdfmetrics.registerFontFamily('Text',normal='Text',bold='Bold',italic='Italic',boldItalic='Bold')
pdfmetrics.registerFont(TTFont('Heading','/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))

class Article:
    def __init__(self,out,refs):
        self.c=canvas.Canvas(str(out),pagesize=A4,pageCompression=1)
        self.c.setTitle('Before the Plume Reaches the Reef')
        self.c.setSubject('LAUTARA 2026 | Multi-source coastal sediment decisions in Indonesia and Russia')
        self.refs=refs
        self.idx=0
    def col(self,h):return colors.HexColor(h)
    def para(self,t,x,y,w=CW,sz=10.5,lead=15.2,color=TXT,font='Text',draw=True):
        p=Paragraph(t,ParagraphStyle('entry',fontName=font,fontSize=sz,leading=lead,textColor=self.col(color)))
        _,hh=p.wrap(w,H)
        if draw:p.drawOn(self.c,x,H-y-hh)
        return hh
    def rect(self,x,y,w,h,fill,r=7):
        self.c.setFillColor(self.col(fill))
        self.c.roundRect(x,H-y-h,w,h,r,stroke=0,fill=1)
    def line(self,y,x=L,w=CW):
        self.c.setStrokeColor(self.col(RULE));self.c.setLineWidth(.6);self.c.line(x,H-y,x+w,H-y)
    def anchors(self,label):
        self.idx+=1
        self.c.bookmarkPage('p'+str(self.idx))
        self.c.addOutlineEntry(f'{self.idx:02}  {label}','p'+str(self.idx),0)
    def end(self,y):
        if y>H-53:raise ValueError(f'Page {self.idx} overflow at {y:.0f}')
        self.line(H-44)
        self.para('LAUTARA 2026     /     COASTAL SEDIMENT STUDY',L,H-35,sz=7.1,lead=9,color=MUTED,font='Bold')
        self.c.setFillColor(self.col(TEAL));self.c.setFont('Bold',9)
        self.c.drawRightString(W-L,26,f'{self.idx:02} / 25')
        self.c.showPage()
    def start(self,section,title,dek):
        self.anchors(title)
        self.para('BEFORE THE PLUME REACHES THE REEF',L,31,sz=7.6,lead=9,color=TEAL,font='Bold')
        self.para(section.upper(),L,63,sz=9,lead=11,color=TEAL,font='Bold')
        y=85+self.para(title,L,85,sz=29,lead=35,color=INK,font='Heading')
        y+=10
        y+=self.para(dek,L,y,sz=11.6,lead=16.4,color=MUTED)+14
        self.line(y)
        return y+19
    def refs_html(self,ids):
        return ' '.join(f'<link href="{self.refs[i][1]}" color="{TEAL}">[{i}]</link>' for i in ids)
    def body(self,t,y):
        return y+self.para(t,L,y)+11
    def heading(self,t,y):
        return y+self.para(t,L,y,sz=11.4,lead=15.2,color=INK,font='Bold')+7
    def caption(self,t,y):
        return y+self.para(t,L,y,sz=8.65,lead=12,color=MUTED)+12
    def call(self,label,t,y,kind='teal'):
        bg,fg=(PALE,TEAL) if kind=='teal' else (SAND,GOLD)
        h1=self.para(label,L+14,y+10,CW-28,sz=10.4,lead=14,font='Bold',draw=False)
        h2=self.para(t,L+14,y+16+h1,CW-28,sz=10,lead=14.25,draw=False)
        h=27+h1+h2
        self.rect(L,y,CW,h,bg)
        self.para(label,L+14,y+10,CW-28,sz=10.4,lead=14,font='Bold',color=fg)
        self.para(t,L+14,y+16+h1,CW-28,sz=10,lead=14.25)
        return y+h+12
    def table(self,headers,rows,y,widths=None,sz=9.5):
        widths=widths or [CW/len(headers)]*len(headers)
        for i,row in enumerate([headers]+rows):
            font='Bold' if not i else 'Text'
            lead=sz*1.4
            h=max(self.para(t,0,y,w-16,sz,lead,font=font,draw=False) for t,w in zip(row,widths))+15
            self.rect(L,y,CW,h,PALE if not i else '#f4f8f7' if i%2 else '#ffffff',4)
            x=L
            for t,w in zip(row,widths):
                self.para(t,x+8,y+7,w-16,sz,lead,font=font);x+=w
            y+=h
        return y+14
    def fig(self,file,y,limit=252):
        path=Path(file)
        if not path.is_absolute():path=FIG/path
        with Image.open(path) as im:
            iw,ih=im.size
        s=min(CW/iw,limit/ih)
        w,h=iw*s,ih*s
        self.c.drawImage(str(path),L+(CW-w)/2,H-y-h,w,h,mask='auto')
        return y+h+9
    def metric(self,items,y):
        gap=10;w=(CW-gap*(len(items)-1))/len(items)
        for i,(value,label) in enumerate(items):
            x=L+i*(w+gap)
            self.rect(x,y,w,81,PALE)
            self.para(value,x+11,y+9,w-22,sz=22,lead=26,color=TEAL,font='Bold')
            self.para(label,x+11,y+40,w-22,sz=8.7,lead=11.4)
        return y+93
    def refs_columns(self,ids,y,sz=8.4):
        gap=24;w=(CW-gap)/2
        yy=[y,y]
        for j,i in enumerate(ids):
            c=int(j>=((len(ids)+1)//2))
            t,url=self.refs[i]
            t=f'<link href="{url}" color="{TEAL}">[{i}] {t}</link>'
            yy[c]+=self.para(t,L+c*(w+gap),yy[c],w,sz=sz,lead=11.6)+3.5
        return max(yy)
