import csv
import tempfile
import unittest
from pathlib import Path
from reconcile import reconcile, read_csv, to_cents

def invoice(v="Supplier", ref="INV-1"):
    return dict(type="invoice", vendor=v, reference=ref, original_invoice=ref, amount="240.00")

def credit(kind, amount, ref, v="Supplier", inv="INV-1"):
    return dict(type=kind, vendor=v, reference=ref, original_invoice=inv, amount=amount)

class Cases(unittest.TestCase):
    def test_missing_partial_credit(self):
        out = reconcile([invoice(), credit("expected_credit","75","RETURN-9"),credit("posted_credit","25","CM-2")])
        self.assertEqual(out[0]["unmatched"],"50.00")
        self.assertEqual(out[0]["status"],"suspected_missing_credit")
    def test_fully_credited(self):
        self.assertEqual(reconcile([credit("expected_credit","5","R1"),credit("posted_credit","5","C1")]),[])
    def test_duplicate_reference(self):
        r=credit("expected_credit","5","R1")
        with self.assertRaises(ValueError): reconcile([r,r])
    def test_negative(self):
        with self.assertRaises(ValueError): reconcile([credit("posted_credit","-2","C1")])
    def test_excess_posted(self):
        out=reconcile([invoice(),credit("expected_credit","25","R"),credit("posted_credit","75","C")])
        self.assertEqual(out[0]["status"],"suspected_excess_credit")
        self.assertEqual(out[0]["difference"],"50.00")
    def test_orphan_invoice(self):
        self.assertEqual(reconcile([credit("expected_credit","75","R")])[0]["status"],"needs_evidence")
    def test_subcent_refused(self):
        with self.assertRaises(ValueError): to_cents("75.004",1)
    def test_thousands(self):
        self.assertEqual(to_cents("1,200.00",1),120000)
    def test_bom_and_malformed_schema(self):
        for raw,expected in [
            ("\ufefftype,vendor,reference,original_invoice,amount\ninvoice,A,I,I,10\n",False),
            ("type,vendor,reference,original_invoice,amount\ninvoice,A,I,I\n",True),
            ("type,vendor,reference,original_invoice\ninvoice,A,I,I\n",True),
            ("type,vendor,reference,original_invoice,amount,\ninvoice,A,I,I,10,surprise\n",True),
            ("type,vendor,reference,original_invoice,amount,amount\ninvoice,A,I,I,10,777\n",True)
        ]:
            with self.subTest(raw=raw[:35]):
                with tempfile.TemporaryDirectory() as tmp:
                    p=Path(tmp)/"x.csv"
                    p.write_text(raw,encoding="utf-8")
                    if expected:
                        with self.assertRaises(ValueError): read_csv(p)
                    else:
                        self.assertEqual(len(read_csv(p)),1)

if __name__=="__main__":
    unittest.main()
