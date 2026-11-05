import test from 'node:test';
import assert from 'node:assert/strict';
import{readFileSync,existsSync}from'node:fs';
const reel=JSON.parse(readFileSync('src/data/showreel.json','utf8'));
test('the reel is a real one-minute MP4 with all verified source demonstrations',()=>{
 const data=readFileSync(`public/${reel.embedUrl}`);assert.equal(data.subarray(4,8).toString(),'ftyp');assert.ok(data.length<30*1024*1024);
 const mvhd=data.indexOf(Buffer.from('mvhd'));assert.ok(mvhd>0);assert.equal(data[mvhd+4],0);
 const timescale=data.readUInt32BE(mvhd+16);const ticks=data.readUInt32BE(mvhd+20);assert.equal(ticks/timescale,60);
 const edit=JSON.parse(readFileSync('docs/showreel-edit.json','utf8'));assert.equal(edit.frames,1800);assert.equal(edit.cuts.reduce((sum,c)=>sum+c.frames,0),1800);
 const videos=JSON.parse(readFileSync('src/data/videos.json','utf8'));for(const v of videos)assert.ok(edit.cuts.some(c=>c.id===v.id));
 assert.equal(edit.cuts.filter(c=>c.image).length,3);assert.ok(existsSync(`public/${reel.thumbnail}`));
});
