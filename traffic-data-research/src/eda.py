import json
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from acquire import ROOT
from settings import CONFIG
def output(name,d):
    pd.DataFrame(d).to_csv(ROOT/'data/processed'/name,index=False,encoding='utf-8-sig')
def main():
    rng=np.random.default_rng(CONFIG['seed']); results={}
    s=pd.read_csv(ROOT/'data/processed/GT-07_segment_status.csv'); ts=pd.to_datetime(s.updated_at,utc=True).dt.tz_convert('Asia/Ho_Chi_Minh'); s['day']=ts.dt.strftime('%Y-%m-%d'); s['hour']=ts.dt.hour
    results['GT-07']={'rows':len(s),'segments':s.segment_id.nunique(),'start_utc':s.updated_at.min(),'end_utc':s.updated_at.max(),'days_observed':s.day.nunique(),'velocity_unit':'NOT_VERIFIED; raw scale','median':s.velocity.median(),'mean':s.velocity.mean(),'q25':s.velocity.quantile(.25),'q75':s.velocity.quantile(.75),'zero':int(s.velocity.eq(0).sum()),'gt120':int(s.velocity.gt(120).sum()),'sample_design':'unknown; event timestamps irregular'}
    hourly=s.groupby('hour').velocity.agg(['size','median','mean']).reset_index(); output('GT-07_hourly_summary.csv',hourly)
    daily=s.groupby('day').size().sort_values(ascending=False); output('GT-07_daily_coverage.csv',daily.rename('rows').reset_index())
    results['GT-07']['top_day_fraction']=daily.iloc[0]/len(s)
    # Exploratory contrast defined before computing it: 7-9/16-18 vs 10-15 local time.
    s['window']=np.select([s.hour.isin([7,8,16,17]),s.hour.between(10,14)],['peak','midday'],default='exclude')
    paired=s[s.window!='exclude'].groupby(['day','segment_id','window']).velocity.median().unstack().dropna()
    paired['difference']=paired['peak']-paired['midday']; days=paired.groupby(level='day')['difference'].mean()
    output('GT-07_paired_segment_day.csv',paired.reset_index()); output('GT-07_paired_day_effects.csv',days.rename('difference').reset_index())
    test={'classification':'EXPLORATORY','H0':'daily mean of within-segment peak-minus-midday recorded velocity = 0','H1':'different from 0, two-sided','sampling_unit':'day after pairing segment-day medians; repeated roads remain dependent','n_segment_days':len(paired),'n_days':len(days),'window_local':'peak 07:00-08:59 and 16:00-17:59; midday 10:00-14:59','multiplicity':'one exploratory primary contrast; no confirmatory claim','unit':'raw velocity unit NOT VERIFIED'}
    if len(days)>=5 and days.std()>0:
        boot=np.array([rng.choice(days.to_numpy(),size=len(days),replace=True).mean() for _ in range(CONFIG['bootstrap_replicates'])])
        res=stats.ttest_1samp(days,0); ci=np.quantile(boot,[.025,.975])
        test.update(estimate=days.mean(),ci95_bootstrap=ci.tolist(),t=float(res.statistic),p=float(res.pvalue),df=len(days)-1,median_day_difference=days.median(),leave_one_day_out_range=[float(days.drop(i).mean()) for i in days.index],assumptions='day-level exchangeability not established; serial dependence and measurement selection limit p-value')
        # Robustness: retain 0..120 on raw scale (screen only, not a validated speed rule).
        clean=s[s.velocity.between(0,120)&s.window.ne('exclude')].groupby(['day','segment_id','window']).velocity.median().unstack().dropna()
        test['sensitivity_0_120_mean_day_difference']=(clean.peak-clean.midday).groupby(level=0).mean().mean()
    else: test['not_tested_reason']='insufficient independent days or degenerate contrast'
    results['GT-07']['exploratory_test']=test
    plt.figure(figsize=(9,4)); plt.bar(hourly.hour,hourly['size']); plt.xlabel('Hour UTC+7'); plt.ylabel('Recorded status rows'); plt.title(f'Observed sample coverage, GT-07; n={len(s):,}; 2020-2021'); plt.tight_layout(); plt.savefig(ROOT/'figures/GT-07_hourly_coverage.png',dpi=160); plt.close()
    t=pd.read_csv(ROOT/'data/processed/GT-07_train.csv'); output('GT-07_LOS_counts.csv',t.groupby('LOS').size().rename('rows').reset_index())
    a=pd.read_csv(ROOT/'data/processed/GT-01_aggregates.csv'); national=a[a.region=='TỔNG SỐ'].pivot(index='year',columns='metric',values='value'); output('GT-01_national.csv',national.reset_index())
    results['GT-01']={'rows':len(a),'regions_including_nested_totals':a.region.nunique(),'years':[2022,2023,2024],'national':national.reset_index().to_dict('records'),'missing_values':int(a.value.isna().sum()),'crash_pct_change_2023_2024':(national.loc[2024,'crashes']/national.loc[2023,'crashes']-1)*100,'death_pct_change_2023_2024':(national.loc[2024,'deaths']/national.loc[2023,'deaths']-1)*100,'warning':'Counts; no exposure. Regional totals nested; no sum over all geographic rows. No causal test of annual counts.'}
    # Reconcile each regional subtotal against province rows, preserve discrepancies.
    regions=['Đồng bằng sông Hồng','Trung du và miền núi phía Bắc','Bắc Trung Bộ và Duyên hải miền Trung','Tây Nguyên','Đông Nam Bộ','Đồng bằng sông Cửu Long']
    order=a.region.drop_duplicates().tolist(); reconciliation=[]
    for i,reg in enumerate(regions):
        start=order.index(reg)+1; end=order.index(regions[i+1]) if i<5 else order.index('Khác')
        for year in [2022,2023,2024]:
            for metric in ['crashes','deaths','injuries']:
                reported=a[(a.region==reg)&(a.year==year)&(a.metric==metric)].value.iloc[0]
                summed=a[a.region.isin(order[start:end])&(a.year==year)&(a.metric==metric)].value.sum(min_count=1)
                reconciliation.append(dict(region=reg,year=year,metric=metric,reported=reported,sum_provinces=summed,difference=reported-summed))
    output('GT-01_reconciliation.csv',reconciliation)
    results['GT-01']['regional_reconciliation_failures']=sum(x['difference']!=0 for x in reconciliation)
    for sid in ['GT-10','GT-11']:
        d=pd.read_csv(ROOT/f'data/processed/{sid}_hazards.csv').fillna(''); text=d['condition'] if sid=='GT-10' else d.note
        counts=d.groupby('road').size().sort_values(ascending=False).rename('records').reset_index(); output(sid+'_road_counts.csv',counts)
        results[sid]={'rows':len(d),'roads':d.road.nunique(),'top_road':counts.iloc[0].to_dict(),'period':'snapshot updated 2025-12-02; current treatment status unverified','selection':'agency hazard inventory, not crash events'}
        if sid=='GT-10':
            flags=pd.DataFrame({'record_id':d.record_id,'visibility_mentioned':text.str.contains('tầm nhìn',case=False),'curve_mentioned':text.str.contains('cong|cua',case=False,regex=True),'treatment_nonempty':d.treated.str.len()>0,'untreated_nonempty':d.untreated.str.len()>0})
            output('GT-10_coding.csv',flags); results[sid].update({c:int(flags[c].sum()) for c in flags if c!='record_id'})
            results[sid]['sensitivity_exact_visibility_phrase']=int(text.str.contains('hạn chế tầm nhìn',case=False).sum())
    p=ROOT/'data/processed/GT-04_osm_sample.csv'
    if p.exists():
        d=pd.read_csv(p); results['GT-04']={'rows':len(d),'types':d.osm_type.value_counts().to_dict(),'highway_tagged':int(d.highway.notna().sum()),'crossing_tagged':int(d.crossing.notna().sum()),'schools_tagged':int(d.amenity.eq('school').sum()),'bbox':[106.797,10.868,106.801,10.872],'warning':'convenience sample; ways may extend outside bbox; absent tags do not establish physical absence; no distances calculated'}
    p=ROOT/'data/processed/GT-20_classes.csv'
    if p.exists():
        d=pd.read_csv(p); col=next(c for c in d if c.lower()=='count'); v=pd.to_numeric(d[col].astype(str).str.replace(',',''),errors='raise'); results['GT-20']={'rows':len(d),'reported_annotation_sum':int(v.sum()),'min_count':int(v.min()),'max_count':int(v.max()),'imbalance_ratio':float(v.max()/v.min()),'warning':'publisher class summary; not independently counted annotations, not road prevalence; label translation audit needed'}
    for part in ['am','md','pm']:
        files=list((ROOT/'data/processed').glob(f'GT-12_hanoi_gtfs_{part}_*.csv'))
        if files:
            results.setdefault('GT-12',{})[part]={p.stem.split('_')[-1]:len(pd.read_csv(p)) for p in files}
    def convert(o):
        if isinstance(o,np.generic): return o.item()
        raise TypeError(type(o).__name__)
    (ROOT/'reports/measured_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2,default=convert,allow_nan=False),encoding='utf-8')
    print(json.dumps(results,ensure_ascii=True,default=convert)[:15000])
if __name__=='__main__': main()
