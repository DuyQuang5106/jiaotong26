import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from acquire import ROOT,fetch
def main():
    es=[json.loads(x) for x in (ROOT/'registry/http_events.jsonl').read_text(encoding='utf-8').splitlines()]
    e=next(e for e in es if e['source_id']=='GT-02' and e['label']=='landing')
    soup=BeautifulSoup((ROOT/e['path']).read_bytes(),'html.parser')
    links=[]
    for a in soup.find_all('a',href=True):
        if 'Tình hình tai nạn giao thông' in a.get_text() and a['href'] not in links: links.append(a['href'])
    for i,url in enumerate(links[:3]): fetch('GT-02',urljoin(e['url'],url),'monthly_'+str(i))
if __name__=='__main__': main()
