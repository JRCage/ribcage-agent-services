# ContactWatch — free medical-directory contact change review tool

Python 3.10+, no third-party dependencies. Built to help health information management and provider-directory teams check *explicitly authorized public business contact pages* for changed office phone numbers and addresses. Produce a **human review queue**, not automatic chart updates. Includes a separate **local-only** authorized patient-record comparison mode.

## Public office contact pages

Put permitted public sites in `organizations.json`:
```json
{"organizations":[{"id":"demo-clinic","kind":"organization","public_contact_url":"https://example.org/contact"}]}
```
Then run:
```sh
python contact_watch.py business --config organizations.json --state observations.json --review review-queue.json
```
First run establishes a baseline; later runs generate review suggestions containing source, observed old/new addresses and telephones. Extracts `tel:` links and HTML `<address>` elements only, not arbitrary text; false positives and false negatives are possible. Use only sites permitting automated access; this prototype doesn't parse robots.txt. Schedule **your own authorized runner** weekly (`0 9 * * 1`) or monthly (`0 9 1 * *`). It does not itself schedule jobs, contact patients, or update medical record systems.

The review queue is the human-facing workflow: staff verify changes by calling official known channels before editing the approved directory. A one-click FHIR update button is **not implemented**, because a safe production integration would require authorized EHR credentials, verified identity, role-based permissions, audit logging, conditional writes, and concurrency checks.

## Private patient record comparisons (never internet-scanned)

```sh
python contact_watch.py patient-local --old authorized-previous.json --new authorized-current.json --review private-review-queue.json
```

Only compare organization-authorized local snapshots of `[{"id":"synthetic-p1","phone":"5550100","address":"Synthetic Ave"}]`. No searches, scraping, SMS, outbound calls, or EHR writes. **Files and review results may contain PHI. Keep them on a governed, access-controlled system. Never commit patient data to GitHub or run this mode on public CI.**

## Tests

```sh
python -m unittest discover -s . -p 'test_*.py' -v
```

## Security and limits

- Input is an opt-in organization URL allowlist. HTTPS only, standard ports, disallows obvious private hostnames and redirects. Deployment must enforce outbound network egress controls against DNS rebinding and internal address access.
- No authentication, clinical inference, identity validation, or completeness guarantee. Website contact details may be stale or spoofed.
- **Not** HIPAA compliance certification, clinical validation, a patient locator, or de-identification software.
- Based on standard FHIR R4 Organization and Patient contact fields, but the input/output is simplified JSON, not a full FHIR implementation.
- MIT-licensed. Please share only synthetic reproductions in bug reports.

References: https://hl7.org/fhir/R4/organization.html , https://hl7.org/fhir/R4/patient.html , https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/minimum-necessary-requirement/index.html
