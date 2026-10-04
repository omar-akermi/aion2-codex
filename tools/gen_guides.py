"""Generate data-driven class guides from questlog skill data + top-ranked Taiwan profiles."""
import json, glob, re, statistics as st, collections as C, html

SK = json.load(open('out/planner_skills.json', encoding='utf8'))['classes']
META = json.load(open('statmeta.json', encoding='utf8'))
ITEMS = {i['id']: i for i in json.load(open('ref/characterBuilder.getEquipmentItems.json', encoding='utf8'))}
E = html.escape

NOTES = {
    'templar': "Your shield skills feed Judgment. Put the Judgment chain on its own key, let the macro handle Pummel and what it triggers, use Punishment whenever it's ready, and block the boss's big hits so the party keeps Fury.",
    'ranger': "Open with your buffs and keep Marking Shot's Precision buff on the target, which adds Critical Hit and Deadshot damage. Then cycle Snipe, the macro and fully charged Deadshots.",
    'sorcerer': "One macro keeps Element Enhancement and Wish of Concentration running and mixes Flame Arrow into the fire and ice lines to protect your MP. Hellfire is the one spell you charge by hand.",
    'elementalist': "Buff before you summon, because a spirit copies your stats at the moment it appears. Keep five Cold Shock stacks, open with buffs and the Ancient Spirit, and let the macro fire Elemental Fusion on cooldown.",
    'cleric': "Earth Punishment makes Condemnation always crit, and every crit resets Condemnation, so it runs with no cooldown. Divine Aura, Bolt and Noble Aura add damage around it.",
    'chanter': "Keep Undefeated Mantra up and press the line where Spinning Strike and Impactful Crush open Dark Crush, weaving Onslaught between hits. Use Marchutan's Wrath by hand while Dark Crush is down.",
}
SLOTS = [('weapon', 'Weapon'), ('guarder', 'Guard'), ('torso', 'Torso'), ('shoulder', 'Shoulders'), ('helmet', 'Helmet'), ('gloves', 'Gloves'),
         ('pants', 'Pants'), ('boots', 'Boots'), ('cape', 'Cape'), ('necklace', 'Necklace'), ('leftEarring', 'Earrings'), ('leftRing', 'Rings'), ('leftBracelet', 'Bracelets')]


def statname(k):
    m = META.get(k)
    return m[0] if m else k


def fmtv(k, v):
    m = META.get(k)
    pct = m and m[1] == 1
    return (f'{v:.1f}%' if pct else f'{v:.0f}')


