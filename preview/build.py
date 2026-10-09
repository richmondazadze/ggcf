"""Build isolated, semantic preview pages from the approved Paper import sources."""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from html import escape
from PIL import Image,ImageOps
import re,json,hashlib,os
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'preview'
ORIGINAL={n:BeautifulSoup((ROOT/(n+'.html')).read_text(),'html.parser') for n in ['index','about','donate','contact','404']}
PHOTO_CACHE={}
def photo(src):
 if 'static.wixstatic.com' in src:src='img/carousel-1.jpg'
 src=src.replace('https://www.goodgodcharityfoundation.org/','').lstrip('/')
 p=ROOT/src
 if not p.exists():raise FileNotFoundError(src)
 if src=='img/gglogo.png' or src in ['img/remitly.png','img/taptap.png','img/lemfi.png']:return '../'+src,None
 if src in PHOTO_CACHE:return PHOTO_CACHE[src]
 im=ImageOps.exif_transpose(Image.open(p)).convert('RGB');name=p.stem
 choices=[]
 for w in [480,768,1280,1920]:
  if w>im.width and choices:continue
  w=min(w,im.width);h=round(im.height*w/im.width)
  target=OUT/'assets'/f'{name}-{w}.webp'
  if not target.exists() or target.stat().st_mtime<p.stat().st_mtime:im.resize((w,h),Image.Resampling.LANCZOS).save(target,'WEBP',quality=86)
  choices.append((target.name,w))
 ret=('assets/'+choices[-1][0],', '.join('assets/'+f+' '+str(w)+'w' for f,w in choices));PHOTO_CACHE[src]=ret;return ret
SOCIALS=[('LinkedIn','https://www.linkedin.com/company/goodgodcharityfoundation/','<path d="M4 8h3v12H4zM5.5 3a1.7 1.7 0 1 0 0 3.4 1.7 1.7 0 0 0 0-3.4M10 8h3v1.7c1-1.5 2.1-2 3.7-2 3 0 4.3 1.8 4.3 5V20h-3v-6.7c0-1.8-.6-2.8-2.1-2.8-1.7 0-2.9 1.2-2.9 3.3V20h-3z" fill="currentColor"/>'),('Instagram','https://www.instagram.com/good_god_charity_foundation_/?igsh=MWZoeWRqODcza2MzYw%3D%3D','<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/>'),('WhatsApp','https://chat.whatsapp.com/IDm55XASRkn166G4i8QROL','<path d="M20.5 11.7a8.5 8.5 0 0 1-12.7 7.4L3 20.5l1.4-4.7a8.5 8.5 0 1 1 16.1-4.1Z" stroke-linejoin="round"/><path d="M8.1 6.9c-.3 0-.6.1-.8.4-.7.7-.8 1.7-.4 2.8.8 2.4 3.5 5 6 5.9 1.1.4 2.2.2 2.9-.5.3-.3.5-.8.4-1.2l-2.3-1.2c-.3-.1-.5-.1-.7.2l-.8 1c-1.6-.6-3-2-3.6-3.5l.9-.9c.2-.2.3-.4.2-.7l-1.1-2.2c-.1-.2-.3-.2-.7-.1Z" fill="currentColor" stroke="none"/>')]
def socials():return '<div class="socials">'+''.join(f'<a href="{escape(url)}" target="_blank" rel="noopener noreferrer" aria-label="{name}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">{path}</svg></a>' for name,url,path in SOCIALS)+'</div>'
def creator_socials():
 urls=['https://www.linkedin.com/in/richmond-azadze/','https://www.instagram.com/__richkay.himself/']
 return '<span class="creator-socials">'+''.join(f'<a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Richmond Azadze on {name}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">{path}</svg></a>' for (name,_,path),url in zip(SOCIALS[:2],urls))+'</span>'
