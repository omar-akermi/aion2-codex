import json, glob, textwrap, statistics as st
from PIL import Image, ImageDraw, ImageFont

F = lambda s, b=False: ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if b else 'arial.ttf'), s)
BG = (27, 31, 39); CARD = (37, 42, 53); TXT = (235, 236, 240); SUB = (160, 168, 182); GOLD = (232, 184, 74); DIM = (58, 64, 78)
RED = (220, 60, 60); BLUE = (96, 165, 250); GREEN = (74, 222, 128); PURPLE = (176, 130, 240)
ALLSK = json.load(open('ref/skillBuilder.getSkills.json', encoding='utf8'))
byname = {s['name']: s['id'] for s in ALLSK if s.get('mainCategory') == 'assassin'}
subcat = {s['id']: s['subCategory'] for s in ALLSK}
items = json.load(open('ref/characterBuilder.getEquipmentItems.json', encoding='utf8'))


def sk(name, size=56):
    return Image.open(f'icons/sk_{byname[name]}.png').convert('RGBA').resize((size, size))


def it(name, size=56):
    m = [i for i in items if i['name'] == name and i.get('icon')][0]
    return Image.open(f"icons/it_{m['id']}.png").convert('RGBA').resize((size, size))


def badge(d, x, y, text, fill=GOLD, fg=BG, size=11):
    w = d.textlength(text, font=F(size, True)) + 10
    d.rounded_rectangle([x, y, x + w, y + size + 7], 4, fill=fill); d.text((x + 5, y + 2), text, font=F(size, True), fill=fg)


