import json, time
D = json.load(open('out/planner_data.json', encoding='utf8'))
items = D['items']; mana = D['stones']['mana']
ARM = {'helmet': 'Helm', 'shoulder': 'Pauldrons', 'torso': 'Breastplate', 'pants': 'Greaves', 'gloves': 'Gloves', 'boots': 'Boots', 'cape': 'Cloak'}
MAIN = ['weapon', 'guard'] + list(ARM)


def find(cat, name, lvl=None):
    m = [i for i in items if i['c'] == cat and i['n'] == name and (lvl is None or i['l'] == lvl)]
    if not m:
        raise SystemExit('missing %s / %s' % (cat, name))
    return m[0]


PREF = {'weapon': ['combatspeed', 'amplifyweapondamage', 'str', 'agi', 'amplifyalldamage', 'additionalhitrate'],
        'guard': ['combatspeed', 'amplifyweapondamage', 'str', 'agi', 'amplifyalldamage', 'additionalhitrate'],
        'torso': ['amplifyalldamage', 'weaponfixingdamage', 'perfect'], 'shoulder': ['amplifycriticaldamage', 'weaponfixingdamage', 'perfect'],
        'helmet': ['damageratio', 'hardhit', 'weaponfixingdamage', 'perfect'], 'cape': ['damageratio', 'hardhit', 'perfect', 'weaponfixingdamage'],
        'pants': ['damageratio', 'decreasedamage', 'perfect', 'weaponfixingdamage'], 'gloves': ['combatspeed', 'perfect', 'weaponfixingdamage', 'damageratio'],
        'boots': ['movespeed', 'perfect', 'weaponfixingdamage', 'damageratio'], 'acc': ['weaponfixingdamage', 'critical', 'weaponaccuracy', 'str', 'agi', 'combatspeed'],
        'bracelet': ['time', 'wisdom', 'destruction', 'illusion', 'death']}


def subs(it, slot, cls, n):
    key = slot if slot in PREF else ('bracelet' if slot.startswith('bracelet') else 'acc')
    pref = PREF[key][:]
    if cls == 'assassin' and key == 'bracelet':
        pref = ['death', 'destruction', 'time', 'illusion', 'wisdom']
    pool = {s[0]: s for s in it['s']}; out = []
    for p in pref + [s[0] for s in it['s']]:
        if p in pool and p not in [o[0] for o in out] and len(out) < min(n, it['sb']):
            out.append([p, pool[p][2]])
    return out


def stones(it, slot, cls, grade):
    if not it['ms']:
        return []
    if slot in ('weapon', 'guard'):
        pick = ['weaponfixingdamage', 'weaponfixingdamage', 'critical', 'amplifyweapondamage']
    elif slot in ARM:
        pick = ['weaponfixingdamage', 'weaponfixingdamage', 'critical', 'amplifycriticaldamage']
        if cls == 'assassin':
            pick[-1] = 'amplifybackattack'
    else:
        pick = ['weaponfixingdamage', 'critical', 'accuracy', 'weaponfixingdamage']
    return [[p, mana[p][grade]] for p in pick[:it['ms']]]


def stage(name, level, cls, picks, ench_main, ench_acc, nsubs, grade):
    gear = {}
    for slot, it in picks.items():
        e = ench_main if slot in MAIN else ench_acc
        e = min(e, len(it['e']) + len(it['x']))
        gear[slot] = {'i': it['i'], 'e': e, 's': subs(it, slot, cls, nsubs), 'm': stones(it, slot, cls, grade) if grade >= 0 else [], 'c': []}
    return {'name': name, 'level': level, 'gear': gear}


