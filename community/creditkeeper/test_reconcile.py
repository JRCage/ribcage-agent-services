import unittest
from reconcile import reconcile

class Cases(unittest.TestCase):
    def test_missing_partial_credit(self):
        rows=[dict(type="expected_credit",vendor="Supplier",reference="RETURN-9",original_invoice="INV-1",amount="75"),
              dict(type="posted_credit",vendor="Supplier",reference="CM-2",original_invoice="INV-1",amount="25")]
        x=reconcile(rows)
        self.assertEqual(x[0]["unmatched"],"50")
        self.assertEqual(x[0]["status"],"suspected_missing_credit")
    def test_fully_credited(self):
        rows=[dict(type="expected_credit",vendor="A",reference="R1",original_invoice="I1",amount="5"),
              dict(type="posted_credit",vendor="A",reference="C1",original_invoice="I1",amount="5")]
        self.assertEqual(reconcile(rows),[])
    def test_reject_duplicate_reference(self):
        r=dict(type="expected_credit",vendor="A",reference="R1",original_invoice="I1",amount="5")
        with self.assertRaises(ValueError): reconcile([r,r])
    def test_reject_negative(self):
        with self.assertRaises(ValueError):
            reconcile([dict(type="posted_credit",vendor="A",reference="X",original_invoice="Y",amount="-2")])
if __name__=="__main__": unittest.main()
