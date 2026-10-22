import assert from "node:assert/strict";
import { test } from "node:test";
import { validateToolArguments } from "../mcp-server/validate-arguments.mjs";

const definition = {
  name: "sample",
  inputSchema: {
    type: "object",
    required: ["packet"],
    properties: {
      packet: { type: "string" },
      tier: { type: "string", enum: ["eval", "paid"] },
      predictions: { type: "array" },
    },
  },
};

test("accepts valid required and optional arguments", () => {
  assert.equal(validateToolArguments(definition, { packet: "hello", tier: "eval", predictions: [] }), null);
});
test("rejects unknown tool", () => {
  assert.deepEqual(validateToolArguments(undefined, {}), { error: "unknown_tool" });
});
test("rejects non-object arguments", () => {
  for (const value of [null, [], "string", 1]) {
    assert.equal(validateToolArguments(definition, value).error, "invalid_arguments");
  }
});
test("rejects absent and empty required fields", () => {
  for (const args of [{}, { packet: "" }, { packet: null }]) {
    assert.deepEqual(validateToolArguments(definition, args), { error: "missing_required_argument", field: "packet" });
  }
});
test("rejects invalid type and enum", () => {
  for (const args of [{ packet: 1 }, { packet: "ok", tier: "other" }, { packet: "ok", predictions: {} }]) {
    assert.equal(validateToolArguments(definition, args).error, "invalid_argument");
  }
});
test("rejects unexpected arguments", () => {
  assert.deepEqual(validateToolArguments(definition, { packet: "ok", extra: 1 }), { error: "unknown_argument", field: "extra" });
});
