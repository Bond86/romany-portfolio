import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
const load=p=>JSON.parse(readFileSync(`src/data/${p}.json`,'utf8'));
const projects=load('projects'),videos=load('videos'),profile=load('profile');
test('published content does not expose withheld projects',()=>{
 assert.ok(projects.every(p=>p.published));
 assert.ok(!projects.some(p=>['private-audio-archive','bible-reading-app','dynamic-ui'].includes(p.slug)));
 assert.equal(new Set(projects.map(p=>p.slug)).size,projects.length);
});
test('all media mappings resolve to published projects and local images',()=>{
 for(const v of videos){assert.match(v.id,/^[\w-]{11}$/);assert.ok(projects.some(p=>p.slug===v.project));assert.ok(existsSync(`public/${v.thumbnail}`));assert.ok(!Number.isNaN(Date.parse(v.published)));}
 for(const p of projects)for(const id of p.videos)assert.ok(videos.some(v=>v.id===id));
});
test('career progression and qualification safeguards remain intact',()=>{
 assert.equal(profile.experience.filter(e=>e.company==='Prime Press Egypt').length,2);
 for(const employer of ['TE Data','Future Academy','Elkhalig for Trade and Import'])assert.ok(profile.experience.some(e=>e.company===employer));
 assert.match(profile.education[0].qualification,/studies/);assert.match(profile.education[0].note,/unconfirmed/);
 assert.equal(profile.certifications.length,7);
 assert.equal(projects.find(p=>p.slug==='pushcraft').status,'In development');
});
test('generated resumes are real PDF downloads',()=>{
 for(const name of ['Romany_Samir_ATS','Romany_Samir_Professional']){const data=readFileSync(`public/resumes/${name}.pdf`);assert.equal(data.subarray(0,5).toString(),'%PDF-');assert.match(data.toString('latin1'),/%%EOF/);assert.equal((data.toString('latin1').match(/\/Type \/Page\b/g)||[]).length,3);}
});
