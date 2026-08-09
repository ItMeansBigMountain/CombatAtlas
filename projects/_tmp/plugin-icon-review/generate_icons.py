from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)
S = 24

def canvas():
    return Image.new('RGBA', (S, S), (0, 0, 0, 0))

def poly(d, xy, fill, outline=None, width=1):
    d.polygon(xy, fill=fill)
    if outline:
        d.line(xy + [xy[0]], fill=outline, width=width, joint='curve')

def save(im, name):
    im.resize((48, 48), Image.Resampling.NEAREST).save(OUT / f'{name}.png')

# 1. BIS Loadouts — gold sword, cyan staff, dark shield
im=canvas(); d=ImageDraw.Draw(im)
poly(d, [(12,3),(20,7),(18,17),(12,22),(6,17),(4,7)], '#243447', '#0b1018')
poly(d, [(12,5),(18,8),(16,16),(12,19),(8,16),(6,8)], '#3d566f', '#7793ac')
# staff
d.line((5,20,17,4), fill='#102733', width=3); d.line((5,20,17,4), fill='#45d9ff', width=1)
d.ellipse((15,2,20,7), fill='#8cf4ff', outline='#d8fdff'); d.point((17,3), fill='white')
# sword
poly(d, [(5,3),(8,4),(16,16),(14,18)], '#ffe07a', '#5f3a00')
poly(d, [(4,2),(8,4),(7,7)], '#fff2a6', '#704800')
d.line((12,15,17,12), fill='#ffbd32', width=2); d.line((13,18,17,20), fill='#b57012', width=2)
save(im,'bis-loadouts')

# 2. Who's Grinding — social heads, pickaxe, progress arrow
im=canvas(); d=ImageDraw.Draw(im)
# people
d.ellipse((2,9,7,14), fill='#40d9ff', outline='#092b3a'); d.rectangle((2,14,7,20), fill='#168db7', outline='#092b3a')
d.ellipse((9,7,15,13), fill='#a5f55b', outline='#18380d'); d.rectangle((9,13,15,21), fill='#55b72d', outline='#18380d')
d.ellipse((17,10,21,14), fill='#6ce8ff', outline='#092b3a'); d.rectangle((17,14,21,20), fill='#237fa8', outline='#092b3a')
# upward arrow
poly(d, [(12,1),(18,7),(15,7),(15,11),(10,11),(10,7),(7,7)], '#d9ff4a', '#25450d')
# pickaxe
d.line((4,21,17,5), fill='#7b4a25', width=2); d.arc((12,3,22,10), 190, 350, fill='#d9e1e8', width=2)
save(im,'whos-grinding')

# 3. Clan War Board — opposing banners and stone score shield
im=canvas(); d=ImageDraw.Draw(im)
d.line((6,2,6,21), fill='#d2b36c', width=2); poly(d,[(7,3),(14,5),(7,10)],'#d84135','#54100d')
d.line((18,2,18,21), fill='#d2b36c', width=2); poly(d,[(17,3),(10,5),(17,10)],'#3488df','#0b2d57')
poly(d,[(5,9),(19,9),(20,17),(16,22),(8,22),(4,17)],'#626a73','#1a2027')
poly(d,[(7,11),(17,11),(17,17),(14,20),(10,20),(7,17)],'#929aa1','#d0d5d9')
d.line((9,14,15,14),fill='#2b3035',width=2); d.line((12,12,12,18),fill='#2b3035',width=2)
save(im,'clan-war-board')

# 4. Deadman Breach Timer — skull hourglass + breach crack
im=canvas(); d=ImageDraw.Draw(im)
# violet breach aura
poly(d,[(12,1),(15,5),(20,4),(18,9),(23,12),(18,15),(20,21),(14,19),(12,23),(9,19),(3,21),(6,15),(1,12),(6,9),(4,4),(9,5)],'#5c258a','#220b35')
# hourglass frame
d.line((7,4,17,4),fill='#d65c3e',width=2); d.line((7,20,17,20),fill='#d65c3e',width=2); d.line((8,5,16,19),fill='#972c28',width=2); d.line((16,5,8,19),fill='#972c28',width=2)
# skull
poly(d,[(8,7),(10,5),(14,5),(17,8),(16,13),(14,15),(10,15),(8,12)],'#e6d6b4','#441510')
d.rectangle((10,14,14,17),fill='#c9b68e',outline='#441510'); d.rectangle((10,9,11,11),fill='#290c16'); d.rectangle((14,9,15,11),fill='#290c16'); d.point((12,12),fill='#6f251f')
# red crack
d.line((12,1,11,7,13,10,11,14,13,18,12,23),fill='#ff4a35',width=1)
save(im,'deadman-breach-timer')

# 5. Boilerplate — wrench + scroll + green creation spark
im=canvas(); d=ImageDraw.Draw(im)
# parchment
poly(d,[(5,5),(16,5),(18,8),(17,20),(6,20),(4,17)],'#d8c28f','#4a3b22')
d.line((7,9,14,9),fill='#7b6841'); d.line((7,12,15,12),fill='#7b6841'); d.line((7,15,12,15),fill='#7b6841')
# wrench
poly(d,[(15,2),(19,3),(17,6),(19,8),(22,6),(22,10),(19,12),(16,10),(9,19),(6,16),(14,8),(13,5)],'#c6d0d8','#28333c')
d.ellipse((7,16,10,19),fill='#46525c')
# plus spark
d.rectangle((18,14,20,22),fill='#79ef54',outline='#173d12'); d.rectangle((15,17,23,19),fill='#79ef54',outline='#173d12')
save(im,'plugin-template')

# review sheet
items=[
 ('BIS LOADOUTS','bis-loadouts','#172536'),
 ("WHO'S GRINDING",'whos-grinding','#122b25'),
 ('CLAN WAR BOARD','clan-war-board','#2b2024'),
 ('DMM BREACH TIMER','deadman-breach-timer','#25152e'),
 ('PLUGIN TEMPLATE','plugin-template','#292923'),
]
W,H=1420,390
sheet=Image.new('RGB',(W,H),'#101317'); sd=ImageDraw.Draw(sheet)
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
small_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(font_path,19); small=ImageFont.truetype(small_path,15)
sd.text((32,18),'RUNELITE PLUGIN ICON REVIEW — UNIQUE CONCEPTS',font=ImageFont.truetype(font_path,25),fill='#f0f2f5')
sd.text((32,52),'Enlarged nearest-neighbor preview + actual 48×48 RuneLite asset',font=small,fill='#9ca8b5')
for i,(label,name,bg) in enumerate(items):
 x=25+i*279; y=85
 sd.rounded_rectangle((x,y,x+254,y+275),12,fill=bg,outline='#4b5560',width=2)
 icon=Image.open(OUT/f'{name}.png').convert('RGBA')
 big=icon.resize((192,192),Image.Resampling.NEAREST)
 sheet.paste(big,(x+31,y+20),big)
 sheet.paste(icon,(x+103,y+210),icon)
 tw=sd.textbbox((0,0),label,font=font)[2]
 sd.text((x+(254-tw)//2,y+252),label,font=font,fill='#f6f7f8')
sheet.save(OUT/'plugin-icon-review-sheet.png')
print(OUT/'plugin-icon-review-sheet.png')
