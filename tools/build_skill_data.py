import json, glob, re, os, urllib.request, concurrent.futures as F
from PIL import Image

CLASSES = ['gladiator', 'templar', 'assassin', 'ranger', 'sorcerer', 'elementalist', 'cleric', 'chanter', 'fighter']
skills = [json.load(open(f)) for f in glob.glob('allsk/*.json')]
skills = [s for s in skills if s.get('_cls') in CLASSES]
MAXL = 40


def num(x):
    try:
        return float(x)
    except Exception:
        return None


def resolve(key, v, lv):
    parts = key.strip('{}').split(':')
    typ = parts[0]
    tail = [p for p in parts[1:] if not p.isdigit()]
    vals = v['base']['values'] if lv == 1 else (v.get('levels', {}).get(str(lv)) or {}).get('values')
    if vals is None:
        lvls = sorted(int(k) for k in v.get('levels', {}))
        cand = [k for k in lvls if k <= lv]
        vals = v['levels'][str(cand[-1])]['values'] if cand else v['base']['values']
    mods = [t.lower() for t in tail]
    field = tail[0] if tail else ''
    val = None
    if typ == 'se_dmg':
        f = field.lower()
        if 'heal' in f:
            idx = 1 if 'max' in f else 0
            val = num(vals[idx])
        else:
            hits = num(vals[4]) if len(vals) > 4 and num(vals[4]) else 1
            base = num(vals[0])
            val = base * (hits if 'sum' in f else 1) if base is not None else None
    elif typ in ('abe', 'se', 'se_abe'):
        m = re.search(r'value(\d+)', field)
        if m:
            i = int(m.group(1)) - 1
            val = num(vals[i]) if i < len(vals) else None
            if val is not None and i == 0 and typ == 'abe' and not num(vals[0]):
                val = None
        elif field == 'aggro_absolute':
            val = num(vals[0])
    elif typ == 'se_abe_dmg':
        return None
    if val is None:
        return None
    for mo in mods[1:]:
        if mo == 'divide100':
            val = val / 100
        elif mo == 'divide100abs':
            val = abs(val) / 100
        elif mo == 'noneabs':
            val = abs(val)
        elif mo == 'divide1000':
            val = val / 1000
        elif mo == 'time':
            val = val / 1000
        elif mo in ('tick', 'total'):
            val = val / 1000 if typ == 'se_abe_dmg' else val
    if typ == 'se_abe_dmg':
        val = val / 1000 if 'tick' not in mods and 'total' not in mods else val
    return round(val, 2)


def fmtn(x):
    if x is None:
        return '?'
    return str(int(x)) if abs(x - round(x)) < 1e-9 else ('%.2f' % x).rstrip('0').rstrip('.')


def template(text, ph):
    keys = []
    def sub(m):
        k = m.group(0)
        if k not in ph:
            return '?'
        if k not in keys:
            keys.append(k)
        return '{%d}' % keys.index(k)
    clean = re.sub(r'<[^>]+>', '', text or '')
    t = re.sub(r'\{[a-z_]+:[^{}]+\}', sub, clean)
    arrs = []
    for k in keys:
        v = ph[k]
        if v.get('levels'):
            arr = [fmtn(resolve(k, v, L)) for L in range(1, MAXL + 1)]
            # compress trailing duplicates
            while len(arr) > 1 and arr[-1] == arr[-2]:
                arr.pop()
        else:
            arr = [fmtn(resolve(k, v, 1))]
        arrs.append(arr)
    return t, arrs


# skill icons sprite
os.makedirs('sicons', exist_ok=True)


def dl(s):
    fn = f"sicons/{s['id']}.png"
    if os.path.exists(fn) or not s.get('icon'):
        return
    u = "https://cdn.questlog.gg/aion-2" + s['icon'].rsplit('.', 1)[0] + ".webp"
    try:
        raw = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://questlog.gg/'}), timeout=30).read()
        open(fn + '.w', 'wb').write(raw)
        Image.open(fn + '.w').convert('RGBA').resize((48, 48), Image.LANCZOS).save(fn); os.remove(fn + '.w')
    except Exception as e:
        print('ERR icon', s['name'], e)


with F.ThreadPoolExecutor(10) as ex:
    list(ex.map(dl, skills))
