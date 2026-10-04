import json, os, sys, time
from qlapi import get

CLASSES = sys.argv[1].split(',') if len(sys.argv) > 1 else ['templar', 'ranger', 'sorcerer', 'elementalist', 'cleric', 'chanter', 'fighter']
TYPES = ['nightmare', 'transcendence', 'abyss']
for cls in CLASSES:
    os.makedirs(f'cls/{cls}/chars', exist_ok=True)
    idx = []
    for typ in TYPES:
        try:
            lb = get('armory.getLeaderboard', {'region': 'tw', 'type': typ, 'classId': cls, 'page': 1})
        except Exception as e:
            print(cls, typ, 'ERR', e); continue
        for row in lb['pageData'][:12]:
            cid = row['characterId']; fn = f'cls/{cls}/chars/' + cid.replace('/', '_').replace('=', '') + '.json'
            idx.append({'type': typ, 'rank': row.get('rank'), 'cid': cid, 'file': fn, 'point': row.get('point')})
            if not os.path.exists(fn):
                try:
                    c = get('armory.getCharacter', {'region': 'tw', 'characterId': cid})
                    json.dump(c, open(fn, 'w', encoding='utf8'))
                except Exception as e:
                    print(cls, cid, 'ERR', e)
                time.sleep(0.25)
    json.dump(idx, open(f'cls/{cls}/idx.json', 'w'))
    print(cls, 'profiles', len(idx), flush=True)
