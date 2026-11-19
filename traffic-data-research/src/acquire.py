"""Bounded HTTP acquisition; immutable raw bytes and complete request events."""
import csv, datetime as dt, hashlib, json, time
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
ROOT=Path(__file__).resolve().parents[1]
def limits():
    import yaml
    p=ROOT/'config.yaml'
    return yaml.safe_load(p.read_text(encoding='utf-8')) if p.exists() else {'max_source_bytes':500_000_000,'max_total_bytes':2_000_000_000}
SESSION=requests.Session()
SESSION.headers['User-Agent']='VietnamTrafficResearch/1.0 (bounded academic source audit)'
SESSION.mount('https://',HTTPAdapter(max_retries=Retry(total=1,backoff_factor=0.5,status_forcelist=[429,502,503,504],respect_retry_after_header=True)))
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def fetch(sid,url,label='landing',cap=8_000_000,data=None):
    folder=ROOT/'data/raw'/sid; folder.mkdir(parents=True,exist_ok=True)
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    event={'source_id':sid,'url':url,'download_utc':now(),'label':label,'status':None,'error':'','path':''}
    try:
        old=[json.loads(x) for x in (ROOT/'registry/http_events.jsonl').read_text(encoding='utf-8').splitlines()] if (ROOT/'registry/http_events.jsonl').exists() else []
        cfg=limits()
        remaining_source=cfg['max_source_bytes']-sum(e.get('byte_size',0) for e in old if e['source_id']==sid)
        remaining_total=cfg['max_total_bytes']-sum(e.get('byte_size',0) for e in old)
        cap=min(cap,remaining_source,remaining_total)
        if cap<=0: raise ValueError('CUMULATIVE_DOWNLOAD_CAP_EXCEEDED')
        event['method']='POST' if data else 'GET'
        if data: event['request_form']=data
        with SESSION.request(event['method'],url,data=data,timeout=(10,35),stream=True) as r:
            event.update(status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type',''),headers=dict(r.headers))
            chunks=[]; size=0
            for c in r.iter_content(65536):
                size+=len(c)
                if size>cap: raise ValueError('DOWNLOAD_CAP_EXCEEDED')
                chunks.append(c)
            blob=b''.join(chunks)
            suffix='.json' if 'json' in event['content_type'] else '.html' if 'html' in event['content_type'] else '.bin'
            path=folder/(stamp+'_'+label+suffix); path.write_bytes(blob)
            event.update(path=str(path.relative_to(ROOT)),byte_size=len(blob),sha256=hashlib.sha256(blob).hexdigest(),period='NOT_VERIFIED',region='NOT_VERIFIED',data_version='NOT_VERIFIED',license='NOT_VERIFIED',transformation_script='src/acquire.py')
    except Exception as e: event['error']=str(e)
    with (ROOT/'registry/http_events.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(event,ensure_ascii=False)+'\n')
    print(sid,label,event['status'],event.get('byte_size'),event['error'][:140],flush=True)
    return event
def main():
    records=json.loads((ROOT/'registry/inventory.json').read_text(encoding='utf-8'))
    for d in records: fetch(d['Mã nguồn'],d['Link nguồn gốc'])
    fetch('COMPETITION','https://sangkienatgt.dantri.com.vn/')
if __name__=='__main__': main()
