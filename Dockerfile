# Ribcage Agent Services — MCP server (stdio transport)
# Prepared for Glama's automated checks: the image builds the stdio MCP
# wrapper in mcp-server/ and runs it as the container command.
FROM node:20-slim

WORKDIR /app

# Production dependencies first, for layer caching. The lockfile is
# optional in the repo (wildcard keeps the build working without one).
COPY mcp-server/package.json mcp-server/package-lock.json* ./
RUN npm install --omit=dev --no-audit --no-fund

# Server code (server.mjs is the entry point per package.json "main").
COPY mcp-server/ ./

ENV NODE_ENV=production

# MCP over stdio. The server calls the desk's public API; the base URL
# can be overridden at runtime with -e RIBCAGE_BASE=<url>.
CMD ["node", "server.mjs"]
