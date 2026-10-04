import json, glob, textwrap
from PIL import Image, ImageDraw, ImageFont

F = lambda s, b=False: ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if b else 'arial.ttf'), s)
BG = (27, 31, 39); CARD = (37, 42, 53); TXT = (235, 236, 240); SUB = (160, 168, 182); GOLD = (232, 184, 74)
skills = {s['id']: s for s in json.load(open('ref/skillBuilder.getSkills.json', encoding='utf8')) if s.get('mainCategory') == 'gladiator'}
byname = {s['name']: k for k, s in skills.items()}


def sk(name, size=64):
    return Image.open(f'icons/sk_{byname[name]}.png').convert('RGBA').resize((size, size))


# ---------- build bars with labels ----------
exec(open('draw.py', encoding='utf8').read().split("bars = {")[0].split("A = [")[0])  # reuse helpers only
src = open('draw.py', encoding='utf8').read()
bars = eval('{' + src.split('bars = {')[1].split('}\nS = 48')[0] + '}')
S = 52; SW = 78
W = 24 + 10 * SW + 30 + 7 * SW + 24; H = 74 + len(bars) * 150
img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
d.text((20, 16), 'Build loadouts', font=F(22, True), fill=TXT)
d.text((20, 44), 'Left of the line: the 10-skill active bar.  Right of the line: stigmas.', font=F(14), fill=SUB)
for r, (bn, (act, stg)) in enumerate(bars.items()):
    y = 74 + r * 150; d.rounded_rectangle([12, y, W - 12, y + 140], 10, fill=CARD); d.text((24, y + 8), bn, font=F(15, True), fill=GOLD)
    x = 24
    def put(n, x):
        im = sk(n, S); img.paste(im, (x + (SW - S) // 2, y + 34), im)
        yy = y + 34 + S + 4
        for line in textwrap.wrap(n.replace("'s Blessing", "'s Bless."), 12, break_long_words=False)[:3]:
            w = d.textlength(line, font=F(10)); d.text((x + (SW - w) / 2, yy), line, font=F(10), fill=TXT); yy += 12
    for n in act:
        put(n, x); x += SW
    x += 18; d.line([(x - 10, y + 34), (x - 10, y + 128)], fill=SUB, width=2)
    for n in stg:
        put(n, x); x += SW
img.save('out/builds.png'); print('builds', img.size)

# ---------- Daevanion heatmaps ----------
nodes = [n for n in json.load(open('ref/daevanionPlanner.getDaevanionNodes.json', encoding='utf8')) if n['boardId'] in ('11', '12', '13', '14')]
idx = json.load(open('idx.json')); prof = {}
for r in idx:
    try:
        dd = json.load(open(r['file'], encoding='utf8'))
    except Exception:
        continue
    s = dd.get('snapshot') or {}
    if s.get('daevanion') and dd['character']['itemLevel'] > 3000:
        prof.setdefault(r['cid'], (r['type'], s['daevanion']))
ABBR = {'Attack': 'ATK', 'Critical Hit': 'CRT', 'Critical Hit Resist': 'CRR', 'Max HP': 'HP', 'Max MP': 'MP', 'Defense': 'DEF',
        'Combat Speed': 'SPD', 'Cooldown Reduction': 'CDR', 'Damage Boost': 'DMG', 'Damage Tolerance': 'TOL',
        'Critical Damage Boost': 'CDB', 'Critical Damage Tolerance': 'CDT', 'Multi-Hit Chance': 'MH', 'Multi-Hit Resist': 'MHR'}
BN = {'11': 'Nezekan (Lv 12)', '12': 'Zikel (Lv 20)', '13': 'Vaizel (Lv 30)', '14': 'Triniel (Lv 40)'}


def col(p):
    # dark grey -> gold
    lo = (58, 64, 78); hi = GOLD
    return tuple(int(lo[i] + (hi[i] - lo[i]) * p) for i in range(3))


def board(group, title, fn, sub):
    sel = [dv for t, dv in prof.values() if t == group]
    CELL = 46; PAD = 24
    boards = ['11', '12', '13', '14']
    sizes = {}
    for b in boards:
        ns = [n for n in nodes if n['boardId'] == b]
        r0 = min(n['row'] for n in ns); c0 = min(n['col'] for n in ns); r1 = max(n['row'] for n in ns); c1 = max(n['col'] for n in ns)
        sizes[b] = (r0, c0, r1 - r0 + 1, c1 - c0 + 1)
    bw = max(s[3] for s in sizes.values()) * CELL + PAD * 2; bh = max(s[2] for s in sizes.values()) * CELL + PAD * 2 + 30
    W = bw * 2 + 40; H = bh * 2 + 160
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    d.text((20, 16), title, font=F(22, True), fill=TXT); d.text((20, 46), sub, font=F(14), fill=SUB)
    for i, b in enumerate(boards):
        ox = 20 + (i % 2) * bw; oy = 76 + (i // 2) * bh
        with_b = [dv for dv in sel if b in dv]; nP = max(len(with_b), 1)
        d.rounded_rectangle([ox, oy, ox + bw - 10, oy + bh - 10], 12, fill=CARD)
        d.text((ox + PAD, oy + 10), BN[b] + f'  ·  {len(with_b)} profiles', font=F(15, True), fill=GOLD)
        r0, c0, R, Cn = sizes[b]
        offx = ox + PAD + (bw - 2 * PAD - 10 - Cn * CELL) // 2; offy = oy + 36
        for n in nodes:
            if n['boardId'] != b:
                continue
            p = sum(1 for dv in with_b if n['id'] in dv[b]) / nP
            cx = offx + (n['col'] - c0) * CELL + CELL // 2; cy = offy + (n['row'] - r0) * CELL + CELL // 2
            if n['nodeType'] == 'start':
                d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=TXT); continue
            if n['nodeType'] == 'skilllevel':
                sid = n['effect'][0]['skill_id']; im = Image.open(f'icons/sk_{sid}.png').convert('RGBA').resize((36, 36))
                if p < 0.5:
                    im = Image.blend(Image.new('RGBA', im.size, (37, 42, 53, 255)), im, 0.35)
                d.rounded_rectangle([cx - 21, cy - 21, cx + 21, cy + 21], 6, fill=col(p))
                img.paste(im, (cx - 18, cy - 18), im)
                continue
            nm = n['name'].split(',')[0]; ab = ABBR.get(nm, nm[:3].upper())
            if n['grade'] >= 41:
                d.polygon([(cx, cy - 21), (cx + 21, cy), (cx, cy + 21), (cx - 21, cy)], fill=col(p), outline=TXT)
                w = d.textlength(ab, font=F(11, True)); d.text((cx - w / 2, cy - 7), ab, font=F(11, True), fill=BG if p > 0.5 else TXT)
            else:
                rr = 15
                d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col(p))
                w = d.textlength(ab, font=F(10, True)); d.text((cx - w / 2, cy - 6), ab, font=F(10, True), fill=BG if p > 0.5 else TXT)
    # legend
    ly = H - 70
    for k in range(11):
        d.rectangle([20 + k * 26, ly, 20 + k * 26 + 24, ly + 16], fill=col(k / 10))
    d.text((20, ly + 22), '0%', font=F(12), fill=SUB); d.text((20 + 10 * 26 - 4, ly + 22), '100%', font=F(12), fill=SUB)
    d.text((320, ly - 2), 'Fill = share of top profiles that took the node.  Icon = Skill Level +1 node (faded if under 50%).', font=F(13), fill=TXT)
    d.text((320, ly + 18), 'Diamond = Unique 4-pt node (SPD Combat Speed, CDR Cooldown, DMG Damage Boost, CDB Crit Dmg, MH Multi-Hit).', font=F(13), fill=SUB)
    d.text((320, ly + 36), 'Circle = stat node: ATK Attack, CRT Crit Hit, CRR Crit Resist, HP, MP, DEF.  White dot = start.', font=F(13), fill=SUB)
    img.save('out/' + fn); print(fn, img.size)


board('nightmare', 'Daevanion: PvE (Nightmare) path', 'daev_pve.png', 'Node pick rate among the top 12 Taiwan Nightmare Gladiators (iLv 4,575-6,931). Class boards only; known nodes.')
board('abyss', 'Daevanion: PvP (Abyss) path', 'daev_pvp.png', 'Node pick rate among top Taiwan Abyss Gladiators with board data. Class boards only; known nodes.')
