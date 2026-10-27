"""Render a local, read-only CreditKeeper exception report to stdout."""
import csv
import sys
from html import escape

from reconcile import read_csv, reconcile


def render_report(rows):
    exceptions = reconcile(rows)
    labels = {
        "suspected_missing_credit": "Suspected missing credit",
        "suspected_excess_credit": "Suspected excess credit",
        "needs_evidence": "Needs invoice evidence",
    }
    actions = {
        "suspected_missing_credit": "Verify the approved return and statement period before asking the supplier about this credit.",
        "suspected_excess_credit": "Check for duplicate posting, allocation errors or missing expected-credit records.",
        "needs_evidence": "Locate the original invoice before interpreting this difference as a missing or excess credit.",
    }
    def cell(value):
        return "<td>" + escape(str(value), quote=True) + "</td>"
    body = []
    for item in exceptions:
        values = [item["vendor"], item["invoice"], labels[item["status"]],
                  item["expected"], item["posted"], item["difference"],
                  ", ".join(item["references"]), actions[item["status"]]]
        body.append("<tr>" + "".join(cell(value) for value in values) + "</tr>")
    if not body:
        body.append('<tr><td colspan="8">No exceptions detected in the supplied rows. This does not establish that the source records are complete or that all credits were received.</td></tr>')
    return '''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>CreditKeeper exception report</title>
<style>
body{font:16px/1.5 system-ui,sans-serif;color:#182d31;max-width:1200px;margin:32px auto;padding:0 20px}
h1{line-height:1.2} .notice{padding:16px;background:#edf5f3;border-left:4px solid #28786b}
.table-wrap{overflow-x:auto} table{border-collapse:collapse;width:100%;font-size:14px}
th,td{padding:12px 10px;border-bottom:1px solid #ccd8d6;text-align:left;vertical-align:top;overflow-wrap:anywhere}
th{background:#edf5f3} footer{font-size:13px;margin-top:24px}
@media print{body{margin:0;padding:0;font-size:11px}table{font-size:9px}th,td{padding:5px}thead{display:table-header-group}tr{break-inside:avoid}.table-wrap{overflow:visible}}
</style></head><body>
<h1>CreditKeeper exception report</h1>
<p class="notice"><strong>Prototype review only. Findings are suspected, not verified or recovered money.</strong>
Manually compare each item with the original invoice, approved return and supplier statement. No supplier has been contacted and no accounting records have been changed.</p>
<p>Scope: supplied CSV rows only. Currency and statement period are not encoded by this prototype; confirm a single currency and period before interpreting any amount. Differences are absolute amounts, with direction shown by status. Missing invoice evidence takes precedence over any apparent balance.</p>
<div class="table-wrap"><table><thead><tr><th>Supplier</th><th>Invoice</th><th>Status</th><th>Expected credit</th><th>Posted credit</th><th>Difference</th><th>Credit references</th><th>Next verification</th></tr></thead><tbody>''' + "".join(body) + '''</tbody></table></div>
<h2>Before acting</h2><ol><li>Confirm source completeness and the statement cutoff date.</li><li>Match the listed references to original documentary evidence.</li><li>Record the owner's decision and obtain separate authorization before supplier contact.</li></ol>
<footer>This local report contains references from the supplied input. It excludes note fields, loads no external resources and runs no scripts. Treat the report as confidential if real records are ever authorized. Delete exported reports according to the agreed retention policy.</footer>
</body></html>'''


def main(args):
    if len(args) != 2:
        print("Usage: python report.py FILE.csv > report.html", file=sys.stderr)
        return 2
    try:
        report = render_report(read_csv(args[1]))
    except (ValueError, OSError, csv.Error) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
