import fs from 'node:fs';
import crypto from 'node:crypto';
import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
export const canonical=x=>x===null||typeof x!=='object'?JSON.stringify(x).replace(/[\u007f-\uffff]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0')):
 Array.isArray(x)?'['+x.map(canonical).join(',')+']':'{'+Object.keys(x).sort().map(k=>canonical(k)+':'+canonical(x[k])).join(',')+'}';
export const digest=x=>crypto.createHash('sha256').update(canonical(x)).digest('hex');
export async function rpc(method,params){
 const r=await fetch('https://studio.genlayer.com/api',{method:'POST',headers:{'content-type':'application/json'},
  body:JSON.stringify({jsonrpc:'2.0',id:1,method,params}),signal:AbortSignal.timeout(20000)});
 if(!r.ok)throw Error('HTTP failure');const p=await r.json();if(p.error||p.result==null)throw Error('RPC read failed');return p.result;
}
if(process.argv[1]?.endsWith('check.mjs'))try{
 const [mode,value,extra]=process.argv.slice(2);
 if(mode==='source'){
  const normalize=x=>x.replace(/\r\n/g,'\n').trimEnd()+'\n';
  const remote=normalize(Buffer.from(await rpc('gen_getContractCode',[value]),'base64').toString('utf8'));
  const local=normalize(fs.readFileSync('contracts/CounterexampleCircuitBreaker.py','utf8'));
  console.log(JSON.stringify({address:value,source_matches:remote===local,source_sha256:crypto.createHash('sha256').update(remote).digest('hex')}));
  if(remote!==local)process.exitCode=1;
 }else if(mode==='nonce'){
  console.log(JSON.stringify({address:value,latest:await rpc('eth_getTransactionCount',[value,'latest']),pending:await rpc('eth_getTransactionCount',[value,'pending'])}));
 }else if(mode==='state'){
  const client=createClient({chain:studionet});
  const read=(functionName,args)=>client.readContract({address:value,functionName,args});
  const key=digest({contract:value,author:extra,nonce:'fire-demo'});
  const item=await read('get_implementation',[key]);
  if(digest(item.spec)!==item.spec_root)throw Error('Specification root mismatch');
  const trials=[];
  for(const nonce of ['match-demo','unknown-demo','synth-demo']){
   const id=digest({contract:value,challenger:extra,nonce});let trial;
   try{trial=await read('get_trial',[id]);}catch{trials.push({nonce,missing:true});continue;}
   const {root,...body}=trial;
   if(digest(body)!==root||trial.report.binding.implementation!==key||trial.report.binding.spec_root!==item.spec_root)throw Error('Trial binding/root');
   trials.push({nonce,id,...trial});
  }
  let guarded_disabled=false;
  try{await read('classify_guarded',[key,item.spec_root,'There is a real fire here!']);}catch{guarded_disabled=true;}
  if((item.state==='FALSIFIED')!==guarded_disabled)throw Error('Guard mismatch');
  console.log(JSON.stringify({address:value,implementation_id:key,...item,trials,guarded_disabled}));
 }else if(['success','error'].includes(mode)){
  let tx=await rpc('eth_getTransactionByHash',[value]);
  for(let i=0;tx.status!=='FINALIZED'&&i<15;i++){await new Promise(r=>setTimeout(r,2000));tx=await rpc('eth_getTransactionByHash',[value]);}
  const leader=tx.consensus_data?.leader_receipt?.find(x=>x.mode==='leader');
  const raw=leader?.genvm_result?.stderr||leader?.result;
  const decoded=typeof raw!=='string'?'':(/^[A-Za-z0-9+/]*={0,2}$/.test(raw)&&raw.length%4===0?Buffer.from(raw,'base64').toString('utf8'):raw);
  console.log(JSON.stringify({hash:value,address:tx.to_address??tx.to,status:tx.status,execution:leader?.execution_result,
   consensus:tx.result_name,...(extra?{expected_error_matched:decoded.includes(extra)}:{})}));
  if(tx.status!=='FINALIZED'||leader?.execution_result!==(mode==='error'?'ERROR':'SUCCESS')||tx.result_name!=='MAJORITY_AGREE'||(extra&&!decoded.includes(extra)))process.exitCode=1;
 }else throw Error('Unknown mode');
}catch{console.error('Sanitized read failed; inspect history before rebroadcast');process.exitCode=1;}
