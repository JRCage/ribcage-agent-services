# Glama verification checklist

This repository provides a stdio MCP server in `mcp-server/server.mjs`.

## Source and container
- GitHub repository: https://github.com/JRCage/ribcage-agent-services
- Dockerfile: repository root `Dockerfile`
- MCP startup command: `node server.mjs` (the Docker image sets `WORKDIR /app`)
- Metadata: `glama.json` at repository root
- The server supports `initialize` and `tools/list` over stdio. Tool calls to the public API require network access; introspection does not.

## Required external steps
1. Open https://glama.ai/mcp/servers and search for this repository.
2. If missing, submit the repository URL using Glama's **Add Server** workflow.
3. Add the root Dockerfile directly to Glama when prompted, as required by the awesome-mcp-servers maintainer.
4. Run Glama's inspection. Confirm the server starts and `tools/list` succeeds. Do not claim success from source inspection alone.
5. Copy the **actual** Glama server path and badge URL from the accepted listing.
6. Edit https://github.com/punkpeye/awesome-mcp-servers/pull/17059 to add the badge after the description, then respond to the maintainer's verification request.

## Local smoke test
```sh
docker build -t ribcage-mcp .
docker run --rm -i ribcage-mcp
```
Use an MCP inspector or JSON-RPC stdio client to issue `initialize` followed by `tools/list`. A running process by itself is not a passed MCP inspection.

**Status:** This checklist does not establish that Glama verification has been completed or that the listing is approved.