def tiles(title, subtitle, its, cols, fn, tw=150, th=150):
    rows = (len(its) + cols - 1) // cols; W = cols * tw + 40; H = rows * th + 90
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    d.text((20, 16), title, font=F(22, True), fill=TXT); d.text((20, 46), subtitle, font=F(14), fill=SUB)
    for i, t in enumerate(its):
        x = 20 + (i % cols) * tw; y = 78 + (i // cols) * th
        d.rounded_rectangle([x + 4, y + 4, x + tw - 4, y + th - 4], 10, fill=CARD, outline=GOLD if t.get('hl') else CARD, width=2)
        ic = t['img']; img.paste(ic, (x + (tw - ic.width) // 2, y + 14), ic)
        yy = y + 14 + ic.height + 6
        for line in textwrap.wrap(t['name'], 19)[:2]:
            w = d.textlength(line, font=F(13, True)); d.text((x + (tw - w) / 2, yy), line, font=F(13, True), fill=TXT); yy += 16
        for line in textwrap.wrap(t.get('sub', ''), 23)[:2]:
            w = d.textlength(line, font=F(11)); d.text((x + (tw - w) / 2, yy), line, font=F(11), fill=GOLD if t.get('hl') else SUB); yy += 14
        if t.get('badge'):
            badge(d, x + 8, y + 8, t['badge'], size=10)
    img.save('out/' + fn); print(fn, img.size)


# ---------- skill cards ----------
A = [('Insignia Explosion', '10s (7s spec) · 990/s at 5 stacks', '#1'), ('Heart Gore', 'On crit · 5s, no CD in Clone', '#2'),
     ('Whirlwind Slice', '10s · 484/s · Stun on Evasion', '#3'), ('Ambush', '10s · +30% from behind', '#4'),
     ('Shadowstrike', '20s · teleport behind, Stun', '#5'), ('Flash Slice', '10s · 4 targets, Blind', '#6'),
     ('Infiltrate', '20s · teleport behind', '#7'), ('Shadow Fall', '20s · Knockdown on Stunned', '#8'),
     ('Savage Roar', 'Filler · +1 Insignia', '#9'), ('Quick Slice', 'Basic · 140% ATK, +100 MP', '#10'),
     ('Storm Rampage', 'Stagger window · no CD', '#11'), ('Defiance', '60s · CC break', 'PvP')]
tiles('Assassin active skills: priority order', 'Ranked by damage per cooldown-second at skill level 20, Attack 1,425',
      [{'img': sk(n), 'name': n, 'sub': s, 'badge': b, 'hl': i < 3} for i, (n, s, b) in enumerate(A)], 6, 'as_skills_active.png')
ST = [('Illusive Clone', '90s · Heart Gore no CD, +20% dmg', 1), ('Swift Contract', '60s · +20% Combat Speed', 1),
      ("Triniel's Dagger", '45s · 256% ATK, +30% behind', 1), ('Savage Fang', '60s · 600% ATK, 5 Insignias', 1),
      ('Evasion Stance', '20s · guaranteed Evasion', 1), ('Throw Shadowblade', '30s · 20m, Slow', 1),
      ('Smoke Bomb', '30s · Blind 5s', 0), ('Shadow Walk', '120s · Stealth opener', 0), ('Evasion Contract', '90s · +200 Evasion (PvP)', 0),
      ('Spiral Slice', '90s · strip buffs (PvP)', 0), ('Shadowstep', '45s · Stealth, 5 Insignias', 0), ('Aerial Bind', '120s · Airborne', 0),
      ('Assault Ambush', '120s · 20m AoE', 0)]
tiles('Assassin stigmas', 'Gold = taken by 88-100% of top PvE Assassins',
      [{'img': sk(n), 'name': n, 'sub': s, 'hl': h, 'badge': 'CORE' if h else None} for n, s, h in ST], 7, 'as_skills_stigma.png', tw=140, th=160)
P = [('Rear Smite', 'Lv30: +17.5% Back Atk & PvE', 1), ('Assault Stance', 'Lv30: +35% Crit Damage', 1),
     ('Exploit Weakness', 'Lv30: 25% chance +20% Attack', 1), ('Impact Hit', 'Lv30: +9% Double', 1), ('Defense Break', 'Lv30: target -70% Defense', 1),
     ('Ambush Stance', 'Bonus hits after movement', 0), ('Determination', 'Bonus dmg under 30% HP', 0),
     ('Heightened Sixth Sense', '+200 Evasion, heal on Evasion', 0), ('Revitalization Contract', 'Status Resist, emergency heal', 0),
     ('Apply Poison', 'Poison, -70% healing at Lv30', 0)]
tiles('Assassin passives: leveling priority', 'Gold = damage core (top players push Rear Smite and Assault Stance to ~30)',
      [{'img': sk(n), 'name': n, 'sub': s, 'hl': h} for n, s, h in P], 5, 'as_skills_passive.png', tw=170)

# ---------- builds ----------
bars = {
    'PvE DPS (Nightmare, Transcendence)': (['Quick Slice', 'Savage Roar', 'Insignia Explosion', 'Heart Gore', 'Ambush', 'Whirlwind Slice', 'Shadowstrike', 'Flash Slice', 'Infiltrate', 'Shadow Fall', 'Storm Rampage'],
                                            ['Illusive Clone', 'Swift Contract', "Triniel's Dagger", 'Savage Fang', 'Evasion Stance', 'Throw Shadowblade', 'Smoke Bomb', 'Shadow Walk']),
    'AoE farming / leveling': (['Quick Slice', 'Savage Roar', 'Flash Slice', 'Whirlwind Slice', 'Insignia Explosion', 'Heart Gore', 'Ambush', 'Shadowstrike', 'Infiltrate', 'Storm Rampage'],
                               ['Savage Fang', 'Swift Contract', 'Illusive Clone', 'Smoke Bomb', 'Throw Shadowblade', 'Evasion Stance']),
    'PvP: Abyss & Arena': (['Quick Slice', 'Savage Roar', 'Shadowstrike', 'Shadow Fall', 'Insignia Explosion', 'Heart Gore', 'Ambush', 'Infiltrate', 'Flash Slice', 'Whirlwind Slice', 'Defiance'],
                           ['Shadow Walk', 'Illusive Clone', 'Swift Contract', "Triniel's Dagger", 'Spiral Slice', 'Evasion Contract', 'Savage Fang', 'Throw Shadowblade'])}
S = 52; SW = 78
W = 24 + 11 * SW + 30 + 8 * SW + 24; H = 74 + len(bars) * 150
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 16), 'Assassin build loadouts', font=F(22, True), fill=TXT)
d.text((20, 44), 'Left of the line: the active bar.  Right of the line: stigmas (top-player usage).', font=F(14), fill=SUB)
for r, (bn, (act, stg)) in enumerate(bars.items()):
    y = 74 + r * 150; d.rounded_rectangle([12, y, W - 12, y + 140], 10, fill=CARD); d.text((24, y + 8), bn, font=F(15, True), fill=GOLD)
    x = 24
    def put(n, x):
        im = sk(n, S); img.paste(im, (x + (SW - S) // 2, y + 34), im)
        yy = y + 34 + S + 4
        for line in textwrap.wrap(n, 12, break_long_words=False)[:3]:
            w = d.textlength(line, font=F(10)); d.text((x + (SW - w) / 2, yy), line, font=F(10), fill=TXT); yy += 12
    for n in act:
        put(n, x); x += SW
    x += 18; d.line([(x - 10, y + 34), (x - 10, y + 128)], fill=SUB, width=2)
    for n in stg:
        put(n, x); x += SW
img.save('out/as_builds.png'); print('builds', img.size)


# ---------- combo chains ----------
def arrow(d, x0, y, x1, col=SUB):
    d.line([(x0, y), (x1 - 6, y)], fill=col, width=3); d.polygon([(x1, y), (x1 - 9, y - 6), (x1 - 9, y + 6)], fill=col)


def chain_rows(title, subtitle, rows, fn, S=56, SW=118):
    maxlen = max(len(r[1]) for r in rows); W = 40 + maxlen * SW + 20; H = 80 + len(rows) * 168
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    d.text((20, 16), title, font=F(22, True), fill=TXT); d.text((20, 46), subtitle, font=F(14), fill=SUB)
    for r, (rt, steps, note) in enumerate(rows):
        y = 78 + r * 168
        d.rounded_rectangle([12, y, W - 12, y + 158], 10, fill=CARD); d.text((26, y + 8), rt, font=F(15, True), fill=GOLD)
        for i, (nm, cap) in enumerate(steps):
            x = 26 + i * SW; cx = x + SW // 2 - 10
            if nm.startswith('!'):
                d.rounded_rectangle([cx - S // 2, y + 36, cx + S // 2, y + 36 + S], 8, fill=RED if 'STAG' in nm else PURPLE)
                for k, line in enumerate(textwrap.wrap(nm[1:], 9)):
                    w = d.textlength(line, font=F(11, True)); d.text((cx - w / 2, y + 48 + k * 14), line, font=F(11, True), fill=TXT)
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


chain_rows('Three Assassin damage engines', 'Every rotation is built from these chains',
           [('1. Insignia cycle', [('Savage Fang', '+5 Insignias, 600% ATK'), ('Ambush', '+2 Insignias from behind'), ('Savage Roar', '+1 Insignia each'),
                                   ('!5 STACKS', 'Stack cap'), ('Insignia Explosion', '352% ATK at 5 stacks, keeps 2 (spec)'), ('Quick Slice', 'Each hit -1s on Explosion (spec)')], 'Explosion every 7-10s'),
            ('2. Crit window', [('Illusive Clone', 'Heart Gore loses its CD, +20% dmg'), ('Swift Contract', '+20-30% Combat Speed'),
                                ('Heart Gore', 'Fires on every crit'), ('Heart Gore', '4 targets, +MP'), ('Heart Gore', 'Exploit Weakness clones add Insignias')], '10s every 90s'),
            ('3. Stun into Defense Break', [('Shadowstrike', 'Teleport behind, Stun 3s'), ('!DEF BREAK', 'Target -50-70% Defense 10s'),
                                            ('Shadow Fall', 'Knockdown on the Stunned target'), ("Triniel's Dagger", '+30% from behind'),
                                            ('Insignia Explosion', 'More Stun chance per stack')], 'Defense Break: 20s cooldown')],
           'as_combo_engines.png')
chain_rows('Assassin rotations', 'Single target, AoE pull and PvP burst, in cast order',
           [('Boss opener', [('Shadowstrike', 'Get behind, trigger Defense Break'), ('Savage Fang', '5 Insignias, +10% PvE (spec)'),
                             ('Swift Contract', '+Combat Speed'), ('Illusive Clone', 'Opens the 10s crit window'), ('Insignia Explosion', '5-stack hit'),
                             ("Triniel's Dagger", 'From behind'), ('Heart Gore', 'On every crit'), ('Ambush', 'Rebuild stacks')], '~1.7x damage inside the window'),
            ('AoE pull', [('Flash Slice', 'Blind the pack, 4 targets'), ('Savage Fang', '5 Insignias on 4 targets'), ('Whirlwind Slice', 'AoE (spec 8)'),
                          ('Insignia Explosion', '4 targets, Stun chance'), ('Savage Roar', 'Spam: +1 Insignia each'), ('Heart Gore', 'Procs on crits')], 'cleaves cap at 4 targets'),
            ('PvP burst', [('Shadow Walk', 'Open from Stealth'), ('Shadowstrike', 'Stun 3s'), ('Shadow Fall', 'Knockdown 3s'), ('Spiral Slice', 'Strip buffs'),
                           ('Insignia Explosion', 'Burst + Stun'), ("Triniel's Dagger", 'Their cooldowns +5%'), ('Evasion Contract', 'Escape: +200 Evasion')], 'open on healers and casters')],
           'as_combo_rotations.png')

# ---------- cooldown timeline (180s) ----------
lanes = [('Illusive Clone', 90, 10, GOLD), ('Swift Contract', 60, 10, GOLD), ('Savage Fang', 60, 10, RED), ("Triniel's Dagger", 45, 0, BLUE),
         ('Insignia Explosion', 10, 0, PURPLE), ('Evasion Stance', 20, 0, GREEN)]
notes = {'Illusive Clone': '90s · Heart Gore off cooldown 10s', 'Swift Contract': '60s · +20% Combat Speed 10s', 'Savage Fang': '60s · 5 Insignias, +10% PvE 10s',
         "Triniel's Dagger": '45s · -10% all your CDs (spec)', 'Insignia Explosion': '10s (7s with spec 16)', 'Evasion Stance': '20s · dodge a boss hit'}
L = 230; T = 180; PX = 5; W = L + T * PX + 40; H = 110 + len(lanes) * 58 + 70
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 16), 'Assassin cooldown alignment: one 180-second cycle', font=F(22, True), fill=TXT)
d.text((20, 46), 'Bars = buff duration, dots = casts. Gold columns = burst windows (0s full, 60s and 120s Fang + Swift, 90s Clone).', font=F(14), fill=SUB)
top = 96; bottom = top + len(lanes) * 58
for wx, a in ((0, 70), (60, 35), (90, 45), (120, 35)):
    ov = Image.new('RGBA', (10 * PX, bottom - top + 10), (232, 184, 74, a)); img.paste(ov, (L + wx * PX, top - 6), ov)
for s in range(0, T + 1, 15):
    x = L + s * PX; d.line([(x, top - 8), (x, bottom)], fill=(55, 61, 75), width=1); d.text((x - 8, bottom + 6), f'{s}s', font=F(11), fill=SUB)
for i, (nm, cd, dur, colr) in enumerate(lanes):
    y = top + i * 58; im = sk(nm, 40); img.paste(im, (20, y), im)
    d.text((68, y + 2), nm, font=F(13, True), fill=TXT); d.text((68, y + 20), textwrap.shorten(notes[nm], 28, placeholder='...'), font=F(10), fill=SUB)
    t = 0
    while t < T:
        if dur:
            d.rounded_rectangle([L + t * PX, y + 8, L + min(t + dur, T) * PX - 2, y + 32], 5, fill=colr)
        d.ellipse([L + t * PX - 5, y + 15, L + t * PX + 5, y + 25], fill=TXT if dur else colr)
        t += cd
d.text((20, bottom + 32), 'Hold Savage Fang and Swift Contract up to ~15s if Illusive Clone is about to come back; otherwise use them on cooldown.', font=F(13), fill=TXT)
img.save('out/as_combo_timeline.png'); print('timeline', img.size)

# ---------- dagger progression ----------
W1 = [('Wisdom Knife', 'Item Lv 36 · Legend t2', '~1,000'), ('Fallen Ancient God Dagger', 'Item Lv 46', '~1,500'), ('Resentful Pain', 'Item Lv 51', '~2,000'),
      ('Rupture Knife', 'Item Lv 54 · dungeon', '~2,000'), ('Enraged Kromede Silver Dagger', 'Item Lv 86 · t2', '2,500-3,000'),
      ('Dark Dragon Lord Dagger', 'Item Lv 78 · t3', '~3,000'), ('Splendent Ebony Dragon Lord Dagger', 'Item Lv 102 · t4', '3,000-3,500'), ("Ludra's Claw", 'Item Lv 102 · t4', '3,500+')]
tiles('Dagger progression', 'Badge = the iLv milestone where profiles carry it. Enchant to +15, then amplify to +20.',
      [{'img': it(n), 'name': n, 'sub': s, 'badge': 'iLv ' + m} for n, s, m in W1], 4, 'as_weapons.png', tw=190, th=150)

# ---------- potency chart ----------
data = [('Insignia Explosion', 990, '10s, 5 stacks'), ('Heart Gore', 648, '5s'), ('Whirlwind Slice', 484, '10s'), ('Ambush', 477, '10s, from behind'),
        ('Savage Fang', 293, '60s'), ('Flash Slice', 293, '10s'), ('Infiltrate', 291, '20s'), ('Shadow Fall', 283, '20s'),
        ("Triniel's Dagger", 217, '45s, from behind'), ('Smoke Bomb', 176, '30s'), ('Throw Shadowblade', 142, '30s'), ('Shadowstrike', 131, '20s'),
        ('Aerial Bind', 114, '120s'), ('Shadowstep', 101, '45s'), ('Spiral Slice', 65, '90s'), ('Assault Ambush', 44, '120s')]
RH = 40; L = 250; BW = 760; W = L + BW + 120; H = 96 + len(data) * RH + 30
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 14), 'Assassin damage per second of cooldown, skill level 20', font=F(22, True), fill=TXT)
d.text((20, 44), 'Single target, Attack 1,425. Insignia Explosion with its -3s spec reaches 1,415. Heart Gore has no cooldown during Illusive Clone.', font=F(14), fill=SUB)
mx = 1050
for i, (n, v, cd) in enumerate(data):
    y = 84 + i * RH; im = sk(n, 32); img.paste(im, (20, y + 2), im)
    d.text((60, y + 4), n, font=F(14, True), fill=TXT); d.text((60, y + 21), cd, font=F(11), fill=SUB)
    w = int(BW * v / mx); d.rounded_rectangle([L, y + 6, L + max(w, 4), y + 30], 5, fill=GOLD if i < 3 else (120, 132, 156))
    d.text((L + max(w, 4) + 8, y + 9), f'{v:,}', font=F(14, True), fill=TXT)
for gx in range(0, 1001, 250):
    x = L + int(BW * gx / mx); d.line([(x, 80), (x, H - 30)], fill=(50, 56, 70)); d.text((x - 10, H - 26), f'{gx:,}', font=F(11), fill=SUB)
img.save('out/as_potency.png'); print('potency', img.size)

# ---------- unlock cards ----------
cards = [(1, ['Quick Slice', 'Savage Roar', 'Shadowstrike'], 'Starter kit'), (3, ['Ambush'], 'Back attack'), (4, ['Heart Gore'], 'Fires on crits'), (5, ['Storm Rampage'], 'Stagger only'),
         (7, ['Whirlwind Slice'], 'Stun on Evasion'), (8, ['Flash Slice'], 'AoE Blind'), (9, [], 'Enhancement'), (10, ['Infiltrate'], 'Teleport behind'), (12, ['Shadow Fall'], '+ Nezekan board'),
         (14, ['Insignia Explosion'], 'Your best skill'), (16, ['Defiance'], 'CC break'), (19, [], 'First level-8 specs'), (20, [], 'Zikel board'),
         (22, ['Savage Fang', 'Swift Contract', 'Illusive Clone'], 'Stigmas'), (25, [], 'Supply Requests'), (30, [], 'Vaizel board, Daily Dungeon'), (40, [], 'Triniel board'),
         (45, [], 'Azphel, Abyss, Nightmare, Arcana, Transcendence')]
COLS = 6; CWD = 196; CH = 128; rows = (len(cards) + COLS - 1) // COLS
W = 20 + COLS * CWD + 10; H = 84 + rows * (CH + 10) + 10
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 14), 'Assassin: what unlocks when, level 1 to 45', font=F(22, True), fill=TXT)
d.text((20, 44), 'Skills at the character level they become learnable; gold cards are systems and Daevanion boards.', font=F(14), fill=SUB)
for i, (lv, sks, cap) in enumerate(cards):
    x = 20 + (i % COLS) * CWD; y = 78 + (i // COLS) * (CH + 10); sysc = not sks
    d.rounded_rectangle([x, y, x + CWD - 12, y + CH], 10, fill=CARD, outline=GOLD if sysc else CARD, width=2)
    d.text((x + 12, y + 8), 'Lv', font=F(11), fill=SUB); d.text((x + 12, y + 20), str(lv), font=F(26, True), fill=GOLD)
    ix = x + 56
    for s in sks[:3]:
        im = sk(s, 38); img.paste(im, (ix, y + 12), im); ix += 42
    yy = y + 60
    for line in textwrap.wrap(', '.join(sks), 26)[:2]:
        d.text((x + 12, yy), line, font=F(12, True), fill=TXT); yy += 15
    for line in textwrap.wrap(cap, 26)[:2]:
        d.text((x + 12, yy), line, font=F(12, not sks), fill=GOLD if sysc else SUB); yy += 15
img.save('out/as_unlocks.png'); print('unlocks', img.size)

# ---------- journey ----------
stages = [('1', 'Beginner', 'Level 1-19', 'Learn the kit', sk('Shadowstrike'), ['Get behind: Shadowstrike, Ambush', 'SP into Insignia Explosion first', 'Nezekan board opens at 12']),
          ('2', 'Leveling', 'Level 20-44', 'Insignias & stigmas', sk('Savage Fang'), ['Savage Fang and Swift Contract at 22', 'Level-8 specs on every active', 'Zikel 20 / Vaizel 30 / Triniel 40']),
          ('3', 'Level 45', 'iLv 1,000-3,000', 'Gear up', it('Resentful Pain'), ['Legend dagger, all gear +15', 'Illusive Clone window opener', '5 Arcana, finish 4 class boards']),
          ('4', 'Endgame ramp', 'iLv 3,000-5,000', 'Amplify & Daevanion', it("Ludra's Claw"), ['Amplify to +18 everywhere', 'Daevanion 400 > 950 nodes', 'Insignia Explosion to skill Lv 16']),
          ('5', 'Min-max', 'iLv 5,000-7,000', 'Perfect it', it('Chalice of Vigor'), ['+20 on everything', '10 Arcana at +5', 'Back Attack manastones, rerolls'])]
CW = 236; W = 20 + len(stages) * CW + 10; H = 330
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 14), 'Assassin journey: five stages to top rank', font=F(22, True), fill=TXT)
d.text((20, 44), 'Each stage is one Part of the guide. Levels gate the first two; item level (iLv) gates the rest.', font=F(14), fill=SUB)
for i, (num, name, rng, goal, ic, pts) in enumerate(stages):
    x = 20 + i * CW; y = 76
    d.rounded_rectangle([x, y, x + CW - 22, y + 236], 12, fill=CARD, outline=GOLD if i == 0 else CARD, width=2)
    d.ellipse([x + 12, y + 12, x + 40, y + 40], fill=GOLD); w = d.textlength(num, font=F(15, True)); d.text((x + 26 - w / 2, y + 17), num, font=F(15, True), fill=BG)
    d.text((x + 50, y + 12), name, font=F(16, True), fill=TXT); d.text((x + 50, y + 32), rng, font=F(12), fill=GOLD)
    img.paste(ic, (x + 12, y + 56), ic); d.text((x + 80, y + 64), 'Goal', font=F(11), fill=SUB)
    for k, line in enumerate(textwrap.wrap(goal, 16)):
        d.text((x + 80, y + 80 + k * 17), line, font=F(14, True), fill=TXT)
    yy = y + 128
    for p in pts:
        for k, line in enumerate(textwrap.wrap(p, 26)):
            d.text((x + 14 if k == 0 else x + 24, yy), ('- ' if k == 0 else '') + line, font=F(12), fill=TXT); yy += 15
        yy += 4
    if i < len(stages) - 1:
        ax = x + CW - 20; ay = y + 118; d.polygon([(ax, ay - 9), (ax + 16, ay), (ax, ay + 9)], fill=GOLD)
