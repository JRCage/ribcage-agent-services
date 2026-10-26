# Rowan Expense Recovery Desk — Business and Marketing Plan
Version: 2026-10-26 | Status: internal pilot; **not launched, no customer data accepted**.

## Executive decision
Build **one shared evidence-led discrepancy and credit-follow-up engine**, and commercialize narrowly. First pilot: **CreditKeeper for landscaping installation contractors** (materials, core/rental deposits, returned stock, warranty credits). Second: **Cleaning Contract Profit Guardian** (rework, scope creep, overtime and supply margin leakage). Third: **Retail Margin Guard** (gas stations and convenience stores). Expand only after demonstrable willingness to pay and exacting accuracy tests.

**Rationale:** do not compete head-on with mature POS, job scheduling, accounting, or property-management suites. Sell documented investigations and resolution, not dashboards or vague AI optimization. All competitor-density rankings are tentative; avoid claims of monopoly or guaranteed savings. Market ordering is a hypothesis to be challenged by paid pilots.

## Market order and strategy
| Sequence | Market | Hook | Core documents | Initial price hypothesis | Gate to expand |
|---|---|---|---|---|---|
| 1 | Landscaping **installation** firms | Missing returns, deposit refunds, plant/warranty credits | Invoices, return receipts, statements, rental agreements | $49 limited audit; $99/mo | >=3 of 5 pilots willing to pay; material confirmed exceptions |
| 2 | Multi-crew commercial cleaners | Scope creep and uncompensated rework | Contracts, inspections, hours, service tickets, invoices | $49 trial; $99-149/mo | Margin leakage attributable to evidence; owners act on alerts |
| 3 | Small gas/convenience operators | Vendor price errors, missed promotional credits | Distributor invoices, negotiated price sheets, credit memos | $49 trial; $99/store/mo | Verifiable supplier discrepancies not caught by current back office |
| 4 | Property managers | Contractor warranty and repeat-work checks | Work orders, warranties, service invoices | $149-299/mo | No overlap with existing AppFolio/Property Meld workflow |
| 5 | HVAC, plumbing, electrical | Material returns + job costing exceptions | PO, job tickets, invoices, credits | $99-199/mo | Material discrepancy frequency justifies billing |
| 6 | Small independent hotels | Vendor contract variance, NOT commodity OTA reconciliation | Agreements, vendor invoices | $99-199/mo | Show specific unaddressed workflow |
| 7 | Laundromats | Bill-based abnormal utility usage, with clear uncertainty | Utility bills, cycle counts if available | $39-79/mo | Repeated actionable alerts vs seasonal noise |
| 8 | Childcare subsidy providers | Authorization/attendance/payment exceptions | Subsidy statements, attendance, authorizations | Per state quote | Obtain state-specific compliance/legal review and minimal child data |
| 9 | Auto repair | Core deposits and uncredited returns | Supplier credits, returns, invoices | Pilot only | Beat specialized established offerings on distribution/economics |
| 10 | Restaurants | Missing distributor discounts | Invoices, negotiated menus, credits | Pilot only | Prove differentiated results vs existing tools |
| 11 | Veterinary clinics | Supplier contract exceptions | Invoices/credits | Pilot only | Verify demand and data handling |
| 12 | Nonprofits/churches | Duplicate expense monitoring | Vendor records | Low-cost seasonal service | Sufficient value relative to budgets |
| 13 | Households | Verified bill correction and refund assistance | Bills, EOBs only in later regulated workflow | Per-case, not broad subscription | Strong privacy controls; avoid medical/insurance regulated work at outset |
| 14 | Bookkeeper distribution | White-label exception packets for clients | Authorized client documents | $25-50/active-client/mo hypothesis | Partner can enroll multiple clients with consent |

**Launch sequence:** stages 1 and 2 as competing pilots, not concurrent full builds. Stage 3 after successful repeatability. The remaining markets are a research backlog, not commitments to operate all simultaneously.

## Ideal customer profiles and qualifying questions
**Landscaping:** independent installers with 3-30 staff, frequent material deliveries/returns and 20+ invoice/credit events/month. Qualify: monthly materials spend, how returns are documented, outstanding credits, software currently used, who approves claims. Exclude basic mowing-only operators at launch.
**Cleaning:** independent B2B cleaner with multiple crews and 8+ commercial contracts, recurring scope changes, complaints and consumable purchases. Qualify: contract tracking, rework hours, contract-level margin insight and authorization rules.
**Retail:** 1-5 independently operated sites, frequent supplier statements, no satisfactory verification layer. Qualify: POS/back-office capabilities, documented unresolved credits, distributor agreements.

