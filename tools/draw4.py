import json, textwrap, urllib.request, os
from PIL import Image, ImageDraw, ImageFont

F = lambda s, b=False: ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if b else 'arial.ttf'), s)
BG = (27, 31, 39); CARD = (37, 42, 53); TXT = (235, 236, 240); SUB = (160, 168, 182); GOLD = (232, 184, 74); DIM = (58, 64, 78)
RED = (220, 60, 60); BLUE = (96, 165, 250); GREEN = (74, 222, 128)
skills = {s['id']: s for s in json.load(open('ref/skillBuilder.getSkills.json', encoding='utf8')) if s.get('mainCategory') == 'gladiator'}
byname = {s['name']: k for k, s in skills.items()}
items = json.load(open('ref/characterBuilder.getEquipmentItems.json', encoding='utf8'))


def sk(name, size=56):
    return Image.open(f'icons/sk_{byname[name]}.png').convert('RGBA').resize((size, size))


def it(name, size=56):
    m = [i for i in items if i['name'] == name and i.get('icon')][0]
    fn = f"icons/it_{m['id']}.png"
    if not os.path.exists(fn):
        u = "https://cdn.questlog.gg/aion-2" + m['icon'].rsplit('.', 1)[0] + ".webp"
        open('tmp.webp', 'wb').write(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://questlog.gg/'}), timeout=30).read())
        im = Image.open('tmp.webp').convert('RGBA'); im.thumbnail((64, 64)); im.save(fn)
    return Image.open(fn).convert('RGBA').resize((size, size))


def badge(d, x, y, text, fill=GOLD, fg=BG, size=11):
    w = d.textlength(text, font=F(size, True)) + 10
    d.rounded_rectangle([x, y, x + w, y + size + 7], 4, fill=fill); d.text((x + 5, y + 2), text, font=F(size, True), fill=fg)
    return w


# ---------------- journey map ----------------
stages = [('1', 'Beginner', 'Level 1-19', 'Learn the kit', sk('Mocking Blade'),
           ['Knockdown chain: Mocking Blade > Overhead Slam', 'SP into Overhead Slam first', 'Nezekan board opens at 12']),
          ('2', 'Leveling', 'Level 20-44', 'Stigmas & AoE', sk('Rage Burst'),
           ['Core stigmas from level 22', 'Level-8 specs on every active', 'Zikel 20 / Vaizel 30 / Triniel 40']),
          ('3', 'Level 45', 'iLv 1,000-3,000', 'Gear up', it('Earthly Authority'),
           ['Legend greatsword, all gear +15', 'Pick a build, learn the boss opener', '5 Arcana, finish 4 class boards']),
          ('4', 'Endgame ramp', 'iLv 3,000-5,000', 'Amplify & Daevanion', it("Ludra's Blade of Extinction"),
           ['Amplify to +18 everywhere', 'Daevanion 360 > 890 nodes', 'Overhead Slam to skill Lv 16']),
          ('5', 'Min-max', 'iLv 5,000-7,000', 'Perfect it', it('Chalice of Vigor'),
           ['+20 on everything, all 25 slots', '10 Arcana at +5, seals, pendant', 'Reroll substats and manastones'])]
CW = 236; W = 20 + len(stages) * CW + 10; H = 330
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 14), 'Your journey: five stages from new Gladiator to top-ranked', font=F(22, True), fill=TXT)
d.text((20, 44), 'Each stage is one Part of this guide. Levels gate the first two; item level (iLv) gates the rest.', font=F(14), fill=SUB)
for i, (num, name, rng, goal, ic, pts) in enumerate(stages):
    x = 20 + i * CW; y = 76
    d.rounded_rectangle([x, y, x + CW - 22, y + 236], 12, fill=CARD, outline=GOLD if i == 0 else CARD, width=2)
    d.ellipse([x + 12, y + 12, x + 40, y + 40], fill=GOLD); w = d.textlength(num, font=F(15, True)); d.text((x + 26 - w / 2, y + 17), num, font=F(15, True), fill=BG)
    d.text((x + 50, y + 12), name, font=F(16, True), fill=TXT); d.text((x + 50, y + 32), rng, font=F(12), fill=GOLD)
    img.paste(ic, (x + 12, y + 56), ic)
    d.text((x + 80, y + 64), 'Goal', font=F(11), fill=SUB)
    for k, line in enumerate(textwrap.wrap(goal, 16)):
        d.text((x + 80, y + 80 + k * 17), line, font=F(14, True), fill=TXT)
    yy = y + 128
    for p in pts:
        for k, line in enumerate(textwrap.wrap(p, 26)):
            d.text((x + 14 if k == 0 else x + 24, yy), ('- ' if k == 0 else '') + line, font=F(12), fill=TXT); yy += 15
        yy += 4
    if i < len(stages) - 1:
        ax = x + CW - 20; ay = y + 118
        d.polygon([(ax, ay - 9), (ax + 16, ay), (ax, ay + 9)], fill=GOLD)
