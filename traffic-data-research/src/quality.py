import json
import pandas as pd
from acquire import ROOT
def main():
    profiles=[]
    for path in sorted((ROOT/'data/processed').glob('*.csv')):
        df=pd.read_csv(path); sid=path.name[:5]
        for col in df:
            profiles.append({'dataset':path.name,'source_id':sid,'field':col,'rows':len(df),'dtype':str(df[col].dtype),'missing':int(df[col].isna().sum()),'unique_nonmissing':int(df[col].nunique()),'duplicate_rows':int(df.duplicated().sum())})
    pd.DataFrame(profiles).to_csv(ROOT/'quality/field_profiles.csv',index=False,encoding='utf-8-sig')
    checks=[]
    def check(sid,name,count,scope): checks.append(dict(source_id=sid,check=name,flagged_count=int(count),scope=scope))
    s=pd.read_csv(ROOT/'data/processed/GT-07_segment_status.csv'); seg=pd.read_csv(ROOT/'data/processed/GT-07_segments.csv'); t=pd.read_csv(ROOT/'data/processed/GT-07_train.csv')
    check('GT-07','duplicate_segment_timestamp',s.duplicated(['segment_id','updated_at']).sum(),len(s))
    check('GT-07','velocity_negative',(s.velocity<0).sum(),len(s))
    check('GT-07','velocity_above_120_raw_unit_unverified',(s.velocity>120).sum(),len(s))
    check('GT-07','unmatched_segment_id',(~s.segment_id.isin(seg._id)).sum(),len(s))
    check('GT-07','zero_length_segment',(seg.length==0).sum(),len(seg))
    check('GT-07','train_missing_max_velocity',t.max_velocity.isna().sum(),len(t))
    check('GT-07','train_duplicate_segment_date_period',t.duplicated(['segment_id','date','period']).sum(),len(t))
    check('GT-07','weekday_disagreement',(pd.to_datetime(t.date).dt.weekday!=t.weekday).sum(),len(t))
    for sid,target in [('GT-10',107),('GT-11',58)]:
        d=pd.read_csv(ROOT/f'data/processed/{sid}_hazards.csv'); check(sid,'missing_expected_records',max(0,target-len(d)),target); check(sid,'duplicate_id',d.record_id.duplicated().sum(),len(d))
    p=ROOT/'reports/GT-09_results.json'
    if p.exists():
        for scene,obj in json.loads(p.read_text(encoding='utf-8')).items():
            check('GT-09',scene+'_duplicate_frame_track',obj['duplicate_frame_track'],obj['box_rows'])
            check('GT-09',scene+'_json_txt_id_key_disagreement',obj['json_txt_box_disagreements'],obj['json_box_count'])
            check('GT-09',scene+'_json_txt_box_count_difference',abs(obj['json_box_count']-obj['box_rows']),obj['json_box_count'])
    p=ROOT/'data/processed/GT-01_reconciliation.csv'
    if p.exists():
        rec=pd.read_csv(p); check('GT-01','nonzero_regional_total_minus_provinces',rec.difference.ne(0).sum(),len(rec))
    p=ROOT/'quality/GT-02_report_reconciliation.csv'
    if p.exists():
        rec=pd.read_csv(p); check('GT-02','different_previous_month_revision_or_error',rec.difference.ne(0).sum(),len(rec))
    for part in ['am','md','pm']:
        p=ROOT/f'data/processed/GT-12_hanoi_gtfs_{part}_stops.csv'
        if p.exists():
            d=pd.read_csv(p); check('GT-12',part+'_invalid_coordinate',(~d.stop_lat.between(-90,90)|~d.stop_lon.between(-180,180)).sum(),len(d))
    p=ROOT/'data/processed/GT-20_classes.csv'
    if p.exists():
        d=pd.read_csv(p); check('GT-20','duplicate_class_id',d.ID.duplicated().sum(),len(d)); check('GT-20','manual_language_conflict_ID31',1,len(d))
    pd.DataFrame(checks).to_csv(ROOT/'quality/sanity_checks.csv',index=False,encoding='utf-8-sig')
    for sid in sorted(set(x['source_id'] for x in profiles)):
        subset=[x for x in checks if x['source_id']==sid]
        (ROOT/f'quality/{sid}_quality.md').write_text('# Kiểm toán '+sid+'\n\n[MEASURED RESULT] Hồ sơ từng cột: `field_profiles.csv`; cờ kiểm tra: `sanity_checks.csv`.\n\n'+json.dumps(subset,ensure_ascii=False,indent=2)+'\n\n[NOT VERIFIED] Thiếu dữ liệu không được thay bằng 0; định nghĩa/đơn vị phải xem dossier. Cờ ngoại lệ không tự động bị loại.\n',encoding='utf-8')
if __name__=='__main__': main()
