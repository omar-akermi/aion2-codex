import json, heapq
from PIL import Image, ImageDraw, ImageFont

F = lambda s, b=False: ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if b else 'arial.ttf'), s)
BG = (27, 31, 39); CARD = (37, 42, 53); TXT = (235, 236, 240); SUB = (160, 168, 182); GOLD = (232, 184, 74); DIM = (52, 58, 72); PATH = (120, 98, 52)
ALLN = json.load(open('ref/daevanionPlanner.getDaevanionNodes.json', encoding='utf8'))
ALL = ALLN
PLANS = {}
ABBR = {'Attack': 'ATK', 'Critical Hit': 'CRT', 'Critical Hit Resist': 'CRR', 'Max HP': 'HP', 'Max MP': 'MP', 'Defense': 'DEF',
        'Combat Speed': 'SPD', 'Cooldown Reduction': 'CDR', 'Damage Boost': 'DMG', 'Damage Tolerance': 'TOL',
        'Critical Damage Boost': 'CDB', 'Critical Damage Tolerance': 'CDT', 'Multi-Hit Chance': 'MH', 'Multi-Hit Resist': 'MHR',
        'PvP Attack': 'PATK', 'PvP Defense': 'PDEF', 'PvP Accuracy': 'PACC', 'PvP Evasion': 'PEVA', 'PvP Critical Hit': 'PCRT',
        'PvP Critical Hit Resist': 'PCRR', 'Status Effect Chance': 'SEC', 'Status Effect Resist': 'SER', 'PvP Damage Tolerance': 'PTOL', 'PvP Damage Boost': 'PDMG'}

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
            sid = n['effect'][0]['skill_id']; im = Image.open(f'out/sk/{sid}.png').convert('RGBA').resize((36, 36))
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



import sys, statistics as stt
sys.argv = sys.argv[:1]
exec(open('gen_guides.py', encoding='utf8').read().split("names = {")[0])
CODE = {'templar': '2', 'ranger': '3', 'elementalist': '5', 'sorcerer': '6', 'cleric': '7', 'chanter': '8'}
BNAME = {'1': ('Nezekan', 12), '2': ('Zikel', 20), '3': ('Vaizel', 30), '4': ('Triniel', 40)}
UPREF = ['Combat Speed', 'Cooldown Reduction', 'Damage Boost', 'Critical Damage Boost', 'Multi-Hit Chance', 'Critical Hit', 'Attack', 'Damage Tolerance', 'Critical Damage Tolerance']
result = {}
for cls, code in CODE.items():
    pve, pvp, tot = load(cls); eq, lv = skillstats(pve)
    names = {s['n']: s for s in SK[cls]}
    imp = {s['n']: (stt.mean(lv[s['i']]) if lv.get(s['i']) else 0) for s in SK[cls]}
    result[cls] = {}
    for k in '1234':
        b = code + k
        ns = [n for n in ALLN if n['boardId'] == b]
        sk = []
        for n in ns:
            if n['nodeType'] == 'skilllevel':
                l = label(n)
                if l not in sk: sk.append(l)
        sk.sort(key=lambda x: -imp.get(x, 0))
        sk = [x for x in sk if x != 'Defiance'] + [x for x in sk if x == 'Defiance']
        uniq = []
        for n in ns:
            if n['grade'] >= 41 and n['nodeType'] != 'skilllevel' and n['name'] not in uniq: uniq.append(n['name'])
        uniq.sort(key=lambda x: UPREF.index(x) if x in UPREF else 99)
        targets = []; si = ui = 0
        while si < len(sk) or ui < len(uniq):
            for _ in range(2):
                if si < len(sk): targets.append(sk[si]); si += 1
            if ui < len(uniq): targets.append('U:' + uniq[ui]); ui += 1
        PLANS[b] = (BNAME[k][0], BNAME[k][1], targets)
        nsx, start, steps, tree = plan(b)
        cut = [s for s in steps if s['cum'] <= 90] or steps[:6]
        tree2 = {start['id']}
        for s in cut: tree2.update(s['path'])
        render(b, nsx, start, cut, tree2, f'{cls}_daevplan_{b}.png')
        result[cls][b] = {'name': BNAME[k][0], 'lvl': BNAME[k][1], 'steps': [(s['n'], s['target'], s['cost'], s['cum']) for s in cut]}
    # Azphel: same PvP list as other classes
    b = code + '6'
    PLANS[b] = ('Azphel (PvP)', 45, ['N:PvP Damage Boost', 'N:PvP Damage Boost', 'N:PvP Damage Tolerance', 'N:PvP Damage Boost', 'N:PvP Damage Tolerance', 'N:Status Effect Chance', 'N:Status Effect Resist'])
    nsx, start, steps, tree = plan(b)
    render(b, nsx, start, steps, tree, f'{cls}_daevplan_{b}.png')
    result[cls][b] = {'name': 'Azphel (PvP)', 'lvl': 45, 'steps': [(s['n'], s['target'], s['cost'], s['cum']) for s in steps]}
json.dump(result, open('out/daevplans_all.json', 'w'), indent=1)
