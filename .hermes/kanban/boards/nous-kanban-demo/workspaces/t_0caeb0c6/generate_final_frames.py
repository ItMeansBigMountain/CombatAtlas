#!/usr/bin/env python3
import math
import os
from pathlib import Path
from xml.sax.saxutils import escape

W, H = 1280, 720
FPS = 15
DURATION = 14.5
N = int(FPS * DURATION)
OUT = Path('frames')
OUT.mkdir(exist_ok=True)

BG = '#080B12'
BG2 = '#0D111C'
PANEL = '#111827'
BORDER = '#2B3447'
MUTED = '#7A859B'
TEXT = '#EEF6FF'
TODO = '#293244'
READY = '#20D3FF'
RUNNING = '#8B5CF6'
BLOCKED = '#FFB020'
BLOCKED2 = '#FF5C7A'
DONE = '#35D07F'
CYAN = '#20D3FF'
GREEN = '#35D07F'
VIOLET = '#8B5CF6'

LANES = {
    'todo': 250,
    'ready': 430,
    'running': 610,
    'blocked': 790,
    'done': 970,
}
LANE_LABELS = [('TODO', 250), ('READY', 430), ('RUNNING', 610), ('BLOCKED', 790), ('DONE', 970)]
CARD_W, CARD_H = 142, 62
ROWS = {
    'Research': 255,
    'Storyboard': 335,
    'Animate': 415,
    'Edit': 495,
    'Review': 575,
}
AGENTS = [('Director', 'D'), ('Researcher', 'R'), ('Designer', 'S'), ('Animator', 'A'), ('Editor', 'E'), ('Reviewer', 'V')]


def clamp(x, a=0, b=1):
    return max(a, min(b, x))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def lerp(a, b, p):
    return a + (b - a) * p


def pos_lerp(p1, p2, p):
    return (lerp(p1[0], p2[0], p), lerp(p1[1], p2[1], p))


def mix_hex(a, b, p):
    p = clamp(p)
    ar = int(a[1:3], 16); ag = int(a[3:5], 16); ab = int(a[5:7], 16)
    br = int(b[1:3], 16); bg = int(b[3:5], 16); bb = int(b[5:7], 16)
    return f'#{int(lerp(ar, br, p)):02x}{int(lerp(ag, bg, p)):02x}{int(lerp(ab, bb, p)):02x}'


def E(tag, attrs='', body='', selfclose=False):
    if selfclose:
        return f'<{tag} {attrs}/>'
    return f'<{tag} {attrs}>{body}</{tag}>'


def rect(x, y, w, h, fill, stroke='none', sw=1, rx=10, opacity=1):
    return E('rect', f'x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity:.3f}"', selfclose=True)


def circle(x, y, r, fill, stroke='none', sw=1, opacity=1):
    return E('circle', f'cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity:.3f}"', selfclose=True)


def line(x1, y1, x2, y2, color, sw=2, opacity=1, dash=''):
    attrs = f'x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" opacity="{opacity:.3f}" stroke-linecap="round"'
    if dash:
        attrs += f' stroke-dasharray="{dash}"'
    return E('line', attrs, selfclose=True)


def text(x, y, s, size=24, fill=TEXT, weight='500', anchor='middle', opacity=1, family='Arial, Helvetica, sans-serif'):
    return E('text', f'x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" font-family="{family}" font-weight="{weight}" text-anchor="{anchor}" opacity="{opacity:.3f}"', escape(s))


def glow_defs():
    return '''<defs>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#000000" flood-opacity="0.45"/></filter>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.22"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<radialGradient id="rad" cx="50%" cy="45%" r="65%"><stop offset="0" stop-color="#15223D"/><stop offset="0.7" stop-color="#0D111C"/><stop offset="1" stop-color="#080B12"/></radialGradient>
</defs>'''


