#!/usr/bin/env python3
"""Render a square Hermes Kanban launch-video cut as SVG frames + ffmpeg MP4."""
from __future__ import annotations

import math
import os
import shutil
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "frames"
OUT = ROOT / "hermes-kanban-launch-square.mp4"
POSTER = ROOT / "hermes-kanban-launch-poster.png"
FPS = 24
DURATION = 22.0
W = H = 1080

BG = "#050507"
PANEL = "#0d1016"
PANEL2 = "#111722"
GRID = "#242b38"
TEXT = "#f4f0e8"
MUTED = "#a3a9b6"
AMBER = "#ffb454"
BLUE = "#6db8ff"
GREEN = "#58d68d"
RED = "#ff5d73"
YELLOW = "#ffe082"
PURPLE = "#b78cff"


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def smooth(x):
    x = clamp(x)
    return x*x*(3-2*x)

def span(t, a, b):
    return smooth((t-a)/(b-a)) if b != a else 1.0

def lerp(a, b, u):
    return a + (b-a)*u

def hex_rgba(color, alpha):
    return color, f"{clamp(alpha):.3f}"

def tag(name, attrs=None, body=""):
    attrs = attrs or {}
    a = " ".join(f'{k}="{escape(str(v))}"' for k, v in attrs.items() if v is not None)
    return f"<{name} {a}>{body}</{name}>" if body else f"<{name} {a}/>"

def text(x, y, s, size=28, fill=TEXT, weight=500, alpha=1, anchor="start", family="DejaVu Sans Mono"):
    return tag("text", {
        "x": round(x, 1), "y": round(y, 1), "fill": fill, "fill-opacity": f"{alpha:.3f}",
        "font-family": family, "font-size": size, "font-weight": weight,
        "text-anchor": anchor, "letter-spacing": "-0.5px"
    }, escape(s))

def rect(x, y, w, h, fill, stroke=None, sw=1, rx=16, alpha=1, dash=None):
    return tag("rect", {"x": round(x,1), "y": round(y,1), "width": round(w,1), "height": round(h,1), "rx": rx,
                        "fill": fill, "fill-opacity": f"{alpha:.3f}", "stroke": stroke, "stroke-width": sw if stroke else None,
                        "stroke-dasharray": dash})

def line(x1,y1,x2,y2, stroke=GRID, sw=3, alpha=1, dash=None):
    return tag("line", {"x1":round(x1,1),"y1":round(y1,1),"x2":round(x2,1),"y2":round(y2,1),"stroke":stroke,"stroke-width":sw,
                         "stroke-opacity":f"{alpha:.3f}","stroke-linecap":"round","stroke-dasharray":dash})

def circle(cx, cy, r, fill, alpha=1, stroke=None):
    return tag("circle", {"cx":round(cx,1),"cy":round(cy,1),"r":round(r,1),"fill":fill,"fill-opacity":f"{alpha:.3f}","stroke":stroke})

def wrap_lines(s, max_chars):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def card(x, y, w, h, title, status, accent, body="", alpha=1.0, glow=0.0, agent=None):
    g=[]
    if glow>0:
        g.append(rect(x-5,y-5,w+10,h+10,accent,rx=20,alpha=0.10*glow))
    g.append(rect(x,y,w,h,"#121722",stroke=accent,sw=2.2,rx=18,alpha=0.96*alpha))
    g.append(rect(x,y,w,8,accent,rx=16,alpha=0.85*alpha))
    g.append(text(x+18,y+34,title,22,TEXT,700,alpha))
    # Put the status pill on its own row so narrow square cards keep titles legible.
    badge_w=max(72,min(118,len(status)*10+22))
    g.append(rect(x+18,y+46,badge_w,26,accent,rx=13,alpha=0.20*alpha))
    g.append(text(x+18+badge_w/2,y+65,status.upper(),13,accent,700,alpha,anchor="middle"))
    yy=y+94
    for ln in wrap_lines(body, 24)[:2]:
        g.append(text(x+18, yy, ln, 15, MUTED, 500, alpha)); yy+=21
    # Agent ownership is implied by the claim/status motion; omit footer labels to keep
    # the small square dashboard cards clean and readable in video compression.
    return "".join(g)

