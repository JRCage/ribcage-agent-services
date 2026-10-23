"""Offline tests: no network calls or wallet operations."""
import io
import json
import unittest
from doomsday_escrow import escrow_url, fetch, report

class Response:
    def __init__(self, body, target):
        self.buffer = io.BytesIO(body)
        self.target = target
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def geturl(self): return self.target
    def read(self, n): return self.buffer.read(n)

class EscrowClientTests(unittest.TestCase):
    def test_list(self):
        self.assertEqual(escrow_url(), "https://doomsday.network/escrow/list")
    def test_issue(self):
        self.assertEqual(escrow_url("doomsday-network","doomsday",11),
                         "https://doomsday.network/escrow/doomsday-network/doomsday/11")
    def test_reject_traversal(self):
        with self.assertRaises(ValueError): escrow_url("..%2fadmin","repo",11)
    def test_reject_issue_zero(self):
        with self.assertRaises(ValueError): escrow_url("owner","repo",0)
    def test_reject_invalid_endpoint(self):
        with self.assertRaises(ValueError): fetch("https://attacker.example/escrow/list")
    def test_json_but_no_trust_upgrade(self):
        url = escrow_url()
        data = fetch(url, lambda req, timeout: Response(b'{"locked":3000}', url))
        self.assertEqual(data["locked"], 3000)
        self.assertFalse(report(url,data)["independently_verified_escrow"])
    def test_reject_cross_host_redirect(self):
        url = escrow_url()
        with self.assertRaises(ValueError):
            fetch(url, lambda req, timeout: Response(b'{}', "https://other.example/"))
    def test_reject_oversize(self):
        url = escrow_url()
        with self.assertRaises(ValueError):
            fetch(url, lambda req, timeout: Response(b' ' * (512 * 1024 + 1),url))

if __name__=="__main__": unittest.main()
