import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import assert from 'node:assert/strict';
const base=process.env.BASE_PATH||'/';
function walk(p){return readdirSync(p,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(join(p,e.name)):[join(p,e.name)]);}
const files=walk('dist');
const html=files.filter(f=>f.endsWith('.html')&&!f.endsWith('404.html'));
const projects=JSON.parse(readFileSync('src/data/projects.json','utf8')).filter(p=>p.published);
assert.equal(html.length,9+projects.length);
for(const file of html){
 const s=readFileSync(file,'utf8');
 assert.match(s,/<title>[^<]+<\/title>/);assert.match(s,/rel="canonical"/);assert.match(s,/application\/ld\+json/);
 for(const match of s.matchAll(/(?:src|href)="([^"#]+)"/g)){
  const url=match[1];if(!url.startsWith(base)||url.startsWith('http'))continue;
  const local=join('dist',url.slice(base.length));
  assert.ok(existsSync(local)||existsSync(join(local,'index.html')),`Missing ${url} from ${file}`);
 }
}
for(const f of files.filter(f=>f.endsWith('.js'))){const s=readFileSync(f,'utf8');assert.ok(!s.includes('private-audio-archive'));assert.ok(!s.includes('YOUTUBE_API_KEY'));}
assert.ok(existsSync('dist/sitemap.xml'));assert.ok(existsSync('dist/404.html'));
console.log(`Verified ${html.length} static routes, metadata, local asset links, PDFs and withheld-content exclusion at base ${base}`);