def card(label, x, y, status, alpha=1, badge='', wait_text='', sheen=0):
    colors = {'todo': TODO, 'ready': READY, 'running': RUNNING, 'blocked': BLOCKED, 'done': DONE}
    fill = colors.get(status, TODO)
    stroke = mix_hex(fill, '#FFFFFF', 0.25)
    body = []
    body.append(rect(x - CARD_W/2, y - CARD_H/2, CARD_W, CARD_H, fill, stroke, 1.2, 12, alpha))
    body.append(rect(x - CARD_W/2 + 10, y - CARD_H/2 + 10, 30, 18, '#0B1020', 'none', 1, 8, alpha*0.45))
    icon = {'Research':'R', 'Storyboard':'S', 'Animate':'A', 'Edit':'E', 'Review':'V'}.get(label, '•')
    body.append(text(x - CARD_W/2 + 25, y - CARD_H/2 + 24, icon, 12, TEXT, '700', 'middle', alpha))
    label_size = 14 if len(label) >= 9 else 16
    body.append(text(x - CARD_W/2 + 48, y - 7, label, label_size, TEXT, '700', 'start', alpha))
    pill = status.upper() if status != 'todo' else 'TODO'
    body.append(text(x - CARD_W/2 + 48, y + 16, pill, 10, '#DCE7F8', '700', 'start', alpha*0.85))
    if badge:
        body.append(rect(x + CARD_W/2 - 46, y - CARD_H/2 + 9, 36, 18, '#0B1020', BORDER, 0.6, 9, alpha*0.8))
        body.append(text(x + CARD_W/2 - 28, y - CARD_H/2 + 23, badge, 10, '#B7C3D8', '700', 'middle', alpha))
    if wait_text:
        body.append(text(x, y + 43, wait_text, 11, MUTED, '600', 'middle', alpha*0.85))
    if status == 'blocked':
        pulse = 0.5 + 0.5 * math.sin(sheen * math.tau)
        body.append(circle(x + CARD_W/2 - 18, y - CARD_H/2 + 17, 6 + pulse*2, BLOCKED2, 'none', 1, alpha*(0.65+0.25*pulse)))
        body.append(text(x + CARD_W/2 - 18, y - CARD_H/2 + 21, '!', 12, '#1A0B0B', '900', 'middle', alpha))
    if status == 'done':
        check_x = x + CARD_W/2 - 11
        body.append(circle(check_x, y - CARD_H/2 + 18, 8, '#0B2518', GREEN, 1, alpha))
        body.append(text(check_x, y - CARD_H/2 + 23, '✓', 13, GREEN, '900', 'middle', alpha))
    if status == 'running':
        sx = (x - CARD_W/2 - 40) + ((sheen % 1) * (CARD_W + 80))
        body.append(E('polygon', f'points="{sx:.1f},{y-CARD_H/2:.1f} {sx+36:.1f},{y-CARD_H/2:.1f} {sx+8:.1f},{y+CARD_H/2:.1f} {sx-28:.1f},{y+CARD_H/2:.1f}" fill="url(#sheen)" opacity="{alpha*0.8:.3f}"', selfclose=True))
    return E('g', 'filter="url(#glow)"', ''.join(body))