img.save('out/as_journey.png'); print('journey', img.size)

# ---------- ladders from assassin profiles ----------
main = ['weapon', 'guarder', 'helmet', 'shoulder', 'torso', 'pants', 'gloves', 'boots', 'cape']; acc = ['necklace', 'leftEarring', 'rightEarring', 'leftRing', 'rightRing', 'leftBracelet', 'rightBracelet']
prof = {}
for f in glob.glob('as/chars/*.json'):
    dd = json.load(open(f, encoding='utf8')); c = dd['character']; s = dd.get('snapshot') or {}
    if c.get('itemLevel') and s.get('equipment') and s.get('skills'): prof[c['characterId']] = dd


def bracket(lo, hi):
    ch = [x for x in prof.values() if lo <= x['character']['itemLevel'] < hi]
    S_ = [x['snapshot'] for x in ch]
    m = lambda xs: st.mean(xs) if xs else 0
    sl = lambda cat: m([k['level'] for s in S_ for k in s['skills'] if subcat.get(str(k['id'])) == cat and (cat != 'stigma' or k['isEquipped'])])
    slots = set()
    for s in S_:
        slots |= set(s['equipment'])
    return dict(n=len(ch), lv=m([x['character']['level'] for x in ch]), slots=m([len(s['equipment']) for s in S_]),
                ench=m([s['equipment'][k]['lvl'] for s in S_ for k in main if k in s['equipment']]), acc=m([s['equipment'][k]['lvl'] for s in S_ for k in acc if k in s['equipment']]),
                arc=m([len(s.get('arcana') or {}) for s in S_]), arct=m([sum(a.get('lvl', 0) for a in (s.get('arcana') or {}).values()) for s in S_]),
                nodes=m([sum(len(v) for v in (s.get('daevanion') or {}).values()) for s in S_]), act=sl('active'), stg=sl('stigma'), pas=sl('passive'))


