import tempfile
import unittest
from pathlib import Path
from catalog_qa import analyze, InputError

HEADER = 'Handle,Variant SKU,Variant Price,Option1 Name,Option1 Value,Variant ID\n'

class CatalogQATests(unittest.TestCase):
    def check(self, content):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'sample.csv'
            p.write_text(content, encoding='utf-8')
            return analyze(p)

    def test_clean(self):
        r = self.check(HEADER+'shirt,S1,12.00,Size,S,101\nshirt,S2,12.00,Size,M,102\n')
        self.assertEqual(r['exception_count'], 0)
    def test_duplicate_sku(self):
        r = self.check(HEADER+'shirt,S1,12.00,Size,S,101\nshirt,S1,12.00,Size,M,102\n')
        self.assertIn('duplicate_sku', [x['code'] for x in r['exceptions']])
    def test_duplicate_option_mapping(self):
        r = self.check(HEADER+'shirt,S1,12.00,Size,S,101\nshirt,S2,12.00,Size,S,102\n')
        self.assertIn('duplicate_variant_mapping', [x['code'] for x in r['exceptions']])
    def test_missing_identifiers(self):
        r = self.check(HEADER+', ,12.00,,,\n')
        self.assertIn('missing_variant_identifier', [x['code'] for x in r['exceptions']])
    def test_bad_price(self):
        r = self.check(HEADER+'shirt,S1,"1,200.00",Size,S,101\n')
        self.assertIn('invalid_price_format', [x['code'] for x in r['exceptions']])
    def test_incomplete_option(self):
        r = self.check(HEADER+'shirt,S1,12.00,,S,101\n')
        self.assertIn('incomplete_variant_option', [x['code'] for x in r['exceptions']])
    def test_bom(self):
        self.assertEqual(self.check('\ufeff'+HEADER+'shirt,S1,12.00,Size,S,101\n')['rows_checked'], 1)
    def test_duplicate_header_rejected(self):
        with self.assertRaisesRegex(InputError, 'Duplicate'):
            self.check('Handle,Variant SKU,Variant SKU,Variant Price\nshirt,A,B,12.00\n')
    def test_ragged_rejected(self):
        with self.assertRaisesRegex(InputError, 'expected'):
            self.check(HEADER+'shirt,S1,12.00\n')
    def test_populated_unnamed_column_rejected(self):
        with self.assertRaisesRegex(InputError, 'unnamed'):
            self.check('Handle,Variant SKU,Variant Price,\nshirt,S1,12.00,secret\n')
    def test_too_many_rows(self):
        with self.assertRaisesRegex(InputError, 'More than 100'):
            self.check(HEADER+('shirt,S1,12.00,Size,S,101\n'*101))
    def test_missing_required_header(self):
        with self.assertRaisesRegex(InputError, 'Required'):
            self.check('Handle,Variant SKU\nshirt,S1\n')

if __name__ == '__main__':
    unittest.main()
