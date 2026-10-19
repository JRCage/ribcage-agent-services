"""Minimal client examples for Ribcage Agent Services (free tier works as-is)."""
import json, urllib.request
BASE = "https://ribcage-agent-services.pages.dev"

def post(path, payload):
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode(),
                                 headers={"content-type": "application/json",
                                          # The API sits behind Cloudflare; the default
                                          # Python-urllib agent is filtered (HTTP 403).
                                          "user-agent": "ribcage-client-examples/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def grade(predictions):  # [{"question","probability","outcome"}]
    return post("/api/grade", {"predictions": predictions})

def verify(venue, market, claimed_outcome):
    return post("/api/verify", {"venue": venue, "market": market, "claimed_outcome": claimed_outcome})

def intake(service, details, contact, tier="eval"):
    return post("/api/intake", {"service": service, "details": details, "contact": contact, "tier": tier})

if __name__ == "__main__":
    print(grade([{"question": "demo", "probability": 0.9, "outcome": 1}]))