def state_positions(t):
    # default todo fan-out positions
    out = {name: (LANES['todo'], ROWS[name], 'todo', 0.25, '', '') for name in ROWS}
    # fan-out appear alpha
    alpha = smooth((t - 1.8) / 1.0)
    # base todo visible after decomposition
    for name in ROWS:
        out[name] = (LANES['todo'], ROWS[name], 'todo', alpha, '', '')
    # waiting badges once visible
    if t >= 4.0:
        out['Animate'] = (LANES['todo'], ROWS['Animate'], 'todo', 0.55, '2', 'waiting on 2')
        out['Edit'] = (LANES['todo'], ROWS['Edit'], 'todo', 0.45, '1', 'waiting on 1')
        out['Review'] = (LANES['todo'], ROWS['Review'], 'todo', 0.45, '1', 'waiting on 1')
    # Research/Storyboard into running
    for name in ['Research', 'Storyboard']:
        if 4.0 <= t < 4.9:
            p = smooth((t - 4.0)/0.9)
            out[name] = (*pos_lerp((LANES['todo'], ROWS[name]), (LANES['ready'], ROWS[name]), p), 'ready', 1, '', '')
        elif 4.9 <= t < 8.8:
            p = smooth((t - 4.9)/0.7)
            out[name] = (*pos_lerp((LANES['ready'], ROWS[name]), (LANES['running'], ROWS[name]), p), 'running', 1, '', '')
    # blocked storyboard moment
    if 6.4 <= t < 7.2:
        p = smooth((t - 6.4)/0.8)
        out['Storyboard'] = (*pos_lerp((LANES['running'], ROWS['Storyboard']), (LANES['blocked'], ROWS['Storyboard']), p), 'blocked', 1, '', '')
    elif 7.2 <= t < 8.15:
        out['Storyboard'] = (LANES['blocked'], ROWS['Storyboard'], 'blocked', 1, '', '')
    elif 8.15 <= t < 8.8:
        p = smooth((t - 8.15)/0.65)
        out['Storyboard'] = (*pos_lerp((LANES['blocked'], ROWS['Storyboard']), (LANES['running'], ROWS['Storyboard']), p), 'running', 1, '', '')
    # done research/storyboard
    if 8.8 <= t:
        for name in ['Research', 'Storyboard']:
            p = smooth((t - 8.8)/0.8)
            out[name] = (*pos_lerp((LANES['running'], ROWS[name]), (LANES['done'], ROWS[name]), p), 'done', 1, '', '')
    # animate unlock
    if 9.5 <= t < 10.1:
        p = smooth((t-9.5)/0.6)
        out['Animate'] = (*pos_lerp((LANES['todo'], ROWS['Animate']), (LANES['ready'], ROWS['Animate']), p), 'ready', 1, '', '')
    elif 10.1 <= t < 11.6:
        p = smooth((t-10.1)/0.7)
        out['Animate'] = (*pos_lerp((LANES['ready'], ROWS['Animate']), (LANES['running'], ROWS['Animate']), p), 'running', 1, '', '')
    elif 11.6 <= t:
        p = smooth((t-11.6)/0.55)
        out['Animate'] = (*pos_lerp((LANES['running'], ROWS['Animate']), (LANES['done'], ROWS['Animate']), p), 'done', 1, '', '')
    # edit cascade
    if 11.9 <= t < 12.4:
        p=smooth((t-11.9)/0.5); out['Edit']=(*pos_lerp((LANES['todo'],ROWS['Edit']),(LANES['running'],ROWS['Edit']),p),'running',1,'','')
    elif 12.4 <= t:
        p=smooth((t-12.4)/0.45); out['Edit']=(*pos_lerp((LANES['running'],ROWS['Edit']),(LANES['done'],ROWS['Edit']),p),'done',1,'','')
    # review cascade
    if 12.75 <= t < 13.25:
        p=smooth((t-12.75)/0.5); out['Review']=(*pos_lerp((LANES['todo'],ROWS['Review']),(LANES['running'],ROWS['Review']),p),'running',1,'','')
    elif 13.25 <= t:
        p=smooth((t-13.25)/0.45); out['Review']=(*pos_lerp((LANES['running'],ROWS['Review']),(LANES['done'],ROWS['Review']),p),'done',1,'','')
    return out


def caption_for(t):
    caps = [
        (0.0, 1.8, 'One brief lands.'),
        (1.8, 4.0, 'Fan-out: director splits parallel tasks.'),
        (4.0, 6.4, 'Parallel agents start.'),
        (6.4, 8.6, 'Blockers surface fast.'),
        (8.6, 11.2, 'Dependencies unlock the next card.'),
        (11.2, 13.4, 'Fan-in: work flows to done.'),
        (13.4, 14.6, 'Coordinate AI work visually.'),
    ]
    for a,b,s in caps:
        if a <= t < b:
            fade = min(smooth((t-a)/0.25), smooth((b-t)/0.25))
            return s, fade
    return '', 0


def packet_on_line(x1,y1,x2,y2,t, start, dur, color=CYAN):
    if t < start or t > start + dur:
        return ''
    p = ((t-start)/dur) % 1
    x,y = pos_lerp((x1,y1),(x2,y2), smooth(p))
    return circle(x, y, 5, color, '#DFFBFF', 1, 0.95)