def brand():return '<a class="brand" href="index.html" aria-label="Good God Charity Foundation home"><img src="../img/gglogo.png" width="44" height="44" alt="Good God Charity Foundation Logo"><span><span class="wordmark">GOOD GOD</span><span class="brand-sub">CHARITY FOUNDATION</span></span></a>'
def header(n):
 links=''.join(f'<a href="{p}.html"'+(' aria-current="page"' if p==n else '')+f'>{label}</a>' for p,label in [('index','Home'),('about','About'),('contact','Contact')])
 return f'''<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="topbar"><div class="shell"><span>Ejisu-Kumasi, Ghana</span><a href="mailto:goodgodcharityfoundation@gmail.com">goodgodcharityfoundation@gmail.com</a><span class="follow">Follow us:</span>{socials()}</div></div><div class="nav-shell shell">{brand()}<button class="menu-toggle" aria-controls="site-menu" aria-expanded="false" aria-label="Open menu"><span></span><span></span></button><nav id="site-menu" aria-label="Main navigation">{links}<a class="button button-primary" href="donate.html">Donate Now<span aria-hidden="true">↗</span></a><div class="menu-details"><span>Ejisu-Kumasi, Ghana</span><a href="mailto:goodgodcharityfoundation@gmail.com">goodgodcharityfoundation@gmail.com</a><span>Follow us:</span>{socials()}</div></nav></div></header>'''
def footer():return f'''<footer class="site-footer"><div class="shell"><div class="footer-grid"><div>{brand()}<p>Let's put smiles on the faces of those who need it most.</p>{socials()}</div><div><h2>Contact Info</h2><address>Ejisu-Kumasi, Ghana<br><a href="tel:+233595603637">+233(0)595603637</a><br><a href="mailto:goodgodcharityfoundation@gmail.com">goodgodcharityfoundation@gmail.com</a></address></div><div><h2>Quick Links</h2><a href="index.html">Home</a><a href="about.html">About Us</a><a href="contact.html">Contact Us</a><a href="donate.html">Donate</a></div></div><div class="footer-bottom"><span>© <a href="index.html">Good God Charity Foundation</a>, All Right Reserved.</span><span class="creator-credit"><span>Built By <a href="https://richmondazadze.com" target="_blank" rel="noopener noreferrer">Richmond Azadze</a></span>{creator_socials()}</span></div></div></footer><button class="back-top" aria-label="Back to top">↑</button>'''
def styles(e):return dict((x.split(':',1)[0].strip(),x.split(':',1)[1].strip()) for x in e.get('style','').split(';') if ':' in x)
def setstyle(e,d):e['style']=';'.join(f'{k}:{v}' for k,v in d.items())
def destination(label,n,el):
 if label=='Donate with PayPal':return 'https://www.paypal.me/THEOPHILUSMENSAH669'
 if label in ['Donate Now','Make a Difference','Support Our Mission','Support Healthcare']:return 'donate.html'
 if label=='Join Us':return 'contact.html#contact-form' if n=='contact' else 'contact.html'
 if label=='Learn More':
  sec=el.find_parent('section');return 'about.html#impact-stories-section-title' if sec and sec.get('data-section')=='impact-stories' else 'about.html'
 return 'index.html'