def desc(s, lvl=10):
    t = s.get('t') or ''
    v = s.get('v') or []
    def rep(m):
        i = int(m.group(1))
        if i < len(v) and v[i]:
            arr = v[i]; return str(arr[min(lvl, len(arr)) - 1])
        return '?'
    t = re.sub(r'\{(\d+)\}', rep, t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t if len(t) < 230 else t[:227].rsplit(' ', 1)[0] + '…'


def load(cls):
    idx = json.load(open(f'cls/{cls}/idx.json'))
    seen = {}
    for j in idx:
        try:
            d = json.load(open(j['file'], encoding='utf8'))
        except Exception:
            continue
        s = d.get('snapshot') or {}
        if not s.get('skills') or not d['character'].get('itemLevel'):
            continue
        seen.setdefault(d['character']['characterId'], (j, d))
    pve = [d for j, d in seen.values() if j['type'] in ('nightmare', 'transcendence')]
    pvp = [d for j, d in seen.values() if j['type'] == 'abyss']
    return pve, pvp, len(seen)


def skillstats(chars):
    eq, lv = C.Counter(), C.defaultdict(list)
    for d in chars:
        for x in d['snapshot']['skills']:
            i = str(x['id']); lv[i].append(x['level'])
            if x.get('isEquipped'):
                eq[i] += 1
    return eq, lv


def icon(i, n):
    return f'<img class="ski" src="img/sk/{i}.png" alt="" loading="lazy" title="{E(n)}">'


def pct(a, n):
    return f'{round(100 * a / n)}%' if n else '—'


def gen(cls, name):
    pve, pvp, total = load(cls)
    n1, n2 = len(pve), len(pvp)
    ilv = [d['character']['itemLevel'] for d in pve + pvp]
    skills = SK.get(cls) or []
    pre = cls + '-g'
    out = []
    if skills:
        eq1, lv1 = skillstats(pve); eq2, lv2 = skillstats(pvp)
        act = [s for s in skills if s['k'] in ('active', 'basic')]
        sti = [s for s in skills if s['k'] == 'stigma']
        pas = [s for s in skills if s['k'] == 'passive']
        avg = lambda lv, i: st.mean(lv[i]) if lv.get(i) else 0
        act.sort(key=lambda s: (-eq1[s['i']], -avg(lv1, s['i'])))
        sti.sort(key=lambda s: (-eq1[s['i']], -avg(lv1, s['i'])))
        pas.sort(key=lambda s: -avg(lv1, s['i']))
        core = [s for s in act if eq1[s['i']] >= 0.6 * n1][:8] or act[:8]
        stig = sti[:6]
        keyp = pas[:5]
        stig_pvp = sorted(sti, key=lambda s: -eq2[s['i']])[:6]

        def row(items):
            return ''.join(f'<span class="gi" title="{E(s["n"])}"><img src="img/sk/{s["i"]}.png" alt=""><small>{E(s["n"])}</small></span>' for s in items)
        note = NOTES.get(cls)
        out.append(f'<h2 id="{pre}-glance">Build at a glance</h2>')
        out.append('<div class="glance">' + (f'<p class="glance-s">{E(note)}</p><p class="meta">Play note summarized from creators collected on <a href="https://couga54.github.io/aion2-guides/en/{cls}/" target="_blank" rel="noopener">couga54\'s {name} guide</a></p>' if note else '') +
                   f'<div class="glance-row"><span class="glance-l">Core skills</span><div class="glance-icons">{row(core)}</div></div>'
                   f'<div class="glance-row"><span class="glance-l">Stigmas · PvE</span><div class="glance-icons">{row(stig)}</div></div>'
                   f'<div class="glance-row"><span class="glance-l">Stigmas · Abyss</span><div class="glance-icons">{row(stig_pvp)}</div></div>'
                   f'<div class="glance-row"><span class="glance-l">Key passives</span><div class="glance-icons">{row(keyp)}</div></div>'
                   f'<div class="glance-links"><a href="#{pre}-actives">Skills</a><a href="#{pre}-stigmas">Stigmas</a><a href="#{pre}-gear">Gear</a><a href="#{cls}-gu">Global gear-up</a><a href="#planner">Open the planner</a></div></div>')
        out.append(f'<p class="note">Built from {total} top-ranked Taiwan {name} profiles ({n1} PvE from Nightmare and Transcendence, {n2} from Abyss; item level {min(ilv):,}–{max(ilv):,}). "On bar" means the share of those players with the skill equipped; levels include Daevanion and gear bonuses.</p>')

        # actives
        out.append(f'<h2 id="{pre}-actives">Active skills</h2><p>Sorted by how many top PvE players keep each skill on their bar. Effects are shown at skill level 10.</p>')
        rows = ''.join(f'<tr><td class="skn">{icon(s["i"], s["n"])}<b>{E(s["n"])}</b>{"<small>basic attack</small>" if s["k"] == "basic" else ""}</td>'
                       f'<td class="num">{(str(int(s["cd"])) + "s") if s.get("cd") else "—"}</td><td><small>{E(desc(s))}</small></td>'
                       f'<td class="num">{pct(eq1[s["i"]], n1)}</td><td class="num">{avg(lv1, s["i"]):.0f}</td><td class="num">{pct(eq2[s["i"]], n2)}</td></tr>' for s in act)
        out.append(f'<div class="tw wide"><table class="sk-table"><thead><tr><th>Skill</th><th>Cooldown</th><th>Effect (level 10)</th><th>On bar · PvE</th><th>Avg level</th><th>On bar · Abyss</th></tr></thead><tbody>{rows}</tbody></table></div>')
        # specs
        sp_rows = ''
        for s in act:
            sp = s.get('sp') or []
            if not sp:
                continue
            groups = C.OrderedDict()
            for lvl, t in sp:
                groups.setdefault(lvl, []).append(t)
            cells = ''.join(f'<td><small>{"<br>".join(E(t) for t in groups.get(L, [])) or "—"}</small></td>' for L in (8, 12, 16))
            sp_rows += f'<tr><td class="skn">{icon(s["i"], s["n"])}<b>{E(s["n"])}</b></td>{cells}</tr>'
        out.append(f'<h3 id="{pre}-specs">Specializations</h3><p>A skill gets one spec slot at level 8, another at 12 and a third at 16. Each slot can take any option from its level or below. Armory profiles don\'t record spec picks, so these are the options, not a ranking. Try combinations in the <a href="#planner">planner</a>.</p>'
                   f'<div class="tw wide"><table class="sk-table"><thead><tr><th>Skill</th><th>Level 8</th><th>Level 12</th><th>Level 16</th></tr></thead><tbody>{sp_rows}</tbody></table></div>')
        # stigmas
        rows = ''.join(f'<tr><td class="skn">{icon(s["i"], s["n"])}<b>{E(s["n"])}</b></td><td class="num">{(str(int(s["cd"])) + "s") if s.get("cd") else "—"}</td><td><small>{E(desc(s, 5))}</small></td>'
                       f'<td class="num">{pct(eq1[s["i"]], n1)}</td><td class="num">{pct(eq2[s["i"]], n2)}</td><td class="num">{avg(lv1, s["i"]):.0f}</td></tr>' for s in sti)
        out.append(f'<h2 id="{pre}-stigmas">Stigmas</h2><p>Stigma slots open one at a time while leveling. Fill them in the order of the "PvE" column; the Abyss column shows what PvP players swap in.</p>'
                   f'<div class="tw wide"><table class="sk-table"><thead><tr><th>Stigma</th><th>Cooldown</th><th>Effect</th><th>Picked · PvE</th><th>Picked · Abyss</th><th>Avg level</th></tr></thead><tbody>{rows}</tbody></table></div>')
        # passives
        rows = ''.join(f'<tr><td class="skn">{icon(s["i"], s["n"])}<b>{E(s["n"])}</b></td><td><small>{E(desc(s, 10))}</small></td><td class="num">{avg(lv1, s["i"]):.0f}</td><td class="num">{avg(lv2, s["i"]):.0f}</td></tr>' for s in pas)
        out.append(f'<h2 id="{pre}-passives">Passives</h2><p>Passives are always on. Top players push the first few to level 20+ through Daevanion skill nodes and Arcana.</p>'
                   f'<div class="tw wide"><table class="sk-table"><thead><tr><th>Passive</th><th>Effect (level 10)</th><th>Avg level · PvE</th><th>Avg level · Abyss</th></tr></thead><tbody>{rows}</tbody></table></div>')
        # leveling order
        train = sorted(core, key=lambda s: -avg(lv1, s['i']))[:6]
        out.append(f'<h2 id="{pre}-leveling">Leveling: what to train first</h2><ol>' +
                   ''.join(f'<li><strong>{E(s["n"])}</strong>: top players average level {avg(lv1, s["i"]):.0f}.</li>' for s in train) +
                   '</ol><p>Get each to skill level 8 first to open its first spec. Stigmas start at level 22; take them in this order: ' + ', '.join(E(s['n']) for s in stig[:4]) + '.</p>')
    else:
        out.append(f'<div class="notice"><strong>No skill data yet.</strong> questlog.gg doesn\'t have the {name}\'s skills in its database, so this page covers gear only, from {total} top-ranked profiles.</div>')

    # gear
    sub = C.defaultdict(C.Counter); subv = C.defaultdict(list); ms = C.Counter(); msv = C.defaultdict(list); arcs = C.Counter()
    for d in pve:
        s = d['snapshot']
        for slot, e in (s.get('equipment') or {}).items():
            for x in (e.get('substats') or {}).values():
                sub[slot][x['id']] += 1; subv[(slot, x['id'])].append(x['value'])
            for x in ((e.get('magicstone') or {}).get('substats') or {}).values():
                if x.get('statId'):
                    ms[x['statId']] += 1; msv[x['statId']].append(x['value'])
        for a in (s.get('arcana') or {}).values():
            it = ITEMS.get(a.get('id'))
            if it:
                arcs[it['name']] += 1
    rows = ''
    for slot, lab in SLOTS:
        if not sub[slot]:
            continue
        top = sub[slot].most_common(4)
        rows += f'<tr><td><b>{lab}</b></td><td>' + ' · '.join(f'{E(statname(k))} <span class="gu-il">{fmtv(k, st.mean(subv[(slot, k)]))}</span> <small>({pct(c, n1)})</small>' for k, c in top) + '</td></tr>'
    msr = ' · '.join(f'{E(statname(k))} <span class="gu-il">{fmtv(k, st.mean(msv[k]))}</span>' for k, c in ms.most_common(6))
    arc = ', '.join(f'{E(k)} ({c})' for k, c in arcs.most_common(6))
    out.append(f'<h2 id="{pre}-gear">Gear: what top players roll</h2><p>The substats top PvE {name}s keep on each slot, with average value and the share of players who have it.</p>'
               f'<div class="tw wide"><table><thead><tr><th>Slot</th><th>Most common substats</th></tr></thead><tbody>{rows}</tbody></table></div>'
               + (f'<p><strong>Mana stones:</strong> {msr}.</p>' if msr else '') + (f'<p><strong>Arcana they equip:</strong> {arc}.</p>' if arc else ''))
    return '\n'.join(out), total


names = {'templar': 'Templar', 'ranger': 'Ranger', 'sorcerer': 'Sorcerer', 'elementalist': 'Elementalist', 'cleric': 'Cleric', 'chanter': 'Chanter', 'fighter': 'Brawler'}
res = {}
for cls, nm in names.items():
    h, n = gen(cls, nm)
    res['brawler' if cls == 'fighter' else cls] = h
    print(cls, n, len(h))
json.dump(res, open('out/class_guides.json', 'w', encoding='utf8'), ensure_ascii=False)
