import json
from PIL import Image, ImageDraw, ImageFont

F = lambda s, b=False: ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if b else 'arial.ttf'), s)
BG = (27, 31, 39); CARD = (37, 42, 53); TXT = (235, 236, 240); SUB = (160, 168, 182); GOLD = (232, 184, 74); DIM = (58, 64, 78); BLUE = (96, 165, 250)
skills = {s['id']: s for s in json.load(open('ref/skillBuilder.getSkills.json', encoding='utf8')) if s.get('mainCategory') == 'gladiator'}
byname = {s['name']: k for k, s in skills.items()}


def sk(name, size=32):
    return Image.open(f'icons/sk_{byname[name]}.png').convert('RGBA').resize((size, size))


# ---- skill potency bars ----
data = [('Overhead Slam', 1841, '5s'), ('Ankle Slice', 871, '10s'), ('Mocking Blade', 821, '20s'), ('Rage Burst', 758, '45s'),
        ('Rush Strike', 737, '10s w/ spec'), ('Ruinous Blow', 458, '45s'), ('Leaping Slam', 424, '15s'), ('Crushing Wave', 305, '20s'),
        ('Blade Toss', 137, '20s'), ('Aerial Snare', 119, '45s'), ('Wrath Wave', 92, '60s'), ('Forced Restraint', 91, '60s'),
        ('Lifestealing Blade', 87, '90s'), ('Fracturing Rush', 56, '90s'), ('Assault Strike', 43, '120s'), ('Wave Armor', 18, '60s')]
RH = 40; L = 250; BW = 760; W = L + BW + 120; H = 96 + len(data) * RH + 30
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 14), 'Damage per second of cooldown, skill level 20', font=F(22, True), fill=TXT)
d.text((20, 44), 'Single target, Attack 1,425. Higher = cast it every time it is ready. Fillers (Rending Blow, Keen Strike) have no cooldown.', font=F(14), fill=SUB)
mx = 1900
for i, (n, v, cd) in enumerate(data):
    y = 84 + i * RH
    im = sk(n); img.paste(im, (20, y + 2), im)
    d.text((60, y + 4), n, font=F(14, True), fill=TXT); d.text((60, y + 21), 'CD ' + cd, font=F(11), fill=SUB)
    w = int(BW * v / mx)
    d.rounded_rectangle([L, y + 6, L + max(w, 4), y + 30], 5, fill=GOLD if i < 3 else BLUE if n == 'Rage Burst' else (120, 132, 156))
    d.text((L + max(w, 4) + 8, y + 9), f'{v:,}', font=F(14, True), fill=TXT)
for gx in range(0, 2001, 500):
    x = L + int(BW * gx / mx)
    if gx <= mx:
        d.line([(x, 80), (x, H - 30)], fill=(50, 56, 70), width=1); d.text((x - 10, H - 26), f'{gx:,}', font=F(11), fill=SUB)
img.save('out/skill_potency.png'); print('potency', img.size)

# ---- iLv drivers ----
rows = [('2,500', 170, 12, 20), ('3,000', 200, 15, 20), ('3,500', 360, 17.8, 20), ('4,000', 660, 17.5, 20.5), ('4,500', 660, 17.9, 22),
        ('5,000', 890, 18.5, 22.2), ('5,500', 1050, 19.2, 21.3), ('6,000', 1055, 19.5, 22.9), ('6,500+', 1083, 20, 25)]
W = 1100; H = 520; L = 90; B = 420; T = 100; PW = 900
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 14), 'What drives iLv: Daevanion nodes and enchant level', font=F(22, True), fill=TXT)
d.text((20, 44), 'Averages of 61 ranked Gladiator profiles per iLv bracket. Bars = Daevanion nodes (left axis); line = average armor enchant (right axis).', font=F(14), fill=SUB)
n = len(rows); step = PW / n
for v in range(0, 1201, 200):
    y = B - (B - T) * v / 1200; d.line([(L, y), (L + PW, y)], fill=(50, 56, 70)); d.text((L - 46, y - 8), f'{v:,}', font=F(12), fill=SUB)
for e in (12, 14, 16, 18, 20):
    y = B - (B - T) * (e - 10) / 10; d.text((L + PW + 10, y - 8), f'+{e}', font=F(12), fill=BLUE)
pts = []
for i, (lab, nodes, ench, slots) in enumerate(rows):
    cx = L + step * i + step / 2
    h = (B - T) * nodes / 1200
    d.rounded_rectangle([cx - step * 0.32, B - h, cx + step * 0.32, B], 5, fill=GOLD)
    t = f'{nodes:,}'; w = d.textlength(t, font=F(12, True)); d.text((cx - w / 2, B - h + 8), t, font=F(12, True), fill=BG)
    w = d.textlength(lab, font=F(13, True)); d.text((cx - w / 2, B + 8), lab, font=F(13, True), fill=TXT)
    t = f'{slots:g} slots'; w = d.textlength(t, font=F(11)); d.text((cx - w / 2, B + 28), t, font=F(11), fill=SUB)
    pts.append((cx, B - (B - T) * (ench - 10) / 10))
d.line(pts, fill=BLUE, width=3)
for p in pts:
    d.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], fill=BLUE)
d.text((L, B + 52), 'iLv bracket', font=F(12), fill=SUB)
d.text((L + 160, B + 52), 'Biggest single jump: 3,500 -> 4,000 = +300 Daevanion nodes while enchant stays flat at +18.', font=F(13, True), fill=TXT)
img.save('out/ilv_drivers.png'); print('drivers', img.size)
