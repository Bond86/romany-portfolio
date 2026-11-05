"""Download only the verified, owner-supplied public portfolio videos for editing."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/video-tools'))
from yt_dlp import YoutubeDL
import imageio_ffmpeg

videos=json.loads((ROOT/'src/data/videos.json').read_text(encoding='utf-8'))
destination=ROOT/'tmp/showreel/source';destination.mkdir(parents=True,exist_ok=True)
class QuietLogger:
    def debug(self,msg):pass
    def warning(self,msg):pass
    def error(self,msg):print('Video retrieval failed; no authentication or access bypass attempted.',flush=True)
options={'format':'best[ext=mp4][height<=720]/best[height<=720]/best','outtmpl':str(destination/'%(id)s.%(ext)s'),'quiet':True,'no_warnings':True,'noplaylist':True,'logger':QuietLogger(),'socket_timeout':25,'retries':1,'ffmpeg_location':imageio_ffmpeg.get_ffmpeg_exe(),'js_runtimes':{'node':{'path':'node'}},'remote_components':['ejs:github']}
selected=[v for v in videos if v['provider']=='youtube']
if len(sys.argv)>1:selected=[v for v in selected if v['id'] in sys.argv[1:]]
for v in selected:
    if any(p.suffix in ['.mp4','.webm','.mkv'] for p in destination.glob(v['id']+'.*')):print('Already available:',v['id'],flush=True);continue
    try:
        with YoutubeDL(options) as downloader:downloader.download([v['url']])
        print('Downloaded:',v['id'],v['title'],flush=True)
    except Exception:print('Unavailable:',v['id'],flush=True)
