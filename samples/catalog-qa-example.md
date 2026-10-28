# Catalog CSV review: sample deliverable

**Fictional demonstration — no customer data, sales or recovered revenue.**

For an agency preparing a small product import, this is what a structural review can make visible before a store change. The input is the [four-row sample](../community/catalog-qa/sample.csv); the [offline checker](../community/catalog-qa/README.md) makes no store changes.

## Findings you can act on

| CSV row (header is row 1) | Finding | Decision needed before repair |
|---|---|---|
| 3 | `LINEN-S` repeats the SKU on row 2, despite a different size option | Confirm whether the shared SKU is intentional. Do not invent a replacement identifier. |
| 4 | `$24.00` is not a plain decimal | Confirm the file's currency and the target format before changing it to `24.00`. |
| 5 | SKU and variant ID are both blank | Obtain an approved identifier mapping. Do not fabricate a store variant ID. |

The checker reports **4 exceptions across 4 product rows**: the last row produces separate missing-SKU and missing-identifier findings. Four exceptions do not mean four products are broken. Duplicate SKUs can be intentional.

## What the work product includes

A scoped engagement can deliver a source-row exceptions table, a list of decisions requiring your approval, and a validation summary. The existing [data-repair offer starts at $49](../SERVICES-AND-PRICING.md): one CSV or JSON input, up to five agreed transformation rules and one output format. A corrected file follows approved rules only; ambiguous product relationships remain flagged. The sample checker accepts up to 100 data rows and 1 MB, so larger jobs need a separately agreed process and scope.

This does not establish inventory accuracy, platform import acceptance, taxes, product parentage, or migration success. No credentials, live store access or customer records are needed to discuss fit.

## Request a scope check

Use the repository's **Issues → New issue**, title it `Service inquiry: Catalog CSV review`, and include only:

- Intended output and deadline.
- Approximate row count and column names.
- A fictional example of the problem and your desired acceptance rule.

Do not attach an actual customer export or confidential identifiers. A private intake/delivery route and payment arrangements must be confirmed before any paid work or real customer files. This example is available now; it is not an active checkout or authorization to collect a payment.

## Reproduce the example

From the repository root:

```sh
python community/catalog-qa/catalog_qa.py community/catalog-qa/sample.csv
```

Expected result: `rows_checked: 4`, `exception_count: 4`, with `duplicate_sku` at row 3, `invalid_price_format` at row 4, and `missing_sku` plus `missing_variant_identifier` at row 5. Checked October 28, 2026.
