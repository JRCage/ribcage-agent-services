#!/usr/bin/env node
// Smoke-test a stdio MCP server running in the Ribcage Docker image.
// Usage: node scripts/check-mcp-stdio.mjs [image-name]
import { spawn } from "node:child_process";

const image = process.argv[2] || "ribcage-mcp";
const child = spawn("docker", ["run", "--rm", "-i", image], {
  stdio: ["pipe", "pipe", "pipe"],
});
let output = "";
let errors = "";
let complete = false;
const timeout = setTimeout(() => finish(new Error("Timed out waiting for MCP tools/list")), 20000);

function finish(error) {
  if (complete) return;
  complete = true;
  clearTimeout(timeout);
  child.kill();
  if (error) {
    console.error("MCP inspection failed:", error.message, errors.trim());
    process.exitCode = 1;
  } else {
    console.log("MCP inspection passed: initialize and tools/list responded.");
  }
}
child.on("error", finish);
child.stderr.on("data", chunk => { errors += chunk.toString(); });
child.on("exit", code => {
  if (!complete) finish(new Error(`Docker exited before inspection finished (code ${code})`));
});
function send(message) {
  child.stdin.write(JSON.stringify(message) + "\n");
}
child.stdout.on("data", chunk => {
  output += chunk.toString();
  const lines = output.split("\n");
  output = lines.pop() || "";
  for (const line of lines) {
    if (!line.trim()) continue;
    let response;
    try { response = JSON.parse(line); } catch { continue; }
    if (response.id === 1) {
      if (response.error || !response.result?.protocolVersion) {
        finish(new Error("initialize returned an error or no protocolVersion"));
        return;
      }
      send({ jsonrpc: "2.0", method: "notifications/initialized" });
      send({ jsonrpc: "2.0", id: 2, method: "tools/list", params: {} });
    }
    if (response.id === 2) {
      if (response.error || !Array.isArray(response.result?.tools)) {
        finish(new Error("tools/list returned an error or invalid tools"));
        return;
      }
      console.log(`Discovered ${response.result.tools.length} tools.`);
      finish();
      return;
    }
  }
});
send({
  jsonrpc: "2.0", id: 1, method: "initialize",
  params: {
    protocolVersion: "2025-03-26",
    capabilities: {},
    clientInfo: { name: "ribcage-stdio-smoke-test", version: "1.0.0" },
  },
});
