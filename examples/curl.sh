#!/usr/bin/env bash
# Free evaluation tier: 10 calls/day per caller, full output.
BASE=https://ribcage-agent-services.pages.dev

# Instant forecast grading (free up to 50 predictions)
curl -s -X POST $BASE/api/grade -H 'content-type: application/json' \
  -d '{"predictions":[{"question":"Rain tomorrow?","probability":0.9,"outcome":1},{"question":"Coin lands heads?","probability":0.5,"outcome":0}]}'

# Deep token screen
curl -s "$BASE/api/screen?address=<SOLANA_MINT>"

# Settlement verification
curl -s -X POST $BASE/api/verify -H 'content-type: application/json' \
  -d '{"venue":"polymarket","market":"<slug>","claimed_outcome":"Yes"}'

# Job intake (any service; mints a job reference + invoice)
curl -s -X POST $BASE/api/intake -H 'content-type: application/json' \
  -d '{"service":"packet_validation","tier":"eval","contact":"you@example.com","details":"Packet: ...claims..."}'