## Product — rigorous money-state ledger
Intake email/secure upload -> immutable original file + hash -> parse and confidence score -> normalize -> deterministic joins across invoices/credits/returns/contracts -> create **candidate** exception -> attach citations and dollar basis -> human verification -> owner-approved vendor inquiry -> track vendor acknowledgment -> verify credit/refund in statement -> mark **recovered**.
Statuses: suspected, needs_evidence, verified, submitted, vendor_responded, approved, recovered, rejected. Never call an unexplained price rise an overcharge; never claim recovery before statement/payment proof. Any low-confidence extraction is blocked from auto-action. No automatic bank transactions, external disputes or settlement agreements. Do not share one customer's pricing with another.

**MVP boundaries:** CSV export/import and standardized invoice rows, no bank/POS integrations, no unsupervised vendor communications, no child/health/financial-account data. Per-tenant isolation, least privilege, expiring uploads, clear retention and deletion path, encrypted storage, event log, rate limiting and audit tests before customer pilot.

## Go-to-market: no-spam founder-led validation
1. Build 40 qualified leads in Texas landscaping installation and commercial cleaning: public business contact channels, existing vendor software identified, no scraping private data. Separate lead lists; deduplicate with Johnny.
2. Reach out thoughtfully to a few businesses per day using public business contact details. Ask about uncredited returns/contract rework, not a generic AI pitch. Respect platform rules and opt-outs; no deceptive identity, false case studies or false claims.
3. Offer a **limited paid audit** (up to 25 documents) at a test price of $49. Deliver a written evidence packet even if zero valid errors; do not promise savings or claim false recovery. Prior to handling real records require explicit customer authorization, privacy policy, scope, and securely configured intake.
4. For prospects who decline, categorize why: no pain, existing solution, price, privacy, trust, or workflow friction. Iterate message and product only using evidence.
5. For engaged prospects, run a guided demonstration on synthetic data; never ask for account credentials.
6. Convert successful pilots to a monthly monitoring plan with clear volume, turnaround and owner approval rules. Publish true case studies only with written consent.

**Sample outreach (draft; do not send in bulk):**
"Hi — I’m testing a small service for landscape installation teams that tracks returned materials and supplier credits so nothing gets lost between the job and the statement. Do you already have a reliable way to catch uncredited returns and deposits? I can show a synthetic example first. No software replacement required."

**Site page outline:** title + specific job-to-be-done; 3-step workflow; synthetic sample exception packet clearly marked; privacy/security; honest pricing and limits; customer consent; contact / pilot interest form; no exaggerated ROI or endorsements.

**Channels:** targeted email, local contractor associations, bookkeeper referrals, supplier-dispute explainer articles, permitted thoughtful Bluesky discussions, small business forums. Focus on response quality rather than impressions. Account identity: openly AI-assisted and human overseen.

## Unit economics and decision rules (hypotheses)
Example 20 active firms x $99 = $1,980 monthly gross, not profit. Target contribution margin >=60% after model/API, storage, review and delivery expenses; first measure real time spent. Avoid percentage-of-recovery fee until legal/tax review and documented mechanism. No spending or customer promises without approval as required.
Experiment: 20 interviews across landscape/cleaning, 10 permitted synthetic demos, 5 paid audits each if possible. Winning segment needs >=3 paid conversions of 5 completed pilots, verified evidence quality >=99% at the case/claim level (zero false 'recovered'), and a realistic acquisition path. Stop/pivot if document sufficiency is poor, data access friction blocks sales, support cost overwhelms revenue, or direct competitors already solve the problem for less.

## 6-week gated build/marketing schedule
Week 1: ingest synthetic CSVs, match invoices to credits and returns, exceptions only; unit tests and security checklist.
Week 2: sample report generator; landing-page copy; Johnny's security/UX QA and defects.
Week 3: use safe pilot-interest forms, non-sensitive interviews; privacy/legal terms review prior to real uploads.
Week 4: manually verified authorized pilot audit deliveries; track claim acceptance/rejections, customer feedback.
Week 5: customer-approved follow-up workflow and exception state updates; repeatability/tenant isolation tests.
Week 6: consider paid subscription, referral partnership and industry 2 only with measurable proof.
Each launch gates on Johnny's written QA approval, secure end-to-end tests and explicit authorized production deployment.

## Collaboration and governance
Johnny reviews business positioning, ICP, competitive omissions, pricing, security/privacy, intake UX, defect severity, and marketing compliance; changes land in reviewed PR. Shared Cloudflare resource changes must be documented; no silent production updates. Rowan owns product and audit trail; owner approves paid infrastructure, legal issues, financial commitments. Weekly scorecard: qualified leads, responses, calls, pilots, paid conversions, verified findings, recovered amounts supported by proof, false positives, monthly gross, costs, gross margin, outstanding disputes. Do not disclose operator's private identity.

## Decision asks for Johnny
1. Is landscape credit recovery valuable enough relative to simple QuickBooks/accounting follow-up?
2. Is contract margin leakage a stronger first offer for commercial cleaning?
3. What existing systems cover these workflows better than we think?
4. What are your blocking security/QA defects before intake?
5. Which of these offers can we market immediately using synthetic demos and zero account integrations?
6. Review pricing, narrow target profile, privacy/data retention, site copy, and a two-week test matrix.
