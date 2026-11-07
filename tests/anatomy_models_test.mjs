import assert from 'node:assert/strict';
import {uencLayout,allocate} from '../workers/anatomies/models.mjs';
assert.deepEqual([0,1,65535,65536,65537,131072].map(n=>uencLayout(n).total),[30,31,65565,65566,65583,131118]);
assert.equal(uencLayout(0).chunks,1);assert.equal(uencLayout(65536).chunks,1);
assert.throws(()=>uencLayout(-1));assert.throws(()=>uencLayout(1.5));
const a=allocate(100000n);assert.deepEqual([a.tax,a.bonus,a.cash,a.rnd,a.assets],[15000n,850n,28050n,28050n,28050n]);
assert.equal(allocate(100000n,4200000n).tax,20000n);
for(const surplus of [0n,1n,2n,3n,99n,12345n,4249999n,4250001n,10000000n])for(const ytd of [0n,4249900n,4250000n,9000000n]){
 const r=allocate(surplus,ytd);assert.equal(r.tax+r.bonus+r.cash+r.rnd+r.assets,surplus);assert.equal(r.rnd,r.assets);assert.ok(r.cash-r.rnd<=2n);
}
assert.throws(()=>allocate(18446744073709551615n,1n));assert.throws(()=>allocate(-1n));
console.log('UENC : tailles et blocs limites OK. Répartition : conservation exacte et seuils OK.');
