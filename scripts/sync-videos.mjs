// Official API only. A failed update leaves the committed manifest intact.
import { readFileSync, writeFileSync, renameSync } from 'node:fs';
const key=process.env.YOUTUBE_API_KEY;
const channel='UCJNeiaYepn7LC_0E9RxK5JA';
if(!key){console.log('No YOUTUBE_API_KEY configured; retaining the verified local manifest.');process.exit(0);}
const path='src/data/videos.json';
async function api(endpoint,params){const u=new URL(`https://www.googleapis.com/youtube/v3/${endpoint}`);Object.entries({...params,key}).forEach(([k,v])=>u.searchParams.set(k,v));const r=await fetch(u);if(!r.ok)throw Error(`YouTube API returned ${r.status}`);return r.json();}
try{
 const existing=JSON.parse(readFileSync(path,'utf8'));
 const channelData=await api('channels',{part:'contentDetails',id:channel});
 const playlist=channelData.items?.[0]?.contentDetails?.relatedPlaylists?.uploads;
 if(!playlist)throw Error('Uploads playlist unavailable');
 const list=await api('playlistItems',{part:'snippet',playlistId:playlist,maxResults:'50'});
 const discovered=new Map(list.items.map(x=>[x.snippet.resourceId.videoId,x.snippet]));
 // Only refresh existing approved mappings. Review new videos before publishing.
 const updated=existing.map(v=>{const s=discovered.get(v.id);return s?{...v,title:s.title,description:s.description,published:s.publishedAt}:v;});
 writeFileSync(`${path}.tmp`,JSON.stringify(updated,null,2)+'\n');renameSync(`${path}.tmp`,path);
 console.log(`Updated ${updated.length} approved videos. New channel uploads require editorial mapping.`);
}catch(error){console.error(`Update skipped: ${error.message}. Existing manifest preserved.`);process.exitCode=1;}
