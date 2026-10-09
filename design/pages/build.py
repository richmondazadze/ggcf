from bs4 import BeautifulSoup
from pathlib import Path
from html import escape as E
ROOT=Path(__file__).resolve().parents[2]
S={n:BeautifulSoup((ROOT/(n+'.html')).read_text(),'html.parser') for n in ['index','about','donate','contact','404']}
TEAL='#001D23'; GREEN='#00704A'; ORANGE='#FF6F0F'; WARM='#F8F5EF'; MINT='#E6F2EC'; PEACH='#FFF0E6'
def tx(el):return el.get_text(' ',strip=True) if el else ''
def div(content,style='',name='Frame'):return f'<div layer-name="{E(name)}" style="display:flex;box-sizing:border-box;flex-shrink:0;{style}">{content}</div>'
def text(v,size=18,color=TEAL,weight=400,extra=''):
 return div(E(v),f'min-width:0;flex-shrink:1;font-family:Switzer;font-weight:{weight};font-size:{size}px;line-height:{1.1 if size>=32 else 1.55};color:{color};letter-spacing:{"-0.04em" if size>=32 else "0"};{extra}',v[:55])
def image(src,w,h,rad=20,pos='center'):
 url=src if src.startswith('https') else 'https://www.goodgodcharityfoundation.org/'+src.lstrip('/')
 return f'<img layer-name="GGCF photograph" src="{E(url)}" style="width:{w}px;height:{h}px;object-fit:cover;object-position:{pos};border-radius:{rad}px;flex-shrink:0;"/>'
