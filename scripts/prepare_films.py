"""Create web-ready H.264 films from approved source downloads.
Run: python3 scripts/prepare_films.py /path/to/source-directory /path/to/ffmpeg
"""
from pathlib import Path
import subprocess,sys
source=Path(sys.argv[1]);ffmpeg=sys.argv[2]
out=Path(__file__).resolve().parent.parent/'preview/assets/films'
out.mkdir(parents=True,exist_ok=True)
for name in (sys.argv[3:] or ['main','the-need','work-begins','taking-shape','the-handover']):
    target=out/(name+'.mp4')
    probe=subprocess.run([ffmpeg,'-hide_banner','-i',str(source/(name+'.mp4'))],capture_output=True,text=True)
    hdr='arib-std-b67' in probe.stderr or 'smpte2084' in probe.stderr
    color='zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,' if hdr else ''
    subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(source/(name+'.mp4')),
        '-map','0:v:0','-map','0:a:0?','-vf',
        color+'scale=1280:1280:force_original_aspect_ratio=decrease:force_divisible_by=2,fps=30',
        '-c:v','libx264','-threads','4','-preset','medium','-crf','25','-maxrate','1800k',
        '-bufsize','3600k','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',
        '-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-movflags','+faststart',str(target)],check=True)
    if target.stat().st_size>50_000_000:
        raise RuntimeError(f'{name}: exceeds 50 MB; reduce bitrate before publishing')
    print(name,target.stat().st_size)
