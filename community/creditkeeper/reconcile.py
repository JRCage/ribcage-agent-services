"""Read-only, deterministic vendor credit reconciliation prototype.
Input rows: type, vendor, reference, original_invoice, amount, note.
Types: invoice, expected_credit, posted_credit. Amounts are positive decimals.
No customer PII, no network calls, no automatic recovery claims.
"""
import csv,sys,json
from decimal import Decimal,InvalidOperation
from collections import defaultdict

def reconcile(rows):
    entries=defaultdict(lambda: {"expected":Decimal("0"),"posted":Decimal("0"),"receipts":[]})
    seen=set()
    for i,r in enumerate(rows,1):
        kind=r["type"].strip().lower()
        if kind not in {"invoice","expected_credit","posted_credit"}:
            raise ValueError(f"row {i}: unsupported type")
        vendor=r["vendor"].strip().casefold()
        invoice=r["original_invoice"].strip().casefold()
        ref=r["reference"].strip()
        if not vendor or not ref: raise ValueError(f"row {i}: vendor and reference required")
        try: amount=Decimal(r["amount"])
        except InvalidOperation: raise ValueError(f"row {i}: invalid amount")
        if not amount.is_finite() or amount<=0: raise ValueError(f"row {i}: amount must be positive finite")
        key=(kind,vendor,ref.casefold())
        if key in seen: raise ValueError(f"row {i}: duplicate reference within type and vendor")
        seen.add(key)
        if kind=="invoice": continue
        if not invoice: raise ValueError(f"row {i}: original_invoice required for credits")
        target=entries[(vendor,invoice)]
        target["expected" if kind=="expected_credit" else "posted"]+=amount
        target["receipts"].append(ref)
    out=[]
    for (vendor,invoice),rec in sorted(entries.items()):
        remaining=rec["expected"]-rec["posted"]
        if remaining>0:
            out.append({"vendor":vendor,"invoice":invoice,"expected":str(rec["expected"]),
                        "posted":str(rec["posted"]),"unmatched":str(remaining),
                        "status":"suspected_missing_credit","references":rec["receipts"]})
    return out

if __name__=="__main__":
    with open(sys.argv[1],newline="",encoding="utf-8") as f:
        print(json.dumps(reconcile(csv.DictReader(f)),indent=2))