def convert(markup,n,alt=False):
 s=BeautifulSoup(markup,'html.parser');root=s.find();root['class']=['page-content'];root.attrs.pop('style',None)
 # Sections carry the same composition and surfaces as Paper, with fluid shells.
 for e in list(root.find_all(recursive=False)):
  name=e.get('layer-name','')
  if name in ['Contact bar','Navigation','Footer']:e.decompose();continue
  e.name='section';e['data-section']=re.sub('[^a-z0-9]+','-',name.lower()).strip('-');e['class']=['section'];d=styles(e)
  if alt and e['data-section']=='second-hero-state':e['data-section']='home-hero'
  for k in ['width','padding','display','flex-direction','flex-shrink']:d.pop(k,None)
  setstyle(e,d)
  inner=e.find(recursive=False);inner['class']=['section-inner','shell','flow']
 # Fluid flex columns retain the desktop ratios and stack at small breakpoints.
 for e in root.find_all('div'):
  d=styles(e);cl=[]
  if d.get('flex-direction')=='row':cl.append('row')
  if d.get('flex-direction')=='column':cl.append('flow')
  if 'width' in d and re.fullmatch(r'[\d.]+px',d['width']):
   w=float(d.pop('width').removesuffix('px'));cl.append('column' if w>=200 else 'small-fixed');d['--basis']=str(w)+'px'
   if w<200:d['width']=str(w)+'px'
   else:d['--grow']=str(w/400)
  if 'gap' in d:d['--gap']=d.pop('gap')
  if 'padding' in d:cl.append('panel')
  d.pop('flex-shrink',None);d.pop('display',None)
  if d.get('min-width')=='0':d.pop('min-width')
  if 'max-width' in d and re.fullmatch(r'[\d.]+px',d['max-width']):d['max-width']='min(100%, '+d['max-width']+')'
  e['class']=list(set(e.get('class',[])+cl));setstyle(e,d)
 for e in list(root.select('[layer-name]')):
  name=e['layer-name'];d=styles(e)
  if name.startswith('Button / '):
   label=name[len('Button / '):];e.name='a';e['href']=destination(label,n,e);e['class']='button '+('button-primary' if d.get('background','').lower()=='#ff6f0f' else 'button-outline');e.attrs.pop('style',None)
   if e['href'].startswith('https'):e['target']='_blank';e['rel']='noopener noreferrer'
   e.clear();e.append(label);arrow=s.new_tag('span');arrow['aria-hidden']='true';arrow.string='↗';e.append(arrow);continue
  if e.name=='img':
   src=e['src'];local,srcset=photo(src);e['src']=local
   if srcset:e['srcset']=srcset;e['sizes']='(max-width: 760px) calc(100vw - 48px), (max-width: 1100px) 45vw, 600px'
   original=next((x for x in ORIGINAL[n].find_all('img') if x.get('src','').lstrip('/')==src.replace('https://www.goodgodcharityfoundation.org/','').lstrip('/')),None)
   e['alt']=original.get('alt','') if original else ('Children receiving support from Good God Charity Foundation' if 'wix' in src else '')
   e['loading']='eager' if e.find_parent('section',attrs={'data-section':'home-hero'}) else 'lazy';e['decoding']='async';e['width']=round(float(d.get('width','600px').removesuffix('px')));e['height']=round(float(d.get('height','400px').removesuffix('px')))
   ratio=e['width']/e['height'];d.pop('width',None);d.pop('height',None);d['aspect-ratio']=str(ratio);d['width']='100%';e['class']='photograph'+(' brand-image' if 'gglogo' in src else '')
   if e.find_parent('section',attrs={'data-section':'home-hero'}):e['fetchpriority']='high';e['class']+=' hero-photo';e['data-parallax']=''
   setstyle(e,d);continue
  if 'font-family' in d:
   size=float(d.get('font-size','16px').removesuffix('px'));weight=d.get('font-weight','400');txt=e.get_text(' ',strip=True)
   if not txt:e.decompose();continue
   d.pop('font-family',None);d.pop('font-size',None);d.pop('flex-shrink',None);d.pop('min-width',None)
   d['--text-size']=f'{size}px';e['class']=e.get('class',[])+['text']
   if size>=64:
    e.name='h1' if not alt else 'h2';e['class']+=['display'];d['--mobile-size']='52px' if n=='index' else '48px'
   elif size>=32:e.name='h2';e['class']+=['heading'];d['--mobile-size']='36px' if size>=48 else '30px'
   elif size>=24:e.name='h3';e['class']+=['subheading'];d['--mobile-size']='26px'
   elif d.get('text-transform')=='uppercase':e.name='p';e['class']+=['eyebrow']
   else:e.name='p' if size>=14 else 'span'
   if txt in ['600+','70+','50+','258M+','400M+','140M+','345M+']:
    e.name='span';e['class']+=['stat'];e['data-count']=txt;e['aria-label']=txt
   if txt=='Page Not Found':e.name='h2'
   if txt=='◉':e.name='span';e['aria-hidden']='true'
   if txt=='404':e.name='p';e['class']+=['error-number'];d['--mobile-size']='120px'
   if txt=='goodgodcharityfoundation@gmail.com':e.name='a';e['href']='mailto:'+txt;e['class']+=['contact-link']
   if txt=='+233(0)595603637':e.name='a';e['href']='tel:+233595603637'
   if txt.startswith('theophilusynagogue@'):
    e.name='a';e['href']='mailto:'+txt
   setstyle(e,d)
 for e in root.select('[layer-name]'):e.attrs.pop('layer-name',None)
 for row in root.select('.row'):
  children=row.find_all(recursive=False)
  if children and children[0].get_text(strip=True)=='•':row['class']+=['bullet-row'];children[0]['aria-hidden']='true'
 # Cards respond subtly to a fine pointer; layout never depends on JavaScript.
 for e in root.select('.panel'):
  if e.find('h3') and not e.find('form'):e['data-tilt']='';e['class']+=['card']
 # Restore the semantic, working forms instead of the static Paper controls.
 if n in ['donate','contact']:
  title=root.find(['h2','h3'],string='Choose Your Impact' if n=='donate' else 'Contact Form');container=title.parent;fake=title.find_next_sibling();form=BeautifulSoup(str(ORIGINAL[n].find('form')),'html.parser').find('form')
  for el in form.find_all():
   el.attrs.pop('style',None);el.attrs.pop('class',None)
   if el.name=='i':el.decompose()
  for field in form.select('input:not([type="checkbox"]),textarea,select'):
   wrapper=field.parent;lab=wrapper.find('label');
   if lab:lab.extract();field.insert_before(lab)
   wrapper['class']='field'
  for inp in form.select('input[type="checkbox"]'):inp.parent['class']='check-field'
  for b in form.select('button'):
   b['class']='button button-primary';b['type']='submit'
  if n=='donate':
   form['data-donation']='';form['action']='https://www.paypal.me/THEOPHILUSMENSAH669';form['method']='GET';amount=form.find(id='amount');amount['type']='number';amount['min']='0.01';amount['step']='0.01';amount['inputmode']='decimal';form.find(id='monthly').parent.decompose()
  else:form['data-contact']=''
  form['class']='form-stack';form['id']='contact-form' if n=='contact' else 'donate-form';fake.replace_with(form)
 if n=='index':
  hero=root.select_one('[data-section="home-hero"]');hero['class']+=['hero-slide'];hero['data-slide']='0'
  # Visible manual carousel controls replace the diagram's decorative arrows.
  for t in hero.select('.text'):
   if t.get_text(strip=True) in ['←','01 / 02','→']:t.parent['data-carousel-placeholder']=''
  for e in hero.select('[data-carousel-placeholder]'):e.decompose()
  if not alt:
   second=convert((ROOT/'design/pages/hero-alternate-desktop.html').read_text(),n,True).select_one('section')
   second['class']+=['hero-slide'];second['data-slide']='1';second['hidden']='';hero.insert_after(second)
   controls=BeautifulSoup('<div class="carousel-controls shell" role="group" aria-label="Hero slides"><button data-prev aria-label="Previous slide">←</button><span data-slide-count>01 / 02</span><button data-next aria-label="Next slide">→</button><span class="sr-only" data-slide-status aria-live="polite"></span></div>','html.parser').find();second.insert_after(controls)
  video=root.select_one('[data-section="story-film"]');
  if video:
   frame=video.find('img').parent;frame['class']='video-poster';frame.attrs.pop('style',None);frame.find('img')['sizes']='(max-width: 1280px) 100vw, 1280px';old=frame.find('img').find_next_sibling();old.decompose()
   button=s.new_tag('button');button['class']='video-play';button['aria-label']='Play video';button['type']='button';button.string='▶';frame.append(button)
  if alt:
   for e in hero.select('.text'):
    if e.get_text(strip=True)=='02 / 02':e.decompose()
 # Meaningful breadcrumbs and anchor destinations retained from the original pages.
 for section in root.select('[data-section="page-hero"]'):
  line=section.find_all('div',recursive=False)[0].find_all('div',recursive=False)[-1]
  if line.get_text(' ',strip=True).startswith('Home /'):
   a=line.find(['p','span']);a.name='a';a['href']='index.html';line['class']=['breadcrumb'];line['aria-label']='Breadcrumb'
 if n=='about':root.select_one('[data-section="full-impact-stories"]')['id']='impact-stories-section-title'
 if n=='donate':
  section=root.select_one('[data-section="donation-allocation"]');
  for h in section.find_all('h3'):h['id']='child-healthcare' if h.get_text(strip=True)=='Child Healthcare' else 'educational-support'
 return root