img.save('out/journey.png'); print('journey', img.size)

# ---------------- skill unlock timeline ----------------
ev = [(1, 'Rending Blow'), (1, 'Leaping Slam'), (1, 'Keen Strike'), (3, 'Mocking Blade'), (4, 'Overhead Slam'), (5, 'Sword Aura Rampage'), (7, 'Ankle Slice'),
      (8, 'Crushing Wave'), (10, 'Rush Strike'), (12, 'Aerial Snare'), (14, 'Ruinous Blow'), (16, 'Defiance'), (22, 'Rage Burst')]
marks = [(9, 'Enhancement', SUB), (12, 'Nezekan board', GOLD), (19, 'First level-8 specs', GREEN), (20, 'Zikel board', GOLD), (22, 'Stigmas', RED),
         (25, 'Supply Requests', SUB), (30, 'Vaizel board, Daily Dungeon', GOLD), (40, 'Triniel board', GOLD), (45, 'Azphel, Abyss, Nightmare, Arcana', GOLD)]
L = 40; PX = 24; W = L + 45 * PX + 120; H = 380
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 14), 'What unlocks when: level 1 to 45', font=F(22, True), fill=TXT)
d.text((20, 44), 'Top: skills (character level they become learnable).  Bottom: boards, stigmas and systems.', font=F(14), fill=SUB)
axis = 210
d.line([(L + PX, axis), (L + 45 * PX, axis)], fill=SUB, width=3)
for lv in (1, 5, 10, 15, 20, 25, 30, 35, 40, 45):
    x = L + lv * PX; d.line([(x, axis - 6), (x, axis + 6)], fill=SUB, width=2); w = d.textlength(str(lv), font=F(12)); d.text((x - w / 2, axis + 10), str(lv), font=F(12), fill=SUB)
