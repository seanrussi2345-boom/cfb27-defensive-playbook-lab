#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, time
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs, unquote
import requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'audit-input.json'
OUT=ROOT/'audit-output'
HEADERS={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}

def slugify(s:str)->str:
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',s.lower())).strip('-')

def abs_url(base,u):
    if not u:return None
    if u.startswith('data:'):return None
    return urljoin(base,u)

def unwrap_next_image(u):
    try:
        q=parse_qs(urlparse(u).query)
        if 'url' in q:return unquote(q['url'][0])
    except Exception:pass
    return u

def image_candidates(soup,base,play):
    out=[]
    for meta in soup.select('meta[property="og:image"],meta[name="twitter:image"],meta[itemprop="image"]'):
        u=meta.get('content')
        if u:out.append(('meta',abs_url(base,u),meta.get('property') or meta.get('name') or 'meta'))
    for img in soup.find_all('img'):
        alt=(img.get('alt') or '').strip()
        attrs=[]
        for k in ('src','data-src','data-lazy-src'):
            if img.get(k):attrs.append(img.get(k))
        for k in ('srcset','data-srcset'):
            if img.get(k):
                attrs.extend(part.strip().split()[0] for part in img.get(k).split(',') if part.strip())
        for raw in attrs:
            out.append(('img',abs_url(base,raw),alt))
    cleaned=[]; seen=set()
    for kind,u,label in out:
        if not u:continue
        u=unwrap_next_image(u)
        u=abs_url(base,u)
        if u in seen:continue
        seen.add(u)
        score=0
        text=(u+' '+label).lower()
        if 'play art' in text:score+=100
        if slugify(play) in slugify(text):score+=30
        if any(x in text for x in ('logo','avatar','icon','favicon')):score-=100
        cleaned.append({'kind':kind,'url':u,'label':label,'score':score})
    return sorted(cleaned,key=lambda x:x['score'],reverse=True)

def extract_routes(soup):
    route_re=re.compile(r'^(Zone|Man|Blitz|Rush|Spy|Contain|Hook|Flat|Deep|Curl|Quarter|Seam)',re.I)
    items=[]
    heading=None
    for tag in soup.find_all(['h2','h3','h4','div','p']):
        if tag.get_text(' ',strip=True).lower()=='routes on this play':
            heading=tag;break
    if heading:
        parent=heading.parent
        for tag in parent.find_all(['a','button','li','span','div']):
            txt=' '.join(tag.get_text(' ',strip=True).split())
            txt=re.sub(r'\s*In \d+ other plays.*$','',txt,flags=re.I).strip()
            if route_re.match(txt) and len(txt)<90 and txt not in items:items.append(txt)
    if not items:
        for tag in soup.find_all(['a','button','li']):
            txt=' '.join(tag.get_text(' ',strip=True).split())
            txt=re.sub(r'\s*In \d+ other plays.*$','',txt,flags=re.I).strip()
            if route_re.match(txt) and len(txt)<90 and txt not in items:items.append(txt)
    return items

def script_signals(soup):
    signals=[]
    needles=('route','assignment','playart','play_art','zone deep','zone hook')
    for i,sc in enumerate(soup.find_all('script')):
        txt=sc.string or sc.get_text() or ''
        low=txt.lower()
        hits=[n for n in needles if n in low]
        if hits:
            signals.append({'index':i,'type':sc.get('type'),'id':sc.get('id'),'length':len(txt),'hits':hits,'sample':txt[:500]})
    return signals

def download(session,cands,dest):
    errors=[]
    for c in cands[:12]:
        try:
            r=session.get(c['url'],headers=HEADERS,timeout=30)
            ct=(r.headers.get('content-type') or '').lower()
            if r.status_code==200 and ct.startswith('image/') and len(r.content)>1500:
                ext='.png' if 'png' in ct else '.webp' if 'webp' in ct else '.jpg'
                path=dest.with_suffix(ext);path.write_bytes(r.content)
                return str(path.relative_to(ROOT)),c['url'],ct,len(r.content),errors
            errors.append({'url':c['url'],'status':r.status_code,'content_type':ct,'bytes':len(r.content)})
        except Exception as e:errors.append({'url':c['url'],'error':repr(e)})
    return None,None,None,0,errors

def main():
    cfg=json.loads(INPUT.read_text())
    formation=cfg['formation']; fslug=cfg['formation_slug']
    outdir=OUT/fslug; outdir.mkdir(parents=True,exist_ok=True)
    session=requests.Session()
    report={'formation':formation,'formation_slug':fslug,'generated_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'plays':[]}
    for idx,play in enumerate(cfg['plays'],1):
        pslug=slugify(play);url=f'https://collegefootball.gg/plays/{fslug}/{pslug}/'
        item={'play':play,'slug':pslug,'url':url}
        try:
            r=session.get(url,headers=HEADERS,timeout=30)
            item.update(status=r.status_code,final_url=r.url,html_bytes=len(r.content))
            if r.status_code==200:
                soup=BeautifulSoup(r.text,'html.parser')
                item['title']=soup.title.get_text(' ',strip=True) if soup.title else None
                item['routes']=extract_routes(soup)
                item['image_candidates']=image_candidates(soup,r.url,play)[:12]
                item['script_signals']=script_signals(soup)
                item['html_sha256']=hashlib.sha256(r.content).hexdigest()
                img_path,img_url,ct,n,errors=download(session,item['image_candidates'],outdir/pslug)
                item.update(image_path=img_path,image_url=img_url,image_content_type=ct,image_bytes=n,image_errors=errors)
                (outdir/f'{pslug}.html').write_text(r.text,encoding='utf-8')
        except Exception as e:item['error']=repr(e)
        report['plays'].append(item)
        print(f'[{idx}/{len(cfg["plays"])}] {play}: {item.get("status")} routes={len(item.get("routes",[]))} image={item.get("image_path")}')
        time.sleep(.2)
    (OUT/f'{fslug}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    summary=['# Play-art audit: '+formation,'']
    for p in report['plays']:
        summary.append(f'- **{p["play"]}** — HTTP {p.get("status")} — routes {len(p.get("routes",[]))} — image `{p.get("image_path") or "missing"}`')
    (OUT/f'{fslug}.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
if __name__=='__main__':main()
