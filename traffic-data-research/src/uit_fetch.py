import json
from bs4 import BeautifulSoup
from acquire import ROOT,fetch
def main():
    import sys
    if '--download-masks' in sys.argv:
        es=[json.loads(x) for x in (ROOT/'registry/http_events.jsonl').read_text(encoding='utf-8').splitlines()]
        e=next(e for e in es if e['source_id']=='GT-08' and e['label']=='masks_folder')
        soup=BeautifulSoup((ROOT/e['path']).read_bytes(),'html.parser'); seen=set()
        for obj in soup.select('[data-id]'):
            name=obj.get_text(' ',strip=True)
            if name.endswith('.npy') and ' ' not in name and obj['data-id'] not in seen:
                seen.add(obj['data-id']); fetch('GT-08','https://drive.google.com/uc?export=download&id='+obj['data-id'],name,500_000)
        return
    if '--masks' in sys.argv:
        fetch('GT-08','https://drive.google.com/drive/folders/1e3JP1FfNjBvPMNqkJD6CrtoO0cbMXWJG','masks_folder')
        return
    fetch('GT-08','https://drive.google.com/drive/folders/1FiMaP8vH7B5YJITLiBcxq0gfsZBN8Mln','test_folder')
    fetch('GT-08','https://drive.google.com/uc?export=download&id=1C5JCoWTxL2DgIEkoPcvnPj8OqBl3_yoz','README.txt')
if __name__=='__main__': main()
