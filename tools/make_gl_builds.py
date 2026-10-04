import json, time
D = json.load(open('out/planner_data.json', encoding='utf8'))
SKD = json.load(open('out/planner_skills.json', encoding='utf8'))
items = D['items']; mana = D['stones']['mana']
ARM = {'helmet': 'Helm', 'shoulder': 'Pauldrons', 'torso': 'Breastplate', 'pants': 'Greaves', 'gloves': 'Gloves', 'boots': 'Boots', 'cape': 'Cloak'}
MAIN = ['weapon', 'guard'] + list(ARM)
CLS = 'gladiator'
SK = {s['n']: s for s in SKD['classes'][CLS]}
BOARDS = SKD['boards'][CLS]
PLANS = SKD['plans'][CLS]


def find(cat, name, lvl=None):
    m = [i for i in items if i['c'] == cat and i['n'] == name and (lvl is None or i['l'] == lvl)]
    assert m, (cat, name)
    return m[0]


def tier_items(t):
    p = {}
    W = {1: 'Fallen Ancient God Greatsword', 2: 'Ebony Dragon Lord Greatsword', 3: "Ludra's Blade of Extinction"}[t]
    p['weapon'] = find('greatsword', W)
    p['guard'] = find('guarder', {1: 'Fallen Ancient God Guard', 2: 'Ebony Dragon Lord Guard', 3: "Ludra's Heart"}[t])
    pre = {1: 'Fallen Ancient God ', 2: 'Ebony Dragon Lord ', 3: 'Splendent Ebony Dragon Lord '}[t]
    for s, n in ARM.items():
        p[s] = find(s, pre + n)
    if t == 1:
        p['necklace'] = find('necklace', 'Fallen Ancient God Ruby Necklace')
        p['earring1'] = p['earring2'] = find('earring', 'Fallen Ancient God Diamond Earrings')
        p['ring1'] = p['ring2'] = find('ring', 'Fallen Ancient God Sapphire Ring')
        p['belt'] = find('belt', 'Noble Belt', 36); p['amulet'] = find('amulet', 'Revelation Amulet', 36)
    else:
        p['necklace'] = find('necklace', pre + 'Necklace')
        p['earring1'] = p['earring2'] = find('earring', pre + 'Earrings')
        p['ring1'] = p['ring2'] = find('ring', pre + 'Ring')
        p['bracelet1'] = p['bracelet2'] = find('bracelet', 'Abyssal Bracelet')
        p['belt'] = find('belt', 'Noble Belt', 65); p['amulet'] = find('amulet', 'Revelation Amulet', 65)
        p['rune1'] = p['rune2'] = find('rune', 'Clash Rune')
    return p


PREF = {'weapon': ['combatspeed', 'amplifyweapondamage', 'str', 'agi', 'amplifyalldamage', 'additionalhitrate'],
        'guard': ['combatspeed', 'amplifyweapondamage', 'str', 'agi', 'amplifyalldamage', 'additionalhitrate'],
        'torso': ['amplifyalldamage', 'weaponfixingdamage', 'perfect'], 'shoulder': ['amplifycriticaldamage', 'weaponfixingdamage', 'perfect'],
        'helmet': ['damageratio', 'hardhit', 'weaponfixingdamage', 'perfect'], 'cape': ['damageratio', 'hardhit', 'perfect', 'weaponfixingdamage'],
        'pants': ['damageratio', 'decreasedamage', 'perfect', 'weaponfixingdamage'], 'gloves': ['combatspeed', 'perfect', 'weaponfixingdamage', 'damageratio'],
        'boots': ['movespeed', 'perfect', 'weaponfixingdamage', 'damageratio'], 'acc': ['weaponfixingdamage', 'critical', 'weaponaccuracy', 'str', 'agi', 'combatspeed']}


