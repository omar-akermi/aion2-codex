import json, textwrap
from PIL import Image, ImageDraw, ImageFont

F = lambda s, b=False: ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if b else 'arial.ttf'), s)
BG = (27, 31, 39); CARD = (37, 42, 53); TXT = (235, 236, 240); SUB = (160, 168, 182); GOLD = (232, 184, 74)
skills = {s['id']: s for s in json.load(open('ref/skillBuilder.getSkills.json', encoding='utf8')) if s.get('mainCategory') == 'gladiator'}
byname = {s['name']: k for k, s in skills.items()}


def icon(key, size=64):
    return Image.open(f'icons/{key}.png').convert('RGBA').resize((size, size))


def sk(name, size=64):
    return icon('sk_' + byname[name], size)


def tiles(title, subtitle, items, cols, fn, tw=150, th=150):
    rows = (len(items) + cols - 1) // cols
    W = cols * tw + 40; H = rows * th + 90
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    d.text((20, 16), title, font=F(22, True), fill=TXT); d.text((20, 46), subtitle, font=F(14), fill=SUB)
    for i, it in enumerate(items):
        x = 20 + (i % cols) * tw; y = 78 + (i // cols) * th
        d.rounded_rectangle([x + 4, y + 4, x + tw - 4, y + th - 4], 10, fill=CARD, outline=GOLD if it.get('hl') else CARD, width=2)
        ic = it['img']; img.paste(ic, (x + (tw - ic.width) // 2, y + 14), ic)
        yy = y + 14 + ic.height + 6
        for line in textwrap.wrap(it['name'], 19)[:2]:
            w = d.textlength(line, font=F(13, True)); d.text((x + (tw - w) / 2, yy), line, font=F(13, True), fill=TXT); yy += 16
        for line in textwrap.wrap(it.get('sub', ''), 23)[:2]:
            w = d.textlength(line, font=F(11)); d.text((x + (tw - w) / 2, yy), line, font=F(11), fill=GOLD if it.get('hl') else SUB); yy += 14
        if it.get('badge'):
            b = it['badge']; w = d.textlength(b, font=F(10, True)) + 10
            d.rounded_rectangle([x + 8, y + 8, x + 8 + w, y + 24], 4, fill=GOLD); d.text((x + 13, y + 10), b, font=F(10, True), fill=BG)
    img.save('out/' + fn); print(fn, img.size)


A = [('Overhead Slam', '5s CD · 1,841 dmg per CD-sec', '#1'), ('Ankle Slice', '10s · 871 per CD-sec', '#2'),
     ('Mocking Blade', '20s · 821 · Knockdown', '#3'), ('Ruinous Blow', '45s · 458 · +20% PvE buff', '#4'),
     ('Leaping Slam', '15s · 424 · gap closer', '#5'), ('Rush Strike', '20s (10s spec) · 737', '#6'),
     ('Crushing Wave', '20s · 305 · AoE', '#7'), ('Aerial Snare', '45s · +100% vs immune', '#8'),
     ('Sword Aura Rampage', 'Stagger window · no CD', '#9'), ('Rending Blow', 'Filler · 148.5% ATK', '#10'),
     ('Keen Strike', 'Basic · -1s Ruinous spec', '#11'), ('Defiance', '60s · CC break', 'PvP')]
tiles('Active skills: priority order', 'Ranked by damage per cooldown-second at skill level 20, Attack 1,425',
      [{'img': sk(n), 'name': n, 'sub': s, 'badge': b, 'hl': i < 3} for i, (n, s, b) in enumerate(A)], 6, 'skills_active.png')

ST = [('Rage Burst', '45s · 1,090% ATK · enables Overhead Slam', 1), ("Zikel's Blessing", '120s · +20% Attack 10s', 1),
      ('Lunge Stance', '60s · +20% Combat Speed', 1), ('Focused Block', '20s · Parry keeps +17% buff', 1),
      ('Lifestealing Blade', '90s · 4 targets · 10% HP', 1), ('Wave Armor', '60s · x1.5 passives', 1),
      ('Tenaciousness', '150s · 3s immune (PvP)', 0), ('Armor of Balance', '90s · Impact resist', 0),
      ('Blade Toss', '20s · -30% Def, -50% heal', 0), ('Wrath Wave', '60s · AoE Knockdown', 0),
      ('Forced Restraint', '60s · Seal', 0), ('Fracturing Rush', '90s · Root rush', 0), ('Assault Strike', '120s · 20m AoE', 0)]
tiles('Stigmas', 'Gold = the core six, run by 91-100% of top Nightmare Gladiators',
      [{'img': sk(n), 'name': n, 'sub': s, 'hl': h, 'badge': 'CORE' if h else None} for n, s, h in ST], 7, 'skills_stigma.png', tw=140, th=160)

P = [('Attack Preparation', 'Lv30: +20% PvE Dmg Boost', 1), ('Experienced Counterstrike', 'Lv30: +17% party buff on Block', 1),
     ('Murderous Burst', 'Lv30: +20% Crit Dmg', 1), ('Impact Hit', 'Lv30: +9% Double', 1), ('Identify Weakness', 'Lv30: +15% Perfect', 1),
     ('Survival Stance', 'Lv30: +65% Max HP', 0), ('Blood Absorption', 'Heal on hit, 55% emergency', 0),
     ('Survival Willpower', 'Lv30: 75% Status Resist', 0), ('Destructive Impulse', 'Bonus dmg vs Staggered', 0),
     ('Protection Armor', '+200 Block, heal on Block', 0)]
tiles('Passives: leveling priority', 'Gold = PvE damage core (top players push these to Lv 25-29)',
      [{'img': sk(n), 'name': n, 'sub': s, 'hl': h} for n, s, h in P], 5, 'skills_passive.png', tw=170)

bars = {
    'Nightmare DPS': (['Keen Strike', 'Rending Blow', 'Overhead Slam', 'Mocking Blade', 'Ankle Slice', 'Ruinous Blow', 'Leaping Slam', 'Rush Strike', 'Crushing Wave', 'Aerial Snare'],
                      ['Rage Burst', "Zikel's Blessing", 'Lunge Stance', 'Focused Block', 'Lifestealing Blade', 'Wave Armor', 'Armor of Balance']),
    'AoE farming / leveling': (['Keen Strike', 'Rending Blow', 'Leaping Slam', 'Crushing Wave', 'Overhead Slam', 'Mocking Blade', 'Ankle Slice', 'Rush Strike', 'Ruinous Blow', 'Aerial Snare'],
                               ['Lifestealing Blade', 'Rage Burst', "Zikel's Blessing", 'Lunge Stance', 'Wrath Wave', 'Focused Block']),
    'PvP: Abyss & Arena': (['Keen Strike', 'Rending Blow', 'Leaping Slam', 'Mocking Blade', 'Overhead Slam', 'Aerial Snare', 'Ankle Slice', 'Rush Strike', 'Ruinous Blow', 'Defiance'],
                           ['Blade Toss', 'Rage Burst', "Zikel's Blessing", 'Lunge Stance', 'Tenaciousness', 'Focused Block', 'Lifestealing Blade']),
    'Transcendence (long bosses)': (['Keen Strike', 'Rending Blow', 'Overhead Slam', 'Sword Aura Rampage', 'Mocking Blade', 'Ankle Slice', 'Ruinous Blow', 'Crushing Wave', 'Rush Strike', 'Aerial Snare'],
                                    ['Rage Burst', "Zikel's Blessing", 'Lunge Stance', 'Focused Block', 'Wave Armor'])}
S = 48; W = 24 + 10 * (S + 6) + 30 + 7 * (S + 6) + 24; H = 74 + len(bars) * 112
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 16), 'Build loadouts', font=F(22, True), fill=TXT)
d.text((20, 44), 'Left: 10-skill active bar, rotation priority left to right.  Right: stigmas.', font=F(14), fill=SUB)
for r, (bn, (act, stg)) in enumerate(bars.items()):
    y = 74 + r * 112; d.rounded_rectangle([12, y, W - 12, y + 102], 10, fill=CARD); d.text((24, y + 8), bn, font=F(15, True), fill=GOLD)
    x = 24
    for n in act:
        im = sk(n, S); img.paste(im, (x, y + 36), im); x += S + 6
    x += 18; d.line([(x - 12, y + 36), (x - 12, y + 36 + S)], fill=SUB, width=2)
    for n in stg:
        im = sk(n, S); img.paste(im, (x, y + 36), im); x += S + 6
img.save('out/builds.png'); print('builds', img.size)

G = json.load(open('icons/index.json', encoding='utf8')); gid = {v: k for k, v in G.items()}
W1 = [('Courage Greatsword', 'Item Lv 41 · Legend t2', '~1,500'), ('Fallen Ancient God Greatsword', 'Item Lv 46', '~1,500'),
      ('Earthly Authority', 'Item Lv 51', '~2,000'), ('Rupture Claymore', 'Item Lv 54 · dungeon', '~2,000'),
      ('Dark Dragon Lord Greatsword', 'Item Lv 78 · t3', '2,500-3,000'), ('Ebony Dragon Lord Greatsword', 'Item Lv 94 · t3', '~3,000'),
      ('Splendent Ebony Dragon Lord Greatsword', 'Item Lv 102 · t4', '3,000-3,500'), ("Ludra's Blade of Extinction", 'Item Lv 102 · t4', '3,500+')]
tiles('Greatsword progression', 'Badge = the iLv milestone where top profiles carry it. Enchant to +15, then amplify to +20.',
      [{'img': icon(gid[n]), 'name': n, 'sub': s, 'badge': 'iLv ' + m} for n, s, m in W1], 4, 'gear_weapons.png', tw=190, th=150)
E = [("Ludra's Heart", 'Guard · t4'), ('Splendent Ebony Dragon Lord Helm', 'Double, Attack increase'),
     ('Splendent Ebony Dragon Lord Pauldrons', 'Crit Damage Boost'), ('Splendent Ebony Dragon Lord Breastplate', 'Damage Boost'),
     ('Splendent Ebony Dragon Lord Gloves', 'Combat Speed'), ('Splendent Ebony Dragon Lord Greaves', 'Attack inc., Tolerance'),
     ('Splendent Ebony Dragon Lord Boots', 'Move Speed, Attack'), ('Splendent Ebony Dragon Lord Cloak', 'Perfect, Double'),
     ('Splendent Ebony Dragon Lord Necklace', 'Attack, Accuracy'), ('Splendent Ebony Dragon Lord Earrings', 'Attack, Accuracy, Crit'),
     ('Splendent Ebony Dragon Lord Ring', 'Attack, Accuracy, Crit'), ('Abyssal Bracelet', 'Time / Wisdom god stats'),
     ('Clash Rune', 'Rune · +6 to +8'), ('Chalice of Vigor', 'Primal Vigor Arcana set')]
tiles('t4 gear set: the substat to roll on each piece', 'Splendent Ebony Dragon Lord (t4, item Lv 102) plus guard, bracelet, rune and Arcana',
      [{'img': icon(gid[n]), 'name': n.replace('Splendent Ebony Dragon Lord ', 'Spl. Ebony DL '), 'sub': s} for n, s in E], 7, 'gear_set.png', tw=150, th=150)
