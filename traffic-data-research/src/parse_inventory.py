"""Read OOXML without evaluating formulas, preserving cells and hyperlinks."""
import csv, hashlib, json, re, shutil, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
NS = {'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def read_workbook(path):
    sheets=[]
    with zipfile.ZipFile(path) as z:
        strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)] if 'xl/sharedStrings.xml' in z.namelist() else []
        for name in z.namelist():
            if re.fullmatch(r'xl/worksheets/sheet\d+.xml',name):
                tree=ET.fromstring(z.read(name)); rows=[]
                for r in tree.findall('.//m:row',NS):
                    cells={}
                    for c in r:
                        v=c.find('m:v',NS); inline=c.find('m:is',NS)
                        cells[c.get('r')]=''.join(inline.itertext()) if inline is not None else strings[int(v.text)] if c.get('t')=='s' and v is not None else v.text if v is not None else ''
                    rows.append(cells)
                sheets.append({'xml':name,'rows':rows,'hyperlinks':[dict(x.attrib) for x in tree.findall('.//m:hyperlink',NS)],'relationships':z.read(name.replace('worksheets/','worksheets/_rels/')+'.rels').decode() if name.replace('worksheets/','worksheets/_rels/')+'.rels' in z.namelist() else ''})
    return sheets
def parse(path):
    sheets=read_workbook(path); records=[]
    for sheet in sheets:
        header=None
        for row in sheet['rows']:
            vals=list(row.values())
            if 'Mã nguồn' in vals: header={re.sub(r'\d','',k):v for k,v in row.items()}; continue
            if header:
                d={header.get(re.sub(r'\d','',k),k):v for k,v in row.items()}
                if re.fullmatch(r'GT-\d{2}',d.get('Mã nguồn','')): records.append(d)
    ids=[d['Mã nguồn'] for d in records]
    assert len(ids)==22 and len(set(ids))==22 and set(ids)=={f'GT-{i:02}' for i in range(1,23)},ids
    return sheets,records
def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('workbook',type=Path); a=ap.parse_args()
    for p in ['input','registry','sources','data/raw','data/interim','data/processed','quality','figures','reports','tests','notebooks']: (ROOT/p).mkdir(parents=True,exist_ok=True)
    dest=ROOT/'input'/a.workbook.name
    if not dest.exists(): shutil.copy2(a.workbook,dest)
    assert hashlib.sha256(dest.read_bytes()).digest()==hashlib.sha256(a.workbook.read_bytes()).digest()
    sheets,records=parse(dest)
    (ROOT/'registry/workbook_structure.json').write_text(json.dumps(sheets,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'registry/inventory.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    with (ROOT/'registry/inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0])); w.writeheader(); w.writerows(records)
    print('VALID: 22 unique IDs GT-01..GT-22; columns:',len(records[0]))
    for d in records: print(d['Mã nguồn'],d['Nguồn / dataset'],d['Link nguồn gốc'])
if __name__=='__main__': main()
