# CreditKeeper review gates

Scope: synthetic local proof of concept only. No real-document intake, checkout,
vendor contact, production deployment or merge is authorized by a passing test.

## Repeatable technical verification

The CreditKeeper synthetic QA workflow runs the prescribed Python command, the
original adversarial categories through the CLI, and 11 demo behavior cases.
It installs no dependencies. The runner imports an empty container filesystem
and mounts only its installed toolchain and this source directory read-only.
The test process has no external network, credentials or repository .git data.
Scratch is a 16 MiB memory filesystem with 256 inodes, discarded on exit.
CPU, memory, processes, file size, open descriptors and wall time are bounded.

Evidence is the Actions run URL, tested commit SHA, complete output and exit
status. A passing builder-run workflow is reproducible evidence, not Johnny's
independent sign-off. Johnny must review the results and explicitly pass or
block the tested revision. A failed or absent run never counts as passing.

## Privacy review of this prototype

- Input: explicitly supplied local CSV; no credentials, integrations or uploads.
- Processing: deterministic integer cents, references grouped by vendor/invoice.
- Output: stdout includes vendor, invoice and credit references and amounts.
  Treat redirected output and terminal logs as confidential if real data are
  ever authorized; the program does not anonymize these fields.
- Input files are not modified. Notes are not included in reconciliation output.
- The demo loads no external resources, sends no requests and uses no browser
  storage. Its mailto link opens a separate, deliberate email action.
- All committed transaction examples are synthetic. Public prospect contact
  research is separate from transaction data and is not customer consent.
- No customer service endpoint or shared storage exists in this PoC. Therefore
  cross-customer access and retention controls cannot be certified from it.

## Before any real customer pilot

Keep intake disabled until a named private route and responsible operator exist.
Record customer authorization, one supplier/currency/statement-period scope,
permitted fields, access list, retention deadline, deletion procedure (including
outputs/backups), and approved delivery/payment route. Do not accept bank login
credentials or confidential attachments through public GitHub or initial email.

Use two fictional customers to verify unauthorized reads/downloads are refused,
expired links stop working, deletion removes inputs and outputs, logs exclude
document contents, and delivery reaches only the intended recipient. Record
actual results against the configured route; this document is not those results.
Use a provider test receipt for any future payment test, never a live charge.

## Current handoff

WAITING ON JOHNNY: independently evaluate the final commit and Actions evidence,
record explicit pass/block for synthetic PoC review, and review any proposed
private intake/delivery route separately. No approval is inferred from silence.

WAITING ON ROWAN: preserve the synthetic-only boundary until that review; record
the actual Actions outcome and fix any failures. Protocol synchronization to main,
the shared ops doc and continuity notes remains separate from the PR-file update.

## Executed evidence, October 27, 2026

Commit 5c2e0c48b2c3fdf1787c4b4687c03edfc2162457 executed successfully in
https://github.com/JRCage/ribcage-agent-services/actions/runs/40534979483 :
17 Python tests passed, the sample reported exactly 50.00 suspected missing
credit, and 11 demo behavior cases plus static privacy checks passed. These
include the original malformed-input categories, excess credits, orphan
invoices, no-argument usage, and source-fixture immutability. No customer data
or payment was used. Follow-up workflow change separates each test command
under shell -e so any failed suite stops execution instead of being masked by
a later successful command. Require the latest commit's check to pass as well.
