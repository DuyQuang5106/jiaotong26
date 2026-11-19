"""Audit the Git index for local-only artifacts and credential-shaped values."""
import json
import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_PARTS = {'node_modules', '.skill-sources', '__pycache__'}
FORBIDDEN_SUFFIXES = {'.mp4', '.avi', '.zip', '.pbf', '.npy', '.pem', '.key'}
PATTERNS = [
    re.compile(rb'gh[pousr]_[A-Za-z0-9]{30,}'),
    re.compile(rb'github_pat_[A-Za-z0-9_]{30,}'),
    re.compile(rb'AKIA[A-Z0-9]{16}'),
    re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(rb'"Set-Cookie"\s*:\s*"[^"\r\n]+'),
]

def main():
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf-8').split('\0')
    paths = [p for p in paths if p]
    failures = []
    total = 0
    input_manifest = ROOT / 'traffic-data-research/registry/input_manifest.json'
    expected_inputs = {}
    if input_manifest.exists():
        for entry in json.loads(input_manifest.read_text(encoding='utf-8')):
            name = 'traffic-data-research/' + entry['path'].replace('\\', '/')
            expected_inputs[name] = entry['sha256']
    for name in paths:
        path = Path(name)
        if (FORBIDDEN_PARTS.intersection(path.parts) or path.suffix.lower() in FORBIDDEN_SUFFIXES
                or '/data/raw/' in '/' + name or '/data/interim/' in '/' + name
                or path.name in {'http_events.jsonl', 'raw_manifest.json'}
                or path.name == '.env' or path.name.startswith('.env.')):
            failures.append((name, 'local-only artifact'))
        mode = subprocess.check_output(['git', 'ls-files', '-s', '--', name], cwd=ROOT).split()[0]
        if mode == b'120000':
            failures.append((name, 'symlink'))
        content = subprocess.check_output(['git', 'show', ':' + name], cwd=ROOT)
        total += len(content)
        if name in expected_inputs and hashlib.sha256(content).hexdigest() != expected_inputs[name]:
            failures.append((name, 'indexed input bytes differ from authoritative checksum'))
        if len(content) > 10_000_000:
            failures.append((name, 'file exceeds publication limit of 10 MB'))
        if path.suffix.lower() not in {'.xlsx', '.png'} and any(p.search(content) for p in PATTERNS):
            failures.append((name, 'credential-shaped content; value not printed'))
    print(json.dumps({'indexed_files': len(paths), 'bytes': total, 'failures': failures}))
    if failures:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