stack = {}
for lv, nm in ev:
    k = stack.get(lv, 0); stack[lv] = k + 1
    x = L + lv * PX; y = axis - 52 - k * 48 if lv < 20 else axis - 52
    S = 40; im = sk(nm, S); img.paste(im, (x - S // 2, y), im)
    if k == 0:
        d.line([(x, y + S), (x, axis)], fill=(80, 88, 104), width=1)
    tx = x + S // 2 + 4
    d.text((tx, y + 12), nm, font=F(11, True), fill=TXT)
for i, (lv, nm, c) in enumerate(marks):
    x = L + lv * PX; y = axis + 34 + (i % 3) * 38
    d.line([(x, axis), (x, y)], fill=c, width=2); d.ellipse([x - 5, axis - 5, x + 5, axis + 5], fill=c)
    badge(d, x - 6, y, f'{lv}: {nm}', fill=c, fg=BG, size=12)
img.save('out/unlocks.png'); print('unlocks', img.size)

# ---------------- gear ladders ----------------
SLOTS = ['Belt', 'Amulet', 'Rune x2', 'Brooch x2', 'Pendant', 'Seal x2', 'Wings']
rows = [
    ('1,000', 'estimate', 'Lv 30-40', 'Wisdom Greatsword', 'Wisdom Breastplate', '+5-10', '+5-10', 'none', 0, '-', 50, '5-8 / - / 5'),
    ('1,500', 'estimate', 'Lv 45', 'Fallen Ancient God Greatsword', 'Fallen Ancient God Breastplate', '+10', '+10', 'belt', 2, '1-2 pcs', 100, '8-10 / 1-5 / 8'),
    ('2,000', 'estimate', 'Lv 45', 'Earthly Authority', 'Vakron Breastplate', '+10-12', '+10-12', 'base20', 4, '3-5 pcs', 150, '10 / 5-8 / 10'),
    ('2,500', 'n = 5', 'Lv 45', 'Dark Dragon Lord Greatsword', 'Nuakum Breastplate', '+12', '+14', 'base20', 5, '5 pcs, +20 total', 170, '11 / 9 / 12'),
    ('3,000', 'n = 5', 'Lv 45', 'Ebony Dragon Lord Greatsword', 'Splendent Ebony Dragon Lord Breastplate', '+15', '+15', 'base20', 5, '5 x +5', 200, '11 / 8 / 14'),
    ('3,500', 'n = 10', 'Lv 45', "Ludra's Blade of Extinction", 'Splendent Ebony Dragon Lord Breastplate', '+18', '+17', 'base20', 6, '6 pcs, 28', 360, '12 / 14 / 14'),
    ('4,000', 'n = 4', 'Lv 45-50', "Ludra's Blade of Extinction", 'Splendent Ebony Dragon Lord Breastplate', '+18', '+16', 'brooch1', 6, '6 pcs, 28', 660, '14 / 18 / 16'),
    ('4,500', 'n = 4', 'Lv 45', "Ludra's Blade of Extinction", 'Splendent Ebony Dragon Lord Breastplate', '+18', '+17', 'brooch', 6, '6 pcs, 30', 660, '12 / 19 / 15'),
    ('5,000', 'n = 5', 'Lv 49-50', "Ludra's Blade of Extinction", 'Splendent Ebony Dragon Lord Breastplate', '+19', '+18', 'pendant', 7, '7 pcs, 31', 890, '14 / 20 / 19'),
    ('5,500', 'n = 7', 'Lv 50', "Ludra's Blade of Extinction", 'Splendent Ebony Dragon Lord Breastplate', '+19', '+19', 'pendant', 7, '7 pcs, 33', 1050, '16 / 21 / 20'),
    ('6,000', 'n = 14', 'Lv 50', "Ludra's Blade of Extinction", 'Splendent Ebony Dragon Lord Breastplate', '+20', '+19', 'seal', 8, '8 pcs, 38', 1055, '16 / 22 / 20'),
    ('6,500-7,000', 'n = 6', 'Lv 50', "Ludra's Blade of Extinction", 'Splendent Ebony Dragon Lord Breastplate', '+20', '+20', 'all', 10, '10 x +5', 1083, '16 / 22 / 21'),
]
STATE = {'none': [], 'belt': ['Belt'], 'base20': ['Belt', 'Amulet', 'Rune x2'], 'brooch1': ['Belt', 'Amulet', 'Rune x2', 'Brooch x2*', 'Wings'],
         'brooch': ['Belt', 'Amulet', 'Rune x2', 'Brooch x2', 'Wings'], 'pendant': ['Belt', 'Amulet', 'Rune x2', 'Brooch x2', 'Pendant*', 'Wings'],
         'seal': ['Belt', 'Amulet', 'Rune x2', 'Brooch x2', 'Pendant*', 'Seal x2*', 'Wings'], 'all': SLOTS}
chal = it('Chalice of Vigor', 22)


def ladder(sel, title, fn):
    RH = 104; W = 1180; H = 96 + len(sel) * (RH + 8) + 20
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    d.text((20, 14), title, font=F(22, True), fill=TXT)
    d.text((20, 44), 'Per milestone: weapon and armor tier with enchant, unlocked extra slots, Arcana, Daevanion nodes, skill levels (active / stigma / passive).', font=F(13), fill=SUB)
    d.text((20, 62), 'n = ranked profiles averaged; "estimate" rows are derived from item level requirements.  * = about half of profiles.', font=F(13), fill=SUB)
    for i, r in enumerate(sel):
        ilv, n, lv, wpn, arm, ench, acc, st, arc, arct, nodes, skl = r
        y = 90 + i * (RH + 8)
        d.rounded_rectangle([12, y, W - 12, y + RH], 10, fill=CARD)
        d.text((26, y + 12), 'iLv', font=F(12), fill=SUB); d.text((26, y + 26), ilv, font=F(24, True), fill=GOLD)
        d.text((26, y + 58), lv, font=F(13, True), fill=TXT); d.text((26, y + 76), n, font=F(11), fill=SUB)
        x = 170
        for nm, en in ((wpn, ench), (arm, acc)):
            im = it(nm, 60); img.paste(im, (x, y + 10), im); badge(d, x + 2, y + 74, en, size=11)
            x += 74
        d.text((x + 4, y + 12), textwrap.shorten(wpn, 30, placeholder='...'), font=F(12, True), fill=TXT)
        d.text((x + 4, y + 28), textwrap.shorten(arm, 30, placeholder='...'), font=F(11), fill=SUB)
        d.text((x + 4, y + 46), f'Armor {ench}  ·  Accessories {acc}', font=F(12), fill=TXT)
        if ilv >= '3,500' and len(ilv) == 5 or ilv.startswith('6,5'):
            d.text((x + 4, y + 64), 'top profiles: newer tier, same enchant', font=F(11), fill=SUB)
        sx = 560
        d.text((sx, y + 10), 'Extra slots', font=F(11), fill=SUB)
        on = STATE[st]; cx = sx; cy = y + 28
        for k, s in enumerate(SLOTS):
            lit = any(o.rstrip('*') == s for o in on); half = (s + '*') in on
            w = d.textlength(s, font=F(10, True)) + 10
            if cx + w > sx + 250:
                cx = sx; cy += 22
            d.rounded_rectangle([cx, cy, cx + w, cy + 17], 4, fill=(GOLD if lit and not half else (PATHC if half else DIM)))
            d.text((cx + 5, cy + 3), s, font=F(10, True), fill=BG if lit else SUB); cx += w + 5
        ax = 830
        d.text((ax, y + 10), 'Arcana', font=F(11), fill=SUB)
        for k in range(10):
            px = ax + (k % 5) * 26; py = y + 28 + (k // 5) * 26
            if k < arc:
                img.paste(chal, (px, py), chal)
            else:
                d.rounded_rectangle([px, py, px + 22, py + 22], 4, outline=DIM, width=2)
        d.text((ax, y + 82), arct, font=F(11), fill=TXT)
        bx = 980
        d.text((bx, y + 10), 'Daevanion nodes', font=F(11), fill=SUB)
        d.rounded_rectangle([bx, y + 30, bx + 180, y + 44], 5, fill=DIM)
        d.rounded_rectangle([bx, y + 30, bx + int(180 * min(nodes, 1100) / 1100), y + 44], 5, fill=GOLD)
        d.text((bx, y + 48), f'~{nodes:,} of ~1,100', font=F(12, True), fill=TXT)
        d.text((bx, y + 68), 'Skill Lv', font=F(11), fill=SUB); d.text((bx + 48, y + 66), skl, font=F(12, True), fill=TXT)
    img.save('out/' + fn); print(fn, img.size)


PATHC = (150, 120, 60)
ladder(rows[0:5], 'Gear ladder, Part 3: iLv 1,000 to 3,000', 'ladder_1.png')
ladder(rows[5:9], 'Gear ladder, Part 4: iLv 3,500 to 5,000', 'ladder_2.png')
ladder(rows[9:], 'Gear ladder, Part 5: iLv 5,500 to 7,000', 'ladder_3.png')
