import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs';
import { join } from 'node:path';
const profile=JSON.parse(readFileSync('src/data/profile.json','utf8'));
const projects=JSON.parse(readFileSync('src/data/projects.json','utf8')).filter(p=>p.published);
const base=(process.env.BASE_PATH||'/').replace(/\/?$/,'/');
const origin=process.env.SITE_URL||'https://romanysamir.com';
const routes=[['','Software Engineer & Unity Developer',profile.summary],['about','About',profile.summary],['portfolio','Selected Work','Explore Unity, games, interactive applications and educational technology projects.'],['experience','Experience','The professional career of Romany Samir, from technical support to interactive software and technical direction.'],['skills','Skills','Unity, C#, educational technology, interactive media and technical leadership.'],['videos','Video Library','Verified demonstrations of classroom tools, games, stories and interactive educational content.'],['visual-work','Visual Work','Educational media references on Behance.'],['resume','Résumé','Career history, skills, education and downloadable ATS and professional resumes.'],['contact','Contact','Get in touch with Romany Samir about employment, freelance work and collaboration.'],...projects.map(p=>[`projects/${p.slug}`,p.name,p.summary])];
const escape=s=>s.replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const source=readFileSync('dist/index.html','utf8');
for(const [route,title,description] of routes){
 const url=`${origin}${base}${route}`;
 const project=projects.find(p=>route===`projects/${p.slug}`);
 const jsonld={'@context':'https://schema.org','@type':project?'CreativeWork':'ProfilePage',name:`${title} — Romany Samir`,url,description,mainEntity:project?{'@type':'CreativeWork',name:project.name,description:project.summary,creator:{'@type':'Person',name:profile.name}}:{'@type':'Person',name:profile.name,jobTitle:'Software Engineer / Unity Developer',email:profile.email,sameAs:[profile.links.linkedin,profile.links.youtube]}};
 let html=source.replace(/<title>.*?<\/title>/,`<title>${escape(title)} — Romany Samir</title>`).replace(/<meta name="description"[^>]*\/>/,`<meta name="description" content="${escape(description)}"/>`);
 html=html.replace('</head>',`<link rel="canonical" href="${url}"/><meta property="og:type" content="website"/><meta property="og:title" content="${escape(title)} — Romany Samir"/><meta property="og:description" content="${escape(description)}"/><meta property="og:url" content="${url}"/><meta property="og:image" content="${origin}${base}media/projects/ksa-QGKLWX9nWem.jpg"/><meta name="twitter:card" content="summary_large_image"/><script type="application/ld+json">${JSON.stringify(jsonld).replaceAll('<','\\u003c')}</script></head>`);
 html=html.replace('<div id="root"></div>',`<div id="root"><article style="padding:8%;font-family:system-ui"><h1>${escape(title)}</h1><p>${escape(description)}</p>${project?`<h2>${escape(project.name)}</h2><p>${escape(project.solution)}</p><p>${escape(project.outcome)}</p>`:''}<nav><a href="${base}">Home</a> · <a href="${base}portfolio">Portfolio</a> · <a href="${base}resume">Résumé</a></nav><noscript><p>This site uses JavaScript for its interactive portfolio. Download the <a href="${base}resumes/Romany_Samir_ATS.pdf">ATS résumé</a> or <a href="mailto:${profile.email}">email Romany</a>.</p></noscript></article></div>`);
 const dir=route?join('dist',route):'dist';mkdirSync(dir,{recursive:true});writeFileSync(join(dir,'index.html'),html);
}
copyFileSync('dist/index.html','dist/404.html');
writeFileSync('dist/robots.txt',`User-agent: *\nAllow: /\nSitemap: ${origin}${base}sitemap.xml\n`);
writeFileSync('dist/sitemap.xml',`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${routes.map(([r])=>`<url><loc>${origin}${base}${r}</loc></url>`).join('')}</urlset>`);
writeFileSync('dist/.nojekyll','');
console.log(`Generated ${routes.length} static routes with metadata, sitemap and GitHub Pages fallback.`);
