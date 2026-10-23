"""Regression tests for the published standalone tools, using only Python stdlib."""
import unittest
from launchcheck import inspect
from receiptmatch import reconcile
from tokenunits import to_raw, from_raw

class ToolkitTests(unittest.TestCase):
    def test_units_usdc(self):
        self.assertEqual(to_raw("1.000001", 6), 1000001)
        self.assertEqual(from_raw(1000001, 6), "1.000001")
    def test_units_reject_fractional_base_unit(self):
        with self.assertRaises(ValueError): to_raw("0.0000001", 6)
    def test_units_reject_nan(self):
        with self.assertRaises(ValueError): to_raw("NaN", 6)
    def test_units_reject_negative(self):
        with self.assertRaises(ValueError): to_raw("-1", 6)
    def test_receipt_paid(self):
        invoices = [{"invoice_id":"a","asset":"USDC","address":"safe","amount":"1.50"}]
        payments = [{"signature":"s1","invoice_id":"a","asset":"USDC","address":"safe","amount":"1.50"}]
        self.assertEqual(reconcile(invoices, payments)["invoices"][0]["status"], "paid")
    def test_receipt_blocks_duplicate_signature(self):
        invoices = [{"invoice_id":"a","asset":"USDC","address":"safe","amount":"1.50"}]
        p = {"signature":"s1","invoice_id":"a","asset":"USDC","address":"safe","amount":"1.50"}
        r = reconcile(invoices, [p,p])
        self.assertEqual(r["invoices"][0]["received"], "1.50")
        self.assertEqual(r["exceptions"][0]["type"], "missing_or_duplicate_signature")
    def test_receipt_wrong_address(self):
        invoices = [{"invoice_id":"a","asset":"USDC","address":"safe","amount":"1.50"}]
        p = {"signature":"s1","invoice_id":"a","asset":"USDC","address":"wrong","amount":"1.50"}
        self.assertEqual(reconcile(invoices,[p])["invoices"][0]["status"], "unpaid")
    def test_launch_bad_supply(self):
        c = {"supply":0,"decimals":6,"mint_authority":"revoked","freeze_authority":"revoked",
             "allocations":[{"name":"all","percent":100}],"public_disclosures_url":"https://example.com"}
        self.assertFalse(inspect(c)["ok"])
    def test_launch_retained_authority_warning(self):
        c = {"supply":10,"decimals":6,"mint_authority":"retained","freeze_authority":"revoked",
             "allocations":[{"name":"all","percent":100}],"public_disclosures_url":"https://example.com"}
        self.assertTrue(inspect(c)["ok"])
        self.assertIn("AUTHORITY_RETAINED", [i["code"] for i in inspect(c)["issues"]])

if __name__ == "__main__": unittest.main()