SLOTS = ['Belt', 'Amulet', 'Rune x2', 'Brooch x2', 'Pendant', 'Seal x2', 'Wings']
STATE = {'none': [], 'belt': ['Belt'], 'base20': ['Belt', 'Amulet', 'Rune x2'], 'brooch1': ['Belt', 'Amulet', 'Rune x2', 'Brooch x2*', 'Wings'],
         'brooch': ['Belt', 'Amulet', 'Rune x2', 'Brooch x2', 'Wings'], 'pendant': ['Belt', 'Amulet', 'Rune x2', 'Brooch x2', 'Pendant*', 'Wings'],
         'seal': ['Belt', 'Amulet', 'Rune x2', 'Brooch x2*', 'Pendant*', 'Seal x2*', 'Wings'], 'all': SLOTS}
EST = {'1,000': dict(lv='Lv 30-40', ench='+5-10', acc='+5-10', arc=0, arct='-', nodes=50, skl='5-8 / - / 5'),
       '1,500': dict(lv='Lv 45', ench='+10', acc='+10', arc=2, arct='1-2 pcs', nodes=100, skl='8-10 / 1-5 / 8'),
       '2,000': dict(lv='Lv 45', ench='+10-12', acc='+10-12', arc=4, arct='3-5 pcs', nodes=150, skl='10 / 5-8 / 10')}
