import unittest,datetime
from audit import audit
BASE={'invoice_id':'I1','customer':'Acme','issued_date':'2026-09-01','due_date':'2026-09-30','amount':'100','paid_amount':'0','status':'sent'}
class AuditTests(unittest.TestCase):
 def test_overdue(self):
  _,flags,_=audit([BASE],datetime.date(2026,10,22));self.assertEqual([f['code'] for f in flags],['past_due_balance'])
 def test_duplicate(self):
  _,flags,_=audit([BASE,BASE],datetime.date(2026,9,2));self.assertIn('duplicate_invoice_id',[f['code'] for f in flags])
 def test_paid_mismatch(self):
  _,flags,_=audit([{**BASE,'status':'paid','paid_amount':'10'}],datetime.date(2026,9,2));self.assertIn('paid_status_with_balance',[f['code'] for f in flags])
 def test_invalid_amount(self):
  _,flags,_=audit([{**BASE,'amount':'NaN'}],datetime.date(2026,9,2));self.assertIn('invalid_amount',[f['code'] for f in flags])
if __name__=='__main__':unittest.main()
