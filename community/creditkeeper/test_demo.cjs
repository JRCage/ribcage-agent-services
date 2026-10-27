const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync('demo/index.html', 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length, 1);
assert.doesNotMatch(html, /<(?:script|link|img|iframe)[^>]+(?:src|href)\s*=/i);
assert.doesNotMatch(html, /\b(?:fetch|XMLHttpRequest|WebSocket|sendBeacon|localStorage|sessionStorage|innerHTML)\b/);
let callback;
const elements = { expected: {}, posted: {}, result: {}, calculate: {
  addEventListener(event, fn) { assert.equal(event, 'click'); callback = fn; }
}};
vm.runInNewContext(scripts[0][1], {document: {getElementById: id => elements[id]}, Intl}, {timeout: 1000});
const cases = [
 ['75','25','Unmatched expected credit: $50.00'],
 ['25','75','Suspected excess credit: $50.00'],
 ['75','75','Expected and posted credits balance in these figures.'],
 ['0','0','Expected and posted credits balance in these figures.'],
 ['1000000.00','0','Unmatched expected credit: $1,000,000.00'],
 ['1000000.01','0','Enter amounts no greater than $1,000,000.00.'],
 ['0','9999999','Enter amounts no greater than $1,000,000.00.'],
 ['75.004','0','Enter nonnegative dollar amounts with up to two decimal places.'],
 ['-1','0','Enter nonnegative dollar amounts with up to two decimal places.'],
 ['','0','Enter nonnegative dollar amounts with up to two decimal places.'],
 ['<img>','0','Enter nonnegative dollar amounts with up to two decimal places.'],
];
for (const [a,b,want] of cases) {
 elements.expected.value=a; elements.posted.value=b; callback();
 assert.equal(elements.result.textContent,want,`${a} / ${b}`);
}
console.log(`${cases.length} demo behavior cases and static privacy checks passed`);
