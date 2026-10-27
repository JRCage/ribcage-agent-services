"""Strict, read-only reconciliation of synthetic invoice and credit rows."""
import csv
import json
import re
import sys
from collections import defaultdict

REQUIRED = ("type", "vendor", "reference", "original_invoice", "amount")
ALLOWED = set(REQUIRED) | {"note"}
KINDS = {"invoice", "expected_credit", "posted_credit"}

def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        headers = next(reader, None)
        if headers is None:
            return []
        fields = [h.strip() for h in headers]
        missing = set(REQUIRED) - set(fields)
        if missing:
            raise ValueError("missing required columns: " + ", ".join(sorted(missing)))
        named = [x for x in fields if x]
        if len(named) != len(set(named)):
            raise ValueError("duplicate header")
        unexpected = set(named) - ALLOWED
        if unexpected:
            raise ValueError("unexpected columns: " + ", ".join(sorted(unexpected)))
        rows = []
        for line, cells in enumerate(reader, 2):
            if len(cells) > len(fields):
                raise ValueError(f"line {line}: extra field")
            cells += [""] * (len(fields) - len(cells))
            if any(c.strip() for c, h in zip(cells, fields) if not h):
                raise ValueError(f"line {line}: data in unnamed column")
            row = dict(zip(fields, cells))
            if not any(str(v).strip() for v in row.values()):
                continue
            if any(not row.get(key, "").strip() for key in ("type", "vendor", "reference", "amount")):
                raise ValueError(f"line {line}: missing mandatory value")
            rows.append(row)
        return rows

def to_cents(raw, row_number):
    value = str(raw).strip()
    # Bound input before Decimal conversion; reject exponent/underscore syntax
    # and separators outside conventional thousands groups.
    if not re.fullmatch(r"(?:[0-9]{1,12}|[0-9]{1,3}(?:,[0-9]{3}){1,3})(?:\.[0-9]{1,2})?", value):
        raise ValueError(f"row {row_number}: invalid amount; use positive dollars and cents")
    whole, _, fraction = value.replace(",", "").partition(".")
    cents = int(whole) * 100 + int((fraction + "00")[:2])
    if cents <= 0:
        raise ValueError(f"row {row_number}: amount must be positive")
    return cents

def money(cents):
    return f"{cents // 100}.{cents % 100:02d}"


def reconcile(rows):
    entries = defaultdict(lambda: {"expected": 0, "posted": 0, "refs": []})
    invoices = set()
    seen = set()
    for i, row in enumerate(rows, 1):
        if any(key not in row or row[key] is None for key in REQUIRED):
            raise ValueError(f"row {i}: required field missing")
        kind = str(row["type"]).strip().lower()
        vendor = str(row["vendor"]).strip().casefold()
        reference = str(row["reference"]).strip().casefold()
        original = str(row["original_invoice"]).strip().casefold()
        if kind not in KINDS or not vendor or not reference:
            raise ValueError(f"row {i}: invalid type, vendor or reference")
        amount = to_cents(row["amount"], i)
        key = (kind, vendor, reference)
        if key in seen:
            raise ValueError(f"row {i}: duplicate reference")
        seen.add(key)
        if kind == "invoice":
            invoices.add((vendor, reference))
            continue
        if not original:
            raise ValueError(f"row {i}: credit requires original_invoice")
        rec = entries[(vendor, original)]
        rec["expected" if kind == "expected_credit" else "posted"] += amount
        rec["refs"].append(reference)
    out = []
    for (vendor, original), rec in sorted(entries.items()):
        delta = rec["expected"] - rec["posted"]
        linked = (vendor, original) in invoices
        if not delta and linked:
            continue
        status = ("suspected_missing_credit" if delta > 0 else "suspected_excess_credit") if linked else "needs_evidence"
        out.append({"vendor": vendor, "invoice": original,
                    "expected": money(rec["expected"]),
                    "posted": money(rec["posted"]),
                    "difference": money(abs(delta)),
                    "unmatched": money(delta) if delta > 0 else "0.00",
                    "status": status, "invoice_present": linked,
                    "references": rec["refs"]})
    return out

def main(args):
    if len(args) != 2:
        print("Usage: python reconcile.py FILE.csv", file=sys.stderr)
        return 2
    try:
        result = reconcile(read_csv(args[1]))
    except (ValueError, OSError, csv.Error) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

