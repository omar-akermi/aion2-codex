import json, os, urllib.request, concurrent.futures as F
from PIL import Image

items = json.load(open('ref/characterBuilder.getEquipmentItems.json', encoding='utf8'))
statmeta = json.load(open('statmeta.json', encoding='utf8'))
levels = json.load(open('ref/characterBuilder.getCharacterLevels.json', encoding='utf8'))

WEAPONS = ['greatsword', 'sword', 'dagger', 'bow', 'magicbook', 'orb', 'mace', 'staff', 'gauntlet', 'guarder']
ARMOR = ['helmet', 'shoulder', 'torso', 'pants', 'gloves', 'boots', 'cape']
ACC = ['necklace', 'earring', 'ring', 'bracelet']
EQUIP = ['belt', 'amulet', 'rune']


def keep(i):
    sc = i['subCategory']
    lvl = i.get('minLevelRequirement') or 0
    if sc in EQUIP or sc in ('bracelet', 'gauntlet'):
        return True
    if sc in WEAPONS + ARMOR + ['necklace', 'earring', 'ring']:
        return i['grade'] >= 41 and lvl >= 30
    return False


sel = {}
for i in items:
    if not keep(i):
        continue
    k = (i['name'], i['subCategory'], i['equipmentInfo'].get('itemLevel'), i['grade'])
    if k not in sel or i.get('exchangeType') == 'soulbind_acquire':
        sel[k] = i
sel = sorted(sel.values(), key=lambda i: (i['subCategory'], -(i['equipmentInfo'].get('itemLevel') or 0), i['name']))
print('items', len(sel))

# icons -> one sprite sheet
os.makedirs('picons', exist_ok=True)


def dl(i):
    fn = f"picons/{i['id']}.png"
    if os.path.exists(fn):
        return
    u = "https://cdn.questlog.gg/aion-2" + i['icon'].rsplit('.', 1)[0] + ".webp"
    try:
        raw = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://questlog.gg/'}), timeout=30).read()
        open(fn + '.webp', 'wb').write(raw)
        im = Image.open(fn + '.webp').convert('RGBA'); im = im.resize((48, 48), Image.LANCZOS); im.save(fn); os.remove(fn + '.webp')
    except Exception as e:
        print('ERR', i['name'], e)


with F.ThreadPoolExecutor(10) as ex:
    list(ex.map(dl, sel))
icons = {}
for i in sel:
    icons.setdefault(i['icon'], i['id'])  # dedupe identical icons
uniq = list(icons.items())
COLS = 24; S = 48
rows = (len(uniq) + COLS - 1) // COLS
sheet = Image.new('RGBA', (COLS * S, rows * S), (0, 0, 0, 0))
pos = {}
for n, (icon, iid) in enumerate(uniq):
    fn = f'picons/{iid}.png'
    if os.path.exists(fn):
        sheet.paste(Image.open(fn), ((n % COLS) * S, (n // COLS) * S))
    pos[icon] = n
sheet.save('out/planner_icons.png', optimize=True)
print('sprite', sheet.size, len(uniq), os.path.getsize('out/planner_icons.png'))

used = set()


def stats_dict(d):
    d = {k: v for k, v in (d or {}).items() if k in statmeta}
    used.update(d)
    return d


def flat(st):
    return {k: (v['value'] if isinstance(v, dict) else v) for k, v in (st or {}).items()}


out_items = []
for i in sel:
    s = i.get('itemStats') or {}
    ei = i.get('equipmentInfo') or {}
    ench = [stats_dict(flat(e['stats'])) for e in sorted(s.get('enchants') or [], key=lambda e: e['level'])]
    exc = [stats_dict(e.get('stats')) for e in sorted(s.get('exceedEnchants') or [], key=lambda e: e['level'])]
    exc = [e for e in exc if e]
    subs = []
    for x in s.get('subStats') or []:
        if x['id'] in statmeta:
            used.add(x['id']); subs.append([x['id'], x['minValue'], x['maxValue']])
    out_items.append({
        'i': i['id'], 'n': i['name'], 'g': i['grade'], 't': i.get('itemTier') or '', 'c': i['subCategory'],
        'l': ei.get('itemLevel') or 0, 'r': i.get('minLevelRequirement') or 0, 'p': pos[i['icon']],
        'm': stats_dict(s.get('mainStats')), 'e': ench, 'x': exc, 's': subs,
        'ms': ei.get('magicStoneSlotCount') or 0, 'sb': ei.get('soulbindRandomStatCount') or 0,
    })

# manastones: best value per stat across Superior variants (by grade)
stones = {}
for i in items:
    if i['subCategory'] != 'magicstone' or 'Superior' not in i['name']:
        continue
    kind = 'soul' if 'Soulstone' in i['name'] else 'mana'
    for m in (i.get('usableInfo') or {}).get('magicStoneStats') or []:
        sid = m['statId']
        if sid not in statmeta:
            continue
        used.add(sid)
        vals = sorted(m['stats'], key=lambda z: z['grade'])
        cur = stones.setdefault(kind, {}).get(sid)
        top = vals[-1]['value']
        if not cur or top > cur[-1]:
            stones[kind][sid] = [v['value'] for v in vals]

base = {}
for r in levels:
    if r['level'] in (30, 40, 45, 50):
        base.setdefault(r['class'], {})[r['level']] = r['stats']
used.update(['hpmax', 'fixingdamage', 'defense'])
for k in ['str', 'agi', 'con', 'dex', 'int', 'wis', 'time', 'wisdom', 'destruction', 'illusion', 'justice', 'freedom', 'death', 'life', 'space', 'destiny',
          'pveamplifydamage', 'amplifybackattack', 'pvpevasion', 'pvpblock', 'criticalratio', 'accuracyratio', 'damageratio', 'maxhpratio']:
    used.add(k)
meta = {k: statmeta[k] for k in sorted(used) if k in statmeta}
data = {'items': out_items, 'stats': meta, 'stones': stones, 'base': base, 'spriteCols': COLS, 'spriteSize': S}
json.dump(data, open('out/planner_data.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print('data bytes', os.path.getsize('out/planner_data.json'), 'stats', len(meta), 'stones', {k: len(v) for k, v in stones.items()})
print('base classes', list(base))