def frame_svg(i):
    t = i / FPS
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    parts.append(glow_defs())
    parts.append(rect(0,0,W,H,'url(#rad)', 'none', 0, 0, 1))
    # subtle grid
    for gx in range(0, W, 80):
        parts.append(line(gx, 0, gx, H, '#172033', 1, 0.18))
    for gy in range(0, H, 80):
        parts.append(line(0, gy, W, gy, '#172033', 1, 0.18))
    panel_alpha = smooth(t/1.0)
    parts.append(E('g', f'opacity="{panel_alpha:.3f}" filter="url(#soft)"', rect(70,72,1140,568,PANEL,BORDER,1.2,22,1)))
    # top bar
    parts.append(text(115, 113, 'Hermes Kanban', 22, TEXT, '800', 'start', panel_alpha))
    board = 'Demo launch video' if t < 13.4 else '5 agents · 1 board · zero lost handoffs'
    parts.append(rect(500, 91, 280 if t < 13.4 else 380, 34, '#0B1020', BORDER, 1, 17, panel_alpha))
    parts.append(text(640, 114, board, 15, '#BFD0EA', '700', 'middle', panel_alpha))
    live_color = GREEN if t > 13.3 else CYAN
    parts.append(rect(1042,91,120,34,'#0B1020',BORDER,1,17,panel_alpha))
    parts.append(circle(1060,108,5,live_color,'none',1,panel_alpha))
    parts.append(text(1115,114,'LIVE BOARD',13,'#BFD0EA','700','middle',panel_alpha))
    # left rail agents
    parts.append(rect(92,145,64,460,'#0B1020',BORDER,1,18,panel_alpha))
    for idx,(name,letter) in enumerate(AGENTS):
        y=180+idx*68
        active = (name in ['Researcher','Designer'] and 4.0<t<8.8) or (name=='Animator' and 9.5<t<12.2) or (name=='Editor' and 11.9<t<12.9) or (name=='Reviewer' and 12.75<t<14.0) or (name=='Director' and (1.0<t<4.1 or 7.2<t<8.2))
        col = CYAN if active else '#344158'
        parts.append(circle(124,y,18,col,BORDER,1,panel_alpha*(1 if active else 0.6)))
        parts.append(text(124,y+6,letter,16,TEXT,'800','middle',panel_alpha))
    # lanes
    for label,x in LANE_LABELS:
        parts.append(rect(x-78,146,156,458,'#0D1424',BORDER,1,16,panel_alpha*0.82))
        parts.append(text(x,171,label,12,'#96A2B8','800','middle',panel_alpha))
    # title and parent brief card
    title_alpha = min(smooth(t/0.6), smooth((3.6-t)/0.55)) if t < 4 else 0
    if title_alpha > 0:
        parts.append(text(640,55,'Agent orchestration, visible.',31,TEXT,'900','middle',title_alpha))
    parent_scale = 0.92 + 0.08*smooth(t/0.8)
    parent_alpha = min(smooth(t/0.35), smooth((4.0-t)/0.7)) if t < 4.1 else 0
    px,py=640,250
    if parent_alpha>0:
        pw,ph=310*parent_scale,104*parent_scale
        parts.append(E('g', 'filter="url(#glow)"', rect(px-pw/2,py-ph/2,pw,ph,'#172338',CYAN,1.6,18,parent_alpha)))
        parts.append(text(px,py-8,'Goal: make a demo video',24,TEXT,'800','middle',parent_alpha))
        parts.append(text(px,py+22,'Creative brief card',15,'#AAB7CE','700','middle',parent_alpha))
        parts.append(circle(px-135,py-33,16,VIOLET,CYAN,1,parent_alpha))
        parts.append(text(px-135,py-28,'D',15,TEXT,'900','middle',parent_alpha))
    # states/cards
    states = state_positions(t)
    # Dependency lines after fanout; draw under cards
    line_alpha = smooth((t-2.2)/0.7)
    if t > 2.0:
        # use current card centers for line endpoints
        def cp(name):
            x,y,_,a,_,_ = states[name]
            return x,y
        col = CYAN
        if t > 8.8: col = GREEN
        # Split lines from invisible director/parent area to first children and onward chain
        p0=(640,245 if t<4 else 210)
        for nm in ['Research','Storyboard']:
            x,y = cp(nm)
            parts.append(line(p0[0],p0[1],x,y,col,2.0,line_alpha*0.8))
        for a,b in [('Research','Animate'),('Storyboard','Animate'),('Animate','Edit'),('Edit','Review')]:
            x1,y1=cp(a); x2,y2=cp(b)
            lcol = BLOCKED if (6.4<t<8.3 and (a=='Storyboard' or b=='Storyboard')) else (GREEN if t>8.8 else CYAN)
            parts.append(line(x1,y1,x2,y2,lcol,2.2,line_alpha*0.82))
        # traveling packets at important beats
        if 2.2 < t < 4.0:
            for k,nm in enumerate(['Research','Storyboard','Animate','Edit','Review']):
                x,y=cp(nm); parts.append(packet_on_line(p0[0],p0[1],x,y,t,2.25+k*0.13,1.0,CYAN))
        if 7.15 < t < 8.3:
            x,y=cp('Storyboard'); parts.append(packet_on_line(124,180,x,y,t,7.18,0.9,CYAN))
        if 9.0 < t < 10.5:
            for nm in ['Research','Storyboard']:
                x1,y1=cp(nm); x2,y2=cp('Animate'); parts.append(packet_on_line(x1,y1,x2,y2,t,9.05,1.1,GREEN))
        if 11.7 < t < 13.6:
            for a,b,st in [('Animate','Edit',11.72),('Edit','Review',12.55)]:
                x1,y1=cp(a); x2,y2=cp(b); parts.append(packet_on_line(x1,y1,x2,y2,t,st,0.9,GREEN))
    # Decomposition sparkle tiny nodes
    if 1.8 < t < 3.4:
        p=smooth((t-1.8)/1.2)
        for ang in [0, 1.3, 2.6, 3.9, 5.2]:
            sx=640+math.cos(ang)*lerp(12,95,p); sy=250+math.sin(ang)*lerp(8,55,p)
            parts.append(circle(sx,sy,3,CYAN,'none',1,0.7*(1-p)))
    # cards over lines
    for name in ['Research','Storyboard','Animate','Edit','Review']:
        x,y,st,a,badge,wait = states[name]
        if a>0.02:
            parts.append(card(name,x,y,st,a,badge,wait,sheen=t*0.8))
    # blocker comment bubble
    if 6.75 <= t <= 8.2:
        a = min(smooth((t-6.75)/0.25), smooth((8.2-t)/0.25))
        bx,by = states['Storyboard'][0]+120, states['Storyboard'][1]-54
        parts.append(E('g', f'opacity="{a:.3f}" filter="url(#soft)"', rect(bx-76,by-25,152,50,'#151C2C',BLOCKED,1,14,1) + text(bx,by-3,'Need visual',14,TEXT,'700','middle',1) + text(bx,by+15,'direction',14,TEXT,'700','middle',1)))
    # final output card / fan-in hero
    if t >= 13.3:
        a=smooth((t-13.3)/0.45)
        parts.append(E('g', f'opacity="{a:.3f}" filter="url(#glow)"', rect(495,586,290,50,'#102D20',GREEN,1.4,15,1)+text(640,618,'Final video card: DONE',20,TEXT,'900','middle',1)))
        for nm in ['Research','Storyboard','Animate','Edit','Review']:
            x,y,_,_,_,_=states[nm]
            parts.append(line(x,y+33,640,586,GREEN,1.8,a*0.45))
    # captions
    cap, ca = caption_for(t)
    if cap:
        parts.append(rect(340,646,600,48,'#080B12',BORDER,1,20,0.78*ca))
        parts.append(text(640,678,cap,30,TEXT,'900','middle',ca))
    # final CTA/tagline
    if t >= 13.55:
        a=smooth((t-13.55)/0.5)
        parts.append(text(640,58,'Hermes Kanban: watch your agents work.',28,CYAN,'900','middle',a))
    parts.append('</svg>')
    return ''.join(parts)


for i in range(N):
    (OUT / f'frame_{i:04d}.svg').write_text(frame_svg(i), encoding='utf-8')
print(f'generated {N} SVG frames in {OUT.resolve()}')