def picks_for(cls, tier):
    W = {'gladiator': 'greatsword', 'assassin': 'dagger'}[cls]
    p = {}
    if tier == 1:
        p['weapon'] = find(W, {'gladiator': 'Fallen Ancient God Greatsword', 'assassin': 'Fallen Ancient God Dagger'}[cls])
        p['guard'] = find('guarder', 'Fallen Ancient God Guard')
        for s, n in ARM.items():
            p[s] = find(s, 'Fallen Ancient God ' + n)
        p['necklace'] = find('necklace', 'Fallen Ancient God Ruby Necklace')
        p['earring1'] = p['earring2'] = find('earring', 'Fallen Ancient God Diamond Earrings')
        p['ring1'] = p['ring2'] = find('ring', 'Fallen Ancient God Sapphire Ring')
        p['belt'] = find('belt', 'Noble Belt', 36); p['amulet'] = find('amulet', 'Revelation Amulet', 36)
    elif tier == 2:
        p['weapon'] = find(W, {'gladiator': 'Ebony Dragon Lord Greatsword', 'assassin': 'Ebony Dragon Lord Dagger'}[cls])
        p['guard'] = find('guarder', 'Ebony Dragon Lord Guard')
        for s, n in ARM.items():
            p[s] = find(s, 'Ebony Dragon Lord ' + n)
        p['necklace'] = find('necklace', 'Ebony Dragon Lord Necklace')
        p['earring1'] = p['earring2'] = find('earring', 'Ebony Dragon Lord Earrings')
        p['ring1'] = p['ring2'] = find('ring', 'Ebony Dragon Lord Ring')
        p['bracelet1'] = p['bracelet2'] = find('bracelet', 'Abyssal Bracelet')
        p['belt'] = find('belt', 'Noble Belt', 65); p['amulet'] = find('amulet', 'Revelation Amulet', 65)
        p['rune1'] = p['rune2'] = find('rune', 'Clash Rune')
    else:
        p['weapon'] = find(W, {'gladiator': "Ludra's Blade of Extinction", 'assassin': "Ludra's Claw"}[cls])
        p['guard'] = find('guarder', "Ludra's Heart")
        for s, n in ARM.items():
            p[s] = find(s, 'Splendent Ebony Dragon Lord ' + n)
        p['necklace'] = find('necklace', 'Splendent Ebony Dragon Lord Necklace')
        p['earring1'] = p['earring2'] = find('earring', 'Splendent Ebony Dragon Lord Earrings')
        p['ring1'] = p['ring2'] = find('ring', 'Splendent Ebony Dragon Lord Ring')
        p['bracelet1'] = p['bracelet2'] = find('bracelet', 'Abyssal Bracelet')
        p['belt'] = find('belt', 'Noble Belt', 65); p['amulet'] = find('amulet', 'Revelation Amulet', 65)
        p['rune1'] = p['rune2'] = find('rune', 'Clash Rune')
    return p


now = int(time.time() * 1000)
DESC = {
    'gladiator': 'Starter path from the Gladiator guide. Stage 1 is the fresh level-45 Legend set at +10; stage 2 is Ebony Dragon Lord t3 at +15 (around iLv 3,000); stage 3 is the t4 Splendent Ebony Dragon Lord set with Ludra\'s Blade, amplified to +20. Substats follow what top-ranked Gladiators roll: Combat Speed and Weapon Damage Boost on the weapon, Damage Boost on the torso, Crit Damage Boost on the shoulders, Combat Speed on the gloves, Time and Wisdom on bracelets. Pair with the Rage Burst into Overhead Slam rotation in the guide.',
    'assassin': 'Starter path from the Assassin guide. Same three tiers as the Gladiator path with daggers: Fallen Ancient God at +10, Ebony Dragon Lord t3 at +15, then Ludra\'s Claw and Splendent Ebony Dragon Lord at +20. Bracelets lean on Death [Triniel] for crit, and armor manastones include Back Attack Damage Boost, as top-ranked Assassins run. Pair with the Illusive Clone opener in the guide.'}
docs = {}
for cls in ('gladiator', 'assassin'):
    b = {'name': {'gladiator': 'Gladiator PvE progression (guide)', 'assassin': 'Assassin PvE progression (guide)'}[cls], 'cls': cls,
         'tags': ['PvE', 'DPS', 'Endgame'], 'desc': DESC[cls], 'author': None, 'created': now, 'updated': now, 'v': 1,
         'stages': [stage('Fresh 45', 45, cls, picks_for(cls, 1), 10, 10, 2, 0),
                    stage('iLv 3,000 · t3 +15', 45, cls, picks_for(cls, 2), 15, 15, 3, 1),
                    stage('Endgame · t4 +20', 50, cls, picks_for(cls, 3), 20, 20, 5, 2)]}
    docs['codex-' + cls + '-pve'] = b
json.dump(docs, open('seeds.json', 'w'), indent=1)
for k, v in docs.items():
    print(k, len(json.dumps(v)), [len(s['gear']) for s in v['stages']])