class Page:
 def __init__(self,n,m=False):self.n=n;self.m=m;self.w=390 if m else 1440;self.pad=24 if m else 80;self.inner=self.w-2*self.pad;self.gap=24 if m else 40
 def col(self,c,w=None,gap=24,style=''):return div(c,f'flex-direction:column;gap:{gap}px;'+(f'width:{w}px;' if w else '')+style)
 def row(self,cs,gap=None,style='',stack=True):return div(''.join(cs),f'flex-direction:{"column" if self.m and stack else "row"};gap:{gap or self.gap}px;{style}')
 def section(self,c,bg=WARM,name='Section',py=None):return div(self.col(c,gap=32 if self.m else 48),f'padding:{py or (64 if self.m else 104)}px {self.pad}px;background:{bg};flex-direction:column;width:{self.w}px;',name)
 def btn(self,label,kind='solid'):
  return div(text(label,16,TEAL if kind=='solid' else GREEN,500)+text('↗',21,TEAL if kind=='solid' else GREEN,500),f'padding:14px 22px;gap:24px;align-items:center;justify-content:space-between;border-radius:8px;background:{ORANGE if kind=="solid" else "transparent"};'+('border:1px solid #A9B6AE;' if kind!='solid' else ''),'Button / '+label)
 def actions(self,labels):return self.row([self.btn(x,'solid' if i==0 else 'outline') for i,x in enumerate(labels)],16,'align-items:flex-start;',stack=False)
 def label(self,x):return text(x,13,GREEN,500,'text-transform:uppercase;letter-spacing:0.1em;')
 def heading(self,label,title,para=''):
  return self.col(self.label(label)+text(title,40 if self.m else 56,weight=500)+(text(para,17 if self.m else 20,color='#50615F') if para else ''),gap=18,style=f'max-width:{self.inner if self.m else 800}px;')
 def brand(self,dark=False):
  return self.row([image('img/gglogo.png',44,44,0),self.col(div('GOOD GOD',f'font-family:Clash Display;font-weight:600;font-size:{22 if self.m else 28}px;line-height:1.05;letter-spacing:-0.035em;color:{ORANGE if dark else TEAL};','Clash Display wordmark')+text('CHARITY FOUNDATION',9 if self.m else 10,'#FFFFFF' if dark else GREEN,500,'letter-spacing:0.17em;'),gap=4)],10,'align-items:center;',stack=False)
 def nav(self):
  top='' if self.m else div(self.row([text('Ejisu-Kumasi, Ghana',12,color='#50615F'),text('goodgodcharityfoundation@gmail.com',12,color='#50615F'),text('Follow us:',12,color='#50615F'),text('in   ◎   ◉',15,GREEN)],24,'align-items:center;',False),'padding:12px 80px;width:1440px;background:#E6F2EC;','Contact bar')
  links=text('☰',24) if self.m else self.row([text(x,15,GREEN if self.n==n else TEAL,500) for x,n in [('Home','index'),('About','about'),('Contact','contact')]]+[self.btn('Donate Now')],32,'align-items:center;',False)
  return top+div(self.row([self.brand(),links],16,'align-items:center;justify-content:space-between;width:100%;',False),f'width:{self.w}px;padding:{20 if self.m else 24}px {self.pad}px;background:{WARM};border-bottom:1px solid #DDE2DA;','Navigation')
 def footer(self):
  cols=[self.col(self.brand(True)+text("Let's put smiles on the faces of those who need it most.",18,'#D1DFD9')+text('in   ◎   ◉',22,ORANGE),None if self.m else 400),self.col(text('Contact Info',20,'#FFFFFF',500)+''.join(text(x,13 if self.m else 16,'#D1DFD9') for x in ['Ejisu-Kumasi, Ghana','+233(0)595603637','goodgodcharityfoundation@gmail.com']),None if self.m else 440,gap=14),self.col(text('Quick Links',20,'#FFFFFF',500)+''.join(text(x,16,'#D1DFD9') for x in ['Home','About Us','Contact Us','Donate']),None if self.m else 220,gap=14)]
  return self.section(self.row(cols,48)+div('',f'height:1px;background:#34514F;width:{self.inner}px;')+self.row([text('© Good God Charity Foundation, All Right Reserved.',12,'#B8C9C2'),text('Built By Richmond Azadze',12,'#B8C9C2')],20,'justify-content:space-between;'),TEAL,'Footer',64)
 def hero(self,title,crumb):
  return self.section(self.label(crumb)+text(title,48 if self.m else 88,weight=500,extra=f'max-width:{self.inner if self.m else 950}px;')+self.row([text('Home',13,GREEN),text(' / ',13,GREEN),text(crumb,13,GREEN)],12,stack=False),MINT,'Page hero',56 if self.m else 88)
 def cards(self,els,columns=3,bg='#FFFFFF',links=True):
  cards=[];cw=self.inner if self.m else (self.inner-(columns-1)*24)/columns
  for i,el in enumerate(els):
   h=el.find(['h3','h4','h5']);c=self.label(f'{i+1:02d}')+text(tx(h),26 if self.m else 30,weight=500)+''.join(text(tx(p),17,color='#50615F') for p in el.find_all('p'))
   if links:
    for a in el.find_all(['a','button']):
     if tx(a):c+=self.btn(tx(a),'outline')
   cards.append(self.col(c,cw,22,f'padding:32px;background:{bg};border:1px solid #DDE2DA;border-radius:16px;'))
  return self.row(cards,24,'align-items:stretch;')
 def form(self,el):
  c='';labels=el.find_all('label')
  for lab in labels:
   field=el.find(id=lab.get('for'))
   if field and field.get('type')=='checkbox':
    c+=self.row([div('','width:20px;height:20px;border:1px solid #9AACAA;border-radius:4px;'),text(tx(lab),14)],12,stack=False);continue
   c+=self.col(text(tx(lab),14,weight=500)+div(text(tx(field.find('option')) if field and field.name=='select' else (field.get('placeholder','') if field else ''),16,'#7A8783'),f'padding:14px 16px;min-height:{144 if field and field.name=="textarea" else 52}px;background:#FFF;border:1px solid #C6D0C9;border-radius:8px;width:100%;'),gap=8)
  for b in el.find_all('button'):
   if tx(b):c+=self.btn(tx(b))
  return self.col(c,gap=24)
 def build(self):
  s=S[self.n];main=s.find('main');blocks=[e for e in main.find_all(recursive=False) if e.name!='script'] if main else []
  c=self.nav()
  if self.n=='index':
   slides=s.select('.carousel-item');a=slides[0]
   left=self.col(text(tx(a.find('h1')),52 if self.m else 88,weight=500)+text(tx(a.find('p')),18 if self.m else 22,GREEN)+self.actions(['Donate Now','Join Us'])+self.row([text('←',20,GREEN),text('01 / 02',13,GREEN),text('→',20,GREEN)],20,stack=False),self.inner if self.m else 612,gap=28)
   photo=image(a.img['src'],self.inner if self.m else 588,360 if self.m else 580,180 if self.m else 260)
   c+=self.section(self.row([left,self.col(photo)],80,'align-items:center;'),WARM,'Home hero',40 if self.m else 72)
   about=blocks[1]
   c+=self.section(self.row([self.col(image(about.img['src'],self.inner if self.m else 552,340 if self.m else 528,24)),self.col(self.heading('Who We Are',tx(about.h2))+text(tx(about.p),17 if self.m else 19,color='#50615F')+self.actions(['Learn More','Join Us']),self.inner if self.m else 648,gap=24)],80,'align-items:center;'),'#FFFFFF','Introduction')
   imp=blocks[2]; labels=['School children supported with educational resources','Mothers and newborns assisted with healthcare','Families provided with essential aid']
   c+=self.section(self.heading('',tx(imp.h2))+text('720+ lives impacted through our programs',20,GREEN,500)+self.row([self.col(text(num,60 if self.m else 88,GREEN,500)+text(lab,16,GREEN),self.inner if self.m else 384,gap=12) for num,lab in zip(['600+','70+','50+'],labels)],40),MINT,'Impact figures')
   st=blocks[3]
   c+=self.section(self.heading('Our Story','Real smiles. Real change.')+div(image(st.img['src'],self.inner,230 if self.m else 600,24)+div(text('▶',26,TEAL),'position:absolute;left:45%;top:43%;width:64px;height:64px;border-radius:32px;background:#FF6F0F;align-items:center;justify-content:center;'),f'position:relative;width:{self.inner}px;','Video thumbnail')+text('Our recent donation impacting 600 school children',15,GREEN),'#FFFFFF','Story film')
   core=blocks[4];corecards=[]
   for h in core.find_all('h3'):corecards.append(h.parent)
   c+=self.section(self.heading('What We Do',tx(core.h2))+self.cards(corecards),WARM,'Core services')
   impact=blocks[5]
   c+=self.section(self.heading('Our Impact','')+self.cards(impact.select('.service-item')), '#FFFFFF','Impact stories')
  elif self.n=='about':
   c+=self.hero(tx(blocks[0].h1),'Who We Are')
   a=blocks[1];c+=self.section(self.row([self.col(self.heading('About Us',tx(a.h2))+text(tx(a.p),19 if not self.m else 17,color='#50615F')+self.actions(['Donate Now','Join Us']),self.inner if self.m else 648),self.col(image(a.img['src'],self.inner if self.m else 552,340 if self.m else 520,24))],80,'align-items:center;'),'#FFFFFF','About the foundation')
   f=blocks[2];c+=self.section(self.row([self.col(image(f.img['src'],self.inner if self.m else 360,360 if self.m else 440,180)+text(tx(f.select_one('.founder-name')),26,'#FFFFFF',500)+text(tx(f.select_one('.founder-title')),15,'#A6C7BB')+text(tx(f.select_one('.founder-email')),13,'#A6C7BB'),self.inner if self.m else 360),self.col(text(tx(f.select_one('.founder-quote-text')),32 if self.m else 46,'#FFFFFF',500),self.inner if self.m else 744)],120,'align-items:center;'),TEAL,'Founder')
   a=blocks[3];teams=s.select('.team-card');cards=[];cw=self.inner if self.m else (self.inner-48)/3
   for t in teams:
    h=t.find(['h4','h5']);pic=image(t.img['src'],cw-48,280,12) if t.img else div(text('◉',44,GREEN),'height:100px;align-items:center;')
    cards.append(self.col(pic+text(tx(h),24,weight=500)+text(tx(t.select_one('.badge')),14,GREEN,500)+text(tx(t.blockquote),15,'#50615F'),cw,gap=16,style='padding:24px;background:#FFFFFF;border:1px solid #DDE2DA;border-radius:16px;'))
   c+=self.section(self.heading('Our Team',tx(a.h2),tx(a.p))+''.join(self.row(cards[i:i+3],24) for i in range(0,len(cards),3)),WARM,'Team')
   a=blocks[5];c+=self.section(self.heading('Our Mission',tx(a.h2),tx(a.p))+self.cards(a.select('.service-item'),links=False,bg=MINT),'#FFFFFF','Mission vision and community')
   a=blocks[6];stats=[]
   for h in a.find_all('h3'):
    par=h.parent;ct=par.select_one('[data-count]');num=f'{int(ct["data-count"])//1000000}M+' if ct else ''
    stats.append(self.col(text(num,50 if self.m else 64,'#FFFFFF',500)+text(tx(h),20,'#FFFFFF',500)+text(tx(par.p),15,'#C3D9D0'),self.inner if self.m else 296,gap=16))
   c+=self.section(self.heading('Global Impact',tx(a.h2)).replace(f'color:{TEAL}', 'color:#FFFFFF')+self.row(stats,32),TEAL,'Global need')
   a=blocks[7];story=''
   for i,el in enumerate(a.select('.causes-item')):
    detail=self.col(self.label(tx(el.find('small')))+text(tx(el.h3),32 if self.m else 42,weight=500)+''.join(text(tx(p),17 if self.m else 18,'#50615F') for p in el.find_all('p'))+self.actions([tx(el.find('a'))]),self.inner if self.m else 712,gap=24)
    pic=self.col(image(el.img['src'],self.inner if self.m else 488,300 if self.m else 600,20))
    story+=self.row([pic,detail] if i%2==0 or self.m else [detail,pic],80,'align-items:flex-start;')
   c+=self.section(self.heading('Our Impact',tx(a.h2))+self.col(story,gap=96),'#FFFFFF','Full impact stories')
  elif self.n=='donate':
   c+=self.hero(tx(blocks[0].h1),'Donate')
   a=blocks[1];form=a.find('form');impact=a.find_all('h3')[1].parent
   formcard=self.col(text('Choose Your Impact',32,weight=500)+self.form(form),self.inner if self.m else 544,24,'padding:32px;background:#FFFFFF;border:1px solid #DDE2DA;border-radius:20px;')
   info=self.col(self.heading('Make a Difference','Your Impact')+text(tx(impact.p),18)+' '.join(self.row([text('•',20,GREEN),text(tx(li),17,'#50615F')],16,stack=False) for li in impact.find_all('li'))+text(tx(impact.find_all('p')[-1]),24,GREEN,500),self.inner if self.m else 656,gap=24)
   c+=self.section(self.row([formcard,info],80,'align-items:flex-start;'),WARM,'Donation and impact')
   c+=self.section(text(tx(blocks[2]),30 if self.m else 48,GREEN,500),MINT,'Giving statement',64)
   a=blocks[3];c+=self.section(self.heading('Payment Options',tx(a.h2))+self.cards(a.select('.service-item'),2), '#FFFFFF','Payment options')
   p=[x for x in a.find_all('p') if 'International' in tx(x)]
   if p:c+=self.section(text(tx(p[0]),17,'#50615F')+self.row([image(x['src'],100,40,0) for x in a.find_all('img')],24,stack=False),WARM,'International transfers',40)
   a=blocks[4];c+=self.section(self.heading('Transparency',tx(a.h2))+self.cards(a.select('.service-item'),2,links=False,bg=MINT),'#FFFFFF','Donation allocation')
  elif self.n=='contact':
   c+=self.hero(tx(blocks[0].h1),'Contact')
   a=blocks[1];info=self.heading('Get Involved',tx(a.h2))
   for h in a.find_all('h3'):info+=div(self.col(text(tx(h),18,GREEN,500)+text(tx(h.parent.p),13 if self.m and tx(h)=='Email Us' else 20),gap=8),'padding:24px 0;border-top:1px solid #CCD8D0;width:100%;')
   form=self.col(text('Contact Form',32,weight=500)+self.form(a.find('form')),self.inner if self.m else 608,28,'padding:32px;background:#FFFFFF;border-radius:20px;border:1px solid #DDE2DA;')
   c+=self.section(self.row([self.col(info,self.inner if self.m else 592),form],80),WARM,'Contact information and form')
   a=blocks[2];c+=self.section(self.heading('Join Foundation',tx(a.h2))+self.cards(a.select('.service-item')),'#FFFFFF','Volunteer opportunities')
  else:
   a=s.select_one('.page-header');c+=self.hero(tx(a.h1),'404 Error')
   block=s.select_one('.container-xxl');c+=self.section(self.col(text('404',120 if self.m else 240,GREEN,500)+text('Page Not Found',40 if self.m else 64,weight=500)+text(tx(block.p),18,'#50615F',extra=f'max-width:{self.inner if self.m else 640}px;')+self.actions([tx(block.find('a'))]),gap=24), '#FFFFFF','Not found',80)
  c+=self.footer()
  name=f'{7+["index","about","donate","contact","404"].index(self.n):02d} {"Home" if self.n=="index" else self.n.title()} / {"Mobile 390" if self.m else "Desktop 1440"}'
  return div(c,f'flex-direction:column;width:{self.w}px;background:{WARM};',name)
