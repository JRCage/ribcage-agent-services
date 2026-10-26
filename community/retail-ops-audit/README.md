# Small-Retail Exception Audit (pilot)

A read-only, CSV-based audit for independent gas stations, convenience shops, laundromats, and small retailers. It detects potential stockouts, stale reorder points, and unusual shrink without connecting to a point-of-sale system or touching payments.

**Status:** free pilot prototype. Not a production inventory management system or a loss-prevention accusation. No customer data is collected.

## Run

```bash
python3 audit.py example.csv
```

CSV columns: `sku,on_hand,average_daily_units,lead_days,reorder_point,recorded_sales_7d,expected_sales_7d`. All quantities are nonnegative; no names, card numbers, or transaction-level data.

## Logic and caveats

- Days of cover = on_hand / average_daily_units; if demand is zero, flag for human review rather than dividing.
- Lead-time risk = days of cover below lead_days.
- Reorder risk = on_hand at or below reorder_point.
- Variance = recorded_sales_7d - expected_sales_7d; values are informational, never proof of theft or shrink. If the source records measure different periods or units, the metric is invalid.
- Results must be checked by the owner; seasonality, fuel delivery disruptions, vendor minimums, promotions, and data entry errors matter.

## Commercial pilot proposal

Offer one no-cost audit **per company** after verifying the business, then quote paid recurring exception monitoring only if the pilot uncovers useful, verifiable savings. Avoid claiming savings or automatic purchasing before measurement. A pilot win requires a documented action, owner-approved baseline, and a 30-day follow-up; track false positive rate and hours saved as well as revenue. Do not upload sensitive POS exports to a public repository.
