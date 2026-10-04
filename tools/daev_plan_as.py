import json, heapq
from PIL import Image, ImageDraw, ImageFont

F = lambda s, b=False: ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if b else 'arial.ttf'), s)
BG = (27, 31, 39); CARD = (37, 42, 53); TXT = (235, 236, 240); SUB = (160, 168, 182); GOLD = (232, 184, 74); DIM = (52, 58, 72); PATH = (120, 98, 52)
ALL = [n for n in json.load(open('ref/daevanionPlanner.getDaevanionNodes.json', encoding='utf8')) if n['boardId'] in ('41', '42', '43', '44', '46')]
ABBR = {'Attack': 'ATK', 'Critical Hit': 'CRT', 'Critical Hit Resist': 'CRR', 'Max HP': 'HP', 'Max MP': 'MP', 'Defense': 'DEF',
        'Combat Speed': 'SPD', 'Cooldown Reduction': 'CDR', 'Damage Boost': 'DMG', 'Damage Tolerance': 'TOL',
        'Critical Damage Boost': 'CDB', 'Critical Damage Tolerance': 'CDT', 'Multi-Hit Chance': 'MH', 'Multi-Hit Resist': 'MHR',
        'PvP Attack': 'PATK', 'PvP Defense': 'PDEF', 'PvP Accuracy': 'PACC', 'PvP Evasion': 'PEVA', 'PvP Critical Hit': 'PCRT',
        'PvP Critical Hit Resist': 'PCRR', 'Status Effect Chance': 'SEC', 'Status Effect Resist': 'SER', 'PvP Damage Tolerance': 'PTOL', 'PvP Damage Boost': 'PDMG'}

PLANS = {
    '41': ('Nezekan', 12, ['Insignia Explosion', 'Exploit Weakness', 'Quick Slice', 'Shadowstrike', 'U:Cooldown Reduction', 'U:Combat Speed', 'Rear Smite',
                           'Storm Rampage', 'Assault Stance', 'Heightened Sixth Sense', 'Ambush', 'Rear Smite', 'U:Cooldown Reduction', 'Heightened Sixth Sense', 'Shadow Fall', 'U:Combat Speed']),
    '42': ('Zikel', 20, ['Defense Break', 'Determination', 'U:Damage Boost', 'Heart Gore', 'Insignia Explosion', 'Quick Slice', 'Ambush Stance', 'Savage Roar',
                         'Defense Break', 'Determination', 'U:Damage Boost', 'U:Damage Tolerance', 'Shadowstrike', 'Defiance', 'Infiltrate', 'Ambush', 'Revitalization Contract']),
    '43': ('Vaizel', 30, ['Assault Stance', 'Impact Hit', 'U:Critical Damage Boost', 'Defense Break', 'Determination', 'Ambush Stance', 'Quick Slice', 'Apply Poison',
                          'Revitalization Contract', 'Defiance', 'U:Critical Damage Tolerance', 'Infiltrate', 'Shadowstrike', 'Storm Rampage']),
    '44': ('Triniel', 40, ['Heart Gore', 'Exploit Weakness', 'Ambush', 'Storm Rampage', 'U:Multi-Hit Chance', 'Whirlwind Slice', 'Quick Slice', 'Rear Smite',
                           'Flash Slice', 'Heightened Sixth Sense', 'Defiance', 'Impact Hit', 'Revitalization Contract']),
    '46': ('Azphel (PvP)', 45, ['N:PvP Damage Boost', 'N:PvP Damage Boost', 'N:PvP Damage Tolerance', 'N:PvP Damage Boost', 'N:PvP Damage Tolerance',
                                'N:Status Effect Chance', 'N:Status Effect Resist', 'N:PvP Damage Boost', 'N:PvP Damage Tolerance', 'N:PvP Damage Tolerance']),
}


def label(n):
    if n['nodeType'] == 'skilllevel':
        return n['name'].replace('Skill Level Up - ', '')
    return n['name']


def matches(n, t):
    if t.startswith('U:'):
        return n['grade'] >= 41 and n['name'] == t[2:]
    if t.startswith('N:'):
        return n['name'] == t[2:]
    return n['nodeType'] == 'skilllevel' and label(n) == t