def terminal_stack(t):
    fade=1-span(t,0.6,2.2)
    if fade<=0: return ""
    g=[]
    for i,lab in enumerate(["research-agent", "designer-agent", "editor-agent"]):
        x=120+i*38; y=245+i*48
        g.append(rect(x,y,790,230,"#080a0f",stroke="#303645",sw=2,rx=18,alpha=0.75*fade))
        g.append(text(x+24,y+38,f"$ hermes run {lab}",22,GREEN,600,fade))
        g.append(text(x+24,y+82,"separate shell • separate context • manual copy/paste",18,MUTED,500,fade))
        g.append(text(x+24,y+128,"status: running? blocked? done?",18,RED if i==1 else AMBER,500,fade))
    return "".join(g)

def board(t):
    enter=span(t,1.0,2.6)
    y=lerp(122,92,enter); alpha=enter
    g=[]
    g.append(rect(54,y,972,820,PANEL,stroke="#2c3443",sw=2,rx=28,alpha=0.98*alpha))
    g.append(rect(54,y,972,64,"#0a0d12",rx=28,alpha=alpha))
    g.append(circle(90,y+32,7,RED,alpha)); g.append(circle(114,y+32,7,AMBER,alpha)); g.append(circle(138,y+32,7,GREEN,alpha))
    g.append(text(175,y+41,"Hermes Kanban — launch video pipeline",24,TEXT,700,alpha))
    g.append(text(805,y+41,"one board, many agents",18,AMBER,700,alpha))
    cols=[("TODO",80), ("RUNNING",317), ("BLOCKED",554), ("DONE",791)]
    for name,x in cols:
        g.append(rect(x,y+92,205,660,"#0f141d",stroke="#222a37",sw=1.4,rx=22,alpha=0.86*alpha))
        g.append(text(x+20,y+128,name,18,MUTED,800,alpha))
    # faint lane separators / grid
    for yy in [y+180,y+310,y+440,y+570,y+700]:
        g.append(line(80,yy,996,yy,"#1a202b",1,0.5*alpha,"5 9"))
    return "".join(g)

