"""Parse preserved HTTP responses into derived tables; no raw mutation."""
import csv,io,json,re,zipfile
from xml.etree import ElementTree as ET
import pandas as pd
from bs4 import BeautifulSoup
from acquire import ROOT
def events(): return [json.loads(x) for x in (ROOT/'registry/http_events.jsonl').read_text(encoding='utf-8').splitlines()]
def latest(sid,label):
    return next((e for e in reversed(events()) if e['source_id']==sid and e['label']==label and e['status']==200 and e['path']),None)
def save(df,name):
    df.to_csv(ROOT/'data/processed'/name,index=False,encoding='utf-8-sig')
    print(name,df.shape)
def safe_zip(path):
    z=zipfile.ZipFile(path)
    assert sum(i.file_size for i in z.infolist())<1_500_000_000
    assert all(not i.filename.startswith(('/','\\')) and '..' not in i.filename.replace('\\','/').split('/') and not (i.flag_bits&1) for i in z.infolist())
    return z
def main():
    e=latest('GT-07','archive3.zip')
    if e:
        with safe_zip(ROOT/e['path']) as z:
            for n in z.namelist():
                if n.endswith('.csv'): save(pd.read_csv(z.open(n)),f'GT-07_{Path(n).name}')
    e=latest('GT-01','selected_table')
    if e:
        soup=BeautifulSoup((ROOT/e['path']).read_bytes(),'html.parser'); rows=[]
        for tr in soup.select('table tr'):
            cells=[c.get_text(' ',strip=True) for c in tr.find_all(['td','th'],recursive=False)]
            if len(cells)==10 and cells[0] not in ['','Địa phương']:
                for j,year in enumerate([2022,2023,2024]):
                    for k,metric in enumerate(['crashes','deaths','injuries']):
                        v=cells[1+j*3+k]; rows.append({'region':cells[0],'year':year,'metric':metric,'value':None if v=='..' else int(v.replace('.',''))})
        save(pd.DataFrame(rows),'GT-01_aggregates.csv')
    for sid in ['GT-10','GT-11']:
        rows=[]
        for e in events():
            if e['source_id']!=sid or not e['path'] or e['status']!=200: continue
            soup=BeautifulSoup((ROOT/e['path']).read_bytes(),'html.parser')
            for tr in soup.select('table tr'):
                vals=[c.get_text(' ',strip=True) for c in tr.find_all('td',recursive=False)]
                if vals and vals[0].isdigit(): rows.append(vals)
        cols=['record_id','road','start_chainage','end_chainage','commune','condition','treated','untreated','note'] if sid=='GT-10' else ['record_id','road','chainage','place','note']
        if rows: save(pd.DataFrame(rows,columns=cols).drop_duplicates().sort_values('record_id',key=lambda s:s.astype(int)),sid+'_hazards.csv')
    e=latest('GT-04','osm_sample')
    if e:
        tree=ET.fromstring((ROOT/e['path']).read_bytes()); rows=[]
        for obj in tree:
            if obj.tag in ['node','way','relation']:
                tags={t.get('k'):t.get('v') for t in obj.findall('tag')}
                rows.append({'osm_type':obj.tag,'osm_id':obj.get('id'),'lat':obj.get('lat'),'lon':obj.get('lon'),'version':obj.get('version'),'timestamp':obj.get('timestamp'),'highway':tags.get('highway'),'amenity':tags.get('amenity'),'crossing':tags.get('crossing'),'sidewalk':tags.get('sidewalk'),'n_refs':len(obj.findall('nd'))})
        save(pd.DataFrame(rows),'GT-04_osm_sample.csv')
    e=latest('GT-20','classid.csv')
    if e: save(pd.read_csv(ROOT/e['path']),'GT-20_classes.csv')
    for label in ['hanoi_gtfs_am.zip','hanoi_gtfs_md.zip','hanoi_gtfs_pm.zip']:
        e=latest('GT-12',label)
        if e:
            with safe_zip(ROOT/e['path']) as z:
                for n in z.namelist():
                    if n.endswith('.txt'): save(pd.read_csv(z.open(n)),f'GT-12_{label[:-4]}_{Path(n).stem}.csv')
    e=latest('GT-09','Vehicle_Tracking.zip')
    if e:
        with safe_zip(ROOT/e['path']) as z:
            info=[{'name':i.filename,'bytes':i.file_size} for i in z.infolist()]
            (ROOT/'quality/GT-09_archive_members.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
            for n in z.namelist():
                if n.lower().endswith(('.txt','.csv','.json')) and z.getinfo(n).file_size<30_000_000:
                    p=ROOT/'data/interim/GT-09'/n; p.parent.mkdir(parents=True,exist_ok=True)
                    if not p.exists(): p.write_bytes(z.read(n))
    e=latest('GT-17','vietnam_transport_dataset.xlsx')
    if e:
        from parse_inventory import read_workbook
        s=read_workbook(ROOT/e['path'])
        (ROOT/'data/interim/GT-17_workbook.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
        with zipfile.ZipFile(ROOT/e['path']) as z: (ROOT/'quality/GT-17_workbook_structure.xml').write_bytes(z.read('xl/workbook.xml'))
if __name__=='__main__':
    from pathlib import Path
    main()
