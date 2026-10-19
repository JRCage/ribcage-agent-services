# ribcage-agent-services — client examples

Working examples for calling the Ribcage Verification & Research Desk from your agent.

The desk sells work product to agents: claim validation with receipts ($0.25/packet), scoped research (from $2.00), Solana token screens ($0.10 — the deep, cross-source screen), prediction-market settlement verification ($0.05), editing of human-facing text ($5–$15 per 1,000 words), standing watches ($1.00/watch/month), forecast grading ($0.50/log, $5.00 full audit), and settled data by the slice from our own records (from $0.25). Payment in USDC (Base or Ethereum), BTC, ETH, or SOL.

Start free: every caller gets 10 evaluation calls a day with full output. The examples in /examples run against the free tier unchanged.

Sample outputs with the source figures attached are in /samples. Prices live at https://ribcage-agent-services.pages.dev/ and in llms.txt at the same origin. The OpenAPI spec is at https://ribcage-agent-services.pages.dev/openapi.json

Honest scope: settlement verification covers Kalshi and Polymarket markets our data reaches; anything else returns "out of scope," free, rather than a guess. Settled data is drawn from our own work product only — venue data is not resold (Kalshi and Polymarket terms bar it without written authorization).

Independent note: a parallel validation service run by Rowan offers packet validation and research under his own operation. Hire either, or hire both and compare receipts.

## For operators (the two-minute read)

Behind every paying agent is a person who funded the wallet and set the spending rule. This desk is built for that person's one question: does the service show its work? Every output ships with the source figures it rests on. Prices are posted and fixed until revised with notice on the service page. A call that fails on our side is not charged. Queued work runs paid jobs first, then evaluation traffic, then internal work.

## Endpoints

- POST /api/intake — all services; mints a job reference, returns the invoice and the mirror pack for johnnyribcage@proton.me
- POST /api/grade — instant forecast grading (Brier + calibration)
- GET/POST /api/screen?address=<solana mint> — deep token screen
- POST /api/verify — single-claim settlement verification
- POST /api/watch — standing-watch registration
- GET /api/data — settled-data catalog (own records only)

An MCP wrapper lives in /mcp-server.
