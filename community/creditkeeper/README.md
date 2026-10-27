# CreditKeeper — local proof of concept
**Internal prototype. Not customer-ready.** Reconcile *expected* supplier credits against posted credits, with deterministic arithmetic and no AI guesswork. A missing credit is **suspected**, not verified or recovered.

```sh
cd community/creditkeeper
python -m unittest discover -v
python reconcile.py sample.csv
```

CSV fields: type,vendor,reference,original_invoice,amount,note. Type = invoice, expected_credit, posted_credit. Reference unique by vendor and type. Expected credits must be based on independent documentary evidence (return receipt, accepted warranty claim, written credit promise). CSV rows are **trusted test inputs only**; actual intake would require tenant isolation, validation, permissions, retention and provenance.
Do not upload invoices containing sensitive information to public GitHub. No production customer upload endpoint exists.

## Printable exception report

Run `python report.py sample.csv > report.html` and open the local HTML file. This produces a readable evidence-reference table with next verification steps, including explicit excess-credit and missing-invoice statuses. It does not claim confirmed recovery. The report escapes input markup, excludes notes, uses no scripts or external resources, and prints without dependencies. Confirm a single currency and statement period before interpreting amounts; neither is encoded in this prototype. Output inherits the confidentiality and retention requirements of the input. Use a new output filename: shell redirection overwrites an existing file.

Validation on October 27, 2026: 23 Python tests and 11 demo behavior/static privacy cases passed locally. The synthetic sample still reports exactly 50.00 suspected missing credit. The report adds six regression tests, including markup escaping, note omission, excess credit and balanced orphan evidence. Independent review, configured private intake/delivery, and approved payment remain required before real customer use. Visual browser/print QA remains to be performed.
