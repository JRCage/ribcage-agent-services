"""ReceiptMatch: offline invoice/payment export reconciliation. No on-chain verification."""
import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation

def amount(value):
    try:
        v = Decimal(str(value))
    except (TypeError, InvalidOperation, ValueError) as exc:
        raise ValueError("invalid amount") from exc
    if not v.is_finite() or v < 0:
        raise ValueError("amount must be finite and nonnegative")
    return v

def reconcile(invoices, payments):
    expected, received, exceptions = {}, defaultdict(lambda: Decimal(0)), []
    for inv in invoices:
        iid = (inv.get("invoice_id") or "").strip()
        if not iid or iid in expected:
            exceptions.append({"type": "invalid_or_duplicate_invoice", "invoice_id": iid})
            continue
        try:
            val = amount(inv["amount"])
            assert val > 0
            assert inv["asset"] and inv["address"]
        except (ValueError, KeyError, AssertionError):
            exceptions.append({"type": "invalid_invoice", "invoice_id": iid})
            continue
        expected[iid] = (inv["asset"], inv["address"], val)
    signatures = set()
    for p in payments:
        sig = (p.get("signature") or "").strip()
        if not sig or sig in signatures:
            exceptions.append({"type": "missing_or_duplicate_signature", "signature": sig})
            continue
        signatures.add(sig)
        iid = (p.get("invoice_id") or "").strip()
        if iid not in expected:
            exceptions.append({"type": "unknown_invoice", "signature": sig})
            continue
        asset, address, _ = expected[iid]
        if p.get("asset") != asset or p.get("address") != address:
            exceptions.append({"type": "asset_or_recipient_mismatch", "signature": sig})
            continue
        try:
            received[iid] += amount(p["amount"])
        except (ValueError, KeyError):
            exceptions.append({"type": "invalid_payment", "signature": sig})
    results = []
    for iid, (asset, _, due) in expected.items():
        paid = received[iid]
        status = "unpaid" if paid == 0 else "partial" if paid < due else "overpaid" if paid > due else "paid"
        results.append({"invoice_id": iid, "asset": asset, "expected": str(due),
                        "received": str(paid), "outstanding": str(max(Decimal(0), due-paid)), "status": status})
    return {"invoices": results, "exceptions": exceptions, "verified_on_chain": False}

def load(path, columns):
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        if not r.fieldnames or not set(columns).issubset(r.fieldnames):
            raise ValueError("missing columns: " + ", ".join(columns))
        return list(r)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("invoices")
    p.add_argument("payments")
    args = p.parse_args()
    print(json.dumps(reconcile(load(args.invoices, ["invoice_id","asset","address","amount"]),
                               load(args.payments, ["signature","invoice_id","asset","address","amount"])), indent=2))
