"""One-command offline reproduction from preserved raw snapshots."""
import subprocess,sys,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for name in ['ingest','eda','extended_analysis','supplemental_analysis','triangulation','quality','build_registry','build_evidence_matrix','write_reports','literature_report']:
    subprocess.run([sys.executable,str(root/'src'/(name+'.py'))],check=True,cwd=root)
if (root.parent/'data/traffic_contest_ideas_2022_2025.xlsx').exists():
    subprocess.run([sys.executable,str(root/'src/discover_opportunities.py')],check=True,cwd=root)
with (root/'tests/test_results.txt').open('w',encoding='utf-8') as f:
    result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=root,stdout=f,stderr=subprocess.STDOUT)
print('Tests exit:',result.returncode)
if result.returncode==0 and shutil.which('node') and (root/'node_modules/@oai/artifact-tool').exists():
    subprocess.run(['node',str(root/'src/export_matrix.mjs')],check=True,cwd=root)
elif result.returncode==0:
    print('XLSX regeneration unavailable: Node/artifact-tool missing; CSV/JSON regenerated.')
if result.returncode==0 and (root/'reports/03_problem_evidence_matrix.xlsx').exists():
    subprocess.run([sys.executable,str(root/'src/finalize.py')],check=True,cwd=root)
sys.exit(result.returncode)