def gear(t, ench, nsubs, grade, bracelet, stones_kind='pve'):
    out = {}
    for slot, it in tier_items(t).items():
        e = min(ench if slot in MAIN else ench, len(it['e']) + len(it['x']))
        key = slot if slot in PREF else ('bracelet' if slot.startswith('bracelet') else 'acc')
        pref = bracelet if key == 'bracelet' else PREF[key]
        pool = {s[0]: s for s in it['s']}; subs = []
        for p in pref + [s[0] for s in it['s']]:
            if p in pool and p not in [x[0] for x in subs] and len(subs) < min(nsubs, it['sb']):
                subs.append([p, pool[p][2]])
        ms = []
        if it['ms'] and grade >= 0:
            if slot in ('weapon', 'guard'):
                pick = ['weaponfixingdamage', 'weaponfixingdamage', 'critical', 'amplifyweapondamage']
            elif slot in ARM:
                pick = ['weaponfixingdamage', 'pvpamplifydamage', 'critical', 'weaponfixingdamage'] if stones_kind == 'pvp' else ['weaponfixingdamage', 'weaponfixingdamage', 'critical', 'amplifycriticaldamage']
            else:
                pick = ['weaponfixingdamage', 'critical', 'accuracy', 'weaponfixingdamage']
            ms = [[p, mana[p][grade]] for p in pick[:it['ms']]]
        out[slot] = {'i': it['i'], 'e': e, 's': subs, 'm': ms, 'c': []}
    return out


def daev(board_names, extra=None):
    out = {}
    for b in BOARDS:
        if b['n'] in board_names and b['id'] in PLANS:
            out[b['id']] = PLANS[b['id']]
    return out


def daev_bonus(dv):
    bonus = {}
    for b in BOARDS:
        own = set(dv.get(b['id'], []))
        for n in b['nodes']:
            if n[0] in own and n[6][0] == 'skill':
                bonus[n[6][1]] = bonus.get(n[6][1], 0) + n[6][2]
    return bonus


def spec_pick(s, eff, keywords):
    th = sorted({p[0] for p in s['sp']}); slots = len([t for t in th if t <= eff])
    chosen = []
    for kw in keywords:
        for j, p in enumerate(s['sp']):
            if j not in chosen and p[0] <= eff and kw.lower() in p[1].lower():
                chosen.append(j); break
        if len(chosen) >= slots:
            break
    return chosen[:slots]


def skills(dv, targets, specs, bar, stig, stig_lv):
    bonus = daev_bonus(dv); out = {}
    for name, s in SK.items():
        if s['k'] == 'stigma':
            if name not in stig:
                continue
            lv = min(stig_lv.get(name, 5) if isinstance(stig_lv, dict) else stig_lv, len(s['l'])); x = max(0, targets.get(name, lv) - lv - bonus.get(s['i'], 0))
            eff = lv + bonus.get(s['i'], 0) + x
            out[s['i']] = {'lv': lv, 'x': x, 'sp': spec_pick(s, eff, specs.get(name, [])), 'eq': True}
        else:
            lv = min(10, len(s['l']) or 1); x = max(0, targets.get(name, lv) - lv - bonus.get(s['i'], 0))
            eff = lv + bonus.get(s['i'], 0) + x
            out[s['i']] = {'lv': lv, 'x': x, 'sp': spec_pick(s, eff, specs.get(name, [])), 'eq': name in bar}
    return out


