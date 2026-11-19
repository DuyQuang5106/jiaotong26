import json,time
from urllib.parse import urljoin,urlencode
from bs4 import BeautifulSoup
from acquire import ROOT,fetch
def main():
    es=[json.loads(x) for x in (ROOT/'registry/http_events.jsonl').read_text(encoding='utf-8').splitlines()]
    e=next(e for e in es if e['source_id']=='GT-01' and e['label']=='landing')
    s=BeautifulSoup((ROOT/e['path']).read_bytes(),'html.parser')
    data={x['name']:x.get('value','') for x in s.select('input[type=hidden][name]')}
    for sel in s.find_all('select'):
        opts=sel.find_all('option')
        data[sel['name']]=[o['value'] for o in opts] if 'ValuesListBox' in sel['name'] else 'tableViewLayout1'
    button=next(x for x in s.find_all('input') if x.get('value')=='Tiếp tục')
    data[button['name']]=button['value']
    fetch('GT-01',e['url'],'selected_table',data=data)
    for sid in ['GT-10','GT-11']:
        e=next(e for e in es if e['source_id']==sid and e['label']=='landing')
        soup=BeautifulSoup((ROOT/e['path']).read_bytes(),'html.parser')
        links=[a['href'] for a in soup.find_all('a',href=True) if 'page=' in a['href']]
        for i,url in enumerate(dict.fromkeys(links)):
            fetch(sid,urljoin(e['url'],url),f'pagination_{i}')
    queries=['Vietnam school road safety helmet intervention','Vietnam traffic congestion adaptive signal evaluation','motorcycle bulky cargo safety Vietnam']
    for i,q in enumerate(queries):
        fetch('LITERATURE','https://api.crossref.org/works?'+urlencode({'query':q,'rows':10}),'crossref_'+str(i)); time.sleep(1)
    for doi in ['10.1136/injuryprev-2017-042517','10.3389/fpubh.2026.1721586','10.1109/JSTARS.2023.3285905','10.18280/mmep.130509']:
        fetch('LITERATURE','https://api.crossref.org/works/'+doi,'doi_'+doi.split('/')[-1])
    urls=['https://pmc.ncbi.nlm.nih.gov/articles/PMC12973589/','https://injuryprevention.bmj.com/content/25/3/206','https://www.iieta.org/journals/mmep/paper/10.18280/mmep.130509','https://sangkienatgt.dantri.com.vn/doi-giai-nhat-sang-kien-an-toan-giao-thong-2025-nhan-them-giai-a-khoa-hoc-quan-su']
    for i,url in enumerate(urls): fetch('LITERATURE',url,'fulltext_'+str(i))
if __name__=='__main__': main()