STORY_PAGES=[]
def story_picture(name,alt,eager=False,full=False):
 paths=sorted((OUT/'assets/stories').glob(name+'-*.webp'),key=lambda p:int(p.stem.rsplit('-',1)[1]))
 if not paths:raise FileNotFoundError(name)
 largest=paths[-1];im=Image.open(largest);srcset=', '.join(f'assets/stories/{p.name} {int(p.stem.rsplit("-",1)[1])}w' for p in paths)
 sizes='(max-width: 760px) calc(100vw - 48px), 1080px' if eager or full else '(max-width: 760px) calc(100vw - 48px), (max-width: 1100px) calc((100vw - 104px) / 2), 410px'
 priority=' fetchpriority="high"' if eager else ''
 return f'<img class="story-photo" src="assets/stories/{largest.name}" srcset="{srcset}" sizes="{sizes}" width="{im.width}" height="{im.height}" alt="{escape(alt,quote=True)}" loading="{"eager" if eager else "lazy"}" decoding="async"{priority}>'
def water_story(item):
 title=escape(item['title']); cover=story_picture(item['image'],item['alt'],True)
 sections=[];films=[]
 for c in item['chapters']:
  paragraphs=''.join(f'<p>{escape(p)}</p>' for p in c['paragraphs'])
  figure=''
  if c.get('image') and c['image']!=item['image']:
   figure=f'<figure class="water-photo">{story_picture(c["image"],c["caption"],full=True)}<figcaption>{escape(c["caption"])}</figcaption></figure>'
  sections.append(f'<section class="water-chapter" aria-labelledby="{c["id"]}-title"><div class="flow" data-reveal><h2 id="{c["id"]}-title">{escape(c["title"])}</h2>{paragraphs}</div>{figure}</section>')
  films.append(f'<details class="water-film" name="water-project-films"><summary>{escape(c["videoLabel"])}<span aria-hidden="true">+</span></summary><div class="story-film" data-video-container><button class="story-film-play" data-story-video="{c["video"]}" aria-label="{escape(c["videoLabel"],quote=True)}"><span class="film-play-icon" aria-hidden="true">▶</span><span>Play film</span></button></div></details>')
 return f'<div class="page-content water-story"><header class="water-intro shell"><a class="story-back" href="about.html#impact-stories-section-title">← Our Impact</a><div class="water-heading"><div class="flow"><p class="eyebrow">{escape(item["date"])}</p><h1>{title}</h1></div><figure>{cover}<figcaption>{escape(item["chapters"][-1]["caption"])}</figcaption></figure></div></header><article class="water-reading"><p class="water-deck">{escape(item["intro"])}</p>'+''.join(sections)+'<section class="water-films" aria-labelledby="water-films-title"><h2 id="water-films-title">Watch the project journey</h2>'+''.join(films)+'</section><div class="story-actions"><a class="button button-primary" href="donate.html">Support Our Mission <span aria-hidden="true">↗</span></a><a class="story-back" href="about.html#impact-stories-section-title">← All stories</a></div></article></div>'

