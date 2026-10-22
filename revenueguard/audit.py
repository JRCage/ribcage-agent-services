#!/usr/bin/env python3
"""RevenueGuard: local-only CSV invoice exception audit (no outbound actions)."""
import argparse,csv,json,datetime,decimal,collections,pathlib
D=decimal.Decimal
REQUIRED=('invoice_id','customer','issued_date','due_date','amount','paid_amount','status')
STATUSES={'draft','sent','overdue','paid','void','cancelled'}
def audit(rows,today):
    seen=set(); findings=[]; report=[]
    for n,row in enumerate(rows,2):
        ident=row.get('invoice_id','').strip()
        flags=[]
        if not ident: flags.append('missing_invoice_id')
        elif ident in seen: flags.append('duplicate_invoice_id')
        seen.add(ident)
        try:
            issued=datetime.date.fromisoformat(row['issued_date'].strip());due=datetime.date.fromisoformat(row['due_date'].strip())
            if due<issued: flags.append('due_before_issue')
        except (ValueError,KeyError,AttributeError):
            due=None;flags.append('invalid_date')
        try:
            amount=D(row['amount'].strip());paid=D(row['paid_amount'].strip())
            if not amount.is_finite() or not paid.is_finite():raise ValueError()
            if amount<0 or paid<0:flags.append('negative_amount')
            if paid>amount:flags.append('overpayment')
        except (decimal.InvalidOperation,ValueError,KeyError,AttributeError):
            amount=paid=None;flags.append('invalid_amount')
        status=row.get('status','').strip().lower()
        if status not in STATUSES:flags.append('invalid_status')
        if amount is not None and paid is not None:
            if status=='paid' and paid<amount:flags.append('paid_status_with_balance')
            if status in {'sent','overdue'} and paid==amount and amount>0:flags.append('fully_paid_but_open')
            if due and due<today and paid<amount and status in {'sent','overdue'}:flags.append('past_due_balance')
        record={'line':n,'invoice_id':ident,'customer':row.get('customer',''),'flags':'|'.join(flags)}
        report.append(record)
        for flag in flags:findings.append({'line':n,'invoice_id':ident,'code':flag})
    return report,findings,{'invoices':len(report),'exceptions':len(findings),'flag_counts':dict(sorted(collections.Counter(x['code'] for x in findings).items())),'as_of':today.isoformat()}
def main():
    p=argparse.ArgumentParser();p.add_argument('csv_file');p.add_argument('--as-of',default=datetime.date.today().isoformat());p.add_argument('--out',default='revenueguard-output');a=p.parse_args()
    today=datetime.date.fromisoformat(a.as_of);dest=pathlib.Path(a.out);dest.mkdir(parents=True,exist_ok=True)
    with open(a.csv_file,newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f);missing=set(REQUIRED)-set(reader.fieldnames or ())
        if missing: p.error('Missing columns: '+', '.join(sorted(missing)))
        report,findings,summary=audit(reader,today)
    with open(dest/'invoice_report.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['line','invoice_id','customer','flags']);w.writeheader();w.writerows(report)
    for name,obj in [('exceptions.json',findings),('summary.json',summary)]:
        (dest/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary))
if __name__=='__main__':main()
