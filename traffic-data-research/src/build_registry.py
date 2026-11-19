import csv,hashlib,json,platform,sys
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from ingest import ROOT,events,latest
CLASSES={1:'B_AGGREGATE_OPEN',2:'B_AGGREGATE_OPEN',3:'C_REPORT_ONLY',4:'A_RAW_OPEN',5:'D_CATALOG_ONLY',6:'B_AGGREGATE_OPEN',7:'A_RAW_OPEN',8:'A_RAW_OPEN',9:'A_RAW_OPEN',10:'A_RAW_OPEN',11:'A_RAW_OPEN',12:'A_RAW_OPEN',13:'D_CATALOG_ONLY',14:'D_CATALOG_ONLY',15:'C_REPORT_ONLY',16:'C_REPORT_ONLY',17:'B_AGGREGATE_OPEN',18:'D_CATALOG_ONLY',19:'E_RESTRICTED',20:'B_AGGREGATE_OPEN',21:'D_CATALOG_ONLY',22:'C_REPORT_ONLY'}
NOTES={
1:('Bảng HTML PX-Web V14.88: 71 nhãn địa lý × 3 năm × 3 chỉ tiêu; metadata ghi Thống kê chính thức: Không. API thử lần đầu 404, biểu mẫu công khai POST thành công.','Tổng vùng miền Trung 2024 không khớp tỉnh thành phần; phạm vi/định nghĩa 2022–2023 chưa thống nhất.','Xin NSO giải thích ba sai lệch, định nghĩa vụ và tử vong; giữ nguyên số gốc.'),
2:('Đã tải 3 báo cáo sơ bộ tháng 8–10/2026 và trích số vụ, chết, bị thương.','Chênh lệch tháng 9 suy ngược từ báo cáo tháng 10 so với báo cáo tháng 9 riêng; không có mẫu số lưu lượng.','Xác minh revision và kỳ chốt thống kê; không cộng nối với NSO năm khác.'),
3:('Trang hồ sơ an toàn đường bộ ATO truy cập được; có đường dẫn PDF. Chưa trích bảng PDF.','Chỉ metadata/nội dung báo cáo; chưa tải hay phân tích PDF.','Tải PDF gốc, ghi năm của từng chỉ tiêu và nguồn WHO/nhà nước; tránh đếm độc lập dữ liệu tái sử dụng.'),
4:('Geofabrik timeout hai lần. Đã tải mẫu XML từ API OSM chính thức bbox [106.797,10.868,106.801,10.872].','Mẫu thuận tiện nhỏ, không đại diện Việt Nam; không có kiểm tra thực địa; Geofabrik chưa xác minh được.','Mở rộng mẫu có thiết kế và kiểm chứng độc lập; OSM thiếu tag không có nghĩa thiếu hạ tầng.'),
5:('Trang hướng dẫn Mapillary tải map data truy cập được.','Chưa thử tải ảnh/map features; quyền token và coverage chưa xác minh.','Kiểm tra chính sách và token của tài khoản được phép, chọn mẫu có quyền sử dụng.'),
6:('Trích hai hàng tổng hợp thành phố từ trang TomTom; kỳ hiển thị 2025.','Không có probe thô hoặc mẫu số chuyến; hai thành phố không xác định nút giao cụ thể.','Lấy định nghĩa vùng/phương pháp và đo lại hàng chờ tại nút chọn khảo sát.'),
7:('ZIP thực tế 8.379.823 byte có 5 CSV; Kaggle metadata gốc ghi CC0 và version 6, cập nhật 2021. TDC license not specified.','Đơn vị velocity và cách thu mẫu chưa xác minh; lịch lấy mẫu lệch; metadata 2026 không phải kỳ quan sát.','Xác nhận đơn vị/LOS với tác giả; đo mẫu hiện hành để kiểm chứng.'),
8:('Đã tải 50 file nhãn nhị phân NPY công khai trong thư mục test_frame_mask, README và metadata dự án.','Nhãn chỉ normal/abnormal, không phân biệt hàng cồng kềnh; video, COCO 379 MB/177,8 MB chưa tải; chưa thấy license rõ.','Xin điều khoản nghiên cứu/redistribution; xác minh ánh xạ frame–video, lấy nhãn loại hành vi và mẫu không tuyển theo sự kiện.'),
9:('Zenodo record 18195750 Version 1, CC-BY-4.0; ZIP 39.489.618 byte có hai tập con. VNTraffic và AICC22 phân tích riêng.','TXT/JSON khác định danh track; có khóa frame-track trùng. Không có homography hoặc ngày quay xác minh.','Xin giải thích ánh xạ track và sửa khóa trùng; hiệu chỉnh camera trước TTC/PET, không công bố ảnh người/biển số.'),
10:('Đã tải đủ 11 trang công khai, trích 107 vị trí/đoạn nguy cơ, cập nhật 02/12/2025.','Không phải tai nạn thực tế; lý trình có dạng rút gọn; chưa geocode/đo hiện trường; không có giấy phép tái phân phối rõ.','Xác nhận trạng thái xử lý 2026, chuẩn hóa lý trình có người kiểm tra, đo lưu lượng và tầm nhìn.'),
11:('Đã tải đủ 6 trang, trích 58 vị trí/đoạn nguy cơ sạt lở, cập nhật 02/12/2025.','Không có ngày xảy ra sạt lở, GPS hay outcome; cùng cơ quan GT-10, không độc lập.','Lấy nhật ký sạt lở, ngày đóng đường, GPS và mưa đo tại chỗ trước kiểm định dự báo.'),
12:('Đã tải đủ ba ZIP AM/MD/PM. Calendar trong cả ba là 01/01/2018–31/12/2018, không phải lịch 2026.','7.670 stop_id tương ứng 3.146 cặp tọa độ; không gọi stop_id là số trạm vật lý; không có GPS thực.','Xin GTFS hiện hành, chuẩn hóa điểm dừng và mạng đi bộ, không cộng chuyến trùng giữa ba khung.'),
13:('Bài Chính phủ xác nhận danh mục 171 dữ liệu mở và 95 dùng chung, Quyết định 5695 ngày 12/10/2026.','Danh mục không chứng minh đã có từng file quan sát giao thông.','Theo cổng Hà Nội tìm từng tài nguyên có schema/license; không coi mọi dữ liệu dùng chung là mở.'),
14:('Trang cơ quan TP.HCM mô tả danh mục 142 và liên kết cổng dữ liệu.','Chưa kiểm chứng từng resource, giấy phép hay dữ liệu đường/nút cụ thể.','Chọn tài nguyên giao thông tại data.hochiminhcity.gov.vn, kiểm tra link và kỳ cập nhật.'),
15:('Bản tin VTV mô tả hệ thống camera AI giai đoạn 2; tải được bài báo.','Thông số camera là công bố năng lực, không phải log quan sát công khai; không thử quyền hệ thống nội bộ.','Đề nghị cơ quan cấp bảng đếm tổng hợp theo nút × 15 phút, loại dữ liệu cá nhân.'),
16:('Bài Chính phủ năm 2022 mô tả ITS: 118 mặt cắt và 216 nút.','Không có raw VDS/phasing; công bố không chứng minh hiệu quả nhân quả.','Xin log lưu lượng và pha đèn cùng thời kỳ; chọn thiết kế đánh giá với đối chứng.'),
17:('Zenodo 17273112 v1.1 CC-BY-4.0, XLSX tải được; đọc 18 sheet, lấy riêng dân số lịch sử 2015–2024.','Có historical, projection và tham số mô hình; công thức chỉ đọc cached value, không tái tính Excel/Solver; không độc lập NSO.','Xác minh nguồn dân số gốc; không dùng dự báo 2026/2050 như quan sát thực.'),
18:('Trang NASA IMERG truy cập được; mô tả sản phẩm, không có file mưa tải trong lần chạy.','Chưa lấy raster hoặc kiểm thử Earthdata; không kết luận đã bị hạn chế tài khoản.','Chọn sản phẩm/phiên bản, bbox và cửa sổ sự kiện có outcome; thử endpoint chính thức và ghi quyền.'),
19:('Tài liệu OpenAQ truy cập được; GET /v3/countries trả 401 và yêu cầu X-API-Key.','NO ACCESS TO DATA trong lần chạy; chưa xác minh phủ trạm Việt Nam.','Dùng API key do người dùng tự quản lý sau khi được phép; không suy nguồn ô nhiễm từ tương quan.'),
20:('Đã tải classid.csv: 82 hàng thống kê lớp; kho có ZIP ảnh 904.774.951 byte.','ZIP vượt 500 MB/nguồn nên không tải. License chưa rõ; ID31 Anh/Viet trái/phải mâu thuẫn; Count là số công bố.','Xác minh license, sửa từ điển lớp và lấy tập nhãn nhỏ có scene split; không gọi Count là số ảnh kiểm đếm.'),
21:('Cổng PX-Web NSO truy cập được; chưa chọn bảng vận tải riêng.','Không có dữ liệu quan sát mới ngoài GT-01; đây là portal.','Chọn bảng theo chỉ tiêu, kiểm tra đơn vị, metadata và lấy toàn bộ giá trị liên quan.'),
22:('Cổng thông tin giao thông TP.HCM truy cập được; giao diện/ứng dụng web.','Không có log lịch sử hoặc API thô đã xác minh; không lưu camera stream.','Xin tài liệu API lịch sử và quyền sử dụng; chỉ thu bảng tổng hợp được cho phép.')}
def main():
    inventory=json.loads((ROOT/'registry/inventory.json').read_text(encoding='utf-8')); es=events(); rows=[]; backlog=[]
    profiles=pd.read_csv(ROOT/'quality/field_profiles.csv')
    definitions={
      'frame':('Chỉ số frame trong file annotation','frame index','nonnegative integer'),
      'track_id':('ID track do file cung cấp; chưa thống nhất TXT/JSON','identifier','do not assume globally unique'),
      'x':('Tọa độ x hộp theo file, chưa xác minh origin','pixel scale','NOT_VERIFIED'),
      'y':('Tọa độ y hộp theo file, chưa xác minh origin','pixel scale','NOT_VERIFIED'),
      'width':('Chiều rộng hộp trong annotation','pixel scale','positive'),
      'height':('Chiều cao hộp trong annotation','pixel scale','positive'),
      'velocity':('Giá trị velocity ghi nhận; chưa xác minh quy trình và đơn vị','NOT_VERIFIED','negative flagged; >120 sensitivity screen only'),
      'max_velocity':('Thuộc tính max_velocity theo bản đồ/dataset, chưa xác minh là pháp định','NOT_VERIFIED','missing retained'),
      'length':('Thuộc tính length của segment; đơn vị chưa xác minh độc lập','NOT_VERIFIED','zero flagged, not dropped'),
      'LOS':('Nhãn LOS có A–F trong train; ngưỡng ánh xạ chưa xác minh','category','A;B;C;D;E;F'),
      'updated_at':('Timestamp cập nhật record, không tự coi thời điểm xe đi qua','ISO8601 UTC where suffix Z','valid timestamp'),
      'date':('Ngày trong bảng train; nguồn không đủ xác nhận timezone gốc','YYYY-MM-DD','valid date'),
      'period':('Mã khung giờ của train','category','observed period strings; duration NOT_VERIFIED'),
      'weekday':('Mã thứ trong train, đối chiếu được Monday=0','integer','0..6'),
      'lat':('Vĩ độ','degrees WGS84','-90..90'), 'long':('Kinh độ','degrees WGS84','-180..180'),
      'stop_lat':('Vĩ độ điểm dừng feed','degrees WGS84','-90..90'), 'stop_lon':('Kinh độ điểm dừng feed','degrees WGS84','-180..180'),
      'arrival_time':('Giờ đến theo lịch, không phải GPS thực','GTFS HH:MM:SS potentially >24','nonnegative'),
      'departure_time':('Giờ đi theo lịch, không phải GPS thực','GTFS HH:MM:SS potentially >24','nonnegative'),
      'Count':('Số annotation theo lớp do nhà cung cấp công bố, chưa kiểm đếm ảnh','published count','nonnegative integer'),
      'population_million':('Dân số lịch sử tổng hợp từ dòng Medium workbook v1.1','million persons','positive; 2015-2024 only'),
      'condition':('Mô tả hiện trạng do cơ quan ghi tại snapshot','text','not independently field validated'),
      'treated':('Văn bản trường Đã xử lý; không rỗng không mặc định hoàn tất','text','blank retained'),
      'untreated':('Văn bản trường Chưa xử lý; có thể đồng thời có treated','text','blank retained'),
      'start_chainage':('Lý trình đầu nguyên bản; chưa geocode','chainage string','abbreviations require manual review'),
      'end_chainage':('Lý trình cuối nguyên bản; chưa geocode','chainage string','abbreviations require manual review')}
    dictionary=[]
    for p in profiles.to_dict('records'):
        meaning,unit,allowed=definitions.get(p['field'],('Tên trường theo file nguồn/dẫn xuất; xem script và dossier trước diễn giải','NOT_VERIFIED unless defined in analysis script','observed values only; no invented allowed domain'))
        dictionary.append({**p,'meaning_vi':meaning,'unit':unit,'allowed_or_validation_rule':allowed,'missing_policy':'empty/NA preserved, no imputation; source-specific semantics NOT_VERIFIED','provenance':'raw_manifest.json + src/ingest.py, eda.py, extended_analysis.py, supplemental_analysis.py'})
    pd.DataFrame(dictionary).to_csv(ROOT/'registry/data_dictionary.csv',index=False,encoding='utf-8-sig')
    for original in inventory:
        sid=original['Mã nguồn']; i=int(sid[-2:]); attempts=[e for e in es if e['source_id']==sid]; fact,blocker,action=NOTES[i]
        observed=profiles[profiles.source_id==sid]
        row={**original,'source_id':sid,'source_type':'row_data' if CLASSES[i].startswith('A_') else 'aggregate' if CLASSES[i].startswith('B_') else 'report_or_catalog','last_checked_utc':max(e['download_utc'] for e in attempts),'access_status':CLASSES[i],'content_status':fact,'data_format':','.join(sorted(set(Path(p).suffix for p in observed.dataset.unique()))),'license':'CC0 (Kaggle original metadata); TDC unspecified' if i==7 else 'CC-BY-4.0' if i in [9,17] else 'ODbL (OSM); attribution required' if i==4 else 'NOT_VERIFIED; no redistribution permission inferred','data_grain':original['Đơn vị quan sát'],'spatial_resolution':'sample bbox EPSG:4326' if i==4 else 'NOT_VERIFIED; see dossier','temporal_resolution':'NOT_VERIFIED; see dossier','coverage_start':'NOT_VERIFIED','coverage_end':'NOT_VERIFIED','observed_field_names':';'.join(observed.field.unique()),'raw_file_path':';'.join(e['path'] for e in attempts if e['path']),'sha256':';'.join(e.get('sha256','') for e in attempts if e['path']),'blocker':blocker,'next_action':action}
        coverage={1:('2022','2024','year','national/legacy provinces and nested region totals'),2:('2026-08','2026-10','month','national'),4:('NOT_VERIFIED','2026-11-19 snapshot','OSM object version','small bbox in HCMC'),6:('2025','2025','annual published city index','TomTom city bounds NOT_VERIFIED'),7:('2020-07-03','2021-04-22','irregular timestamp','segment/node network in HCMC'),8:('NOT_VERIFIED','NOT_VERIFIED','frame mask','three roundabouts as reported metadata; per-file mapping NOT_VERIFIED'),9:('NOT_VERIFIED','NOT_VERIFIED','frame/track','one Vietnam video; precise camera NOT_VERIFIED'),10:('2025-12-02 snapshot','2025-12-02 snapshot','inventory snapshot','road chainage; no validated GPS'),11:('2025-12-02 snapshot','2025-12-02 snapshot','inventory snapshot','road chainage; no validated GPS'),12:('2018-01-01','2018-12-31','scheduled trip/stop time','Hanoi feed coordinates'),17:('2015','2024 historical subset','year','Vietnam national'),20:('NOT_VERIFIED','NOT_VERIFIED','class aggregate','Vietnam signs benchmark; no geolocation')}
        if i in coverage:
            start,end,temporal,spatial=coverage[i]; row.update(coverage_start=start,coverage_end=end,temporal_resolution=temporal,spatial_resolution=spatial)
        formats={1:'HTML table (derived CSV)',2:'HTML report (derived CSV)',3:'HTML report metadata; PDF linked, not downloaded',4:'OSM XML (derived CSV)',5:'HTML documentation',6:'HTML published table (derived CSV)',7:'ZIP with 5 CSV',8:'NPY binary masks; README text; HTML metadata',9:'ZIP with JSON/TXT annotations and MP4 (video not decoded)',10:'paginated HTML table (derived CSV)',11:'paginated HTML table (derived CSV)',12:'ZIP with GTFS TXT/CSV',13:'HTML catalog announcement',14:'HTML catalog announcement',15:'HTML system announcement',16:'HTML system announcement',17:'XLSX OOXML and cached values',18:'HTML product documentation',19:'HTML docs; JSON 401 error',20:'CSV class counts; README; ZIP metadata only',21:'HTML portal',22:'HTML application shell'}
        row['data_format']=formats[i]
        rows.append(row); backlog.append(dict(source_id=sid,priority='deep' if i in [1,4,7,8,9,10] else 'secondary',blocker=blocker,next_action=action,status='FOLLOWUP_REQUIRED',evidence_state='NO ACCESS TO DATA' if i==19 else 'NO EVIDENCE for local causal effect',owner='provider / field research team',fetch_script='src/'+('uit_fetch.py' if i==8 else 'deep_fetch.py' if i in [1,7,9,17] else 'acquire.py')))
        lines=[f'# {sid} — {original["Nguồn / dataset"]}','',f'[VERIFIED SOURCE FACT] {fact}',f'\nPhân lớp truy cập: **{CLASSES[i]}**. Kiểm tra UTC: {row["last_checked_utc"]}.',f'\nNguồn danh mục: {original["Link nguồn gốc"]}',f'\n[NOT VERIFIED] {blocker}',f'\n[RECOMMENDATION] {action}','\n## Mô tả Excel chưa phải quan sát','\n[HYPOTHESIS] '+original['Vấn đề có thể xảy ra (GIẢ THUYẾT)'],'\n## Lược đồ thực tế và từ điển','\n'+('; '.join(observed.field.unique()) if len(observed) else 'Chưa có bảng quan sát tải được. Không suy ra schema từ mô tả.')+'\n\nĐịnh nghĩa, kiểu dữ liệu, số thiếu, số duy nhất: `../quality/field_profiles.csv`. Đơn vị chưa xác minh ghi NOT_VERIFIED, không tự gán.',f'\nGiấy phép/quyền: {row["license"]}. Công khai để xem không tự động cho phép tái phân phối.','\n## Nhật ký truy cập','\n| UTC | Loại | HTTP | byte | URL cuối / lỗi | SHA256 |','|---|---|---:|---:|---|---|']
        for e in attempts: lines.append(f'| {e["download_utc"]} | {e["label"]} | {e["status"]} | {e.get("byte_size","")} | {e.get("final_url",e["url"])} {e["error"][:160]} | {e.get("sha256","")} |')
        lines+=['\n## Phạm vi suy luận','\n[INTERPRETATION] Kết quả chỉ áp dụng cho bản snapshot/mẫu tải được. Không có dữ liệu về can thiệp làm giảm tai nạn tại địa bàn chọn dự thi. Các nguồn chung tác giả/cơ quan hoặc dùng lại NSO không được tính là xác nhận độc lập.']
        (ROOT/f'sources/{sid}.md').write_text('\n'.join(lines),encoding='utf-8')
        q=ROOT/f'quality/{sid}_quality.md'
        if not q.exists(): q.write_text(f'# Kiểm toán {sid}\n\n[NOT VERIFIED] Chưa có bảng quan sát để kiểm toán chất lượng. {blocker}\n\nBước tiếp: {action}\n',encoding='utf-8')
    pd.DataFrame(rows).to_csv(ROOT/'registry/source_audit.csv',index=False,encoding='utf-8-sig'); pd.DataFrame(backlog).to_csv(ROOT/'registry/acquisition_backlog.csv',index=False,encoding='utf-8-sig')
    md='# Kiểm chứng 22 nguồn\n\nNgày nghiên cứu: 19/11/2026, UTC+7. Phân lớp theo nội dung thực tải, không theo HTTP 200 đơn thuần.\n\n|Mã|Trạng thái|Nội dung đã kiểm chứng|\n|---|---|---|\n'+'\n'.join(f'|{r["source_id"]}|{r["access_status"]}|{r["content_status"]}|' for r in rows)
    (ROOT/'registry/source_audit.md').write_text(md,encoding='utf-8')
    (ROOT/'registry/licenses_and_access.md').write_text('# Giấy phép và tiếp cận\n\nDữ liệu raw được giữ tại máy trong phạm vi nghiên cứu do người dùng yêu cầu. Không có việc cấp quyền tái phân phối mặc định. Không tải ZIP ảnh GT-20 vượt trần 500 MB. Không phát tán video/ảnh nhận dạng. Không truy cập API yêu cầu tài khoản Sơn La. OpenAQ 401 được giữ lại.\n\n'+'\n'.join(f'- {r["source_id"]}: {r["license"]}' for r in rows),encoding='utf-8')
    manifest=[]
    for e in es:
        if e['path']:
            assert hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest()==e['sha256']
            sid=e['source_id']; r=next((r for r in rows if r['source_id']==sid),{})
            version='Version 1, record 18195750' if sid=='GT-09' else 'v1.1 record 17273112' if sid=='GT-17' else 'snapshot SHA256; provider version linkage NOT_VERIFIED'
            manifest.append({**e,'original_filename':e['label'],'license':r.get('license','copyright / metadata; redistribution NOT_VERIFIED'),'data_version':version,'transformation_script':'src/ingest.py; src/extended_analysis.py; src/supplemental_analysis.py','period':str(r.get('coverage_start','NOT_VERIFIED'))+' / '+str(r.get('coverage_end','NOT_VERIFIED')),'region':r.get('spatial_resolution','NOT_VERIFIED')})
    (ROOT/'registry/raw_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(pd.DataFrame(rows).access_status.value_counts().to_string()); print('Raw bytes:',sum(e.get('byte_size',0) for e in es))
def re_source(sid): return sid.startswith('GT-') and sid[-2:].isdigit()
if __name__=='__main__': main()