def additional_stories():
 cards=[]
 for item in json.loads((OUT/'content/impact-stories.json').read_text()):
  href='story-'+item['slug']+'.html';title=escape(item['title']);date=escape(item['date']);intro=escape(item['intro']);image=story_picture(item['image'],item['alt'])
  cards.append(f'<article class="card story-card" data-reveal><a class="story-image-link" href="{href}" aria-label="{title}">{image}</a><div class="story-card-copy"><p class="eyebrow">{date}</p><h3><a href="{href}">{title}</a></h3><a class="story-link" href="{href}">Read story <span aria-hidden="true">↗</span></a></div></article>')
  nav=''.join(f'<a href="#{c["id"]}">{escape(c["title"])}</a>' for c in item['chapters'])
  chapters=[]
  for c in item['chapters']:
   paragraphs=''.join(f'<p>{escape(p)}</p>' for p in c['paragraphs'])
   figure=''
   if c.get('image'):figure=f'<figure class="story-documentary-photo">{story_picture(c["image"],c["caption"],full=True)}<figcaption>{escape(c["caption"])}</figcaption></figure>'
   video=''
   if c.get('video'):
    video=f'<div class="story-film" data-video-container><button class="story-film-play" data-story-video="{c["video"]}" aria-label="{escape(c["videoLabel"],quote=True)}"><span class="film-play-icon" aria-hidden="true">▶</span><span>{escape(c["videoLabel"])}</span></button></div>'
   chapters.append(f'<section class="story-chapter" id="{c["id"]}" aria-labelledby="{c["id"]}-title"><div class="story-body flow" data-reveal><h2 id="{c["id"]}-title">{escape(c["title"])}</h2>{paragraphs}</div>{figure}<div class="story-body">{video}</div></section>')
  cover=story_picture(item['image'],item['alt'],True)
  status='<span class="story-status">Completed & handed over</span>' if item['year']==2026 else ''
  body=f'<div class="page-content"><section class="section story-header"><div class="shell flow"><a class="story-back" href="about.html#impact-stories-section-title">← Our Impact</a><p class="eyebrow">{date}</p><h1>{title}</h1><p class="story-deck">{intro}</p>{status}</div></section><div class="shell story-cover">{cover}</div><nav class="story-chapter-nav shell" aria-label="Story chapters">{nav}</nav>'+''.join(chapters)+'<section class="section"><div class="story-body story-actions"><a class="button button-primary" href="donate.html">Support Our Mission <span aria-hidden="true">↗</span></a><a class="story-back" href="about.html#impact-stories-section-title">← All stories</a></div></section></div>'
  if item['year']==2026:body=water_story(item)
  STORY_PAGES.append((href,item['title'],body))
 return cards

