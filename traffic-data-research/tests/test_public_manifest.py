"""Publication checks independent of the private raw snapshot."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from prepare_public_manifest import PUBLIC_FIELDS, public_url

class PublicManifestTests(unittest.TestCase):
    def test_removes_sensitive_query_and_fragment(self):
        result = public_url('https://example.org/data?id=42&api_key=private#session')
        self.assertEqual(result, 'https://example.org/data?id=42')

    def test_rejects_embedded_credentials(self):
        with self.assertRaises(ValueError):
            public_url('https://user:private@example.org/data')

    def test_excludes_headers_and_form_state(self):
        for field in ('headers', 'request_form', 'cookie', 'authorization'):
            self.assertNotIn(field, PUBLIC_FIELDS)

if __name__ == '__main__':
    unittest.main()