BAR = ['Keen Strike', 'Rending Blow', 'Overhead Slam', 'Mocking Blade', 'Ankle Slice', 'Ruinous Blow', 'Leaping Slam', 'Rush Strike', 'Crushing Wave', 'Aerial Snare']
END_LV = {'Overhead Slam': 20, 'Ruinous Blow': 20, 'Rending Blow': 19, 'Crushing Wave': 15, 'Mocking Blade': 16, 'Ankle Slice': 16, 'Leaping Slam': 16, 'Rush Strike': 15,
          'Keen Strike': 14, 'Aerial Snare': 12, 'Sword Aura Rampage': 12, 'Defiance': 13, 'Attack Preparation': 29, 'Experienced Counterstrike': 29, 'Murderous Burst': 28,
          'Impact Hit': 25, 'Identify Weakness': 20, 'Survival Stance': 16, 'Blood Absorption': 16, 'Survival Willpower': 14, 'Destructive Impulse': 14, 'Protection Armor': 8,
          'Rage Burst': 20, "Zikel's Blessing": 24, 'Lunge Stance': 24, 'Focused Block': 20, 'Lifestealing Blade': 21, 'Wave Armor': 23, 'Tenaciousness': 18, 'Blade Toss': 16, 'Armor of Balance': 17, 'Wrath Wave': 15}
PVE_SPECS = {'Overhead Slam': ['Upward Strike', 'Critical Hit on hit', 'Remove cooldown'], 'Mocking Blade': ['Absorbs 4%', 'Changes to AoE damage', 'Ignores Block'],
             'Ankle Slice': ['+16m', 'Ignores Block', 'reset [Ankle Slice] cooldown'], 'Ruinous Blow': ['+12.5m', 'Extra damage', 'Ignores Block'],
             'Leaping Slam': ['trigger [Ankle Slice]', 'Resets cooldown on defeating', 'AoE'], 'Rush Strike': ['+10m', '-10s cooldown', 'Knockdown'],
             'Crushing Wave': ['Absorbs 2%', 'Resets cooldown on landing', 'pull'], 'Aerial Snare': ['Multi-Hit', '+100% damage', '-50%'],
             'Sword Aura Rampage': ['Restores 120 MP', 'Multi-Hit', '-1s all'], 'Rending Blow': ['mobile', 'more damage when less', 'Restores 50 MP'],
             'Keen Strike': ['+20% MP restored', '[Ruinous Blow] cooldown', 'Reckless'], 'Defiance': ['Restores 1000 Stamina', 'Restores 20% HP', 'Tenacity duration'],
             'Rage Burst': ['cooldown', 'PvE Damage Boost increase', 'Critical Hit on hit', 'Attack reduction'], "Zikel's Blessing": ['Stagger', 'PvE Damage Boost', 'Multi-Hit', 'Status'],
             'Lunge Stance': ['Double', 'Move Speed', 'Identify Weakness', 'cooldowns by 1s'], 'Focused Block': ['consecutive', '10% HP', 'Move Speed', 'mobile'],
             'Lifestealing Blade': ['-30s', 'Predation', 'HP absorbed', 'more targets'], 'Wave Armor': ['Experienced Counterstrike', 'Murderous Burst', 'Reflects', 'Absorbs'],
             'Armor of Balance': ['Blood Absorption', 'Protection Armor', 'Ailment', 'Impact-type Resist']}
PVP_SPECS = dict(PVE_SPECS)
PVP_SPECS.update({'Ruinous Blow': ['+12.5m', 'Skill Critical', 'Ignores Block'], 'Ankle Slice': ['Ignores Block', 'Knockdown', 'reset'], 'Mocking Blade': ['Ignores Block', '2 additional', '+1s Knockdown'],
                  'Leaping Slam': ['Damage Tolerance', 'Prepare for Battle', 'AoE'], 'Rush Strike': ['Knockdown Chance', '-10s', 'range'],
                  'Blade Toss': ['Incoming Heal reduction', 'breaks Protective', 'Slow', 'Knockdown'], 'Tenaciousness': ['Attack', '20% Max HP', 'Incoming Heal', 'Impact-type'],
                  'Rage Burst': ['cooldown', 'Attack reduction', 'Critical Hit on hit', 'PvE Damage Boost'], 'Focused Block': ['consecutive', 'Move Speed', '10% HP', 'mobile']})
