"""Read-only, bounded Doomsday bounty discovery. Publisher data is NOT chain proof.

Python 3.10+, stdlib only. No wallets, code execution, signing or fund movements.
"""
import argparse
import json
import re
import sys
import urllib.request
from urllib.error import HTTPError, URLError

HOST = "https://doomsday.network"
MAX_BYTES = 512 * 1024
SEGMENT = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")


def escrow_url(owner=None, repo=None, issue=None):
    if owner is None and repo is None and issue is None:
        return HOST + "/escrow/list"
    if not all(isinstance(x, str) and SEGMENT.fullmatch(x) for x in (owner, repo)):
        raise ValueError("owner and repository must be safe URL segments")
    if not isinstance(issue, int) or isinstance(issue, bool) or not 1 <= issue <= 1_000_000_000:
        raise ValueError("issue must be a positive integer")
    return f"{HOST}/escrow/{owner}/{repo}/{issue}"


def fetch(url, opener=None):
    """Download bounded JSON from one trusted HTTPS host; never follow cross-host redirects."""
    if not (url == HOST + "/escrow/list" or
            re.fullmatch(re.escape(HOST) + r"/escrow/[A-Za-z0-9_.-]{1,100}/[A-Za-z0-9_.-]{1,100}/[0-9]+", url)):
        raise ValueError("unexpected endpoint")
    client = opener or urllib.request.urlopen
    req = urllib.request.Request(url, headers={
        "Accept": "application/json", "User-Agent": "rowan-escrow-preflight/0.1"})
    with client(req, timeout=8) as response:
        if response.geturl().split("/", 3)[:3] != ["https:", "", "doomsday.network"]:
            raise ValueError("redirected outside expected host")
        content = response.read(MAX_BYTES + 1)
        if len(content) > MAX_BYTES:
            raise ValueError("response too large")
    return json.loads(content.decode("utf-8"))


def report(url, payload):
    return {
        "endpoint": url,
        "classification": "PROJECT_CLAIM_ONLY",
        "independently_verified_escrow": False,
        "payout_confirmed": False,
        "liquidity_verified": False,
        "warning": "The issuer's API cannot independently prove segregated or collectible funds.",
        "publisher_payload": payload
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List project-reported bounties")
    parser.add_argument("--owner", help="GitHub owner")
    parser.add_argument("--repo", help="GitHub repo")
    parser.add_argument("--issue", type=int, help="GitHub issue number")
    args = parser.parse_args(argv)
    try:
        url = (escrow_url() if args.list and not any((args.owner, args.repo, args.issue))
               else escrow_url(args.owner, args.repo, args.issue))
        result = report(url, fetch(url))
    except (ValueError, HTTPError, URLError, TimeoutError, OSError,
            UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"classification": "UNVERIFIED", "error": str(exc),
                          "payout_confirmed": False}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
