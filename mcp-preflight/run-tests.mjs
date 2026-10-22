import { spawnSync } from 'node:child_process';
const cases = [['normal',0],['paged',0],['repeat',1],['duplicate',1],['invalid',1],['nulltool',1]];
let failures=0;
for (const [mode,expected] of cases){
 const run=spawnSync(process.execPath,['check.mjs','--',process.execPath,'fixture.mjs',mode],{cwd:new URL('.',import.meta.url),encoding:'utf8',timeout:15000});
 const data=JSON.parse(run.stdout);
 const pass=run.status===expected && data.ok===(expected===0);
 console.log(`${pass?'PASS':'FAIL'} ${mode}: exit=${run.status}`);
 if(!pass) failures++;
}
process.exitCode=failures?1:0;
