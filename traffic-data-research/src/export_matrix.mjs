import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const records=JSON.parse(await fs.readFile(path.join(root,'reports/evidence_matrix.json'),'utf8'));
const wb=Workbook.create();
const summary=wb.worksheets.add('Xep hang');
const details=wb.worksheets.add('Bang chung');
const first=['problem_id','problem_statement_vi','competition_theme','evidence_strength','observed_metric','metric_value','metric_unit','denominator','source_ids','analysis_file','weighted_score'];
const headers=[...first,...Object.keys(records[0]).filter(k=>!first.includes(k))];
const lastCol=n=>{let s='';for(n++;n>0;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
for(const sheet of [summary,details]){sheet.showGridLines=false;sheet.tabColor='#24415E';}
summary.getRange('A2').values=[['Vấn đề giao thông cần kiểm chứng']];
summary.getRange('A2').format.font={name:'Arial',size:15,bold:true};
summary.getRange('A4:H4').values=[['Mã','Vấn đề','Bằng chứng','Điểm /5','Thấp','Cao','Quyền triển khai','Tính mới']];
summary.getRange(`A5:H${records.length+4}`).values=records.map(r=>[r.problem_id,r.problem_statement_vi,r.evidence_strength,r.weighted_score,r.score_low,r.score_high,r.eligible_for_empirical_deployment,r.novelty_status]);
summary.getRange(`A4:H${records.length+4}`).format.font={name:'Arial',size:11};
summary.getRange(`A5:H${records.length+4}`).format.wrapText=true;
summary.getRange(`A5:H${records.length+4}`).format.rowHeight=65;
summary.getRange(`A5:H${records.length+4}`).format.verticalAlignment='center';
summary.getRange('A:A').format.columnWidth=9;
summary.getRange('B:B').format.columnWidth=70;
summary.getRange('C:F').format.columnWidth=12;
summary.getRange('G:H').format.columnWidth=27;
summary.getRange(`D5:F${records.length+4}`).setNumberFormat('0.00');
summary.getRange('A12').values=[['Điểm do người phân tích đánh giá theo trọng số giao thức; khoảng điểm là kịch bản, không là CI.']];
summary.getRange('A13').values=[['E0 tách khỏi shortlist có bằng chứng. Không ứng viên nào đủ điều kiện triển khai thực địa.']];
summary.getRange('A14').values=[['Nguồn, mẫu số, giới hạn, H0/H1 và baseline nằm trong bảng chi tiết và báo cáo tiếng Việt.']];
details.getRangeByIndexes(0,0,1,headers.length).values=[headers];
details.getRangeByIndexes(1,0,records.length,headers.length).values=records.map(r=>headers.map(h=>r[h]??null));
details.getRangeByIndexes(0,0,records.length+1,headers.length).format.font={name:'Arial',size:11};
details.getRangeByIndexes(0,0,records.length+1,headers.length).format.columnWidth=32;
details.getRangeByIndexes(1,0,records.length,headers.length).format.rowHeight=160;
details.getRangeByIndexes(0,0,records.length+1,headers.length).format.wrapText=true;
details.getRangeByIndexes(0,0,records.length+1,headers.length).format.verticalAlignment='center';
details.getRangeByIndexes(0,0,1,headers.length).format.rowHeight=45;
details.getRange('A:A').format.columnWidth=14;
details.getRange('B:B').format.columnWidth=70;
for(const [sheet,range] of [[summary,'A4:H4'],[details,`A1:${lastCol(headers.length-1)}1`]]){
 sheet.getRange(range).format.fill='#24415E';sheet.getRange(range).format.font={name:'Arial',size:11,bold:true,color:'#FFFFFF'};
 sheet.freezePanes.freezeRows(sheet===summary?4:1);
}
wb.recalculate();
const inspect=await wb.inspect({kind:'table',range:'Xep hang!A4:H9',include:'values,formulas',tableMaxRows:6,tableMaxCols:8,maxChars:4000});
await fs.writeFile(path.join(root,'quality/xlsx_inspect.jsonl'),inspect.ndjson);
for(const [name,range,file] of [['Xep hang','A2:H14','matrix_summary_preview.png'],['Bang chung','A1:E6','matrix_evidence_preview.png']]){
 try{const png=await wb.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(path.join(root,'quality',file),new Uint8Array(await png.arrayBuffer()));}catch(e){await fs.writeFile(path.join(root,'quality',file+'.error.txt'),String(e));}
}
const output=await SpreadsheetFile.exportXlsx(wb);await output.save(path.join(root,'reports/03_problem_evidence_matrix.xlsx'));
console.log('Exported matrix workbook with',records.length,'records,',headers.length,'fields.');
