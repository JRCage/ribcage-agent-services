# MCP Preflight

A small, dependency-free, Node.js 22+ smoke test for local stdio MCP servers. It launches the specified command, sends `initialize`, then `notifications/initialized` and `tools/list`. It checks that the server returns an initialization result and tool descriptors with unique names and object input schemas. It follows `tools/list` pagination through `nextCursor` and rejects repeated cursors (up to 100 pages). It does **not** invoke tools, send credentials, scan for vulnerabilities, or certify compatibility.

```sh
node mcp-preflight/check.mjs -- node path/to/your-mcp-server.mjs
```

Prints a JSON report and exits 0 on pass or 1 on failure. Timeout is eight seconds. The child server may execute its own startup logic, so run only trusted server commands in an appropriate test environment.

For the tested, expanded v0.2 ZIP and optional fixed-price review, see [MCP Preflight service](../MCP-PREFLIGHT-SERVICE.md).

License: MIT, consistent with the repository license where applicable.

## Regression tests

Run `node mcp-preflight/run-tests.mjs` from the repository root (or `node run-tests.mjs` from this directory). Five cases cover normal operation, pagination, repeated cursors, duplicate tool names, and invalid schemas. Expected failures are treated as passing tests. Five scenarios were previously tested locally; the current GitHub Actions workflow has not yet been independently confirmed passing.
