import json,re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from ingest import ROOT,events,latest,save
def main():
    # NPY array loading never allows pickle/object payloads; binary validation required.
    records=[]; seen=set()
    for e in events():
        if e['source_id']=='GT-08' and e['label'].endswith('.npy') and e['status']==200 and e['label'] not in seen:
            seen.add(e['label']); a=np.load(ROOT/e['path'],allow_pickle=False)
            assert a.ndim==1 and set(np.unique(a)).issubset({0,1})
            records.append({'file':e['label'],'sha256':e['sha256'],'frames':len(a),'abnormal_frames':int(a.sum()),'abnormal_fraction':float(a.mean()),'event_runs':int(np.sum(np.diff(np.r_[0,a.astype(int)])==1))})
    if records: save(pd.DataFrame(records),'GT-08_binary_masks_summary.csv')
    # Published TomTom aggregates parsed from text, not raw probe trajectories.
    e=latest('GT-06','landing'); text=BeautifulSoup((ROOT/e['path']).read_bytes(),'html.parser').get_text(' ',strip=True)
    rows=[]
    for city in ['Ha Noi','Ho Chi Minh']:
        m=re.search(re.escape(city)+r' (\d+\.\d+)%.*?\+ (\d+\.\d+) pp (\d+) hours',text)
        if m: rows.append({'city':city,'congestion_percent':float(m[1]),'change_pp':float(m[2]),'rush_hours_lost':int(m[3]),'period':'2025','grain':'publisher city aggregate; probe denominator unavailable'})
    if rows: save(pd.DataFrame(rows),'GT-06_published_city_summary.csv')
    # Preserve monthly report text as extraction evidence; parse only explicit summary sentences.
    reports=[]; monthly=[]
    for e in events():
        if e['source_id']=='GT-02' and e['label'].startswith('monthly_') and e['status']==200:
            soup=BeautifulSoup((ROOT/e['path']).read_bytes(),'html.parser')
            text=soup.get_text(' ',strip=True)
            title=soup.find('h1'); title=title.get_text(' ',strip=True) if title else ''
            chunks=[text[max(0,m.start()-100):m.start()+1100] for m in re.finditer('Từ ngày|xảy ra|Xảy ra',text)]
            (ROOT/'data/interim'/('GT-02_'+e['label']+'.txt')).write_text(title+'\n'+'\n\n'.join(chunks),encoding='utf-8')
            reports.append({'title':title,'url':e['url'],'raw_file':e['path'],'extract_file':'data/interim/GT-02_'+e['label']+'.txt'})
            m=re.search(r'Toàn quốc xảy ra ([\d.]+) vụ, làm chết ([\d.]+) người, bị thương ([\d.]+) người',text)
            month=re.search(r'tháng (\d+)/2026',title)
            if m and month: monthly.append({'year':2026,'month':int(month[1]),'crashes':int(m[1].replace('.','')),'deaths':int(m[2].replace('.','')),'injuries':int(m[3].replace('.','')),'url':e['url'],'status':'sơ bộ','scope':'toàn quốc; không ghép năm với GT-01'})
    save(pd.DataFrame(reports),'GT-02_report_index.csv')
    if monthly: save(pd.DataFrame(monthly).sort_values('month'),'GT-02_monthly_counts.csv')
if __name__=='__main__': main()