def scene_cards(t):
    g=[]; by=92
    # static positions
    brief=(92,220); plan=(330,220); research=(92,392); design=(330,392); animate=(568,392); edit=(568,600); review=(806,600); final=(806,392)
    # intro: brief lands from above
    u=span(t,2.0,3.0); bx=brief[0]; b_y=lerp(110,brief[1],u)
    g.append(card(bx,b_y,180,120,"Launch brief","todo",AMBER,"goal: demo multi-agent work",span(t,1.8,2.6),span(t,2.6,3.4),"user"))
    # plan card claim and finish
    if t>2.7:
        st="running" if t<5.2 else "done"
        acc=BLUE if t<5.2 else GREEN
        g.append(card(plan[0],plan[1],180,120,"Plan","done" if t>=5.2 else "running",acc,"decompose into specialist cards",span(t,2.7,3.5),span(t,3.2,5.0),"planner"))
        g.append(line(brief[0]+180,brief[1]+60,plan[0],plan[1]+60,GREEN if t>5.2 else BLUE,3,span(t,3.3,4.3),"8 10"))
    # fanout research/design/animate ghost
    if t>4.6:
        g.append(line(plan[0]+90,plan[1]+120,research[0]+90,research[1],GREEN,3,span(t,4.8,6.2),"8 10"))
        g.append(line(plan[0]+90,plan[1]+120,design[0]+90,design[1],GREEN,3,span(t,5.0,6.4),"8 10"))
        g.append(card(research[0],research[1],180,128,"Research","running" if t<8.3 else "done",GREEN if t>=8.3 else AMBER,"value props + launch line",span(t,4.8,5.8),span(t,6.2,8.3),"researcher"))
        g.append(card(design[0],design[1],180,128,"Design","running" if t<8.8 else "done",GREEN if t>=8.8 else BLUE,"square motion language",span(t,5.2,6.2),span(t,6.4,8.8),"designer"))
    if t>7.5:
        astatus = "locked"
        acc = "#4b5567"
        if t>=9.2: astatus="running"; acc=PURPLE
        if t>=11.2: astatus="blocked"; acc=RED
        if t>=14.0: astatus="done"; acc=GREEN
        g.append(card(animate[0],animate[1],180,132,"Animation","done" if t>=14 else astatus,acc,"waits for parent handoffs",span(t,7.5,8.4),span(t,9.0,11.0),"animator"))
        # dependencies + moving packets from parents
        for src,offset in [(research,0.0),(design,0.35)]:
            g.append(line(src[0]+180,src[1]+65,animate[0],animate[1]+65,GREEN,3,span(t,8.4+offset,9.4+offset),"8 10"))
            pu=span(t,8.9+offset,10.0+offset)
            if 0<pu<1:
                g.append(circle(lerp(src[0]+180,animate[0],pu), lerp(src[1]+65,animate[1]+65,pu), 8, GREEN, 1))
    # blocker/comment panel
    if 10.7<t<14.7:
        a=span(t,10.7,11.4)*(1-span(t,14.0,14.7))
        g.append(rect(604,552,342,104,"#251017",stroke=RED,sw=2,rx=18,alpha=0.95*a))
        g.append(text(626,584,"BLOCKED: needs human call",20,RED,800,a))
        g.append(text(626,616,"review before final assembly",16,TEXT,600,a))
        g.append(rect(766,632,150,34,"#1f2b1f",stroke=GREEN,sw=2,rx=17,alpha=0.95*a))
        g.append(text(841,656,"unblock card",15,GREEN,800,a,anchor="middle"))
        # cursor click
        cu=span(t,12.4,13.0)
        cx=lerp(970,846,cu); cy=lerp(710,646,cu)
        g.append(text(cx,cy,"↖",42,TEXT,900,a))
        if 0.45<cu<0.9:
            g.append(circle(846,646,24,GREEN,0.20*a))
    if t>13.6:
        g.append(line(animate[0]+90,animate[1]+132,edit[0]+90,edit[1],GREEN,3,span(t,13.6,14.8),"8 10"))
        g.append(card(edit[0],edit[1],180,132,"Edit","running" if t<17.0 else "done",GREEN if t>=17 else AMBER,"assemble tight square cut",span(t,13.8,14.8),span(t,15.0,17.0),"editor"))
    if t>15.6:
        g.append(line(edit[0]+180,edit[1]+66,review[0],review[1]+66,GREEN,3,span(t,15.8,17.0),"8 10"))
        g.append(card(review[0],review[1],180,132,"Review","accepted" if t>=18 else "checking",GREEN if t>=18 else YELLOW,"human sees the handoff",span(t,15.8,16.8),span(t,17.0,18.0),"reviewer"))
    if t>17.3:
        g.append(line(review[0]+90,review[1],final[0]+90,final[1]+132,GREEN,3,span(t,17.5,18.4),"8 10"))
        g.append(card(final[0],final[1],180,142,"Final video","done",GREEN,"traceable from every parent",span(t,17.8,18.8),span(t,18.2,20.5),"artifact"))
        # miniature play triangle
        a=span(t,18,19)
        g.append(tag("polygon", {"points":"876,476 876,516 912,496", "fill":GREEN, "fill-opacity":f"{0.9*a:.3f}"}))
    return "".join(g)

