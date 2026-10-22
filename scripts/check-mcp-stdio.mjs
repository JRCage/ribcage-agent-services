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
    if (response.id === 5) {
      const result = response.result;
      if (response.error || result?.isError !== true ||
          !result.content?.some(item => item.type === "text" && item.text.includes("unknown_argument"))) {
        finish(new Error("Unexpected tool argument was not rejected locally"));
        return;
      }
      console.log("Validated unknown-argument rejection without an upstream call.");
      finish();
      return;
    }
    if (response.id === 4) {
      const result = response.result;
      if (response.error || result?.isError !== true ||
          !result.content?.some(item => item.type === "text" && item.text.includes("invalid_argument"))) {
        finish(new Error("Invalid enum value was not rejected locally"));
        return;
      }
      console.log("Validated invalid-enum rejection without an upstream call.");
      send({ jsonrpc: "2.0", id: 5, method: "tools/call",
        params: { name: "data_catalog", arguments: { unexpected: "value" } } });
      return;
    }
    if (response.id === 3) {
      const result = response.result;
      if (response.error || result?.isError !== true ||
          !result.content?.some(item => item.type === "text" && item.text.includes("missing_required_argument"))) {
        finish(new Error("Invalid tool arguments were not rejected locally"));
        return;
      }
      console.log("Validated missing-argument rejection without an upstream call.");
      send({ jsonrpc: "2.0", id: 4, method: "tools/call",
        params: { name: "validate_packet", arguments: { packet: "sample", tier: "invalid-tier" } } });
      return;
    }
    if (response.id === 2) {
      if (response.error || !Array.isArray(response.result?.tools)) {
        finish(new Error("tools/list returned an error or invalid tools"));
        return;
      }
      const tools = response.result.tools;
      const expected = [
        "validate_packet", "research_memo", "token_screen", "verify_settlement",
        "edit_text", "grade_log", "create_watch", "data_catalog",
      ];
      const names = tools.map(tool => tool.name);
      if (new Set(names).size !== names.length || expected.some(name => !names.includes(name))) {
        finish(new Error(`Unexpected or duplicate MCP tools: ${names.join(", ")}`));
        return;
      }
      if (tools.some(tool => !tool.description || tool.inputSchema?.type !== "object")) {
        finish(new Error("MCP tool descriptions or input schemas are invalid"));
        return;
      }
      console.log(`Validated ${tools.length} MCP tools and schemas.`);
      // Verify invalid calls fail locally rather than reaching the paid upstream API.
      send({ jsonrpc: "2.0", id: 3, method: "tools/call",
        params: { name: "research_memo", arguments: {} } });
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
