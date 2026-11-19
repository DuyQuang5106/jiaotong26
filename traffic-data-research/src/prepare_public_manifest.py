"""Publish provenance fields without exporting HTTP headers, cookies or forms.

The original manifest and raw bytes remain unchanged and local.
"""
import json
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FIELDS = (
    'source_id', 'url', 'final_url', 'download_utc', 'label', 'status', 'path',
    'content_type', 'byte_size', 'sha256', 'period', 'region', 'data_version',
    'license', 'transformation_script', 'original_filename',
)
SENSITIVE_QUERY_KEYS = {
    'token', 'access_token', 'api_key', 'apikey', 'key', 'authorization',
    'password', 'secret', 'email', 'mailto', 'signature', 'x-amz-signature',
}

def public_url(value):
    parts = urlsplit(value)
    if parts.username is not None or parts.password is not None:
        raise ValueError('Do not publish URLs with embedded credentials')
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if k.lower() not in SENSITIVE_QUERY_KEYS]
    return urlunsplit((parts.scheme, parts.netloc, parts.path,
                       urlencode(query), ''))

def main():
    source = ROOT / 'registry/raw_manifest.json'
    original_bytes = source.read_bytes()
    records = json.loads(original_bytes)
    public_records = []
    for record in records:
        public = {key: record[key] for key in PUBLIC_FIELDS if key in record}
        for key in ('url', 'final_url'):
            if key in public:
                public[key] = public_url(public[key])
        public_records.append(public)
    target = ROOT / 'registry/public_raw_manifest.json'
    target.write_text(json.dumps(public_records, ensure_ascii=False, indent=2)
                      + '\n', encoding='utf-8')
    assert source.read_bytes() == original_bytes
    print(f'Public provenance: {len(public_records)} records; original unchanged.')

if __name__ == '__main__':
    main()
