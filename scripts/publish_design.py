"""Promote generated preview documents without altering their review URLs."""
from pathlib import Path
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent
ORIGIN='https://www.goodgodcharityfoundation.org'
def route(name):
    return '/' if name=='index.html' else '/'+Path(name).stem
for source in (ROOT/'preview').glob('*.html'):
    doc=BeautifulSoup(source.read_text(),'html.parser')
    for el in doc.select('[href],[src],[srcset]'):
        for attr in ['href','src']:
            value=el.get(attr,'')
            if value.startswith('../'):el[attr]=value[3:]
            elif value.startswith('assets/'):el[attr]='preview/'+value
        if el.has_attr('srcset'):el['srcset']=el['srcset'].replace('assets/','preview/assets/')
    for link in doc.select('a[href]'):
        value=link['href'];path,separator,fragment=value.partition('#')
        if path.endswith('.html') and not path.startswith(('http:', 'https:')):
            link['href']=route(path)+(separator+fragment if separator else '')
    doc.find('meta',attrs={'name':'robots'})['content']='noindex,follow' if source.name=='404.html' else 'index,follow'
    for meta in doc.select('meta[property="og:image"],meta[property="og:image:secure_url"],meta[name="twitter:image"]'):
        meta['content']=ORIGIN+'/preview/assets/og-ggcf.jpg'
    doc.find('meta',attrs={'property':'og:url'})['content']=ORIGIN+route(source.name)
    doc.head.append(doc.new_tag('link',attrs={'rel':'canonical','href':ORIGIN+route(source.name)}))
    (ROOT/source.name).write_text(str(doc))
namespace='http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('',namespace)
urls=ET.Element('{'+namespace+'}urlset')
for page in sorted((ROOT/'preview').glob('*.html')):
    if page.name=='404.html':continue
    entry=ET.SubElement(urls,'{'+namespace+'}url');ET.SubElement(entry,'{'+namespace+'}loc').text=ORIGIN+route(page.name)
ET.indent(urls);ET.ElementTree(urls).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
print('Promoted 11 pages with production paths, canonical URLs and sharing metadata.')
