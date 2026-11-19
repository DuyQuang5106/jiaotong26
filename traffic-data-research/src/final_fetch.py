import json
from urllib.parse import urlencode
from acquire import ROOT,fetch
def main():
    import sys
    if '--small' in sys.argv:
        fetch('GT-20','https://huggingface.co/datasets/star092304/Traffic-sign-detection-VietNam/raw/main/classid.csv','classid.csv')
        for part,code in [('am','DR0046582'),('md','DR0046583'),('pm','DR0046584')]: fetch('GT-12',f'https://datacatalogfiles.worldbank.org/ddh-published/0038236/1/{code}/hanoi_gtfs_{part}.zip',f'hanoi_gtfs_{part}.zip',40_000_000)
        fetch('GT-17','https://zenodo.org/api/records/17273112/files/vietnam_transport_dataset.xlsx/content','vietnam_transport_dataset.xlsx',2_000_000)
        return
    es=[json.loads(x) for x in (ROOT/'registry/http_events.jsonl').read_text(encoding='utf-8').splitlines()]
    e=next(e for e in es if e['source_id']=='GT-10' and e['label']=='landing')
    for page in range(5,10): fetch('GT-10',e['url']+f'?page={page}',f'page_{page}')
    fetch('GT-04','https://api.openstreetmap.org/api/0.6/map?bbox=106.797,10.868,106.801,10.872','osm_sample',15_000_000)
    fetch('LITERATURE','https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urlencode({'query':'Vietnam AND ("school" OR "helmet") AND "road safety"','format':'json','resultType':'core','pageSize':20}),'europepmc')
    fetch('GT-19','https://api.openaq.org/v3/countries','api_access_test')
    fetch('GT-20','https://huggingface.co/datasets/star092304/Traffic-sign-detection-VietNam/raw/main/README.md','readme')
if __name__=='__main__': main()
