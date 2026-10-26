#!/usr/bin/env python3
"""Read-only small-retail inventory exception report; standard library only."""
import csv, sys, math

FIELDS = ("sku","on_hand","average_daily_units","lead_days","reorder_point","recorded_sales_7d","expected_sales_7d")

def audit(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not set(FIELDS).issubset(reader.fieldnames):
            raise ValueError("Missing required CSV columns")
        for n, row in enumerate(reader, 2):
            sku = (row["sku"] or "").strip()
            if not sku:
                raise ValueError(f"Row {n}: missing sku")
            vals = {}
            for key in FIELDS[1:]:
                value = float(row[key])
                if not math.isfinite(value) or value < 0:
                    raise ValueError(f"Row {n}: {key} must be finite and nonnegative")
                vals[key] = value
            stock, demand = vals["on_hand"], vals["average_daily_units"]
            cover = stock / demand if demand else None
            risks = []
            if cover is None:
                risks.append("ZERO_DEMAND_REVIEW")
            elif cover < vals["lead_days"]:
                risks.append("LEAD_TIME_RISK")
            if stock <= vals["reorder_point"]:
                risks.append("REORDER_THRESHOLD")
            variance = vals["recorded_sales_7d"] - vals["expected_sales_7d"]
            print(f"{sku}: cover={cover:.2f}d" if cover is not None else f"{sku}: cover=N/A", 
                  f"flags={','.join(risks) or 'NONE'} variance_7d={variance:+.2f}")
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 audit.py inventory.csv")
    try:
        audit(sys.argv[1])
    except (ValueError, OSError, KeyError) as e:
        sys.exit(f"Audit failed: {e}")