def impact_journal(root):
 section=root.select_one('[data-section="full-impact-stories"]')
 rows=[r for r in section.select('.row') if r.find('img') and r.find('h2')]
 slugs=['christmas-at-the-orphanage-2022','kumasi-childrens-home-2023','maternal-child-health-2023']
 cards=[]
 for row,slug in zip(rows,slugs):
  img=row.find('img');title=row.find('h2').get_text(' ',strip=True);date=row.select_one('.eyebrow').get_text(' ',strip=True)
  paragraphs=[p.get_text(' ',strip=True) for p in row.find_all('p') if 'eyebrow' not in p.get('class',[])]
  cta=str(row.select_one('.button'))
  img.attrs.pop('style',None);img.attrs.pop('data-parallax',None);img.attrs.pop('data-reveal',None)
  img['class']=['story-photo'];img['sizes']='(max-width: 760px) calc(100vw - 48px), (max-width: 1100px) calc((100vw - 104px) / 2), 410px'
  href='story-'+slug+'.html'
  cards.append(f'<article class="card story-card" data-reveal><a class="story-image-link" href="{href}" aria-label="{escape(title,quote=True)}">{img}</a><div class="story-card-copy"><p class="eyebrow">{escape(date)}</p><h3><a href="{href}">{escape(title)}</a></h3><a class="story-link" href="{href}">Read story <span aria-hidden="true">↗</span></a></div></article>')
  detail_img=BeautifulSoup(str(img),'html.parser').img;detail_img['sizes']='(max-width: 760px) calc(100vw - 48px), 1080px';detail_img['loading']='eager';detail_img['fetchpriority']='high'
  body=f'<div class="page-content"><section class="section story-header"><div class="shell flow"><a class="story-back" href="about.html#impact-stories-section-title">← Our Impact</a><p class="eyebrow">{escape(date)}</p><h1>{escape(title)}</h1></div></section><div class="shell story-cover">{detail_img}</div><section class="section"><article class="story-body flow">'+''.join(f'<p>{escape(p)}</p>' for p in paragraphs)+f'<div class="story-actions">{cta}<a class="story-back" href="about.html#impact-stories-section-title">← All stories</a></div></article></section></div>'
  STORY_PAGES.append((href,title,body))
 grid=BeautifulSoup('<div class="story-grid">'+''.join(additional_stories()+list(reversed(cards)))+'</div>','html.parser').find()
 rows[0].parent.replace_with(grid)

