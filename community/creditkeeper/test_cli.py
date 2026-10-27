"""Black-box checks of the published CLI using synthetic input only."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HEADER = 'type,vendor,reference,original_invoice,amount,note\n'
INVOICE = 'invoice,A,I,I,240,Synthetic\n'

class CommandLineCases(unittest.TestCase):
    def run_csv(self, raw, code=0):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'synthetic.csv'
            path.write_text(raw, encoding='utf-8')
            result = subprocess.run([sys.executable, 'reconcile.py', str(path)],
                                    text=True, capture_output=True, timeout=3)
            self.assertEqual(path.read_text(encoding='utf-8'), raw)
        self.assertEqual(result.returncode, code, result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        if code:
            self.assertEqual(result.stdout, '')
            self.assertTrue(result.stderr.startswith('Input error:'))
            return None
        self.assertEqual(result.stderr, '')
        return json.loads(result.stdout)

    def test_original_adversarial_cases(self):
        cases = [
          ('BOM', '\ufeff'+HEADER+INVOICE, 0),
          ('ragged', HEADER+'invoice,A,I,I\n', 2),
          ('missing amount', 'type,vendor,reference,original_invoice\ninvoice,A,I,I\n', 2),
          ('unnamed populated', HEADER.rstrip('\n')+',\ninvoice,A,I,I,10,,lost\n', 2),
          ('duplicate header', HEADER.rstrip('\n')+',amount\ninvoice,A,I,I,10,,777\n', 2),
          ('subcent', HEADER+INVOICE+'expected_credit,A,R,I,75.004,Synthetic\n', 2),
          ('thousands', HEADER+'invoice,A,I,I,"1,200.00",Synthetic\n', 0),
          ('empty', '', 0),
          ('header only', HEADER, 0),
        ]
        for name, raw, code in cases:
            with self.subTest(name=name): self.run_csv(raw, code)

    def test_excess_and_orphan(self):
        credits = 'expected_credit,A,R,I,25,Synthetic\nposted_credit,A,C,I,75,Synthetic\n'
        row = self.run_csv(HEADER+INVOICE+credits)[0]
        self.assertEqual((row['status'],row['difference']), ('suspected_excess_credit','50.00'))
        row = self.run_csv(HEADER+credits)[0]
        self.assertEqual(row['status'], 'needs_evidence')

    def test_no_argument(self):
        result=subprocess.run([sys.executable,'reconcile.py'],capture_output=True,text=True,timeout=3)
        self.assertEqual(result.returncode,2)
        self.assertEqual(result.stdout,'')
        self.assertEqual(result.stderr,'Usage: python reconcile.py FILE.csv\n')

    def test_sample_exact_result(self):
        result=subprocess.run([sys.executable,'reconcile.py','sample.csv'],capture_output=True,text=True,timeout=3)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout),[{
            'vendor':'example supply','invoice':'inv-100','expected':'75.00',
            'posted':'25.00','difference':'50.00','unmatched':'50.00',
            'status':'suspected_missing_credit','invoice_present':True,
            'references':['return-1','cm-100']}])