rows = []
spec = [('1,000', None, 'Wisdom Knife', 'Wisdom Breastplate', 'none'), ('1,500', None, 'Fallen Ancient God Dagger', 'Fallen Ancient God Breastplate', 'belt'),
        ('2,000', None, 'Resentful Pain', 'Vakron Breastplate', 'base20'), ('2,500', (2400, 3000), 'Enraged Kromede Silver Dagger', 'Nuakum Breastplate', 'base20'),
        ('3,000', (3000, 3500), 'Dark Dragon Lord Dagger', 'Ebony Dragon Lord Breastplate', 'base20'), ('3,500', (3500, 4000), 'Splendent Ebony Dragon Lord Dagger', 'Splendent Ebony Dragon Lord Breastplate', 'base20'),
        ('4,000', (4000, 4500), "Ludra's Claw", 'Splendent Ebony Dragon Lord Breastplate', 'brooch1'), ('4,500', (4500, 5000), "Ludra's Claw", 'Splendent Ebony Dragon Lord Breastplate', 'brooch1'),
        ('5,000', (5000, 5500), "Ludra's Claw", 'Splendent Ebony Dragon Lord Breastplate', 'pendant'), ('5,500', (5500, 6000), "Ludra's Claw", 'Splendent Ebony Dragon Lord Breastplate', 'pendant'),
        ('6,000', (6000, 6500), "Ludra's Claw", 'Splendent Ebony Dragon Lord Breastplate', 'seal'), ('6,500-7,000', (6500, 7100), "Ludra's Claw", 'Splendent Ebony Dragon Lord Breastplate', 'all')]
