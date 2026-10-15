import assert from 'node:assert/strict';
import {abi} from 'genlayer-js';
const {calldata}=abi;
for(const [name,args] of [['register',['n','A rubric defining the intended classification.','has.fire']],
 ['synthesize',['search','a'.repeat(64)]],['test_input',['check','a'.repeat(64),'A fire drill next week.']],
 ['classify_guarded',['a'.repeat(64),'b'.repeat(64),'A real fire now!']]]){
 const encoded=calldata.encode(calldata.makeCalldataObject(name,args,{}));
 assert.deepEqual(calldata.encode(calldata.decode(encoded)),encoded);
}
console.log('4 SDK calldata roundtrips passed');
