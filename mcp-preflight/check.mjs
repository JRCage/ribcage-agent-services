#!/usr/bin/env node
// MCP stdio smoke test. Node 22+. Usage: node check.mjs -- node server.mjs
import { spawn } from 'node:child_process';
const args = process.argv.slice(2);
if (args[0] === '--') args.shift();
if (!args.length) { console.error('Usage: node check.mjs -- <server command> [args]'); process.exit(2); }
const child = spawn(args[0], args.slice(1), { stdio: ['pipe','pipe','pipe'], shell: false });
let buffer = '', seq = 0, done = false;
const failures = [];
const results = [];
const names = new Set();
const cursors = new Set();
let pages = 0;
let toolCount = 0;
const deadline = setTimeout(() => finish('timeout'), 8000);
child.on('error', e => finish('spawn: ' + e.message));
child.on('exit', (code) => { if (!done) finish('server exited: ' + code); });
function send(method, params, id) {
  const obj = {jsonrpc:'2.0',method,...(params ? {params}:{}),...(id ? {id}: {})};
  child.stdin.write(JSON.stringify(obj) + '\n');
}
function finish(error) {
  if (done) return;
  done = true; clearTimeout(deadline);
  if (error) failures.push(error);
  child.kill();
  console.log(JSON.stringify({ok: failures.length===0,results,failures},null,2));
  process.exitCode = failures.length ? 1 : 0;
}
send('initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'rowan-preflight',version:'0.1.0'}},++seq);
child.stdout.setEncoding('utf8');
child.stdout.on('data', chunk => {
  buffer += chunk;
  if (buffer.length > 1024*1024) return finish('response exceeds 1 MiB');
  while (buffer.includes('\n') && !done) {
    const i=buffer.indexOf('\n'), line=buffer.slice(0,i).trim(); buffer=buffer.slice(i+1);
    if (!line) continue;
    let msg; try {msg=JSON.parse(line)} catch {return finish('non-JSON stdout');}
    if (msg.id===1) {
      if (msg.error || !msg.result?.protocolVersion) return finish('initialize failed');
      results.push('initialize');
      send('notifications/initialized');
      send('tools/list',{},++seq);
    } else if (msg.id===2) {
      if (msg.error || !Array.isArray(msg.result?.tools)) return finish('tools/list failed');
      pages++;
      if (pages > 100) return finish('too many tool pages');
      for (const t of msg.result.tools) {
        if (typeof t.name!=='string' || !t.name || !t.inputSchema || t.inputSchema.type!=='object') failures.push('invalid tool descriptor');
        if (names.has(t.name)) failures.push('duplicate tool: '+t.name);
        names.add(t.name);
        toolCount++;
      }
      const cursor=msg.result.nextCursor;
      if (cursor !== undefined && cursor !== null && cursor !== '') {
        if (typeof cursor !== 'string' || cursors.has(cursor)) return finish('invalid or repeated pagination cursor');
        cursors.add(cursor);
        send('tools/list',{cursor},2);
      } else {
        results.push('tools/list: '+toolCount+' tools across '+pages+' pages');
        finish();
      }
    }
  }
});
