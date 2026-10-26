# CreditKeeper — local proof of concept
**Internal prototype. Not customer-ready.** Reconcile *expected* supplier credits against posted credits, with deterministic arithmetic and no AI guesswork. A missing credit is **suspected**, not verified or recovered.

```sh
cd community/creditkeeper
python -m unittest discover -v
python reconcile.py sample.csv
```

CSV fields: type,vendor,reference,original_invoice,amount,note. Type = invoice, expected_credit, posted_credit. Reference unique by vendor and type. Expected credits must be based on independent documentary evidence (return receipt, accepted warranty claim, written credit promise). CSV rows are **trusted test inputs only**; actual intake would require tenant isolation, validation, permissions, retention and provenance.
Do not upload invoices containing sensitive information to public GitHub. No production customer upload endpoint exists.