order = sorted(skills, key=lambda s: (CLASSES.index(s['_cls']), s['id']))
COLS = 24; S = 48
rows = (len(order) + COLS - 1) // COLS
sheet = Image.new('RGBA', (COLS * S, rows * S), (0, 0, 0, 0))
pos = {}
for n, s in enumerate(order):
    fn = f"sicons/{s['id']}.png"
    if os.path.exists(fn):
        sheet.paste(Image.open(fn), ((n % COLS) * S, (n // COLS) * S))
    pos[s['id']] = n
sheet.save('out/planner_skills.webp', 'WEBP', quality=88, method=6)

out = {'cols': COLS, 'size': S, 'classes': {}}
SUB_ORDER = {'active': 0, 'stigma': 1, 'passive': 2}
for c in CLASSES:
    lst = []
    for s in sorted([x for x in order if x['_cls'] == c], key=lambda x: (SUB_ORDER.get(x['subCategory'], 3), x['id'])):
        ph = s['descriptionData']['placeholders']
        tpl, arrs = template(s['description'], ph)
        learn = [[l['level'], l['characterLevel'], l['skillPoints'], l['stigmaPoints']] for l in (s.get('learning') or [])]
        specs = [[sp['parentSkillLvl'], re.sub(r'<[^>]+>', '', sp.get('specialized') or '')] for sp in (s.get('specializations') or [])]
        dm = [v for k, v in ph.items() if v['type'] == 'se_dmg' and 'max' in k.lower() and 'heal' not in k.lower()]
        coef = 0
        if dm:
            b = dm[0]['base']['values']; h = num(b[4]) or 1
            coef = round((num(b[2]) or 0) * h / 100, 2)
        lst.append({'i': s['id'], 'n': s['name'], 'k': 'basic' if s.get('isBasicSkill') else s['subCategory'], 'cd': (s.get('cooldown') or 0) / 1000,
                    'mp': ((s.get('consumed') or {}).get('mp') or 0), 'l': learn, 't': tpl, 'v': arrs, 'sp': specs, 'p': pos[s['id']], 'co': coef})
    out['classes'][c] = lst

# daevanion
boards = json.load(open('ref/daevanionPlanner.getDaevanionBoards.json', encoding='utf8'))
nodes = json.load(open('ref/daevanionPlanner.getDaevanionNodes.json', encoding='utf8'))
statmeta = json.load(open('statmeta.json', encoding='utf8'))
statmeta['cooltimedecrease'] = ['Cooldown Reduction', 1, 'Special', 7]
statmeta['pvpdecreasedamage'] = ['PvP Damage Tolerance', 1, 'PVP', 3]
json.dump(statmeta, open('statmeta.json', 'w', encoding='utf8'), ensure_ascii=False)
dv = {}
for b in boards:
    ns = [n for n in nodes if n['boardId'] == b['id']]
    if not ns:
        continue
    cl = []
    for n in ns:
        e = (n.get('effect') or [{}])
        if n['nodeType'] == 'skilllevel':
            eff = ['skill', e[0].get('skill_id'), e[0].get('level_increase', 1)]
        elif n['nodeType'] == 'start':
            eff = ['start']
        else:
            eff = ['stat'] + [[x.get('stat_name'), x.get('stat_value')] for x in e if x.get('type') == 'stat']
        cl.append([n['id'], n['row'], n['col'], n['grade'], n['costDaevanionPoint'], n['name'].replace('Skill Level Up - ', ''), eff])
    dv.setdefault(b['classId'], []).append({'id': b['id'], 'n': b['name'], 'lv': b['needLevel'], 'pt': b['costPointType'], 'o': b['order'], 'nodes': cl})
for c in dv:
    dv[c].sort(key=lambda b: b['o'])
out['boards'] = dv
# guide plans (cheapest paths computed for the guides)
plans = {}
for cls, fn in (('gladiator', 'daevplan.json'), ('assassin', 'as/daevplan.json')):
    if os.path.exists(fn):
        p = json.load(open(fn))
        plans[cls] = {b: sorted({nid for st in steps for nid in st['path']}) for b, steps in p.items()}
out['plans'] = plans
out['statsExtra'] = {'cooltimedecrease': statmeta['cooltimedecrease'], 'pvpdecreasedamage': statmeta['pvpdecreasedamage']}
json.dump(out, open('out/planner_skills.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print('skills json', os.path.getsize('out/planner_skills.json'), 'sprite', os.path.getsize('out/planner_skills.webp'), sheet.size)
print({c: len(v) for c, v in out['classes'].items()}, {c: [b['n'] for b in v] for c, v in dv.items() if c in ('gladiator', 'fighter')})
for nm in ['Rending Blow', 'Blade Toss', 'Ruinous Blow', 'Blood Absorption', 'Insignia Explosion', 'Defense Break', 'Determination', 'Tenaciousness', 'Apply Poison']:
    for c in out['classes'].values():
        for s in c:
            if s['n'] == nm:
                t = s['t']
                for j, a in enumerate(s['v']):
                    t = t.replace('{%d}' % j, a[0])
                print('--', nm, '|', t.replace('\n', ' ')[:300])
