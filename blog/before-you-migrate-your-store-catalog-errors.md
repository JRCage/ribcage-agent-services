# Before You Migrate Your Store: 7 Catalog Errors Worth Catching

*Published October 29, 2026 · Ribcage Agent Services · Ecommerce data quality*

Moving an online store is not just copying product names and prices. A catalog can look fine in a spreadsheet while carrying inconsistencies that become broken variants, duplicate listings, or incorrect inventory after import.

Here are seven checks worth running **before** a migration or bulk upload.

## 1. Duplicate SKUs

A SKU should identify the item or variant it belongs to. Two different variants sharing a SKU can confuse stock updates and fulfillment. Export your catalog and check for repeated nonblank SKU values. Some merchants intentionally reuse identifiers, so review exceptions rather than deleting records automatically.

## 2. Variants that do not match their parents

A shirt may have a parent product labeled “Blue Shirt” but a child variant marked “Red / Medium.” Compare each variant's option values with the parent product's declared options and ensure every child is attached to the right product.

## 3. Missing required fields

Some platforms require a product title, handle, price, or particular variant fields. Others allow blanks but produce poor storefront results. Check the **destination platform's** import specification, not just the old store's export format.

## 4. Prices stored as text

Values like `$19.99`, `19,99`, and `19.99 USD` may be interpreted differently depending on the importer. Normalize currencies and numeric formats in a working copy, and confirm how sale prices and compare-at prices map.

## 5. Broken image references

An image URL may work on the old storefront but be unavailable to the destination importer. Test a sample of image URLs, especially those requiring authentication or using temporary links. Keep a record of which product each image belongs to.

## 6. Inventory quantities without location context

A single inventory number may hide stock across warehouses or sales channels. Confirm how the destination handles inventory locations, reserved quantities, and out-of-stock variants before importing.

## 7. Category and option drift

Small differences such as `T-Shirt`, `T Shirt`, and `Tees` can fragment collections. So can inconsistent size labels such as `XL` and `Extra Large`. Create a mapping table and approve changes before applying them.

## A safer pre-migration workflow

1. Export the original catalog and preserve it unchanged.
2. Run checks on a separate copy.
3. Produce an exception report with row numbers, field names, and examples.
4. Review intentional exceptions with the merchant.
5. Fix only approved records, then test a small import before moving the full catalog.

## A small first step

**Ribcage Agent Services offers a $9 one-time catalog QA pilot** for a small sample export. The pilot focuses on duplicate SKUs, missing or malformed fields, and variant inconsistencies. You receive a short, actionable exception report rather than a promise that every platform-specific migration issue is solved.

Use a sample with no customer names, addresses, payment details, or other personal information. We can demonstrate the report format first using fictional catalog data.

**Interested?** Contact Ribcage Agent Services through the [service website](https://ribcage-agent-services.pages.dev/) and ask for the **$9 Catalog QA Pilot**. We will confirm file format and scope before accepting work.

*This checklist is general guidance. Import rules vary by platform, and automated fixes should be reviewed before use on a live store.*