for n in S:
 for m in [False,True]:
  html=Page(n,m).build();stem=n+('-mobile' if m else '-desktop')
  (ROOT/'design/pages'/f'{stem}.html').write_text(html)
  (ROOT/'design/pages'/f'{stem}-preview.html').write_text('<html><head><meta charset="utf-8"><link rel="stylesheet" href="../../css/fonts.css"></head><body style="margin:0;background:#ddd">'+html+'</body></html>')
# Alternate hero retains original second slide content, separate from the default page state.
for m in [False,True]:
 p=Page('index',m);a=S['index'].select('.carousel-item')[1]
 c=p.nav()+p.section(p.row([p.col(text(tx(a.h2),50 if m else 80,weight=500)+text(tx(a.p),18,GREEN)+p.actions(['Make a Difference'])+text('02 / 02',13,GREEN),p.inner if m else 612),p.col(image(a.img['src'],p.inner if m else 588,360 if m else 580,180 if m else 260))],80,'align-items:center;'),WARM,'Second hero state',56)
 (ROOT/'design/pages'/('hero-alternate-mobile.html' if m else 'hero-alternate-desktop.html')).write_text(div(c,f'flex-direction:column;width:{p.w}px;background:{WARM};',f'12 Home / Alternate hero / {"Mobile" if m else "Desktop"}'))
print('Generated 10 full pages and 2 carousel states')
