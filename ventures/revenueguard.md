# RevenueGuard — paid invoice operations pilot

Status: **proposed, not launched; no customers or revenue**. Operated by Rowan with human oversight.

## Customer and problem
Small US B2B service businesses with 20–200 monthly invoices, especially repair contractors, small agencies, equipment servicing and commercial maintenance firms. Owners risk missing invoices, rejected submissions, unrecorded remittances and cash-flow surprises. The service is preventive accounts-receivable administration, **not third-party debt collection**.

## Fixed-price paid pilot
**$149 upfront for a 14-day pilot**, up to 50 business-to-business invoices. Manual review supported by scripts; no account credentials shared. Client supplies an export with sensitive personal data removed, invoice dates, statuses, due dates, amounts, customer business names, and approved terms. Deliverables: (1) missing/duplicate/inconsistent invoice exception list, (2) aging and payment-reconciliation summary, (3) drafts of polite reminders for owner approval, (4) next-action list and a reproducible CSV report. No collection guarantee. Scope and payment accepted before work begins; refund policy agreed in writing.

## Recurring offer, contingent on successful pilot
**$99/month** for up to 100 invoices, weekly exception review, one owner-approved reminder draft batch, and an owner-visible ledger. Additional scope requires separate quote. No automatic renewals without explicit informed consent and a simple cancellation process.

## Minimum viable technology
CSV ingestion, column mapping, stable invoice IDs, exact duplicate detection, overdue buckets, payment/reconciliation exceptions, evidence links and audit log. Owner reviews every outbound message. Initial processing local/offline. No bank access, payment custody, automatic card charging, credit reporting, legal demands, liens or settlement negotiation. Do not upload unredacted customer financial data to LLMs. Explicit retention and deletion policy before onboarding.

## Innovation roadmap
1. Client-approved export from QuickBooks, Xero or CSV, no live connector initially.
2. Read-only reconciliation with job completion and payment processor exports.
3. Evidence-backed anomaly scoring (invoice rejected, paid-but-not-matched, purchase order mismatch), not opaque AI verdicts.
4. Optional integration into approved accounting workflow; payments handled by licensed payment processor, not Rowan.
5. Agent-accessible, permissioned exception API with source-backed findings and human approval gates.

## Compliance boundaries
Business-to-business accounts-receivable admin for the original creditor only. Do not collect debts on behalf of others, buy debts, charge contingency collection fees, contact consumers about debts, or imply legal authority without counsel reviewing federal and Texas debt-collection requirements. Follow FTC guidance on truthful marketing, data minimization, reasonable security and CAN-SPAM for commercial email; obtain explicit consent for any automated texts/calls. Texas construction prompt-payment rules are industry-specific and do not automatically apply to this service. Do not assert legal compliance until reviewed by qualified counsel.

## Validation milestone
Offer 10 qualified owners a 15-minute discovery conversation. Obtain at least 2 paid $149 pilots before building any live integrations. Track qualified outreach, replies, demos, paid pilots, refunds and owner-measured hours saved or invoices recovered. No invented testimonials.

## Source
Intuit QuickBooks, 2026 Small Business Late Payments Report: https://quickbooks.intuit.com/r/small-business-data/small-business-late-payments-report-2026/
