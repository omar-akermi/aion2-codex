"""Fast-track progression visuals: icon set for the HTML phase cards and a waterfall 'climb' chart."""
import math
from PIL import Image, ImageDraw, ImageFont

F = lambda s, b=False: ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if b else 'arial.ttf'), s)
BG = (18, 21, 28); PANEL = (26, 31, 41); LINE = (46, 53, 69); TXT = (232, 230, 224); SUB = (155, 164, 182); GOLD = (232, 184, 74)
CAT = {'base': (110, 118, 135), 'free': (94, 196, 182), 'craft': (232, 184, 74), 'dungeon': (130, 174, 232),
       'enh': (176, 140, 232), 'arcana': (127, 201, 107), 'stone': (232, 120, 160)}
CAT_NAME = {'base': 'Level 45 gear', 'free': 'Free systems', 'craft': 'Crafting', 'dungeon': 'Dungeon gear',
            'enh': 'Enhancing', 'arcana': 'Arcana', 'stone': 'Magic stones'}

S = 192  # glyph canvas, downsampled for smoothness


def canvas():
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


def frame(d, col):
    d.rounded_rectangle([6, 6, S - 6, S - 6], 30, fill=(30, 35, 46, 255), outline=col + (255,), width=8)


def g_daev():
    im, d = canvas(); frame(d, (94, 196, 182)); c = S / 2
    pts = []
    for i in range(10):
        r = 62 if i % 2 == 0 else 26; a = -math.pi / 2 + i * math.pi / 5
        pts.append((c + r * math.cos(a), c + r * math.sin(a)))
    d.polygon(pts, fill=(94, 196, 182, 255))
    for a in range(0, 360, 90):
        x = c + 70 * math.cos(math.radians(a + 45)); y = c + 70 * math.sin(math.radians(a + 45))
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(94, 196, 182, 200))
    return im


def g_feather(col=(94, 196, 182)):
    im, d = canvas(); frame(d, col)
    d.polygon([(60, 150), (140, 40), (150, 52), (78, 152)], fill=col + (255,))
    for t in range(6):
        x = 70 + t * 13; y = 135 - t * 16
        d.line([(x, y), (x + 34, y + 2)], fill=col + (255,), width=7)
        d.line([(x, y), (x - 10, y - 30)], fill=col + (255,), width=7)
    d.line([(52, 162), (78, 130)], fill=(232, 230, 224, 255), width=7)
    return im


def g_card(col, label=None):
    im, d = canvas(); frame(d, col)
    for k, off in enumerate((-16, 0, 16)):
        x0 = 58 + off; y0 = 38 + abs(off) // 2
        shade = tuple(int(v * (0.55 + 0.22 * k)) for v in col)
        d.rounded_rectangle([x0, y0, x0 + 76, y0 + 112], 10, fill=shade + (255,), outline=(18, 21, 28, 255), width=4)
    d.ellipse([84, 78, 108, 102], outline=(18, 21, 28, 255), width=6)
    return im


def g_stone():
    im, d = canvas(); col = (232, 120, 160); frame(d, col)
    c = S / 2; pts = [(c, 34), (c + 52, 76), (c + 30, 152), (c - 30, 152), (c - 52, 76)]
    d.polygon(pts, fill=col + (255,))
    d.polygon([(c, 34), (c + 52, 76), (c, 92), (c - 52, 76)], fill=(250, 180, 205, 255))
    d.line([(c, 92), (c, 152)], fill=(150, 60, 95, 255), width=5)
    return im


def g_enh():
    im, d = canvas(); col = (176, 140, 232); frame(d, col)
    d.polygon([(96, 30), (150, 92), (118, 92), (118, 150), (74, 150), (74, 92), (42, 92)], fill=col + (255,))
    d.text((96, 120), '+', font=F(56, True), fill=(30, 35, 46, 255), anchor='mm')
    return im


