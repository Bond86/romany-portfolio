"""Build an exactly 60-second, owner-footage portfolio reel with FFmpeg.

Sources stay in ignored tmp/showreel/source. Requires imageio-ffmpeg, numpy, Pillow.
Use --inspect to render source contact sheets before choosing excerpt positions.
"""
from pathlib import Path
import sys,os,json,re,subprocess,shutil,wave,concurrent.futures
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/video-tools'))
import imageio_ffmpeg
import numpy as np
from PIL import Image,ImageDraw,ImageFont

FFMPEG=os.environ.get('FFMPEG_BINARY') or imageio_ffmpeg.get_ffmpeg_exe()
WORK=ROOT/'tmp/showreel';SOURCES=WORK/'source';WORK.mkdir(parents=True,exist_ok=True)
OUTPUT=ROOT/'public/media/showreel';OUTPUT.mkdir(parents=True,exist_ok=True)
FONT_SOURCE=next((ROOT/'public/fonts').glob('xn7*4jE*'))
shutil.copy2(FONT_SOURCE,WORK/'title.ttf')
FONT=WORK/'title.ttf'

def run(args):
    result=subprocess.run([FFMPEG,'-hide_banner','-y',*map(str,args)],cwd=ROOT,capture_output=True,text=True,errors='replace')
    if result.returncode:raise RuntimeError(result.stderr[-4000:])
    return result.stderr

def duration(path):
    result=subprocess.run([FFMPEG,'-hide_banner','-i',str(path)],capture_output=True,text=True,errors='replace')
    match=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',result.stderr)
    if not match:raise ValueError('Cannot read video duration: '+path.name)
    h,m,s=map(float,match.groups());return h*3600+m*60+s

def source_path(video_id):
    found=[p for p in SOURCES.glob(video_id+'.*') if p.suffix in ['.mp4','.webm','.mkv']]
    if not found:raise FileNotFoundError('Missing verified source '+video_id)
    return found[0]