def plan(b):
    ns = [n for n in ALL if n['boardId'] == b]
    pos = {(n['row'], n['col']): n for n in ns}
    start = [n for n in ns if n['nodeType'] == 'start'][0]
    tree = {start['id']}
    steps = []; total = 0
    for t in PLANS[b][2]:
        # dijkstra from tree
        dist = {}; prev = {}; pq = []
        for nid in tree:
            dist[nid] = 0; heapq.heappush(pq, (0, nid))
        byid = {n['id']: n for n in ns}
        while pq:
            dd, u = heapq.heappop(pq)
            if dd > dist[u]:
                continue
            un = byid[u]
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                v = pos.get((un['row'] + dr, un['col'] + dc))
                if not v:
                    continue
                nd = dd + (0 if v['id'] in tree else v['costDaevanionPoint'])
                if nd < dist.get(v['id'], 1e9):
                    dist[v['id']] = nd; prev[v['id']] = u; heapq.heappush(pq, (nd, v['id']))
        cands = [n for n in ns if matches(n, t) and n['id'] not in tree]
        if not cands:
            got = [n for n in ns if matches(n, t) and n['id'] in tree and n['id'] not in {s['node'] for s in steps}]
            if got:
                steps.append({'n': len(steps) + 1, 'target': t.split(':')[-1] + ' (on path)', 'node': got[0]['id'], 'path': [], 'cost': 0, 'cum': total, 'via': []})
            else:
                print('  !! no target', t)
            continue
        best = min(cands, key=lambda n: dist.get(n['id'], 1e9))
        path = []; cur = best['id']
        while cur not in tree:
            path.append(cur); cur = prev[cur]
        cost = sum(byid[p]['costDaevanionPoint'] for p in path)
        total += cost
        for p in path:
            tree.add(p)
        steps.append({'n': len(steps) + 1, 'target': t.split(':')[-1], 'node': best['id'], 'path': path[::-1], 'cost': cost, 'cum': total,
                      'via': [label(byid[p]) for p in path[::-1][:-1]]})
    return ns, start, steps, tree


def render(b, ns, start, steps, tree, fn):
    name, lvl, _ = PLANS[b]
    r0 = min(n['row'] for n in ns); c0 = min(n['col'] for n in ns); R = max(n['row'] for n in ns) - r0 + 1; Cn = max(n['col'] for n in ns) - c0 + 1
    CELL = 46; PAD = 24; LW = 330
    W = Cn * CELL + PAD * 2 + LW; H = max(R * CELL + PAD * 2 + 70, 90 + len(steps) * 30 + 40)
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    d.text((20, 14), f'{name}: unlocks at level {lvl}', font=F(22, True), fill=TXT)
    d.text((20, 44), f'Numbered = buy order. Lit path = nodes you must pass through.  Core plan: {steps[-1]["cum"]} of {sum(n["costDaevanionPoint"] for n in ns)} points.', font=F(13), fill=SUB)
    target_num = {s['node']: s['n'] for s in steps}
    oy = 76
    for n in ns:
        cx = PAD + (n['col'] - c0) * CELL + CELL // 2; cy = oy + (n['row'] - r0) * CELL + CELL // 2
        on = n['id'] in tree
        if n['nodeType'] == 'start':
            d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=TXT); continue
        if n['nodeType'] == 'skilllevel':
            sid = n['effect'][0]['skill_id']; im = Image.open(f'icons/sk_{sid}.png').convert('RGBA').resize((36, 36))
            if not on:
                im = Image.blend(Image.new('RGBA', im.size, (37, 42, 53, 255)), im, 0.25)
            d.rounded_rectangle([cx - 21, cy - 21, cx + 21, cy + 21], 6, fill=GOLD if n['id'] in target_num else (PATH if on else DIM))
            img.paste(im, (cx - 18, cy - 18), im)
        else:
            ab = ABBR.get(n['name'].split(',')[0], n['name'][:3].upper())
            fill = GOLD if n['id'] in target_num else (PATH if on else DIM)
            if n['grade'] >= 41:
                d.polygon([(cx, cy - 21), (cx + 21, cy), (cx, cy + 21), (cx - 21, cy)], fill=fill, outline=TXT)
            else:
                d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=fill)
            fs = 9 if len(ab) > 3 else 10
            w = d.textlength(ab, font=F(fs, True)); d.text((cx - w / 2, cy - 6), ab, font=F(fs, True), fill=BG if on else SUB)
        if n['id'] in target_num:
            k = str(target_num[n['id']]); bx, by = cx + 12, cy - 24
            d.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(220, 60, 60), outline=TXT)
            w = d.textlength(k, font=F(11, True)); d.text((bx - w / 2, by - 7), k, font=F(11, True), fill=TXT)
    lx = Cn * CELL + PAD * 2 + 4
    d.text((lx, oy - 2), 'Order   Node                    Pts  Total', font=F(12, True), fill=SUB)
    for i, s in enumerate(steps):
        y = oy + 20 + i * 30
        d.ellipse([lx, y, lx + 20, y + 20], fill=(220, 60, 60)); k = str(s['n']); w = d.textlength(k, font=F(11, True)); d.text((lx + 10 - w / 2, y + 3), k, font=F(11, True), fill=TXT)
        d.text((lx + 30, y + 2), s['target'].replace('Experienced','Exp.')[:26], font=F(13), fill=TXT)
        d.text((lx + 228, y + 2), f"{s['cost']:>3}", font=F(13), fill=GOLD)
        d.text((lx + 270, y + 2), f"{s['cum']:>4}", font=F(13), fill=SUB)
    img.save('out/' + fn); print(fn, img.size)


out = {}
for b in PLANS:
    ns, start, steps, tree = plan(b)
    render(b, ns, start, steps, tree, f'as_daevplan_{b}.png')
    out[b] = steps
    print(PLANS[b][0], [(s['n'], s['target'], s['cost'], s['cum']) for s in steps])
json.dump(out, open('as/daevplan.json', 'w'), indent=1)
