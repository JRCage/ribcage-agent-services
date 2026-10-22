// Pure argument validation shared by the MCP runtime and dependency-free tests.
export function validateToolArguments(definition, args) {
  if (!definition) return { error: "unknown_tool" };
  if (args === null || typeof args !== "object" || Array.isArray(args)) {
    return { error: "invalid_arguments", message: "Expected an object" };
  }
  for (const field of definition.inputSchema.required || []) {
    if (!(field in args) || args[field] === null || args[field] === "") {
      return { error: "missing_required_argument", field };
    }
  }
  for (const [field, value] of Object.entries(args)) {
    const schema = definition.inputSchema.properties[field];
    if (!schema) return { error: "unknown_argument", field };
    const validType = schema.type === "array" ? Array.isArray(value) : typeof value === schema.type;
    if (!validType || (schema.enum && !schema.enum.includes(value))) {
      return { error: "invalid_argument", field };
    }
  }
  return null;
}
