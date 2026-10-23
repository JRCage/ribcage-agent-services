import unittest
from contact_watch import extract, compare, compare_authorized_snapshots, safe_url, run_business

class ContactWatchTests(unittest.TestCase):
    def test_extract(self):
        self.assertEqual(extract('<a href="tel:+1 555 555 0100">Call</a><address>12 Example Ave<br>Dallas</address>'), {'phones':['+1 555 555 0100'], 'addresses':['12 Example Ave Dallas']})
    def test_change_flags_review(self):
        x=compare({'phones':['1111111111'],'addresses':[]},{'phones':['2222222222'],'addresses':[]},'clinic1','https://clinic.example.org/contact')
        self.assertEqual(x[0]['action'],'REVIEW_BY_PERSON')
        self.assertEqual(x[0]['field'],'phones')
    def test_same_no_alert(self):
        self.assertEqual(compare({'phones':[],'addresses':[]},{'phones':[],'addresses':[]},'a','https://example.org'),[])
    def test_private_url_rejected(self):
        for u in ('http://example.org','https://localhost/a','https://127.0.0.1/','https://a.example.org:8443/','https://admin:pass@example.org/'):
            with self.assertRaises(ValueError): safe_url(u)
    def test_patient_only_local(self):
        r=compare_authorized_snapshots([{'id':'p1','phone':'111'}],[{'id':'p1','phone':'222'}])
        self.assertEqual(r['reviews'][0]['ehr_updated'], False)
    def test_patient_duplicate_reject(self):
        with self.assertRaises(ValueError):compare_authorized_snapshots([{'id':'x'},{'id':'x'}],[])
    def test_first_business_run_baseline(self):
        r, state=run_business({'organizations':[{'id':'a','public_contact_url':'https://example.org'}]}, {}, lambda _: {'phones':['1234567890'],'addresses':[]})
        self.assertEqual(r['reviews'],[])
        self.assertEqual(state['a']['phones'],['1234567890'])
    def test_second_business_run_review(self):
        r,_=run_business({'organizations':[{'id':'a','public_contact_url':'https://example.org'}]}, {'a':{'phones':['1234567890'],'addresses':[]}}, lambda _: {'phones':['2345678901'],'addresses':[]})
        self.assertEqual(len(r['reviews']),1)
    def test_patient_not_crawled(self):
        with self.assertRaises(ValueError):run_business({'organizations':[{'id':'patient:123','kind':'patient'}]}, {}, lambda _: None)

if __name__=='__main__':unittest.main()