def refine(root,n):
 s=BeautifulSoup('', 'html.parser')
 if n=='index':
  slides=root.select('.hero-slide');controls=root.select_one('.carousel-controls');wrap=s.new_tag('div',attrs={'class':'hero-carousel','role':'region','aria-roledescription':'carousel','aria-label':'Foundation highlights'})
  slides[0].insert_before(wrap)
  for i,slide in enumerate(slides):
   content=slide.find(['h1','h2']).parent.extract();content['class']=['hero-copy','shell','flow'];content.attrs.pop('style',None)
   img=slide.find('img').extract();img['class']=['hero-background'];img.attrs.pop('style',None);img.attrs.pop('data-parallax',None);img['sizes']='100vw';img['loading']='eager';img['fetchpriority']='high' if i==0 else 'low';img['alt']='';img['aria-hidden']='true'
   slide.clear();slide.attrs.pop('hidden',None);slide['class']=['hero-slide']+(['is-active'] if i==0 else []);slide['aria-hidden']='false' if i==0 else 'true'
   if i:slide['inert']=''
   slide.append(img);overlay=s.new_tag('div',attrs={'class':'hero-overlay','aria-hidden':'true'});slide.append(overlay);slide.append(content);wrap.append(slide.extract())
  controls['class']=['carousel-controls','shell'];wrap.append(controls.extract())
 if n=='about':
  impact_journal(root)
  founder=root.select_one('[data-section="founder"]');profile=founder.find('img').parent;profile['class']+=['founder-profile'];profile['id']='founder-profile';img=profile.find('img');img['src']='assets/theo_mensah.webp';img['srcset']='assets/theo_mensah-480.webp 480w, assets/theo_mensah.webp 800w';img['sizes']='(max-width: 760px) calc(100vw - 50px), 432px';img['width']=800;img['height']=800;img.attrs.pop('style',None);img['class']=['founder-portrait','photograph'];img['data-parallax']=''
  identity=s.new_tag('div',attrs={'class':'founder-identity'});profile.append(identity)
  for el in list(profile.find_all(['h3','p','a'],recursive=False)):identity.append(el.extract())
  identity.find('h3')['class']+=['founder-name'];identity.find('p')['class']+=['founder-role'];identity.find('a')['class']+=['founder-email']
  social=BeautifulSoup(socials(),'html.parser').find('div');social.find_all('a')[0]['href']='https://www.linkedin.com/in/-theophilusmensah/';social.find_all('a')[0]['aria-label']='Theophilus Mensah on LinkedIn';social.find_all('a')[1]['href']='https://www.instagram.com/theophilus__mensah/';social.find_all('a')[1]['aria-label']='Theophilus Mensah on Instagram';social.find_all('a')[2].decompose();identity.append(social)
  quote=founder.find('h2');quote.name='blockquote';quote['class']+=['founder-quote']
  for dot in root.find_all('span',string='◉'):dot.parent.decompose()
 for img in root.select('[data-section=team] img'):
  img['sizes']='(max-width: 760px) calc(100vw - 96px), (max-width: 1100px) calc((100vw - 272px) / 3), (max-width: 1440px) calc((100vw - 352px) / 3), 363px'
 # Independent reveal targets create visible, staggered motion throughout long pages.
 for section in root.find_all('section'):
  if section.get('data-section')=='home-hero':continue
  for el in section.select('.heading,.display,.card,.photograph,.video-poster,.founder-identity,.founder-quote'):
   if not el.find_parent(class_='card') and not el.find_parent(class_='video-poster'):el['data-reveal']=''
  for img in section.select('.photograph'):
   if '/img/' not in img.get('src','') and not img.get('class')==['founder-portrait','photograph']:img['data-parallax']=''
 for img in list(root.select('[data-parallax]')):
  if img.find_parent(class_='card') or img.find_parent(class_='video-poster') or 'founder-portrait' in img.get('class',[]):
   img.attrs.pop('data-parallax',None);continue
  d=styles(img);window=s.new_tag('div',attrs={'class':'photo-window','data-reveal':''});setstyle(window,{'border-radius':d.get('border-radius','16px'),'aspect-ratio':d.get('aspect-ratio','1.3')});img.wrap(window);img.attrs.pop('data-reveal',None)
 for img in root.find_all('img'):
  for child in reversed(list(img.contents)):img.insert_after(child.extract())
 return root
