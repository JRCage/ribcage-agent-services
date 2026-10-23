# MarginGuard — free offline price-change checker

A single-file browser app that lets independent retailers test supplier cost increases and promotional discounts against a required gross-margin floor, before changing shelf prices.

## Use

1. Download [index.html](index.html) and open it in any modern browser. No server, account, installation, or internet connection required.
2. Paste an inventory export with columns `name,cost,price` (extra columns allowed).
3. Set supplier cost change, planned discount, and minimum gross margin.
4. Analyze and optionally download a results CSV.

Example input:

```csv
name,cost,price
Coffee beans,8,15
"Notebook, ruled",3.25,8
```

Gross margin is `(price - cost) / price`; minimum price is `cost / (1 - target margin)`. Percentages apply to unit costs and selling prices before margin is calculated. Prices are unitless; use one currency throughout.

## Privacy and limitations

Everything runs inside the browser. Nothing is uploaded, persisted, or sent to a POS. No CDN, dependencies, analytics, or third-party requests. You can view the source in [index.html](index.html). This is not a full profit model; it excludes labor, card processing, platform fees, tax, shipping, spoilage, overhead, and other costs. Review margins before making business decisions.

## License

MIT — free to use, change and redistribute. Copyright (c) 2026 contributors to Ribcage Agent Services.