def g_level():
    im, d = canvas(); col = (110, 118, 135); frame(d, col)
    d.ellipse([34, 34, S - 34, S - 34], outline=col + (255,), width=10)
    d.text((S / 2, S / 2 + 2), '45', font=F(64, True), fill=(232, 230, 224, 255), anchor='mm')
    return im


def item(iid, col):
    im, d = canvas(); frame(d, col)
    ic = Image.open(f'picons/{iid}.png').convert('RGBA').resize((136, 136), Image.LANCZOS)
    im.paste(ic, (28, 28), ic); return im


def fin(im, n=96):
    return im.resize((n, n), Image.LANCZOS)


ICONS = {
    'level': fin(g_level()), 'daev': fin(g_daev()), 'amulet': fin(item('311030001', CAT['free'])),
    'belt': fin(item('215230001', CAT['free'])), 'feather': fin(g_feather()), 'rune': fin(item('310900001', CAT['free'])),
    'acc': fin(item('310130109', CAT['craft'])), 'weapon': fin(item('110130094', CAT['craft'])),
    'draupnir': fin(item('210130108', CAT['dungeon'])), 'vakron': fin(item('210130112', CAT['dungeon'])),
    'enh': fin(g_enh()), 'arc1': fin(g_card((150, 200, 120))), 'craft2': fin(item('310130112', CAT['craft'])),
    'stone': fin(g_stone()), 'arc2': fin(g_card((110, 160, 235))), 'horn': fin(item('210130117', CAT['dungeon'])),
    'arc4': fin(g_card((232, 184, 74))), 'craft3': fin(item('310130119', CAT['craft'])),
}
for k, im in ICONS.items():
    im.save(f'out/prog_{k}.png')

STEPS = [  # (icon, short label, +iLv, category, phase)
    ('level', 'Level 45', 645, 'base', 0), ('daev', 'Daevanion', 360, 'free', 0), ('amulet', 'Amulet', 65, 'free', 0),
    ('belt', 'Belt', 65, 'free', 0), ('feather', 'Abyss', 52, 'free', 0), ('rune', 'Runes', 82, 'free', 0),
    ('acc', 'Accessories', 118, 'craft', 1), ('weapon', 'Weapon', 17, 'craft', 1), ('draupnir', 'Draupnir', 16, 'dungeon', 1),
    ('vakron', 'Vakron', 32, 'dungeon', 2), ('enh', 'Enhance', 159, 'enh', 2),
    ('arc1', 'Arcana I', 140, 'arcana', 3), ('craft2', 'Splendent', 144, 'craft', 3), ('stone', 'Stones', 105, 'stone', 3),
    ('arc2', 'Arcana II', 100, 'arcana', 4),
    ('horn', 'Horn Den', 332, 'dungeon', 5), ('enh', 'Enhance', 10, 'enh', 5), ('arc4', 'Arcana IV', 160, 'arcana', 5),
    ('craft3', 'Wise/Ebony', 98, 'craft', 5),
]
PHASES = ['1 · Free item level', '2 · First crafts', '3 · Enhance', '4 · Arcana + Splendent', '5 · Blue cards', '6 · Tier 3 → raid']
GATES = [(700, 'Draupnir, Crow Cave'), (1400, 'Conquest T2'), (1600, 'Transcendence I'), (1900, 'Transcendence II'),
         (2000, 'Horn Den (T3)'), (2100, '3-star dungeons'), (2700, 'Sanctuary raid')]

W, H = 1600, 780
L, R, T, B = 86, 1380, 118, 600
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img, 'RGBA')
d.text((L - 50, 22), 'The climb: level 45 to the first raid', font=F(28, True), fill=TXT)
d.text((L - 50, 60), 'Each bar is one step; it starts where the last one ended. Dashed lines are content gates on the global playtest.', font=F(16), fill=SUB)
y = lambda v: B - (B - T) * v / 2800
for v in range(0, 2801, 500):
    d.line([(L, y(v)), (R, y(v))], fill=LINE + (120,), width=1)
    d.text((L - 12, y(v)), f'{v:,}', font=F(14), fill=SUB, anchor='rm')
