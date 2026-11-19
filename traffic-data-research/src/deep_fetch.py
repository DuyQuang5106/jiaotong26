import json,time
from urllib.parse import quote
from acquire import ROOT,fetch
def main():
    import sys
    if '--resources' in sys.argv:
        from bs4 import BeautifulSoup
        from urllib.parse import urljoin
        es=[json.loads(x) for x in (ROOT/'registry/http_events.jsonl').read_text(encoding='utf-8').splitlines()]
        for sid in ['GT-07','GT-09','GT-17']:
            e=next(e for e in es if e['source_id']==sid and e['label']=='api_metadata' and e['status']==200)
            meta=json.loads((ROOT/e['path']).read_text(encoding='utf-8'))
            if sid=='GT-07':
                fetch(sid,meta['result']['resources'][0]['url'],'archive3.zip',20_000_000)
                fetch(sid,'https://www.kaggle.com/api/v1/datasets/list?search=traffic-flow-data-in-ho-chi-minh-city-viet-nam','original_metadata')
            else:
                for file in meta['files']: fetch(sid,file['links']['self'],file['key'],100_000_000)
        for sid in ['GT-10','GT-11']:
            e=next(e for e in es if e['source_id']==sid and e['label']=='landing')
            soup=BeautifulSoup((ROOT/e['path']).read_bytes(),'html.parser')
            (ROOT/'data/interim'/f'{sid}_page_structure.txt').write_text('\n'.join(str(x) for x in soup.find_all(['form','select','button','script']) if any(k in str(x) for k in ['limit','page','download','export','per_page','length','ajax'])),encoding='utf-8')
            fetch(sid,e['url']+'?limit=100&page=1','page100')
        e=next(e for e in es if e['source_id']=='GT-12' and e['label']=='landing')
        soup=BeautifulSoup((ROOT/e['path']).read_bytes(),'html.parser')
        for a in soup.find_all('a',href=True):
            if a['href'].endswith('.zip'): fetch('GT-12',a['href'],a['href'].split('/')[-1],40_000_000)
        fetch('GT-08','https://drive.google.com/drive/folders/1ygWcuOZ7kEwS-rC35gWv6f6qeNx0BHyg','download_folder')
        fetch('GT-04','https://download.geofabrik.de/asia/vietnam.html','retry_landing')
        fetch('GT-01','https://pxweb.nso.gov.vn/api/v1/vi/','api_root')
        fetch('GT-01','https://pxweb.nso.gov.vn/Download.aspx?file=V14.88.px','px_attempt')
        return
    jobs=[('GT-01','https://pxweb.nso.gov.vn/api/v1/vi/Y tế, văn hóa và MSDC/Y tế, văn hóa và MSDC/V14.88.px','api_metadata'),('GT-07','https://ckan.transport-data.org/api/3/action/package_show?id=traffic-flow-data-in-ho-chi-minh-city-viet-nam-hochiminhcity','api_metadata'),('GT-09','https://zenodo.org/api/records/18195750','api_metadata'),('GT-17','https://zenodo.org/api/records/17273112','api_metadata'),('GT-20','https://huggingface.co/api/datasets/star092304/Traffic-sign-detection-VietNam/tree/main','api_metadata'),('COMPETITION','https://sangkienatgt.dantri.com.vn/the-le','rules'),('COMPETITION','https://sangkienatgt.dantri.com.vn/san-pham-du-thi','entries'),('SKILLS','https://arxiv.org/abs/2609.00065','citation_check')]
    for sid,url,label in jobs: fetch(sid,url,label)
if __name__=='__main__': main()
