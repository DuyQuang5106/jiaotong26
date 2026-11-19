import json
import pandas as pd
from acquire import ROOT
def main():
    a=pd.read_csv(ROOT/'data/processed/GT-10_hazards.csv'); b=pd.read_csv(ROOT/'data/processed/GT-11_hazards.csv')
    ra=set(a.road.str.strip()); rb=set(b.road.str.strip()); common=sorted(ra&rb)
    rows=[{'source_a':'GT-10','source_b':'GT-11','join_key':'exact stripped road label','matched_road_labels':len(common),'labels':';'.join(common),'compatibility':'same snapshot date and agency; road overlap only, not event or coordinate match','independent_corroboration':False},
          {'source_a':'GT-01','source_b':'GT-17','join_key':'year, national totals','matched_road_labels':None,'labels':'2022;2023;2024','compatibility':'population denominator derived from historical compiled NSO values; geographic national coverage plausible; definitions need checking','independent_corroboration':False},
          {'source_a':'GT-06','source_b':'GT-07','join_key':'city only','matched_road_labels':None,'labels':'Ho Chi Minh','compatibility':'2025 versus 2020-2021; different coverage and data collection; no record-level join','independent_corroboration':False},
          {'source_a':'GT-04','source_b':'GT-12','join_key':'coordinates','matched_road_labels':None,'labels':'different cities','compatibility':'small HCMC bbox vs Hanoi GTFS 2018; join not performed','independent_corroboration':False},
          {'source_a':'GT-08','source_b':'GT-09','join_key':'none','matched_road_labels':None,'labels':'different videos/cities/cameras','compatibility':'anomaly masks vs tracking; no common events or exposure','independent_corroboration':False}]
    pd.DataFrame(rows).to_csv(ROOT/'reports/cross_source_compatibility.csv',index=False,encoding='utf-8-sig')
    # Compare latest report change to previous report, do not silently revise either.
    d=pd.read_csv(ROOT/'data/processed/GT-02_monthly_counts.csv').set_index('month')
    discrepancies=[{'metric':k,'September_standalone':int(d.loc[9,k]),'September_implied_by_October':int(d.loc[10,k]+delta),'difference':int(d.loc[10,k]+delta-d.loc[9,k])} for k,delta in [('crashes',64),('deaths',67),('injuries',26)]]
    pd.DataFrame(discrepancies).to_csv(ROOT/'quality/GT-02_report_reconciliation.csv',index=False,encoding='utf-8-sig')
if __name__=='__main__': main()
