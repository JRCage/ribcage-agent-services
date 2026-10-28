# Catalog QA — synthetic-only, offline preflight

A dependency-free, read-only CSV structural preflight supporting **Ribcage Agent Services' proposed small catalog QA offer**. This is a local proof of capability, **not a public upload service, paid checkout, Shopify integration, or verified migration audit**.

Run from this directory:

```sh
python catalog_qa.py sample.csv
python -m unittest discover -p 'test_*.py' -v
```

The example is fictional. Output is JSON containing source row numbers and deterministic exceptions. The tool checks duplicate SKUs/variant IDs, missing identifiers, plain-decimal price format, incomplete option name/value pairs, and duplicate product/option combinations. It accepts common Shopify CSV aliases (`Handle`, `Variant SKU`, `Variant Price`, `Option1 Name`, `Option1 Value`) and simple generic aliases. A schema mismatch, duplicate header, populated unnamed column, ragged row, more than 100 data rows, or input over 1 MB is rejected rather than silently ignored.

**Limits:** This cannot prove actual store inventory, tax handling, conversion quality, variant parentage, platform rules, or that a migration succeeded. It does not repair files or modify stores. It does not compare pre/post exports. A written exceptions report is a human-reviewed separate deliverable, not the JSON alone. False positives are possible (some catalogs legitimately share SKU values). Do not describe a clean result as a certification.

**Privacy and commercial gate:** Only run on fictional or explicitly authorized non-sensitive samples until the business has an approved private intake, retention/deletion, delivery, payment and independent QA process. Never send customer exports through public GitHub, email, or this repository. The proposed $2.99/$4.99 impulse-buy prices are **not yet authorized for collection or publication** and must be checked against actual fulfillment costs. This code does not collect or transmit any data; it only reads the local file and prints output.
