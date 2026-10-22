// MCP wrapper: the same endpoints, in tool-calling form. Discovery asset —
// payment and fulfillment still run through the desk's invoice + intake flow.
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
const BASE = process.env.RIBCAGE_BASE || "https://ribcage-agent-services.pages.dev";
async function call(path, payload, method = "POST") {
  try {
    const r = await fetch(BASE + path, {
      method,
      headers: { "content-type": "application/json" },
      body: method === "POST" ? JSON.stringify(payload || {}) : undefined,
      signal: AbortSignal.timeout(15000),
    });
    const raw = await r.text();
    let body;
    try { body = raw ? JSON.parse(raw) : {}; }
    catch { body = { error: "invalid_api_response", message: "Upstream returned non-JSON content" }; }
    return { status: r.status, body };
  } catch (error) {
    return { status: 503, body: { error: "upstream_unavailable", message: String(error?.message || error) } };
  }
}
const tools = [
  { name: "validate_packet", description: "Queue a packet (up to 40 claims) for primary-source validation with receipts. $0.25/packet; free evaluation tier 10 calls/day.", inputSchema: { type: "object", properties: { packet: { type: "string" }, contact: { type: "string" }, tier: { type: "string", enum: ["paid", "eval"] } }, required: ["packet"] } },
  { name: "research_memo", description: "Queue a scoped research memo. From $2.00; scope and price quoted before any charge.", inputSchema: { type: "object", properties: { question: { type: "string" }, contact: { type: "string" } }, required: ["question"] } },
  { name: "token_screen", description: "Deep Solana token screen from public data with raw receipts. $0.10; cached repeat 15 min $0.02.", inputSchema: { type: "object", properties: { address: { type: "string" } }, required: ["address"] } },
  { name: "verify_settlement", description: "Verify a single Kalshi/Polymarket settlement claim against the venue print. $0.05; out-of-scope free.", inputSchema: { type: "object", properties: { venue: { type: "string" }, market: { type: "string" }, claimed_outcome: { type: "string" } }, required: ["venue", "market"] } },
  { name: "edit_text", description: "Editing of human-facing text. Standard $5.00/1,000 words; deep $15.00/1,000 words.", inputSchema: { type: "object", properties: { text: { type: "string" }, level: { type: "string", enum: ["standard", "deep"] }, contact: { type: "string" } }, required: ["text"] } },
  { name: "grade_log", description: "Grade a prediction log instantly: Brier score + calibration. $0.50/log up to 500; one log up to 50 free.", inputSchema: { type: "object", properties: { predictions: { type: "array" } }, required: ["predictions"] } },
  { name: "create_watch", description: "Register a standing watch ($1.00/month; one free 7 days). Fires once per change with old/new/source/timestamp.", inputSchema: { type: "object", properties: { type: { type: "string" }, target: { type: "string" }, cadence: { type: "string" }, notify: { type: "string" } }, required: ["type", "target"] } },
  { name: "data_catalog", description: "Settled-data catalog: our own graded records only; venue data excluded on venue terms.", inputSchema: { type: "object", properties: {} } }
];
const server = new Server({ name: "ribcage-agent-services", version: "1.0.0" }, { capabilities: { tools: {} } });
server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools }));
server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: a = {} } = req.params; let out;
  const definition = tools.find(tool => tool.name === name);
  if (!definition) {
    return { isError: true, content: [{ type: "text", text: JSON.stringify({ error: "unknown_tool" }) }] };
  }
  if (a === null || typeof a !== "object" || Array.isArray(a)) {
    return { isError: true, content: [{ type: "text", text: JSON.stringify({ error: "invalid_arguments", message: "Expected an object" }) }] };
  }
  for (const field of definition.inputSchema.required || []) {
    if (!(field in a) || a[field] === null || a[field] === "") {
      return { isError: true, content: [{ type: "text", text: JSON.stringify({ error: "missing_required_argument", field }) }] };
    }
  }
  for (const [field, value] of Object.entries(a)) {
    const schema = definition.inputSchema.properties[field];
    if (!schema) {
      return { isError: true, content: [{ type: "text", text: JSON.stringify({ error: "unknown_argument", field }) }] };
    }
    const validType = schema.type === "array" ? Array.isArray(value) : typeof value === schema.type;
    if (!validType || (schema.enum && !schema.enum.includes(value))) {
      return { isError: true, content: [{ type: "text", text: JSON.stringify({ error: "invalid_argument", field }) }] };
    }
  }
  if (name === "token_screen") out = await call("/api/screen?address=" + encodeURIComponent(a.address), null, "GET");
  else if (name === "verify_settlement") out = await call("/api/verify", a);
  else if (name === "grade_log") out = await call("/api/grade", a);
  else if (name === "create_watch") out = await call("/api/watch", a);
  else if (name === "data_catalog") out = await call("/api/data", null, "GET");
  else if (name === "validate_packet") out = await call("/api/intake", { service: "packet_validation", details: a.packet, contact: a.contact || "", tier: a.tier || "eval" });
  else if (name === "research_memo") out = await call("/api/intake", { service: "research", details: a.question, contact: a.contact || "", tier: "paid" });
  else if (name === "edit_text") out = await call("/api/intake", { service: a.level === "deep" ? "editing_deep" : "editing_standard", details: a.text, contact: a.contact || "", tier: "paid", word_count: (a.text || "").split(/\s+/).filter(Boolean).length });
  else out = { status: 404, body: { error: "unknown_tool" } };
  return { isError: out.status >= 400, content: [{ type: "text", text: JSON.stringify(out.body, null, 2) }] };
});
await server.connect(new StdioServerTransport());
