#!/usr/bin/env python3
"""Offline, read-only SKU/variant CSV preflight for authorized, non-sensitive samples."""
import csv
import json
import re
import sys
from pathlib import Path

MAX_BYTES = 1_000_000
MAX_ROWS = 100
ALIASES = {
    'sku': ('sku', 'variant sku'),
    'product': ('product_id', 'product id', 'handle', 'product handle'),
    'variant': ('variant_id', 'variant id'),
    'price': ('price', 'variant price'),
    'option1_name': ('option1_name', 'option1 name'),
    'option1_value': ('option1_value', 'option1 value'),
    'option2_name': ('option2_name', 'option2 name'),
    'option2_value': ('option2_value', 'option2 value'),
}
PRICE_RE = re.compile(r'^[0-9]+(?:\.[0-9]{1,2})?$')

class InputError(ValueError):
    pass

def analyze(path):
    path = Path(path)
    if path.stat().st_size > MAX_BYTES:
        raise InputError('File exceeds 1 MB limit')
    issues = []
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        try:
            reader = csv.reader(f, strict=True)
            header = next(reader, None)
            if not header:
                raise InputError('Missing header row')
            norm = [x.strip().casefold() for x in header]
            if len(set(x for x in norm if x)) != len([x for x in norm if x]):
                raise InputError('Duplicate column headers')
            idx = {}
            for canonical, aliases in ALIASES.items():
                matches = [i for i, n in enumerate(norm) if n in aliases]
                if len(matches) > 1:
                    raise InputError('Ambiguous columns for ' + canonical)
                if matches:
                    idx[canonical] = matches[0]
            if not {'sku', 'price', 'product'}.issubset(idx):
                raise InputError('Required columns: SKU (or Variant SKU), Price (or Variant Price), and Product ID/Handle')
            seen_sku, seen_variant, seen_options = {}, {}, {}
            count = 0
            for line, raw in enumerate(reader, start=2):
                if not raw or all(not v.strip() for v in raw):
                    continue
                count += 1
                if count > MAX_ROWS:
                    raise InputError('More than 100 nonblank rows; split into smaller authorized samples')
                if len(raw) != len(header):
                    raise InputError(f'Row {line}: expected {len(header)} columns, got {len(raw)}')
                if any(not norm[i] and raw[i].strip() for i in range(len(header))):
                    raise InputError(f'Row {line}: populated unnamed column')
                get = lambda key: raw[idx[key]].strip() if key in idx else ''
                sku, product, variant, price = (get(k) for k in ('sku', 'product', 'variant', 'price'))
                def flag(code, detail):
                    issues.append({'row': line, 'code': code, 'detail': detail})
                if not product:
                    flag('missing_product_reference', 'Product ID/Handle is blank')
                if not sku:
                    flag('missing_sku', 'SKU is blank')
                if not sku and not variant:
                    flag('missing_variant_identifier', 'Both SKU and variant ID are blank')
                if not price:
                    flag('missing_price', 'Price is blank')
                elif not PRICE_RE.fullmatch(price):
                    flag('invalid_price_format', 'Expected plain nonnegative decimal with at most two fractional digits; no currency symbol or thousands separator')
                if sku:
                    key = sku.casefold()
                    if key in seen_sku:
                        flag('duplicate_sku', f'SKU also appears on row {seen_sku[key]}')
                    else:
                        seen_sku[key] = line
                if variant:
                    key = variant.casefold()
                    if key in seen_variant:
                        flag('duplicate_variant_id', f'Variant ID also appears on row {seen_variant[key]}')
                    else:
                        seen_variant[key] = line
                options = []
                for j in (1, 2):
                    name, value = get(f'option{j}_name'), get(f'option{j}_value')
                    if bool(name) != bool(value):
                        flag('incomplete_variant_option', f'Option {j} needs both a name and value')
                    if name and value:
                        options.append((name.casefold(), value.casefold()))
                if product and options:
                    key = (product.casefold(), tuple(options))
                    if key in seen_options:
                        flag('duplicate_variant_mapping', f'Same product/option combination appears on row {seen_options[key]}')
                    else:
                        seen_options[key] = line
        except (csv.Error, UnicodeError) as exc:
            raise InputError(f'CSV decoding/parsing error: {exc}') from exc
    return {'status': 'exceptions_found' if issues else 'no_exceptions_in_checked_rules',
            'rows_checked': count, 'exception_count': len(issues),
            'rules': ['duplicate_sku', 'missing_identifiers', 'price_format', 'variant_option_mapping'],
            'exceptions': issues,
            'limitations': 'Structural preflight only. Does not validate store state, inventory, tax, product relationships or actual migration correctness.'}

def main(argv):
    if len(argv) != 2:
        print('Usage: python catalog_qa.py authorized_sample.csv', file=sys.stderr)
        return 2
    try:
        result = analyze(argv[1])
    except (InputError, OSError) as exc:
        print(f'Input rejected: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
