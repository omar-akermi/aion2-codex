import json, textwrap
from PIL import Image, ImageDraw, ImageFont

F = lambda s, b=False: ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if b else 'arial.ttf'), s)
BG = (27, 31, 39); CARD = (37, 42, 53); TXT = (235, 236, 240); SUB = (160, 168, 182); GOLD = (232, 184, 74); RED = (220, 60, 60); BLUE = (96, 165, 250); GREEN = (74, 222, 128)
skills = {s['id']: s for s in json.load(open('ref/skillBuilder.getSkills.json', encoding='utf8')) if s.get('mainCategory') == 'gladiator'}
byname = {s['name']: k for k, s in skills.items()}


def sk(name, size=56):
    return Image.open(f'icons/sk_{byname[name]}.png').convert('RGBA').resize((size, size))


def arrow(d, x0, y, x1, col=SUB):
    d.line([(x0, y), (x1 - 6, y)], fill=col, width=3); d.polygon([(x1, y), (x1 - 9, y - 6), (x1 - 9, y + 6)], fill=col)


def chain_rows(title, subtitle, rows, fn, S=56, SW=118):
    maxlen = max(len(r[1]) for r in rows)
    W = 40 + maxlen * SW + 20; H = 80 + len(rows) * 168
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    d.text((20, 16), title, font=F(22, True), fill=TXT); d.text((20, 46), subtitle, font=F(14), fill=SUB)
    for r, (rt, steps, note) in enumerate(rows):
        y = 78 + r * 168
        d.rounded_rectangle([12, y, W - 12, y + 158], 10, fill=CARD); d.text((26, y + 8), rt, font=F(15, True), fill=GOLD)
        for i, st in enumerate(steps):
            nm, cap = st[0], st[1]; x = 26 + i * SW
            cx = x + SW // 2 - 10
            if nm.startswith('!'):
                txt = nm[1:]; d.rounded_rectangle([cx - S // 2, y + 36, cx + S // 2, y + 36 + S], 8, fill=RED)
                for k, line in enumerate(textwrap.wrap(txt, 8)):
                    w = d.textlength(line, font=F(11, True)); d.text((cx - w / 2, y + 50 + k * 14), line, font=F(11, True), fill=TXT)
            else:
                im = sk(nm, S); img.paste(im, (cx - S // 2, y + 36), im)
            yy = y + 36 + S + 5
            for line in textwrap.wrap(cap, 15, break_long_words=False)[:4]:
                w = d.textlength(line, font=F(11)); d.text((cx - w / 2, yy), line, font=F(11), fill=TXT); yy += 13
            if i < len(steps) - 1:
                arrow(d, cx + S // 2 + 6, y + 36 + S // 2, cx + SW - S // 2 - 6)
        if note:
            w = d.textlength(note, font=F(12)); d.text((W - 26 - w, y + 10), note, font=F(12), fill=SUB)
    img.save('out/' + fn); print(fn, img.size)


chain_rows('Three damage engines', 'Every Gladiator rotation is built from these three chains',
           [('1. Rage Burst window (bosses)', [('Ruinous Blow', 'Prepare for Battle +20% PvE 20s'), ('Rage Burst', 'Unlocks Overhead Slam for 10s'),
                                              ('Overhead Slam', 'Spam: no CD with spec 16'), ('Overhead Slam', '9,207 per cast'), ('Overhead Slam', '2.2x the filler'), ('Mocking Blade', 'Weave in on CD')], 'every 30s with Rage Burst spec'),
            ('2. Knockdown chain (trash, PvP)', [('Mocking Blade', 'Knockdown 3s (4s spec)'), ('Overhead Slam', 'Needs Knockdown'), ('Aerial Snare', 'Airborne, then Forced Fall chain'),
                                                 ('Ankle Slice', 'Root; 30% Knockdown spec'), ('Rush Strike', 'Knockdown after Dodge')], 'keeps targets locked ~7s'),
            ('3. Stagger break (bosses)', [('Ruinous Blow', '25 gauge'), ('Rage Burst', '20 gauge'), ('Lifestealing Blade', '20 gauge'), ('Mocking Blade', '15 gauge'),
                                           ('!STAGGER', 'Boss Staggered'), ('Sword Aura Rampage', 'No CD while Staggered, -1s all CDs/hit')], "Zikel's spec 5: +50% gauge")],
           'combo_engines.png')
chain_rows('Rotations', 'Single target, AoE pull and PvP burst, in cast order',
           [('Boss opener', [('Focused Block', 'Parry a boss hit: +17% party buff'), ('Ruinous Blow', '+20% PvE, +100 Crit'), ("Zikel's Blessing", '+20% Attack'),
                             ('Lunge Stance', '+20% Combat Speed'), ('Wave Armor', 'x1.5 passives'), ('Rage Burst', 'Opens 10s window'),
                             ('Overhead Slam', 'Every GCD for 10s'), ('Lifestealing Blade', 'End of window / heal')], '~1.9x DPS inside the window'),
            ('AoE pull (dungeon trash, leveling)', [('Leaping Slam', 'AoE + pull (spec 16)'), ('Crushing Wave', '50% pull (spec 16)'), ('Ankle Slice', 'Root all NPCs'),
                                                    ('Mocking Blade', 'Knock down the biggest'), ('Overhead Slam', 'AoE (spec 8)'), ('Lifestealing Blade', '4 targets, 10% HP'),
                                                    ('Rending Blow', 'Spam on 4 targets')], 'cleaves cap at 4 targets'),
            ('PvP burst', [('Blade Toss', '-30% Def, -50% healing 10s'), ('Leaping Slam', 'Close 20m'), ('Mocking Blade', 'Knockdown'), ('Overhead Slam', 'Free hit on Knockdown'),
                           ('Aerial Snare', 'Airborne'), ('Rage Burst', 'Target -10-20% Attack'), ('Ruinous Blow', 'Finisher'), ('Defiance', 'Break CC, 7s Tenacity')], 'open on healers')],
           'combo_rotations.png')

# cooldown timeline 0-120s
lanes = [("Zikel's Blessing", 120, 10, GOLD, 0), ('Lunge Stance', 60, 10, GOLD, 0), ('Wave Armor', 60, 10, GOLD, 0),
         ('Rage Burst', 30, 10, RED, 0), ('Ruinous Blow', 30, 20, BLUE, 0), ('Focused Block', 20, 20, GREEN, 0)]
notes = {"Zikel's Blessing": '120s CD · +20% Attack 10s', 'Lunge Stance': '60s · +20% Combat Speed 10s', 'Wave Armor': '60s · x1.5 Exp. Counterstrike / Murderous Burst 10s',
         'Rage Burst': '30s with spec · Overhead Slam window 10s', 'Ruinous Blow': '45s, ~30s with Keen Strike spec · Prepare for Battle 20s',
         'Focused Block': '20s · Parry refreshes the 20s Exp. Counterstrike party buff'}
L = 230; T = 120; PX = 7; W = L + T * PX + 40; H = 110 + len(lanes) * 58 + 70
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 16), 'Cooldown alignment: one 120-second cycle', font=F(22, True), fill=TXT)
d.text((20, 46), 'Bars = buff uptime. Gold columns = burst windows where everything overlaps (0s full, 60s mini, 30s/90s Rage Burst only).', font=F(14), fill=SUB)
top = 96; bottom = top + len(lanes) * 58
for wx, ww, a in ((0, 10, 70), (60, 10, 50), (30, 10, 25), (90, 10, 25)):
    ov = Image.new('RGBA', (ww * PX, bottom - top + 10), (232, 184, 74, a)); img.paste(ov, (L + wx * PX, top - 6), ov)
for s in range(0, T + 1, 10):
    x = L + s * PX; d.line([(x, top - 8), (x, bottom)], fill=(55, 61, 75), width=1); d.text((x - 8, bottom + 6), f'{s}s', font=F(12), fill=SUB)
for i, (nm, cd, dur, colr, off) in enumerate(lanes):
    y = top + i * 58; im = sk(nm, 40); img.paste(im, (20, y), im)
    d.text((68, y + 2), nm, font=F(13, True), fill=TXT); d.text((68, y + 20), textwrap.shorten(notes[nm], 28, placeholder='…'), font=F(10), fill=SUB)
    t = off
    while t < T:
        d.rounded_rectangle([L + t * PX, y + 8, L + min(t + dur, T) * PX - 2, y + 32], 5, fill=colr)
        d.ellipse([L + t * PX - 5, y + 15, L + t * PX + 5, y + 25], fill=TXT)
        t += cd
d.text((20, bottom + 32), 'White dot = cast.  Focused Block every 20s keeps the 20s party buff permanently up; Rage Burst and Ruinous Blow are kept in sync by Keen Strike\'s -1s spec.', font=F(13), fill=TXT)
img.save('out/combo_timeline.png'); print('timeline', img.size)
