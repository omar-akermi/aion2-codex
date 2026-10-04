"""Crafting visuals: necklace upgrade chain and material-source map."""
from PIL import Image, ImageDraw, ImageFont

F = lambda s, b=False: ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if b else 'arial.ttf'), s)
BG = (18, 21, 28); PANEL = (26, 31, 41); PANEL2 = (34, 40, 54); LINE = (46, 53, 69); TXT = (232, 230, 224); SUB = (155, 164, 182)
GOLD = (232, 184, 74); TEAL = (94, 196, 182); BLUE = (130, 174, 232); PINK = (232, 120, 160)


def ic(k, n=44):
    return Image.open(f'out/cr_{k}.png').convert('RGBA').resize((n, n), Image.LANCZOS)


def arrow(d, x0, y, x1, col=GOLD, label=None):
    d.line([(x0, y), (x1 - 10, y)], fill=col, width=4)
    d.polygon([(x1, y), (x1 - 14, y - 9), (x1 - 14, y + 9)], fill=col)
    if label:
        d.text(((x0 + x1) / 2, y - 12), label, font=F(13, True), fill=col, anchor='mb')


def card(img, d, x, y, w, h, title, sub, icon, mats, accent=GOLD, badge=None):
    d.rounded_rectangle([x, y, x + w, y + h], 14, fill=PANEL, outline=accent, width=2)
    im = ic(icon, 64); img.paste(im, (x + 14, y + 14), im)
    d.text((x + 90, y + 18), title, font=F(17, True), fill=TXT)
    d.text((x + 90, y + 44), sub, font=F(13), fill=SUB)
    if badge:
        tw = d.textlength(badge, font=F(12, True)) + 14
        d.rounded_rectangle([x + w - tw - 10, y - 11, x + w - 10, y + 11], 11, fill=accent)
        d.text((x + w - tw / 2 - 10, y), badge, font=F(12, True), fill=BG, anchor='mm')
    yy = y + 92
    for i, (k, q, name) in enumerate(mats):
        cx = x + 14 + (i % 2) * ((w - 28) // 2); cy = yy + (i // 2) * 52
        d.rounded_rectangle([cx, cy, cx + (w - 28) // 2 - 6, cy + 46], 8, fill=PANEL2)
        if k:
            m = ic(k, 34); img.paste(m, (cx + 6, cy + 6), m)
        d.text((cx + 46, cy + 6), f'×{q}', font=F(14, True), fill=GOLD)
        d.text((cx + 46, cy + 25), name, font=F(11), fill=SUB)


W, H = 1600, 600
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((40, 24), 'How a crafted accessory is made: the necklace', font=F(28, True), fill=TXT)
d.text((40, 62), 'Elyos names shown (True → White → Wise). Asmodians craft the same recipes as Star → Dark → Ebony. Earrings and rings use the same pattern with smaller amounts.', font=F(16), fill=SUB)

cw, ch, top = 350, 312, 130
xs = [40, 430, 820, 1210]
card(img, d, xs[0], top, cw, ch, "Artisan's Splendent Necklace", 'Base item · Jewelcrafting, beginner 40', 'artnl',
     [(None, 1, "Expert's Splendent"), ('refstone', 4, "Artisan's Refining"), ('ruby', 5, 'Pure Ruby'), ('odyle', 2, 'Pure Odyle')],
     accent=TEAL, badge='STEP 1')
card(img, d, xs[1], top, cw, ch, 'True Dragon Lord Necklace', 'Jewelcrafting, intermediate 60 · 62 iLv', 'nl_true',
     [('artnl', 1, 'Artisan\'s Splendent'), ('refstone', 3, 'Ultimate Refining'), ('scale', 14, 'Thick Balaur Scale'),
      ('mind', 6, 'Wrathful Mind'), ('ruby', 6, 'Radiant Ruby'), ('odyle', 2, 'Radiant Odyle')], badge='STEP 2')
card(img, d, xs[2], top, cw, ch, 'White Dragon Lord Necklace', 'Jewelcrafting, intermediate 75', 'nl_white',
     [('artnl', 1, 'Artisan\'s Splendent'), ('refstone', 3, 'Ultimate Refining'), ('scale2', 19, 'Hard Balaur Scale'),
      ('mind', 2, 'Wrathful Mind'), ('will', 9, 'Wrathful Will'), ('ruby', 8, 'Radiant Ruby'), ('odyle', 5, 'Radiant Odyle')], accent=BLUE, badge='STEP 3')
card(img, d, xs[3], top, cw, ch, 'Wise Dragon Lord Necklace', 'Jewelcrafting, intermediate 90', 'nl_wise',
     [('artnl', 1, 'Artisan\'s Splendent'), ('refstone', 4, 'Ultimate Refining'), ('scale3', 26, 'Durable Balaur Scale'),
      ('mind', 2, 'Wrathful Mind'), ('will', 2, 'Wrathful Will'), ('ego', 12, 'Wrathful Ego'), ('ruby', 8, 'Radiant Ruby'), ('odyle', 7, 'Radiant Odyle')], accent=PINK, badge='STEP 4')
for a, b in zip(xs, xs[1:]):
    arrow(d, a + cw + 6, top + 48, b - 6)

# combo explainer strip
y0 = top + ch + 30
d.rounded_rectangle([40, y0, W - 40, y0 + 110], 14, fill=PANEL2)
d.text((64, y0 + 18), 'Every craft rolls a 25% "combo"', font=F(18, True), fill=GOLD)
d.text((64, y0 + 46), 'A combo turns the result into the Splendent (better) version for free. No combo? Upgrade it later with a small', font=F(15), fill=TXT)
d.text((64, y0 + 68), 'Splendent recipe: True needs 7 Thick Scales + 2 Wrathful Mind; White needs 10 Hard Scales, 3 Will, 1 Ruby, 1 Odyle.', font=F(15), fill=TXT)
d.text((W - 64, y0 + 18), 'Step 2 needs the Splendent version of step 1', font=F(14, True), fill=TEAL, anchor='ra')
d.text((W - 64, y0 + 40), 'It only comes from the combo, so expect several tries.', font=F(14), fill=SUB, anchor='ra')
img.save('out/craft_chain.png'); print('chain', img.size)

# material sources map
W2, H2 = 1600, 560
im2 = Image.new('RGB', (W2, H2), BG); d = ImageDraw.Draw(im2)
d.text((40, 24), 'Where crafting materials come from', font=F(28, True), fill=TXT)
d.text((40, 62), 'Three sources feed every Dragon Lord recipe. Alts can farm the dungeon column and pass transferable drops through server storage.', font=F(16), fill=SUB)
cols = [
    ('GATHER', TEAL, 'Open-world nodes; Radiant grade at max level', [('ruby', 'Radiant gemstones', 'Ruby (necklace), Diamond (earrings), Sapphire (ring)'), ('ore', 'Radiant ore / logs', 'Weapon metal or wood for your weapon type'), ('odyle', 'Radiant Odyle', 'In almost every recipe')]),
    ('DUNGEONS', GOLD, 'Conquest dungeons by tier', [('mind', 'Wrathful Mind', 'Tier 1-2 Conquest (Crow Cave, Draupnir, Canyon, Vakron)'), ('will', 'Wrathful Will', 'Higher-tier Conquest; for White Dragon'), ('ego', 'Wrathful Ego', 'Tier 3 (Ferocious Horn Den); for Wise Dragon'), ('essence', "Balaur's Essence", 'Conquest drops; turned into scales / horns')]),
    ('CRAFT IT', PINK, 'Sub-materials you make yourself', [('scale', 'Balaur Scale (Jewelcrafting)', "2 Balaur's Essence + 1 Dragon Scale Hardener"), ('horn', 'Balaur Horn (Blacksmithing)', "2 Balaur's Essence + 1 Hammer"), ('intms', 'Intermediate Manastone (Alchemy)', '5 Lesser Manastone + 3 Spiritstone Powder + 2 Ink')]),
]
cw2 = (W2 - 80 - 40) // 3
for i, (t, col, sub, rows) in enumerate(cols):
    x = 40 + i * (cw2 + 20); y = 110
    d.rounded_rectangle([x, y, x + cw2, H2 - 30], 14, fill=PANEL, outline=col, width=2)
    d.text((x + 20, y + 18), t, font=F(18, True), fill=col)
    d.text((x + 20, y + 44), sub, font=F(13), fill=SUB)
    for j, (k, name, note) in enumerate(rows):
        yy = y + 80 + j * 88
        m = ic(k, 56); im2.paste(m, (x + 20, yy), m)
        d.text((x + 90, yy + 4), name, font=F(16, True), fill=TXT)
        words = note.split(); line = ''; ly = yy + 28
        for w in words:
            if d.textlength(line + ' ' + w, font=F(13)) > cw2 - 110:
                d.text((x + 90, ly), line.strip(), font=F(13), fill=SUB); ly += 17; line = ''
            line += ' ' + w
        d.text((x + 90, ly), line.strip(), font=F(13), fill=SUB)
im2.save('out/craft_sources.png'); print('sources', im2.size)