AOE_SPECS = dict(PVE_SPECS)
AOE_SPECS.update({'Leaping Slam': ['AoE', 'Resets cooldown on defeating', 'Prepare for Battle'], 'Crushing Wave': ['pull', 'Resets cooldown on landing', 'more targets'],
                  'Overhead Slam': ['AoE', 'Remove cooldown', 'Critical'], 'Rending Blow': ['mobile', '-20% MP', 'Restores 50 MP'], 'Rush Strike': ['Charge Skill', '-10s', 'Knockdown'],
                  'Wrath Wave': ['more targets', '1 additional', 'Knockdown Chance', 'Attack by 20%']})
TR_SPECS = dict(PVE_SPECS)
TR_SPECS.update({'Sword Aura Rampage': ['-1s all', 'Multi-Hit', 'Restores 120 MP'], "Zikel's Blessing": ['Stagger', 'PvE Damage Boost', 'Multi-Hit', 'Status']})

PVE_STIG = ['Rage Burst', "Zikel's Blessing", 'Lunge Stance', 'Focused Block', 'Lifestealing Blade', 'Wave Armor', 'Armor of Balance']
PVP_STIG = ['Rage Burst', "Zikel's Blessing", 'Lunge Stance', 'Tenaciousness', 'Focused Block', 'Lifestealing Blade', 'Blade Toss']
AOE_STIG = ['Lifestealing Blade', 'Rage Burst', "Zikel's Blessing", 'Lunge Stance', 'Wrath Wave', 'Focused Block']
TR_STIG = ['Rage Burst', "Zikel's Blessing", 'Lunge Stance', 'Focused Block', 'Wave Armor']
CLASS4 = ['Nezekan', 'Zikel', 'Vaizel', 'Triniel']
B_PVE = ['time', 'wisdom', 'illusion', 'destruction']
now = int(time.time() * 1000)


def stage(name, level, t, ench, nsubs, grade, br, dvb, stig, stig_lv, specs, bar, targets, kind='pve'):
    dv = daev(dvb)
    return {'name': name, 'level': level, 'gear': gear(t, ench, nsubs, grade, br, kind), 'daev': dv, 'daevOn': True,
            'skills': skills(dv, targets, specs, bar, stig, stig_lv)}


