// Public fixture arguments only. Signing remains inside the native CLI.
const {spawnSync}=require('node:child_process'),fs=require('node:fs'),path=require('node:path');
const [action,address,key]=process.argv.slice(2);
if(!/^0x[0-9a-fA-F]{40}$/.test(address??''))throw Error('Contract address required');
const demo=JSON.parse(fs.readFileSync(path.join(__dirname,'../examples/demo.json'),'utf8'));
const actions={
 register:['register','fire-demo',demo.rubric,demo.program],
 match:['test_input','match-demo',key,demo.matching_input],
 unknown:['test_input','unknown-demo',key,demo.ambiguous_input],
 synthesize:['synthesize','synth-demo',key],
 terminal:['test_input','post-falsification',key,demo.matching_input],
 replay:['test_input','match-demo',key,demo.matching_input]
};
if(!actions[action]||(action!=='register'&&!/^[0-9a-f]{64}$/.test(key??'')))throw Error('Invalid documented action');
const [method,...args]=actions[action];
const result=spawnSync(process.execPath,[path.join(__dirname,'run-cli.cjs'),'write',address,method,'--args',...args],
 {stdio:'inherit',windowsHide:true});
process.exitCode=result.status??1;