def captions(t):
    beats=[
        (0,3.2,"Stop juggling terminals.","Put the project on one board."),
        (3.2,6.4,"Agents claim the right cards.","Planning turns one brief into specialist work."),
        (6.4,10.3,"Research and design run in parallel.","Dependencies wait; handoffs stay durable."),
        (10.3,14.4,"When blocked, the card asks you.","Unblock it from the same dashboard."),
        (14.4,18.4,"Downstream work resumes automatically.","The editor sees every parent result."),
        (18.4,22.1,"Hermes Kanban is the control plane.","One board. Many agents. Visible progress."),
    ]
    current=beats[-1]
    for b in beats:
        if b[0]<=t<b[1]: current=b; break
    a=span(t,current[0],current[0]+0.5)*(1-span(t,current[1]-0.5,current[1]))
    g=[]
    g.append(rect(86,940,908,92,"#080a0f",stroke="#252d3a",sw=1.5,rx=24,alpha=0.82*a))
    g.append(text(118,982,current[2],32,TEXT,800,a,family="DejaVu Sans"))
    g.append(text(118,1014,current[3],20,AMBER if t<18.4 else GREEN,700,a,family="DejaVu Sans"))
    return "".join(g)

def side_metrics(t):
    a=span(t,4.0,5.0)
    if a<=0: return ""
    done = 0
    if t>5.2: done+=1
    if t>8.3: done+=1
    if t>8.8: done+=1
    if t>14: done+=1
    if t>17: done+=1
    if t>18: done+=1
    g=[]
    g.append(rect(766,170,230,40,"#101722",stroke="#293244",sw=1,rx=20,alpha=.78*a))
    g.append(text(784,197,f"running: {3 if 6<t<8.5 else 1 if 3<t<17 else 0}",15,BLUE,700,a))
    g.append(text(890,197,f"done: {done}",15,GREEN,700,a))
    return "".join(g)

def svg_frame(t):
    pulse=0.08*math.sin(t*2.3)+0.08
    g=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    g.append(rect(0,0,W,H,BG,rx=0))
    # subtle radial glow
    g.append(tag("radialGradient", {"id":"glow", "cx":"50%", "cy":"42%", "r":"65%"},
                 tag("stop", {"offset":"0%", "stop-color":"#1a2230", "stop-opacity":f"{0.55+pulse:.2f}"})+
                 tag("stop", {"offset":"100%", "stop-color":"#050507", "stop-opacity":"0"})))
    g.append(rect(0,0,W,H,"url(#glow)",rx=0,alpha=0.9))
    g.append(text(68,66,"HERMES KANBAN",22,AMBER,900,1))
    g.append(text(300,66,"multi-agent work, visible from one dashboard",21,MUTED,600,1,family="DejaVu Sans"))
    g.append(terminal_stack(t))
    g.append(board(t))
    g.append(scene_cards(t))
    g.append(side_metrics(t))
    g.append(captions(t))
    # timeline bar
    g.append(rect(86,1040,908,8,"#1a2029",rx=4,alpha=1))
    g.append(rect(86,1040,908*clamp(t/DURATION),8,GREEN if t>18.4 else AMBER,rx=4,alpha=0.9))
    g.append('</svg>')
    return "\n".join(g)

def main():
    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)
    total=int(DURATION*FPS)
    for i in range(total):
        t=i/FPS
        (FRAMES / f"frame_{i:04d}.svg").write_text(svg_frame(t), encoding="utf-8")
    cmd=["ffmpeg","-hide_banner","-y","-framerate",str(FPS),"-i",str(FRAMES/"frame_%04d.svg"),
         "-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=48000",
         "-t",str(DURATION),"-vf","format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
         "-pix_fmt","yuv420p","-c:a","aac","-shortest",str(OUT)]
    subprocess.run(cmd, check=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss","19.0","-i",str(OUT),"-frames:v","1",str(POSTER)], check=True)
    print(OUT)
    print(POSTER)

if __name__ == "__main__":
    main()