early_t = {k: min(v, 10) for k, v in END_LV.items()}
mid_t = {k: min(v, 14) for k, v in END_LV.items()}
builds = {
    'codex-gladiator-pve': {'name': 'Gladiator Nightmare DPS', 'tags': ['PvE', 'DPS', 'Endgame'],
        'desc': 'The guide\'s main build in three stages. Fresh 45: Legend set at +10, first two Daevanion boards, actives at 10. iLv 3,000: Ebony Dragon Lord t3 at +15 and all four class boards. Endgame: t4 Splendent Ebony set with Ludra\'s Blade at +20, skill levels matching top Nightmare players (Overhead Slam 20 for its no-cooldown spec, Attack Preparation and Experienced Counterstrike 29). Specs follow Chef_Zhab\'s PvE video guide: Keen Strike MP regen, Leaping Slam Ankle Slice proc and reset on kill, Ruinous Blow range. Stigma order: Lunge Stance to 20 first, because its 1s cooldown cut on crits pairs with Overhead Slam\'s guaranteed crit; then Focused Block and Zikel\'s Blessing, with Rage Burst last. Play it from a priority macro: Leaping Slam in, Ruinous Blow, Focused Block on a parryable (yellow) boss attack, Rage Burst, then Overhead Slam every time it comes back.',
        'stages': [stage('Fresh 45', 45, 1, 10, 2, 0, B_PVE, CLASS4[:2], PVE_STIG[:4], {'Lunge Stance': 10}, PVE_SPECS, BAR, early_t),
                   stage('iLv 3,000 · t3 +15', 45, 2, 15, 3, 1, B_PVE, CLASS4, PVE_STIG, {'Lunge Stance': 20, 'Focused Block': 15, 'Rage Burst': 10, "Zikel's Blessing": 10, 'Lifestealing Blade': 10, 'Wave Armor': 10, 'Armor of Balance': 10}, PVE_SPECS, BAR, mid_t),
                   stage('Endgame · t4 +20', 50, 3, 20, 5, 2, B_PVE, CLASS4, PVE_STIG, 20, PVE_SPECS, BAR, END_LV)]},
    'codex-gladiator-aoe': {'name': 'Gladiator AoE farming', 'tags': ['PvE', 'DPS', 'Budget'],
        'desc': 'Pack-clearing setup for dungeon trash and open-world farming at around iLv 3,000. Leaping Slam (AoE + pull) and Crushing Wave (pull) group mobs, Wrath Wave knocks them down, Lifestealing Blade keeps you topped up. Pull 4 mobs: every cleave caps at 4 targets.',
        'stages': [stage('iLv 3,000 farmer', 45, 2, 15, 3, 1, B_PVE[:2] + ['destruction', 'illusion'], CLASS4, AOE_STIG, 15, AOE_SPECS, BAR, {k: max(v, 16) if k in ('Leaping Slam', 'Crushing Wave', 'Overhead Slam') else min(v, 14) for k, v in END_LV.items()})]},
    'codex-gladiator-pvp': {'name': 'Gladiator Abyss PvP', 'tags': ['PvP', 'DPS', 'Endgame'],
        'desc': 'Abyss and Arena diver. Same t4 gear as the PvE build but with PvP Damage Boost manastones, Tenaciousness and Blade Toss on the stigma bar, PvP specs (Ruinous Blow +12.5m range, Ankle Slice and Mocking Blade ignore Block) and the Azphel board filled for PvP stats. Open on healers with Blade Toss, Leaping Slam in, Mocking Blade into Overhead Slam and Aerial Snare, then Rage Burst and Ruinous Blow.',
        'stages': [stage('Endgame PvP', 50, 3, 20, 5, 2, ['time', 'illusion', 'destruction', 'wisdom'], CLASS4 + ['Azphel'], PVP_STIG, 20, PVP_SPECS, BAR[:9] + ['Defiance'], END_LV, 'pvp')]},
    'codex-gladiator-trans': {'name': 'Gladiator Transcendence', 'tags': ['PvE', 'DPS', 'Endgame'],
        'desc': 'Long single-target boss fights. Sword Aura Rampage takes a bar slot for Stagger windows (its level-16 spec cuts every cooldown by 1s per hit), Zikel\'s Blessing takes the +50% Stagger spec, and bracelets lean on Illusion for shorter cooldowns.',
        'stages': [stage('Endgame Transcendence', 50, 3, 20, 5, 2, ['illusion', 'time', 'wisdom', 'destruction'], CLASS4, TR_STIG, 20, TR_SPECS, ['Keen Strike', 'Rending Blow', 'Overhead Slam', 'Sword Aura Rampage', 'Mocking Blade', 'Ankle Slice', 'Ruinous Blow', 'Crushing Wave', 'Rush Strike', 'Aerial Snare'], dict(END_LV, **{'Sword Aura Rampage': 16}))]},
}
for k, b in builds.items():
    b.update({'cls': CLS, 'author': None, 'created': now, 'updated': now, 'v': 2})
    json.dump(b, open(f'glb_{k}.json', 'w'))
    st = b['stages'][-1]
    eqs = [SK_ for SK_ in SK.values() if st['skills'].get(SK_['i'], {}).get('eq')]
    print(k, len(json.dumps(b)), 'stigmas', [s['n'] for s in eqs if s['k'] == 'stigma'], 'specs', {SK[n]['n']: [SK[n]['sp'][j][1][:28] for j in st['skills'][SK[n]['i']]['sp']] for n in ['Overhead Slam', 'Ruinous Blow', 'Rage Burst']})