n = len(STEPS); cw = (R - L) / n; bw = cw * 0.62
# phase bands
start = 0
for ph in range(6):
    idx = [i for i, s in enumerate(STEPS) if s[4] == ph]
    x0 = L + idx[0] * cw; x1 = L + (idx[-1] + 1) * cw
    if ph % 2 == 0:
        d.rectangle([x0, T - 6, x1, B], fill=(255, 255, 255, 9))
    lab = PHASES[ph] if d.textlength(PHASES[ph], font=F(15, True)) < x1 - x0 - 8 else PHASES[ph].replace(' · ', ' · \n', 1)
    d.multiline_text(((x0 + x1) / 2, B + 104), lab, font=F(15, True), fill=GOLD, anchor='mm', align='center', spacing=2)
    d.line([(x0 + 6, B + 84), (x1 - 6, B + 84)], fill=GOLD + (90,), width=2)
# gates
for v, lab in GATES:
    yy = y(v)
    for xx in range(L, R, 14):
        d.line([(xx, yy), (xx + 7, yy)], fill=GOLD + (150,), width=2)
    d.text((R + 10, yy), f'{v:,}  {lab}', font=F(14, True if v == 2700 else False), fill=GOLD if v == 2700 else TXT, anchor='lm')
# bars
run = 0
for i, (ic, lab, val, cat, ph) in enumerate(STEPS):
    x0 = L + i * cw + (cw - bw) / 2; x1 = x0 + bw
    y0, y1 = y(run + val), y(run)
    d.rounded_rectangle([x0, y0, x1, y1], 4, fill=CAT[cat] + (255,))
    if i:
        d.line([(x0 - (cw - bw), y(run)), (x0, y(run))], fill=SUB + (140,), width=1)
    run += val
    d.text(((x0 + x1) / 2, y0 - 8), f'+{val}' if i else f'{val}', font=F(13, True), fill=TXT, anchor='mb')
    icon = ICONS[ic].resize((44, 44), Image.LANCZOS)
    img.paste(icon, (int((x0 + x1) / 2 - 22), B + 10), icon)
    d.text(((x0 + x1) / 2, B + 66), lab, font=F(12), fill=SUB, anchor='mm')
assert run == 2700, run
# subtotal markers
run = 0
for ph in range(6):
    for s in STEPS:
        if s[4] == ph:
            run += s[2]
    last = max(i for i, s in enumerate(STEPS) if s[4] == ph)
    xx = L + (last + 1) * cw
    d.ellipse([xx - 6, y(run) - 6, xx + 6, y(run) + 6], fill=GOLD, outline=BG, width=2)
    lab = f'{run:,}'; tw = d.textlength(lab, font=F(14, True))
    d.rounded_rectangle([xx + 6, y(run) + 8, xx + 18 + tw, y(run) + 30], 6, fill=GOLD)
    d.text((xx + 12, y(run) + 19), lab, font=F(14, True), fill=BG, anchor='lm')
# legend
lx = L - 50; ly = H - 30
for k in ['base', 'free', 'craft', 'dungeon', 'enh', 'arcana', 'stone']:
    total = sum(s[2] for s in STEPS if s[3] == k)
    lab = f'{CAT_NAME[k]} {total:,}'
    d.rounded_rectangle([lx, ly - 7, lx + 14, ly + 7], 3, fill=CAT[k])
    d.text((lx + 20, ly), lab, font=F(14), fill=TXT, anchor='lm')
    lx += 34 + d.textlength(lab, font=F(14))
img.save('out/prog_climb.png'); print('climb', img.size)
print({k: sum(s[2] for s in STEPS if s[3] == k) for k in CAT})
