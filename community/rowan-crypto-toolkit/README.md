# Rowan Crypto Developer Toolkit — free MIT utilities

Independent, openly AI-assisted developer experiment by Rowan, linked here for discovery; not part of the paid Ribcage Verification Desk.

Three local, dependency-free Python tools useful when prototyping Solana and stablecoin apps:

1. **LaunchCheck** — lint *user-supplied* token launch JSON (authority, supply, allocation, and disclosures). No on-chain verification.
2. **ReceiptMatch** — match exported payments to invoices by invoice ID, asset, and recipient; flag duplicates, mismatches, and partial/overpayments. No on-chain verification.
3. **TokenUnits** — exact token decimal / raw-unit conversion without floating-point errors.

## Run

Python 3.10+.

```bash
python community/rowan-crypto-toolkit/tokenunits.py to-raw 1.000001 --decimals 6
python community/rowan-crypto-toolkit/tokenunits.py from-raw 1000001 --decimals 6
python community/rowan-crypto-toolkit/receiptmatch.py path/to/invoices.csv path/to/payments.csv
python community/rowan-crypto-toolkit/launchcheck.py path/to/config.json
```

ReceiptMatch invoice CSV columns: `invoice_id,asset,address,amount`.
Payment CSV columns: `signature,invoice_id,asset,address,amount`. A signature is used as a unique reference but is **not verified**.
LaunchCheck JSON: `supply` positive; `decimals` integer 0..9; `mint_authority` and `freeze_authority` values `revoked` or `retained`; `allocations` is a list of `{"name":"team","percent":10}` totaling 100.

## Safety

No secrets, RPC requests, wallet signing, fund custody or transactional execution. Never treat CSV receipt matches as confirmation of an on-chain payment. Verify chain data independently. These tools are prototypes, not financial, tax, legal or security advice.

## License and support

MIT; see LICENSE. Contributions welcome through GitHub issues/PRs. For custom integrations, hardened hosted APIs or payment/accounting workflows, request a scoped paid development engagement with acceptance tests. Keep public source free.


## Doomsday read-only escrow preflight

The community-maintained `doomsday_escrow.py` script checks the bounty publisher's stated escrow API without downloading/running remote code, signing wallet transactions or calling a faucet.

```bash
python community/rowan-crypto-toolkit/doomsday_escrow.py --list
python community/rowan-crypto-toolkit/doomsday_escrow.py --owner doomsday-network --repo doomsday --issue 11
python -m unittest discover -s community/rowan-crypto-toolkit -p 'test_*.py' -v
```

Publisher API results are always `PROJECT_CLAIM_ONLY`. The program does not itself perform independent on-chain escrow verification; never infer a funded/collectible bounty or a realizable USDC price from it. The `skills/doomsday-escrow/SKILL.md` companion explains the independent verification steps required before financial decisions. The script rejects path traversal, excessive response bodies and cross-host redirects **after fetching**. Do not treat it as a full security audit.
