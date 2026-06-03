#!/usr/bin/env python3
import argparse, subprocess, tempfile
from pathlib import Path
parser=argparse.ArgumentParser(description='Render timestamp-named images + voiceover to MP4 using ffmpeg concat.')
parser.add_argument('--images', required=True)
parser.add_argument('--audio', required=True)
parser.add_argument('--out', required=True)
args=parser.parse_args()
images=sorted(Path(args.images).glob('*.png'), key=lambda p: float(p.stem))
if len(images)<1: raise SystemExit('No .png images found')
probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nk=1:nw=1',args.audio], text=True, capture_output=True, check=True)
audio_dur=float(probe.stdout.strip())
starts=[float(p.stem) for p in images]
lines=[]
for idx,p in enumerate(images):
    end=starts[idx+1] if idx+1<len(starts) else audio_dur
    dur=max(0.1,end-starts[idx])
    lines.append(f"file '{p.resolve()}'\n")
    lines.append(f'duration {dur:.3f}\n')
lines.append(f"file '{images[-1].resolve()}'\n")
Path(args.out).parent.mkdir(parents=True, exist_ok=True)
with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
    f.writelines(lines); concat=f.name
cmd=['ffmpeg','-y','-f','concat','-safe','0','-i',concat,'-i',args.audio,'-vf','scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p','-c:v','libx264','-c:a','aac','-shortest',args.out]
subprocess.run(cmd, check=True)
print(args.out)