if '--inspect' in sys.argv:
    videos=json.loads((ROOT/'src/data/videos.json').read_text(encoding='utf-8'))
    rows=[]
    for v in videos:
        try:p=source_path(v['id'])
        except FileNotFoundError:continue
        d=duration(p);row=Image.new('RGB',(960,210),'#f6f4ee');draw=ImageDraw.Draw(row)
        draw.text((8,3),v['id']+' / '+v['title'][:85],fill='#202a29',font=ImageFont.truetype(str(FONT),13))
        for j,fraction in enumerate([.15,.4,.7]):
            shot=WORK/f'{v["id"]}-{j}.jpg'
            run(['-ss',d*fraction,'-i',p,'-frames:v','1','-vf','scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:(ow-iw)/2:(oh-ih)/2',shot])
            row.paste(Image.open(shot),(j*320,25));draw.text((j*320+5,186),f'{d*fraction:.1f}s',fill='#e7ef93',font=ImageFont.truetype(str(FONT),13))
        rows.append(row)
    for page in range((len(rows)+5)//6):
        selected=rows[page*6:(page+1)*6];sheet=Image.new('RGB',(960,210*len(selected)),'white')
        for i,row in enumerate(selected):sheet.paste(row,(0,i*210))
        sheet.save(WORK/f'source-review-{page+1}.jpg',quality=90)
    print('Saved source-review contact sheets.',flush=True);sys.exit(0)

def title_card(path,heading,subtitle,footer):
    im=Image.new('RGB',(1280,720),'#142d27');draw=ImageDraw.Draw(im)
    draw.rectangle((75,80,122,87),fill='#e7ef93')
    draw.text((75,225),heading,font=ImageFont.truetype(str(FONT),86),fill='#fffef9')
    draw.text((80,350),subtitle,font=ImageFont.truetype(str(FONT),30),fill='#c7dfcf')
    draw.line((80,530,1200,530),fill='#476657',width=1)
    draw.text((80,568),footer,font=ImageFont.truetype(str(FONT),23),fill='#e7ef93')
    draw.text((1090,82),'01:00',font=ImageFont.truetype(str(FONT),25),fill='#c7dfcf')
    im.save(path)

title_card(WORK/'intro.png','ROMANY SAMIR','Software Engineer / Unity Developer','MUSEUMS   /   XR   /   EDUCATION   /   GAMES')
title_card(WORK/'outro.png','LET’S BUILD.','Software engineering. Interactive experiences.','romanysamir.com   /   rsks_86@yahoo.com')

# Exact frame counts: intro 60 + Adobe 600 + YouTube 780 + stills 300 + outro 60 = 1800.
cuts=[
 {'still':'intro.png','frames':60,'label':'','detail':''},
 {'id':'PtBtphgHb9n','fraction':.4,'frames':120,'label':'MUSEUM SYSTEMS','detail':'Interactive exhibits / Prophet’s Biography Museum'},
 {'id':'Ctmsq2Uw6HS','fraction':.4,'frames':120,'label':'VIRTUAL EXHIBITIONS','detail':'3D navigation / Interactive content'},
 {'id':'QGKLWX9nWem','fraction':.7,'frames':120,'label':'MOBILE-CONTROLLED 3D MAPS','detail':'Large-display interaction / Unity'},
 {'id':'GYfPDkxUJX9','fraction':.7,'frames':120,'label':'IMMERSIVE EXPLORATION','detail':'VR / Interactive 3D models'},
 {'id':'TxiQpTfssKy','fraction':.4,'frames':120,'label':'3D WALKTHROUGHS','detail':'Navigable spaces / Unity'},
 {'id':'U5lkFF6gRvc','fraction':.15,'frames':60,'label':'PRIME PRESS E-KIT','detail':'Android / Interactive classroom tools'},
 {'id':'5iDkEmcCmVw','fraction':.4,'frames':60,'label':'CLASSROOM TOOLS','detail':'Prime Press E-Kit / V1 demonstration'},
 {'id':'pBzIDb4jhnQ','fraction':.4,'frames':60,'label':'EDUCATIONAL GAMES','detail':'Journeys / Learning through play'},
 {'id':'lKY5Vk5b3k4','fraction':.4,'frames':60,'label':'PHONICS','detail':'Games / Interactive learning content'},
 {'id':'sP_ZczrpTdM','fraction':.4,'frames':60,'label':'STORIES + PUZZLES','detail':'Crime Scene / Interactive activities'},
 {'id':'nPnWZgPQ_1I','fraction':.4,'frames':60,'label':'YOUNG LEARNERS','detail':'Story-based games / Puzzle activities'},
 {'id':'XSZCX61SM8w','fraction':.4,'frames':60,'label':'SOCIAL LEARNING','detail':'Learn while you play'},
 {'id':'eerSTcCXSF0','fraction':.15,'frames':60,'label':'NUMERACY','detail':'Interactive games / Exercises'},
 {'id':'N2zaSRNP0xc','fraction':.4,'frames':60,'label':'SCIENCE TOUR','detail':'Exploration / Educational content'},
 {'id':'_0j8CvajLI0','fraction':.15,'frames':60,'label':'DIGITAL READING','detail':'Interactive HTML5 e-books'},
 {'id':'-2f-1pTzPbU','fraction':.7,'frames':60,'label':'CLASSIC E-BOOKS','detail':'Multimedia reading experiences'},
 {'id':'ZexIK1AG1e0','fraction':.7,'frames':60,'label':'PHONICS + BLENDING','detail':'Stepping Stone / Classroom learning'},
 {'id':'nTWKmcNGJts','fraction':.7,'frames':60,'label':'INTERACTIVE STORIES','detail':'Storyland / Puzzles and games'},
 {'image':'pushcraft-gameplay.jpg','frames':120,'label':'PUSHCRAFT','detail':'Step-based 3D logic puzzles / Gameplay screenshot'},
 {'image':'pushcraft-editor.jpg','frames':90,'label':'BUILD + TEST + SHARE','detail':'Pushcraft / In-game level editor screenshot'},
 {'image':'pushcraft-key-art.jpg','frames':90,'label':'THINK. PUSH. CRAFT.','detail':'Pushcraft / Project key art / In development'},
 {'still':'outro.png','frames':60,'label':'','detail':''}
]
assert sum(c['frames'] for c in cuts)==1800

def render(index_cut):
    index,cut=index_cut;seconds=cut['frames']/30
    if 'id' in cut:
        path=source_path(cut['id']);start=min(max(0,duration(path)*cut['fraction']),max(0,duration(path)-seconds-.2))
        inputs=['-ss',f'{start:.3f}','-i',path]
        cut['sourceStartSeconds']=round(start,3)
    else:
        path=WORK/cut['still'] if 'still' in cut else ROOT/'public/media/projects'/cut['image']
        inputs=['-loop','1','-i',path]
    vf='scale=1280:720:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x142d27,setsar=1,fps=30'
    if 'image' in cut:
        vf+=",zoompan=z='min(zoom+0.00018,1.025)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1280x720:fps=30"
    if cut['label']:
        (WORK/f'label-{index}.txt').write_text(cut['label'],encoding='utf-8')
        (WORK/f'detail-{index}.txt').write_text(cut['detail'],encoding='utf-8')
        vf+=f',drawbox=x=0:y=626:w=1280:h=94:color=0x142d27@0.94:t=fill,drawbox=x=42:y=648:w=5:h=48:color=0xe7ef93:t=fill,drawtext=fontfile=tmp/showreel/title.ttf:textfile=tmp/showreel/label-{index}.txt:fontcolor=white:fontsize=27:x=66:y=641,drawtext=fontfile=tmp/showreel/title.ttf:textfile=tmp/showreel/detail-{index}.txt:fontcolor=0xc7dfcf:fontsize=17:x=66:y=680'
    else:vf+=f',fade=t=in:st=0:d=0.18,fade=t=out:st={seconds-.18}:d=0.18'
    vf+=',format=yuv420p'
    output=WORK/f'cut-{index:02d}.mp4'
    if '--reuse-cuts' in sys.argv and output.exists() and cut.get('still')!='outro.png':
        return output
    run([*inputs,'-an','-vf',vf,'-frames:v',cut['frames'],'-c:v','libx264','-preset','fast','-crf','21','-maxrate','4M','-bufsize','8M','-threads','2','-video_track_timescale','15360',output])
    print(f'Rendered {index+1}/{len(cuts)}: {cut.get("label") or cut.get("still")}',flush=True)
    return output

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:segments=list(pool.map(render,enumerate(cuts)))
(WORK/'concat.txt').write_text('\n'.join("file '"+p.as_posix()+"'" for p in segments),encoding='utf-8')

# Original synthesized instrumental pulse. No third-party recording or source-video audio.
sr=44100;t=np.arange(sr*60)/sr;rng=np.random.default_rng(20261105);audio=np.zeros(t.shape,dtype=np.float64)
for beat in np.arange(0,60,.5):
    start=int(beat*sr);n=min(int(.22*sr),len(audio)-start);q=np.arange(n)/sr
    phase=2*np.pi*(48*q+65*.025*(1-np.exp(-q/.025)))
    audio[start:start+n]+=.34*np.sin(phase)*np.exp(-q*22)
for beat in np.arange(.25,60,.25):
    start=int(beat*sr);n=min(int(.045*sr),len(audio)-start);q=np.arange(n)/sr
    audio[start:start+n]+=.038*rng.standard_normal(n)*np.exp(-q*100)
for beat in np.arange(.5,60,1):
    start=int(beat*sr);n=min(int(.11*sr),len(audio)-start);q=np.arange(n)/sr
    audio[start:start+n]+=.075*rng.standard_normal(n)*np.exp(-q*40)
chords=[[220,261.626,329.628],[174.614,220,261.626],[196,246.942,293.665],[164.814,220,261.626]]
for i in range(15):
    start=i*4*sr;n=min(4*sr,len(audio)-start);q=np.arange(n)/sr;envelope=np.minimum(q/.4,1)*np.minimum((4-q)/.5,1)
    for note in chords[i%4]:audio[start:start+n]+=.025*np.sin(2*np.pi*note*q)*envelope
audio*=np.minimum(t/.35,1)*np.minimum((60-t)/.7,1)
pcm=(np.clip(audio,-.95,.95)*32767).astype('<i2')
with wave.open(str(WORK/'original-score.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
final=OUTPUT/'romany-samir-showreel.mp4'
run(['-f','concat','-safe','0','-i',WORK/'concat.txt','-i',WORK/'original-score.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-ac','2','-t','60','-movflags','+faststart',final])
assert abs(duration(final)-60)<.06
run(['-v','error','-xerror','-i',final,'-f','null','-'])
manifest={'durationSeconds':60,'frames':1800,'fps':30,'resolution':'1280x720','audio':'Original code-synthesized instrumental pulse; source audio removed','cuts':cuts,'note':'Pushcraft uses explicitly labeled gameplay/editor stills and project key art, not a claimed gameplay recording.'}
(ROOT/'docs/showreel-edit.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for second in [2.5,10.5,23,38,49,53]:run(['-ss',second,'-i',final,'-frames:v','1',WORK/f'final-{second}.jpg'])
poster=Image.new('RGB',(1280,720),'#142d27')
for i,second in enumerate([2.5,10.5,23,38,49,53]):
    im=Image.open(WORK/f'final-{second}.jpg');im=im.resize((426,240),Image.Resampling.LANCZOS);poster.paste(im,((i%3)*426,(i//3)*240))
draw=ImageDraw.Draw(poster);draw.rectangle((0,480,1280,720),fill='#142d27');draw.text((58,523),'ROMANY SAMIR',font=ImageFont.truetype(str(FONT),57),fill='#fffef9');draw.text((60,614),'60-SECOND SHOWREEL / SELECTED WORK',font=ImageFont.truetype(str(FONT),25),fill='#e7ef93')
poster.save(OUTPUT/'romany-samir-showreel-poster.jpg',quality=92,optimize=True)
review=Image.new('RGB',(1280,720),'white')
for i,second in enumerate([2.5,10.5,23,38,49,53]):review.paste(Image.open(WORK/f'final-{second}.jpg').resize((426,360)),((i%3)*426,(i//3)*360))
review.save(WORK/'final-review.jpg',quality=92)
print(f'FINAL: {final}; 60.00 seconds; {final.stat().st_size/1024/1024:.1f} MiB; full decode passed.',flush=True)
