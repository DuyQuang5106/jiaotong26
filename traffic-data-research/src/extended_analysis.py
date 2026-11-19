import json,zipfile,re
from pathlib import Path
import pandas as pd
import numpy as np
from xml.etree import ElementTree as ET
from ingest import ROOT,latest,safe_zip,save
def main():
    result={}
    # Both annotation representations independently reconciled; Vietnam subset only.
    for scene in ['VNTraffic','AICC22-Custom']:
        p=ROOT/'data/interim/GT-09'/scene
        if not p.exists(): continue
        name='VNTraffic' if scene=='VNTraffic' else scene
        d=pd.read_csv(p/(name+'_GroundTruth.txt'),header=None,names=['frame','track_id','x','y','width','height','confidence','unknown1','unknown2','unknown3'])
        save(d,f'GT-09_{scene}_boxes.csv')
        j=json.loads((p/(name+'_GroundTruth.json')).read_text(encoding='utf-8'))
        tracks=d.groupby('track_id').agg(first=('frame','min'),last=('frame','max'),observations=('frame','size'))
        tracks['span_frames']=tracks['last']-tracks['first']+1; tracks['gaps']=tracks.span_frames-tracks.observations
        save(tracks.reset_index(),f'GT-09_{scene}_tracks.csv')
        crowd=d.groupby('frame').size()
        result[scene]={'box_rows':len(d),'frames':d.frame.nunique(),'frame_min':int(d.frame.min()),'frame_max':int(d.frame.max()),'tracks':d.track_id.nunique(),'json_tracks':len(j),'json_box_count':sum(len(x['boxes']) for x in j.values()),'duplicate_frame_track':int(d.duplicated(['frame','track_id']).sum()),'nonpositive_boxes':int(((d.width<=0)|(d.height<=0)).sum()),'tracks_with_gaps':int((tracks.gaps>0).sum()),'track_length_median_frames':float(tracks.observations.median()),'boxes_per_frame_median':float(crowd.median()),'boxes_per_frame_range':[int(crowd.min()),int(crowd.max())],'class_labels':'absent in TXT and JSON','calibration':'not supplied; no TTC/PET/physical speed computed','dates':'record publication 2026-01-09; video observation date unknown','selection':'one video per subset; AICC22 excluded from Vietnam inference'}
        # Cross-check exact frame-track boxes in JSON, independently from TXT.
        mismatches=0
        lookup={(int(x.frame),str(int(x.track_id))):[int(x.x),int(x.y),int(x.width),int(x.height)] for x in d.itertuples()}
        for tid,obj in j.items():
            for f,b in zip(obj['frames'],obj['boxes']):
                frame=int(Path(f).stem)
                mismatches+=lookup.get((frame,tid))!=b
        result[scene]['json_txt_box_disagreements']=mismatches
    if result: (ROOT/'reports/GT-09_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    # GTFS linkage, timetable range, duplicated physical coordinates and headways.
    gtfs={}
    for part in ['am','md','pm']:
        prefix=ROOT/f'data/processed/GT-12_hanoi_gtfs_{part}'
        if not Path(str(prefix)+'_trips.csv').exists(): continue
        trip=pd.read_csv(str(prefix)+'_trips.csv'); stop=pd.read_csv(str(prefix)+'_stops.csv'); times=pd.read_csv(str(prefix)+'_stop_times.csv'); cal=pd.read_csv(str(prefix)+'_calendar.csv')
        def seconds(v):
            h,m,s=map(int,v.split(':')); return h*3600+m*60+s
        times['seconds']=times.departure_time.map(seconds)
        first=times.sort_values('stop_sequence').groupby('trip_id').first().reset_index().merge(trip[['trip_id','route_id']],on='trip_id',validate='one_to_one')
        headway=first.sort_values('seconds').groupby('route_id').seconds.diff().dropna()/60
        gtfs[part]={'trips':len(trip),'route_ids':trip.route_id.nunique(),'stop_ids':len(stop),'unique_coordinates':len(stop[['stop_lat','stop_lon']].drop_duplicates()),'stop_time_rows':len(times),'start_date':int(cal.start_date.min()),'end_date':int(cal.end_date.max()),'unmatched_trip_ids':int((~times.trip_id.isin(trip.trip_id)).sum()),'unmatched_stop_ids':int((~times.stop_id.isin(stop.stop_id)).sum()),'duplicate_trip_sequence':int(times.duplicated(['trip_id','stop_sequence']).sum()),'median_scheduled_headway_minutes':float(headway.median()),'departure_seconds_min':int(times.seconds.min()),'departure_seconds_max':int(times.seconds.max()),'warning':'scheduled feed calendar is 2018, not 2020 update or 2026 operation; stop IDs not unique physical stops'}
    (ROOT/'reports/GT-12_results.json').write_text(json.dumps(gtfs,indent=2),encoding='utf-8')
    # GT-17 isolate historical population, never use projections as measured denominators.
    p=ROOT/'data/interim/GT-17_workbook.json'
    if p.exists():
        sheets=json.loads(p.read_text(encoding='utf-8')); pop=next(s for s in sheets if any('Calculations for population (million)' in str(row) for row in s['rows']))
        rows=pop['rows']; header=next(row for row in rows if row.get('F6')=='2015'); values=next(row for row in rows if row.get('B8')=='Medium'); population=[]
        for cell,year in header.items():
            if year.isdigit() and 2015<=int(year)<=2024:
                key=re.sub('6$','8',cell); population.append({'year':int(year),'population_million':float(values[key]),'provenance':'GT-17 v1.1 Population sheet row 8; historical compiled series; cached formula results'})
        save(pd.DataFrame(population),'GT-17_historical_population.csv')
        a=pd.read_csv(ROOT/'data/processed/GT-01_national.csv').merge(pd.DataFrame(population),on='year',validate='one_to_one')
        for metric in ['crashes','deaths','injuries']: a[metric+'_per_100k_population']=a[metric]/(a.population_million*10)
        save(a,'GT-01_GT-17_population_rates.csv')
        e=latest('GT-17','vietnam_transport_dataset.xlsx'); stats=[]
        with zipfile.ZipFile(ROOT/e['path']) as z:
            ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            for name in z.namelist():
                if re.fullmatch(r'xl/worksheets/sheet\d+.xml',name):
                    tree=ET.fromstring(z.read(name)); stats.append({'xml':name,'rows':len(tree.findall('.//m:row',ns)),'formulas':len(tree.findall('.//m:f',ns)),'error_cells':len(tree.findall('.//m:c[@t="e"]',ns))})
        save(pd.DataFrame(stats),'GT-17_sheet_profile.csv')
if __name__=='__main__': main()