def vector_arrows(html,filename):
 document=BeautifulSoup(html,'html.parser')
 origin=os.environ.get('GGCF_SHARE_ORIGIN','https://goodgodcharityfoundation-git-codex-n-45ec37-richmond-s-projects.vercel.app').rstrip('/')
 title=document.title.get_text();description=document.find('meta',attrs={'name':'description'})['content'];image=origin+'/preview/assets/og-ggcf.jpg'
 properties={'og:title':title,'og:description':description,'og:type':'article' if filename.startswith('story-') else 'website','og:url':origin+'/preview/'+filename,'og:site_name':'Good God Charity Foundation','og:image':image,'og:image:secure_url':image,'og:image:type':'image/jpeg','og:image:width':'1200','og:image:height':'630','og:image:alt':'Good God Charity Foundation — Giving hope to those who need it the most. Schoolchildren at New Amakom.'}
 names={'twitter:card':'summary_large_image','twitter:title':title,'twitter:description':description,'twitter:image':image,'twitter:image:alt':properties['og:image:alt']}
 for key,value in properties.items():document.head.append(document.new_tag('meta',attrs={'property':key,'content':value}))
 for key,value in names.items():document.head.append(document.new_tag('meta',attrs={'name':key,'content':value}))
 paths={'↗':'M5 19 19 5M5 5h14v14','↑':'M12 20V4M5 11l7-7 7 7','←':'M20 12H4M11 5l-7 7 7 7','→':'M4 12h16M13 5l7 7-7 7'}
 for node in list(document.find_all(string=True)):
  if node.parent.name in ['script','style']:continue
  if not any(char in str(node) for char in paths):continue
  for part in re.split('([↗↑←→])',str(node)):
   if not part:continue
   if part in paths:
    icon=BeautifulSoup(f'<svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="{paths[part]}"></path></svg>','html.parser').svg
    node.insert_before(icon)
   else:node.insert_before(NavigableString(part))
  node.extract()
 return str(document)

portrait=Image.open(OUT/'assets/theo_mensah.png').convert('RGB')
for width in [480,800]:
 target=OUT/'assets'/('theo_mensah.webp' if width==800 else 'theo_mensah-480.webp')
 if not target.exists() or target.stat().st_mtime<(OUT/'assets/theo_mensah.png').stat().st_mtime:portrait.resize((width,width),Image.Resampling.LANCZOS).save(target,'WEBP',quality=91)
for n in ORIGINAL:
 root=refine(convert((ROOT/'design/pages'/f'{n}-desktop.html').read_text(),n),n)
 root=BeautifulSoup(str(root),'html.parser').find()
 # All top-level sections have an accessible name from their visible title.
 for i,sec in enumerate(root.find_all('section')):
  h=sec.find(['h1','h2','h3']);
  if h:
   if not h.get('id'):h['id']=f'{n}-section-{i}'
   sec['aria-labelledby']=h['id']
 title=ORIGINAL[n].title.get_text();description=ORIGINAL[n].find('meta',attrs={'name':'description'})
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{escape(title)}</title><meta name="description" content="{escape(description.get('content','') if description else '')}"><link rel="icon" href="../img/favicon.png"><link rel="preload" href="../fonts/switzer-500.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="../fonts/clash-display-600.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="../css/fonts.css"><link rel="stylesheet" href="assets/site.css?v={hashlib.sha256((OUT/'assets/site.css').read_bytes()).hexdigest()[:10]}"><script defer src="assets/site.js?v={hashlib.sha256((OUT/'assets/site.js').read_bytes()).hexdigest()[:10]}"></script></head><body data-page="{n}">{header(n)}<main id="main" tabindex="-1">{root}</main>{footer()}</body></html>'''
 (OUT/(n+'.html')).write_text(vector_arrows(html,n+'.html'))
for filename,title,body in STORY_PAGES:
 document=BeautifulSoup((OUT/'about.html').read_text(),'html.parser')
 document.title.string=title+' | Good God Charity Foundation'
 document.find('meta',attrs={'name':'description'})['content']=title+' — Good God Charity Foundation impact story.'
 for meta in document.select('meta[property^="og:"],meta[name^="twitter:"]'):meta.decompose()
 document.main.clear();document.main.append(BeautifulSoup(body,'html.parser'))
 document.body['data-page']='story'
 (OUT/filename).write_text(vector_arrows(str(document),filename))
print(f'Built five preview pages and {len(STORY_PAGES)} individual impact stories.')
