// Run from any directory after installing the dependency in tools/: npm install.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const file=path.join(root,'data/atlas.json'),data=JSON.parse(fs.readFileSync(file,'utf8'));
const documents=[];
function walk(dir){for(const f of fs.readdirSync(dir,{withFileTypes:true})){const filename=path.join(dir,f.name);if(f.isDirectory())walk(filename);else if(f.name.endsWith('.md')){const raw=fs.readFileSync(filename,'utf8'),rel=path.relative(root,filename).replaceAll('\\','/');let html=marked.parse(raw,{gfm:true});html=html.replace(/href="([^"#][^"]*)"/g,(m,url)=>/^(https?:|mailto:)/.test(url)?m:'href="'+path.posix.normalize(path.posix.join(path.posix.dirname(rel),url))+'"');documents.push({path:rel,title:raw.match(/^#\s+(.+)/m)?.[1]||f.name,html});}}}
walk(path.join(root,'knowledge'));walk(path.join(root,'pedagogie'));data.documents=documents;
for(const g of data.graphs){const b=data.branches.find(b=>b.name===g.branch);for(const item of [...g.nodes,...g.edges]){if(!item.sourceUrl.includes('/blob/'+b.sha+'/'))throw Error('Mismatched branch: '+item.path);const lines=fs.readFileSync(path.join(root,'doxygen/snapshots',b.key,item.path),'utf8').split(/\r?\n/);if(item.start<1||item.end>lines.length||item.end<item.start)throw Error('Invalid source lines: '+item.path);item.snippet=lines.slice(item.start-1,Math.min(item.end,item.start+31)).map((l,i)=>String(item.start+i).padStart(4)+'  '+l).join('\n');}}
fs.writeFileSync(file,JSON.stringify(data,null,2));fs.writeFileSync(path.join(root,'assets/data.js'),'window.FEZ_DATA = '+JSON.stringify(data)+';\n');console.log('Refreshed '+documents.length+' documents; source references checked.');
