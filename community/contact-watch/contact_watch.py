"""ContactWatch: opt-in public business contact checks; authorized patient snapshots offline."""
import argparse, json, re, sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

MAX_HTML = 250000
PHONE = re.compile(r'^\+?[0-9][0-9().\- ]{6,25}$')

class ContactParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.phones, self.addresses = set(), set()
        self.in_address, self.parts = False, []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            href = attrs.get('href', '')
            if href.startswith('tel:'):
                p = href[4:].split('?',1)[0].strip()
                if PHONE.fullmatch(p): self.phones.add(' '.join(p.split()))
        if tag == 'address':
            self.in_address, self.parts = True, []
    def handle_data(self, data):
        if self.in_address: self.parts.append(data)
    def handle_endtag(self, tag):
        if tag == 'address' and self.in_address:
            address = ' '.join(' '.join(self.parts).split())
            if 3 <= len(address) <= 300: self.addresses.add(address)
            self.in_address, self.parts = False, []
    def result(self):
        return {'phones': sorted(self.phones), 'addresses': sorted(self.addresses)}

def extract(html):
    p = ContactParser()
    p.feed(html)
    return p.result()

def safe_url(url):
    u = urlparse(url)
    if u.scheme != 'https' or not u.hostname or not re.fullmatch(r'[A-Za-z0-9.-]+', u.hostname):
        raise ValueError('Expected public HTTPS hostname')
    if u.username or u.password or u.port not in (None,443) or u.fragment:
        raise ValueError('No credentials, custom ports, fragments')
    if (re.fullmatch(r'(?:\d{1,3}\.){3}\d{1,3}', u.hostname)
        or u.hostname in ('localhost',) or u.hostname.endswith(('.local','.internal','.test','.invalid'))):
        raise ValueError('Private or reserved hosts not supported')
    return url

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def retrieve(url, opener=None):
    safe_url(url)
    req = Request(url, headers={'User-Agent': 'ContactWatch/0.1 (public business contact maintenance)', 'Accept':'text/html'})
    with (opener or build_opener(NoRedirect()).open)(req, timeout=8) as response:
        if response.geturl() != url:
            raise ValueError('Redirect prohibited')
        if 'text/html' not in response.headers.get('Content-Type',''):
            raise ValueError('Not HTML')
        data = response.read(MAX_HTML+1)
        if len(data)>MAX_HTML: raise ValueError('Response too large')
    return extract(data.decode('utf-8', errors='replace'))

def compare(previous, current, company_id, url):
    findings = []
    for field in ('phones', 'addresses'):
        old, new = sorted(set(previous.get(field, []))), sorted(set(current.get(field, [])))
        if old != new:
            findings.append({'company_id':company_id,'field':field,'old':old,'observed':new,
                             'source_url':url,'action':'REVIEW_BY_PERSON',
                             'note':'Call the business to verify; do not automatically update records.'})
    return findings

def run_business(config, state, fetch=retrieve):
    if not isinstance(config,dict) or not isinstance(config.get('organizations'),list):
        raise ValueError('Expected organizations list')
    nxt, reviews, errors = dict(state), [], []
    for row in config['organizations']:
        if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id']:
            raise ValueError('Each organization needs an id')
        key = row['id']
        if row.get('kind','organization') != 'organization' or key.startswith('patient:'):
            raise ValueError('Public web checks support organizations only')
        url = row.get('public_contact_url','')
        try:
            observation = fetch(url)
            if key in nxt: reviews.extend(compare(nxt[key], observation, key, url))
            nxt[key] = observation
        except (ValueError,OSError,UnicodeError) as error:
            errors.append({'company_id':key,'error_type':type(error).__name__})
    return {'reviews':reviews,'errors':errors,'status':'REVIEW_ONLY'}, nxt

def compare_authorized_snapshots(old, new):
    """Only local, authorized input. Results contain PHI; never put in public CI."""
    def index(rows):
        if not isinstance(rows,list): raise ValueError('Expected list')
        out={}
        for row in rows:
            if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id'] or row['id'] in out:
                raise ValueError('Invalid or duplicate id')
            out[row['id']]=row
        return out
    first, second = index(old), index(new)
    reviews=[]
    for rid in sorted(first.keys() & second.keys()):
        for field in ('phone','address'):
            if first[rid].get(field) != second[rid].get(field):
                reviews.append({'record_id':rid,'field':field,'old':first[rid].get(field),
                                'proposed':second[rid].get(field),'action':'REVIEW_AND_VERIFY','ehr_updated':False})
    return {'reviews':reviews,'status':'LOCAL_AUTHORIZED_SNAPSHOTS_ONLY'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command', required=True)
    a=sub.add_parser('business');a.add_argument('--config',required=True);a.add_argument('--state',required=True);a.add_argument('--review',required=True)
    a=sub.add_parser('patient-local');a.add_argument('--old',required=True);a.add_argument('--new',required=True);a.add_argument('--review',required=True)
    args=p.parse_args(argv)
    try:
        if args.command=='business':
            config=json.loads(Path(args.config).read_text(encoding='utf8'))
            state_path=Path(args.state)
            prior=json.loads(state_path.read_text(encoding='utf8')) if state_path.exists() else {}
            result, state=run_business(config, prior)
            Path(args.review).write_text(json.dumps(result,indent=2),encoding='utf8')
            state_path.write_text(json.dumps(state,indent=2),encoding='utf8')
        else:
            before=json.loads(Path(args.old).read_text(encoding='utf8'))
            after=json.loads(Path(args.new).read_text(encoding='utf8'))
            result=compare_authorized_snapshots(before,after)
            Path(args.review).write_text(json.dumps(result,indent=2),encoding='utf8')
        print(json.dumps({'reviews':len(result['reviews']),'errors':len(result.get('errors',[])),'status':result['status']}))
        return 0
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print('Input error: '+type(exc).__name__,file=sys.stderr)
        return 2
if __name__=='__main__':sys.exit(main())
