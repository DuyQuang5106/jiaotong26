import json
from urllib.parse import urlparse,parse_qs
import pandas as pd
from acquire import ROOT
from ingest import events
from write_reports import write,table
def main():
    records=[]; search=[]
    for e in events():
        if e['source_id']!='LITERATURE' or e['status']!=200: continue
        if e['label'].startswith('crossref_'):
            j=json.loads((ROOT/e['path']).read_text(encoding='utf-8')); items=j['message']['items']; query=parse_qs(urlparse(e['url']).query)['query'][0]
            search.append({'database':'Crossref','query':query,'utc':e['download_utc'],'expected_total':j['message']['total-results'],'retrieved':len(items),'pages':1,'complete':False,'raw_file':e['path'],'url':e['url']})
            for x in items: records.append({'database':'Crossref','doi':x.get('DOI','').lower(),'title':x.get('title',[''])[0],'content_read':'metadata only','query':query})
        elif e['label']=='europepmc':
            j=json.loads((ROOT/e['path']).read_text(encoding='utf-8')); items=j['resultList']['result']; query=j['request']['queryString']
            search.append({'database':'Europe PMC','query':query,'utc':e['download_utc'],'expected_total':j['hitCount'],'retrieved':len(items),'pages':1,'complete':False,'raw_file':e['path'],'url':e['url']})
            for x in items: records.append({'database':'Europe PMC','doi':x.get('doi','').lower(),'title':x['title'],'content_read':'core metadata and available abstract','query':query})
    d=pd.DataFrame(records); selected={'10.3389/fpubh.2026.1721586','10.1136/injuryprev-2017-042517','10.1109/jstars.2023.3285905','10.18280/mmep.130509'}
    d['screening']='not taken forward in bounded narrative review; local relevance/fulltext not established'
    d.loc[d.doi.isin(selected),'screening']='selected for targeted source verification'
    d.to_csv(ROOT/'reports/literature_search_records.csv',index=False,encoding='utf-8-sig'); pd.DataFrame(search).to_csv(ROOT/'reports/literature_search_log.csv',index=False,encoding='utf-8-sig')
    rows=[
    {'candidate':'P02','reference':'Nhan et al., Evaluation of an integrated multisector campaign to increase child helmet use in Vietnam','url':'https://doi.org/10.1136/injuryprev-2017-042517','read_scope':'publisher abstract; full text not available there','design':'100 schools, four repeated cross-sectional waves; integrated campaign','claim_status':'reported study results; not reanalysed individual records','limitation':'multiple simultaneous components, no isolated education effect; passengers differ from electric-bike riders','existing_solution':'school education, helmet campaigns, parental involvement, enforcement','novelty':'NOT ESTABLISHED'},
    {'candidate':'P02','reference':'A scalable model for child road safety ... Slow Zones, Safe Zones ... Vietnam (2026)','url':'https://doi.org/10.3389/fpubh.2026.1721586','read_scope':'PMC full text, methods, tables and limitations','design':'school-zone infrastructure/education/enforcement; city-wide pre-post; some early speed controls','claim_status':'published observations, no new causal reanalysis','limitation':'changed measurement instruments, different recall windows, no sustained city-wide control, COVID confounding','existing_solution':'Safe School Zones, iRAP school ratings, low speed and education','novelty':'NOT ESTABLISHED'},
    {'candidate':'P03','reference':'Projected Impacts of SURTRAC-Enabled Adaptive Signal Control ... District 1, Ho Chi Minh City (2026)','url':'https://doi.org/10.18280/mmep.130509','read_scope':'publisher full text and Crossref identity','design':'projection/scenario analysis','claim_status':'ILLUSTRATIVE / projected, excluded from empirical benefits and ranking metrics','limitation':'not field intervention evidence; cannot transfer projected savings/crash changes','existing_solution':'adaptive signals already known; GT-16 reports ITS operation','novelty':'NOT ESTABLISHED'},
    {'candidate':'H01/P03','reference':'UIT-ADrone: A Novel Drone Dataset for Traffic Anomaly Detection (2023)','url':'https://doi.org/10.1109/JSTARS.2023.3285905','read_scope':'project metadata, README, binary labels, Crossref identity','design':'curated drone anomaly benchmark','claim_status':'50 mask files measured; ten anomaly types only reported metadata','limitation':'no cargo-specific frequency or crash outcome, enriched scenes','existing_solution':'anomaly detection benchmark, not an intervention evaluation','novelty':'NOT ESTABLISHED'},
    {'candidate':'P01','reference':'FHWA Enhanced Delineation for Horizontal Curves / FHWA-SA-21-035','url':'https://highways.fhwa.dot.gov/safety/proven-safety-countermeasures/enhanced-delineation-horizontal-curves','read_scope':'official web guidance via web tool; not downloaded PDF','design':'guidance linking existing safety evaluations','claim_status':'prior-art context only','limitation':'foreign road context; no Vietnamese effect assumed','existing_solution':'curve signs, markings, delineators, dynamic warnings','novelty':'warning itself is established prior art'},
    {'candidate':'P04','reference':'NASA IMERG metadata and Son La hazard inventory','url':'https://gpm.nasa.gov/data/imerg','read_scope':'official metadata and downloaded hazard tables','design':'products/inventory, no matched event study','claim_status':'no empirical intervention evidence','limitation':'rain-event linkage missing; academic early warning coverage not completed','existing_solution':'remote precipitation products exist; local warning gap unverified','novelty':'NOT ESTABLISHED; review incomplete'}]
    pd.DataFrame(rows).to_csv(ROOT/'reports/prior_art_matrix.csv',index=False,encoding='utf-8-sig')
    write('reports/06_prior_art_vi.md',f'''# Rà soát tài liệu và tính mới

Ngày 19/11/2026. Rà soát **tường thuật có giới hạn**, một người đánh giá, không phải systematic review hay kết luận exhaustive về tính mới. Câu hỏi: bằng chứng nào hỗ trợ cơ chế can thiệp/giới hạn triển khai trong bốn ứng viên, và đã có giải pháp tương tự chưa? Chọn nghiên cứu/nguồn gốc có thiết kế hoặc mô tả vận hành liên quan; loại khỏi kết luận thực nghiệm các mô phỏng/dự phóng, kết quả ngoài Việt Nam không chuyển giao, metadata không có outcome. Không có hạn năm cứng; tìm nguồn gần và lịch sử phù hợp, không diễn giải thứ hạng tìm kiếm như chất lượng.

## Dấu vết tìm kiếm

Crossref 3 truy vấn, 10 kết quả/truy vấn; Europe PMC 1 truy vấn, 20 kết quả trong tổng hitCount 321. Tổng {len(d)} bản ghi API trả về, {d.doi.nunique()} DOI duy nhất trong tập có DOI; đây không là số nghiên cứu đủ điều kiện hoặc đã đọc toàn văn. Không phân trang hết, log ghi complete=False. Tìm mục tiêu bổ sung 4 DOI có JSON riêng và nguồn web gốc. Chi tiết `literature_search_log.csv`, `literature_search_records.csv`; mọi raw JSON có manifest. Screening giới hạn chỉ giữ bài phù hợp để đọc mục tiêu; các bài chưa đọc toàn văn ghi deferred, không gọi là loại vì chất lượng thấp.

Truy vấn web bổ sung Anh/Việt thực chạy: “Vietnam school road safety helmet education intervention randomized trial”; “motorcycle bulky goods road safety Vietnam intervention”; “Vietnam adaptive traffic signals congestion evaluation SCATS”; “Sáng kiến an toàn giao thông chở hàng cồng kềnh giải thưởng 2025”; “site.fhwa.dot.gov enhanced delineation horizontal curves safety evaluation warning signs”; “site.nhess.copernicus.org Vietnam landslide rainfall road warning evaluation”; “site.aip-foundation.org Vietnam school zone slow zones safe zones”; “site.sangkienatgt.dantri.com.vn 2025 Vành đai”. Không có kết quả phù hợp từ một truy vấn không chứng minh lĩnh vực chưa có giải pháp.

## Học sinh: hành vi và hạ tầng cần xem đồng thời

[VERIFIED SOURCE FACT] [Nghiên cứu NCHAP](https://doi.org/10.1136/injuryprev-2017-042517) mô tả 84.218 lượt học sinh qua bốn đợt quan sát tại 100 trường. Tỷ lệ đội mũ được tác giả báo cáo 36,1% trước chiến dịch, 69,3% ngay sau và 56,9% ở đợt cuối. Chỉ đọc abstract nhà xuất bản; chưa tái phân tích raw, không cô lập hiệu quả giáo dục khỏi cưỡng chế/phụ huynh. Đây là bằng chứng lịch sử về hành khách, không baseline xe điện hiện tại.

[VERIFIED SOURCE FACT] [Bài Slow Zones, Safe Zones](https://pmc.ncbi.nlm.nih.gov/articles/PMC12973589/) có bảng tốc độ, khảo sát tai nạn và đánh giá vùng trường. Tác giả thừa nhận thiết kế chuyển sang pre-post diện rộng, đổi thiết bị đo, cửa sổ hồi tưởng và nhiễu COVID. Không dùng tuyên bố nhân quả trong kết luận của tác giả để thay đánh giá thiết kế. Chương trình cùng [hướng dẫn Safe School Zones](https://www.fiafoundation.org/news/global-launch-of-safe-school-zones-guide-vietnam-supported-by-fia-foundation) cho thấy can thiệp vùng trường đã có prior art.

[INTERPRETATION] Khoảng trống khả dĩ là duy trì kỹ năng đúng nhóm/địa bàn và đánh giá có đối chứng, chưa xác nhận nhu cầu hoặc novelty. Giáo dục đơn độc có thể thiếu tác động nếu hạ tầng và thực hành phụ huynh không thay đổi. Chi phí pilot báo trong kế hoạch là giả định riêng, không lấy dự toán hạ tầng của chương trình làm giá địa phương.

## Ùn tắc: đã có ITS; dự phóng không thay thử nghiệm

[VERIFIED SOURCE FACT] [GT-16](https://tphcm.chinhphu.vn/giao-thong-thong-minh-giai-phap-giam-un-tac-va-tai-nan-giao-thong-101221207120448167.htm) mô tả điều khiển thích ứng và VDS. [Bài SURTRAC 2026](https://doi.org/10.18280/mmep.130509) tự xác định là nghiên cứu dự phóng/kịch bản. Không đưa số giảm trễ/tai nạn dự phóng vào bảng kết quả thực hoặc làm bằng chứng E4 tại Việt Nam.

[INTERPRETATION] Prototype mới cần ràng buộc vận hành cụ thể và đo trễ/xe với baseline hiện hành; điều khiển thích ứng tự thân không mới. Rủi ro là luồng xe máy, dữ liệu không đều, quyền truy cập và tăng thời gian chờ của người đi bộ. Đo an toàn phải giữ tách khỏi tối ưu thông xe.

## Đoạn cong và sạt lở

[VERIFIED SOURCE FACT] [FHWA](https://highways.fhwa.dot.gov/safety/proven-safety-countermeasures/enhanced-delineation-horizontal-curves) liệt kê biển/vạch, delineator và cảnh báo động. Đây là prior art cho P01, không là effect size có thể chuyển sang Sơn La. GT-10 tự ghi nhiều thiết bị hiện hữu; phải kiểm tra điều kiện thiếu hụt trước bổ sung.

[NOT VERIFIED] P04 mới chỉ có kiểm kê nguy cơ và metadata IMERG; rà soát học thuật cảnh báo sạt lở tại đúng địa bàn còn thiếu. Không có cơ sở tuyên bố mới hoặc hiệu quả cảnh báo sau mưa. NASA/GT-11 không phải nghiên cứu kiểm chứng dự báo sự kiện.

## Hàng cồng kềnh và sản phẩm có trước

[VERIFIED SOURCE FACT] [UIT-ADrone](https://uit-together.github.io/datasets/UIT-ADrone/) có nhắc loại hành vi này, còn 50 mask tải chỉ mã 0/1. Không đủ suy prevalence hoặc tác hại. Dùng benchmark huấn luyện detector là đóng góp phương pháp khác với chứng minh giải pháp vận tải làm giảm xung đột.

[NOT VERIFIED] Trang [sản phẩm cuộc thi](https://sangkienatgt.dantri.com.vn/san-pham-du-thi) đã truy cập nhưng nội dung đọc được chỉ khung trang. Link bài giải 2025 thử không cung cấp hồ sơ kỹ thuật đủ đối chiếu. Chưa hoàn tất tra sản phẩm startup/bằng sáng chế hoặc mọi bài thi cũ. Novelty của mọi ứng viên: **NOT ESTABLISHED**. Không có nghĩa “chưa thấy” là “chưa tồn tại”.

Ma trận prior art gồm design, giới hạn, nội dung đã đọc: `prior_art_matrix.csv`. Không gộp các báo cáo cùng dự án thành xác nhận độc lập. Các nghiên cứu/metadata ngoài bảng được giữ ở log nhưng không dùng như kết quả đã thẩm định.

## Nguồn quy trình/phần mềm

Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. [arXiv](https://doi.org/10.48550/arXiv.2609.00065). Bản ghi mới nhất đã kiểm tra; trích dẫn cho skill, không hỗ trợ kết luận giao thông.
''')
    print('Literature returned records:',len(d),'unique DOI:',d.doi.nunique())
if __name__=='__main__': main()