table = []
for ilv, rng, wpn, arm, stt in spec:
    if rng:
        b = bracket(*rng)
        r = dict(ilv=ilv, n=f"n = {b['n']}", lv=f"Lv {b['lv']:.0f}", wpn=wpn, arm=arm, ench=f"+{b['ench']:.0f}", acc=f"+{b['acc']:.0f}", st=stt, arc=round(b['arc']),
                 arct=f"{b['arc']:.0f} pcs, total {b['arct']:.0f}", nodes=int(round(b['nodes'], -1)), skl=f"{b['act']:.0f} / {b['stg']:.0f} / {b['pas']:.0f}")
    else:
        e = EST[ilv]; r = dict(ilv=ilv, n='estimate', lv=e['lv'], wpn=wpn, arm=arm, ench=e['ench'], acc=e['acc'], st=stt, arc=e['arc'], arct=e['arct'], nodes=e['nodes'], skl=e['skl'])
    rows.append(r); table.append(r)
json.dump(table, open('as/ladder.json', 'w'), indent=1)
chal = it('Chalice of Vigor', 22); PATHC = (150, 120, 60)


def ladder(sel, title, fn):
    RH = 104; W = 1180; H = 96 + len(sel) * (RH + 8) + 20
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    d.text((20, 14), title, font=F(22, True), fill=TXT)
    d.text((20, 44), 'Per milestone: dagger and armor with enchant, extra slots, Arcana, Daevanion nodes, skill levels (active / stigma / passive).', font=F(13), fill=SUB)
    d.text((20, 62), 'n = ranked Assassin profiles averaged; "estimate" rows come from item level requirements.  * = about half of profiles.', font=F(13), fill=SUB)
    for i, r in enumerate(sel):
        y = 90 + i * (RH + 8); d.rounded_rectangle([12, y, W - 12, y + RH], 10, fill=CARD)
        d.text((26, y + 12), 'iLv', font=F(12), fill=SUB); d.text((26, y + 26), r['ilv'], font=F(24, True), fill=GOLD)
        d.text((26, y + 58), r['lv'], font=F(13, True), fill=TXT); d.text((26, y + 76), r['n'], font=F(11), fill=SUB)
        x = 170
        for nm, en in ((r['wpn'], r['ench']), (r['arm'], r['acc'])):
            im = it(nm, 60); img.paste(im, (x, y + 10), im); badge(d, x + 2, y + 74, en); x += 74
        d.text((x + 4, y + 12), textwrap.shorten(r['wpn'], 32, placeholder='...'), font=F(12, True), fill=TXT)
        d.text((x + 4, y + 28), textwrap.shorten(r['arm'], 32, placeholder='...'), font=F(11), fill=SUB)
        d.text((x + 4, y + 46), f"Armor {r['ench']}  ·  Accessories {r['acc']}", font=F(12), fill=TXT)
        sx = 560; d.text((sx, y + 10), 'Extra slots', font=F(11), fill=SUB)
        on = STATE[r['st']]; cx = sx; cy = y + 28
        for s in SLOTS:
            lit = any(o.rstrip('*') == s for o in on); half = (s + '*') in on
            w = d.textlength(s, font=F(10, True)) + 10
            if cx + w > sx + 250:
                cx = sx; cy += 22
            d.rounded_rectangle([cx, cy, cx + w, cy + 17], 4, fill=(GOLD if lit and not half else (PATHC if half else DIM)))
            d.text((cx + 5, cy + 3), s, font=F(10, True), fill=BG if lit else SUB); cx += w + 5
        ax = 830; d.text((ax, y + 10), 'Arcana', font=F(11), fill=SUB)
        for k in range(10):
            px = ax + (k % 5) * 26; py = y + 28 + (k // 5) * 26
            if k < r['arc']:
                img.paste(chal, (px, py), chal)
            else:
                d.rounded_rectangle([px, py, px + 22, py + 22], 4, outline=DIM, width=2)
        d.text((ax, y + 82), r['arct'], font=F(11), fill=TXT)
        bx = 980; d.text((bx, y + 10), 'Daevanion nodes', font=F(11), fill=SUB)
        d.rounded_rectangle([bx, y + 30, bx + 180, y + 44], 5, fill=DIM)
        d.rounded_rectangle([bx, y + 30, bx + int(180 * min(r['nodes'], 1100) / 1100), y + 44], 5, fill=GOLD)
        d.text((bx, y + 48), f"~{r['nodes']:,} of ~1,100", font=F(12, True), fill=TXT)
        d.text((bx, y + 68), 'Skill Lv', font=F(11), fill=SUB); d.text((bx + 48, y + 66), r['skl'], font=F(12, True), fill=TXT)
    img.save('out/' + fn); print(fn, img.size)


ladder(rows[0:5], 'Assassin gear ladder, Part 3: iLv 1,000 to 3,000', 'as_ladder_1.png')
ladder(rows[5:9], 'Assassin gear ladder, Part 4: iLv 3,500 to 5,000', 'as_ladder_2.png')
ladder(rows[9:], 'Assassin gear ladder, Part 5: iLv 5,500 to 7,000', 'as_ladder_3.png')
for r in table:
    print(r['ilv'], r['n'], r['lv'], r['ench'], r['acc'], r['arct'], r['nodes'], r['skl'])
