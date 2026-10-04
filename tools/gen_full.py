import json, re, statistics as st, html
exec(open('gen_guides.py', encoding='utf8').read().split("names = {")[0])
from guide_text import T

DP = json.load(open('out/daevplans_all.json', encoding='utf8'))
REF = json.load(open('out/class_guides.json', encoding='utf8'))
NAMES = {'templar': 'Templar', 'ranger': 'Ranger', 'sorcerer': 'Sorcerer', 'elementalist': 'Elementalist', 'cleric': 'Cleric', 'chanter': 'Chanter'}
CODE = {'templar': '2', 'ranger': '3', 'elementalist': '5', 'sorcerer': '6', 'cleric': '7', 'chanter': '8'}
E = html.escape


def dmg20(s):
    t = desc(s, 20)
    m = re.search(r'(\d[\d,]*)-(\d[\d,]*)', t) or re.search(r'deals? (\d[\d,]*) ', t, re.I)
    if not m:
        return 0
    return max(int(x.replace(',', '')) for x in m.groups() if x)


def checklist(pid, items):
    return f'<h3 id="{pid}-check">Checklist <span class="progress" data-for="{pid}"></span></h3><ul class="check" data-list="{pid}">' + \
        ''.join(f'<li><label><input type="checkbox" id="{pid}-{i + 1}"><span>{x}</span></label></li>' for i, x in enumerate(items)) + '</ul>'


def plan_rows(cls, b):
    p = DP[cls][b]
    return ', '.join(f'{t}' for n, t, c, cum in p['steps'][:6]), p['steps'][-1][3] if p['steps'] else 0


def gen(cls):
    t = T[cls]; P = t['pre']; name = NAMES[cls]; code = CODE[cls]
    pve, pvp, total = load(cls); eq1, lv1 = skillstats(pve); n1 = len(pve)
    skills = SK[cls]; by = {s['n']: s for s in skills}
    ic = lambda n: f'<img class="ski" src="img/sk/{by[n]["i"]}.png" alt="">' if n in by else ''
    # toolkit: flat damage per cooldown-second at level 20
    pot = []
    for s in skills:
        if s['k'] in ('active', 'stigma') and s.get('cd') and s['cd'] > 0:
            d = dmg20(s)
            if d:
                pot.append((d / s['cd'], d, s))
    pot.sort(key=lambda x: -x[0]); pot = pot[:8]
    mx = pot[0][0] if pot else 1
    tool = ''.join(f'<tr><td class="skn">{ic(s["n"])}<b>{E(s["n"])}</b>{" <small>stigma</small>" if s["k"] == "stigma" else ""}</td><td class="num">{int(s["cd"])}s</td><td class="num">{d:,}</td>'
                   f'<td><div class="potbar"><span style="width:{100 * v / mx:.0f}%"></span><b>{v:,.0f}</b></div></td></tr>' for v, d, s in pot)
    stig_pct = {s['n']: (round(100 * eq1[s['i']] / n1) if n1 else 0) for s in skills if s['k'] == 'stigma'}

    h = []
    h.append(f'<div data-chero="{cls}"></div>')
    h.append(f'<p class="lead">This guide follows a {name} through five stages, from your first skill to item level 7,000. Find your stage, jump to that Part and work through its checklist. Skill tables and every data point are in the Reference tab.</p>')
    h.append('<div class="stages">' + ''.join(f'<a class="stage" href="#{P}-part-{i}"><b>Part {i}</b><span>{a}</span><small>{b}</small></a>' for i, (a, b) in enumerate(
        [('Beginner', 'Level 1–19'), ('Leveling', 'Level 20–44'), ('Level 45', 'iLv 1,000–3,000'), ('Endgame ramp', 'iLv 3,000–5,000'), ('Min-max', 'iLv 5,000–7,000')], 1)) + '</div>')
    h.append(f'<h3 id="{P}-thirty">The {name} in 30 seconds</h3><ul>' + ''.join(f'<li><strong>{a}:</strong> {b}</li>' for a, b in t['thirty']) + '</ul>')
    if cls in NOTES:
        h.append(f'<div class="goal"><b>Play note</b><p>{E(NOTES[cls])} <span class="meta">From creators collected on <a href="https://couga54.github.io/aion2-guides/en/{cls}/" target="_blank" rel="noopener">couga54\'s {name} guide</a>, summarized.</span></p></div>')

    # PART 1
    h.append(f'<section><h2 id="{P}-part-1"><span class="tag">Part 1 · Level 1–19</span>Beginner</h2>')
    h.append('<div class="goal"><b>Goal</b><p>Learn your core loop, put skill points in the right order, and open the first Daevanion board at level 12.</p></div>')
    h.append(f'<h3 id="{P}-p1-toolkit">Your toolkit</h3><p>Skills with a cooldown, ranked by flat damage per second of cooldown at skill level 20. Attack scaling comes on top, so treat this as an order, not exact numbers. Fillers with no cooldown (your basic attack and its partners) are what you press in between.</p>'
             f'<div class="tw"><table class="sk-table"><thead><tr><th>Skill</th><th>Cooldown</th><th>Damage (lv 20)</th><th>Per cooldown-second</th></tr></thead><tbody>{tool}</tbody></table></div>')
    h.append(f'<h3 id="{P}-p1-train">What to train</h3><p>A skill costs 21 SP to reach level 10. Level 8 opens its first specialization, so get your main skills to 8 before spreading points.</p><ol>' +
             ''.join(f'<li>{ic(a)}<strong>{E(a)}:</strong> {b}.</li>' for a, b in t['train']) + '</ol>')
    h.append(f'<h3 id="{P}-p1-combo">Your first combo</h3><ol>' + ''.join(f'<li>{x}</li>' for x in t['combo']) + f'</ol><p>{t["packs"]}</p>')
    h.append(f'<h3 id="{P}-p1-gear">Gear at this stage</h3><p>Use quest gear and take your weapon to +5. Enhancement unlocks at level 9 and every step up to +10 always succeeds. Don\'t spend real resources yet: everything here is replaced within a few levels.</p>')
    nb = code + '1'; s6, cost = plan_rows(cls, nb)
    h.append(f'<h3 id="{P}-p1-daevanion">Daevanion: Nezekan (level 12)</h3><p>You start at the center node; every node you buy must touch one you own. Buy in the numbered order: first {E(s6)}. The full plan costs {cost} points.</p>'
             f'<figure><button data-full="img/{cls}_daevplan_{nb}.png"><img src="img/{cls}_daevplan_{nb}.png" alt="{name} Nezekan board buy order" loading="lazy"></button></figure>')
    h.append(checklist(f'{P}1', [f'{t["train"][0][0]}, {t["train"][1][0]} and {t["train"][2][0]} trained first', 'First combo practiced on a single target', 'Weapon at +5', 'Nezekan plan started', 'First level-8 specs taken']))
    h.append('</section>')

    # PART 2
    h.append(f'<section><h2 id="{P}-part-2"><span class="tag">Part 2 · Level 20–44</span>Leveling</h2>')
    h.append('<div class="goal"><b>Goal</b><p>Fill your stigma slots, take the level-8 and level-12 specs on your main skills, and open three new Daevanion boards.</p></div>')
    h.append(f'<p><strong>What unlocks:</strong> Zikel board (20), stigmas (22, then one more slot at 27, 32 and 37), Supply Requests (25), Vaizel board and the Daily Dungeon (30), Triniel board (40).</p>')
    h.append(f'<h3 id="{P}-p2-stigmas">Stigmas</h3><p>In the order the slots open. The percentage is how many top PvE {name}s run it.</p><ol>' +
             ''.join(f'<li>{ic(a)}<strong>{E(a)}</strong> <small class="pick">{stig_pct.get(a, 0)}%</small>: {b}</li>' for a, b in t['stig']) + '</ol>')
    h.append(f'<h3 id="{P}-p2-passives">Passives</h3><p>Passives are always on. They level with skill points up to 10, then only through Daevanion skill nodes and Arcana. {t["passives"]}</p>')
    h.append(f'<h3 id="{P}-p2-specs">Specs to take while leveling</h3><p>One spec slot at skill level 8 and a second at 12. The second slot can take the level-12 option or another level-8 one. Level 12 arrives around character level 35 once Daevanion adds skill levels.</p>'
             '<div class="tw"><table><thead><tr><th>Skill</th><th>Slot 1 (level 8)</th><th>Slot 2 (level 12)</th><th>Why</th></tr></thead><tbody>' +
             ''.join(f'<tr><td class="skn">{ic(a)}<b>{E(a)}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in t['specs']) + '</tbody></table></div>')
    h.append(f'<h3 id="{P}-p2-rotation">Leveling rotation</h3><ol>' + ''.join(f'<li>{x}</li>' for x in t['lvl_rot']) + '</ol>')
    h.append(f'<h3 id="{P}-p2-macro">Set up your macro</h3><p>Aion 2 is played with skill macros: one held key fires a priority list, so the first skill that is off cooldown goes out. Put your buffs and conditional hits at the top and fillers at the bottom. Bind it in <em>Settings → General → Skill macro</em>. Keep big cooldowns, defensives and anything you need to time by hand off the macro.</p>')
    rows = ''
    for k, lvl in (('2', 20), ('3', 30), ('4', 40)):
        b = code + k; s6, cost = plan_rows(cls, b)
        rows += f'<tr><td>Level {lvl}</td><td><strong>{DP[cls][b]["name"]}</strong>: {E(s6)}</td><td class="num">{cost}</td></tr>'
    h.append(f'<h3 id="{P}-p2-daevanion">Daevanion: Zikel (20), Vaizel (30), Triniel (40)</h3><p>When a new board opens, buy its first steps before finishing the old board\'s leftovers.</p>'
             f'<div class="tw"><table><thead><tr><th>When</th><th>Buy first</th><th>Plan cost</th></tr></thead><tbody>{rows}</tbody></table></div>' +
             ''.join(f'<figure><button data-full="img/{cls}_daevplan_{code}{k}.png"><img src="img/{cls}_daevplan_{code}{k}.png" alt="{name} {DP[cls][code + k]["name"]} board plan" loading="lazy"></button><figcaption>{DP[cls][code + k]["name"]}, level {DP[cls][code + k]["lvl"]}</figcaption></figure>' for k in '234'))
    h.append(checklist(f'{P}2', ['All stigma slots filled in the order above', 'Level-8 spec on every main skill; level 12 on the top three by about level 36', 'Skill macro bound', 'Zikel, Vaizel and Triniel plans started']))
    h.append('</section>')

    # PART 3
    h.append(f'<section><h2 id="{P}-part-3"><span class="tag">Part 3 · Level 45 · iLv 1,000–3,000</span>Level 45 and first endgame</h2>')
    h.append('<div class="goal"><b>Goal</b><p>Climb to iLv 2,700 on the global route, craft your weapon and accessories, and get your boss rotation into your fingers.</p></div>')
    h.append(f'<p>The full route is on <a href="#progression">After level 45</a>. Here is what it means for a {name}:</p>')
    h.append(f'<div data-gearup="{cls}"></div>')
    h.append(f'<h3 id="{P}-p3-rotation">Boss rotation</h3><ol>' + ''.join(f'<li>{x}</li>' for x in t['boss']) + '</ol>')
    b6 = code + '6'; s6, cost = plan_rows(cls, b6)
    h.append(f'<h3 id="{P}-p3-daevanion">Daevanion at 45</h3><ul><li><strong>PvE:</strong> finish the four class-board plans, then the remaining Unique nodes and stat nodes.</li><li><strong>PvP:</strong> after the level-40 steps, buy the Azphel PvP Damage Boost and Tolerance nodes ({cost} points).</li></ul>'
             f'<figure><button data-full="img/{cls}_daevplan_{b6}.png"><img src="img/{cls}_daevplan_{b6}.png" alt="{name} Azphel PvP board plan" loading="lazy"></button></figure>')
    h.append(checklist(f'{P}3', ['True Dragon weapon and accessories crafted', 'Belt, amulet and 2 Clash Runes', 'Arcana slots filled from Transcendence', 'Boss rotation practiced', 'iLv 2,100 reached before your energy caps']))
    h.append('</section>')

    # PART 4
    h.append(f'<section><h2 id="{P}-part-4"><span class="tag">Part 4 · iLv 3,000–5,000</span>Endgame ramp</h2>')
    h.append('<div class="goal"><b>Goal</b><p>Amplify gear to +18, grow Daevanion toward 900 nodes, and reach the skill levels that unlock the big level-12 and level-16 specs.</p></div>')
    h.append(f'<h3 id="{P}-p4-specs">Skill levels past 10: the big specs</h3><p>Levels above 10 come from Daevanion skill nodes, Arcana sub-skills and gear rolls. Chase these:</p>'
             '<div class="tw"><table><thead><tr><th>Spec</th><th>Needs level</th><th>Why</th></tr></thead><tbody>' +
             ''.join(f'<tr><td>{a}</td><td class="num">{b}</td><td>{c}</td></tr>' for a, b, c in t['big']) + '</tbody></table></div>')
    h.append(f'<p><strong>Stigma levels:</strong> {t["stig_levels"]}</p>')
    h.append(f'<h3 id="{P}-p4-substats">Substats: what top players roll</h3><p>The full table by slot is in the Reference tab under <a href="#{cls}-g-gear">Gear</a>. Amplify every piece to +18 before any piece goes to +20, as explained on <a href="#sys-enchant">Systems: Enchanting</a>.</p>')
    h.append(checklist(f'{P}4', ['Everything at +18 before any piece at +20', t['big'][0][0] + ' unlocked', 'Top three stigmas at level 20', '~900 Daevanion nodes']))
    h.append('</section>')

    # PART 5
    h.append(f'<section><h2 id="{P}-part-5"><span class="tag">Part 5 · iLv 5,000–7,000</span>Min-max</h2>')
    h.append('<div class="goal"><b>Goal</b><p>The last 10–20%: all slots at +20, Arcana at +5 with the right sub-skills, and every reroll aimed at the emptiest stat pool.</p></div>')
    h.append(f'<h3 id="{P}-p5-stats">Which stat to roll next</h3><p>Boosts in the same pool add together, so +1% is worth 1 / (1 + what you already have). Roll toward the pool you have least of. The stat math is on <a href="#sys-stats">Systems: Stats</a>.</p>')
    h.append(f'<h3 id="{P}-p5-mistakes">Common mistakes</h3><div class="tw"><table><thead><tr><th>Mistake</th><th>Why it costs you</th><th>Fix</th></tr></thead><tbody>' +
             ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in t['mistakes']) + '</tbody></table></div>')
    h.append(checklist(f'{P}5', ['All slots at +20', 'Arcana at +5 with the right sub-skills', 'Rerolls aimed at the emptiest stat pool']))
    h.append('</section>')

    guide = '\n'.join(h)
    ref = (f'<section><h1 id="{P}-ref">{name} reference</h1><div class="byline"><span>Data as of 2026-10-04</span><span>{total} top-ranked Taiwan profiles · questlog.gg database</span></div>'
           f'<p class="lead">Every {name} skill, stigma and passive with what top players run, gear substats, and the Daevanion plans behind the guide.</p></section><section>{REF[cls]}</section>'
           f'<section><h2 id="{P}-ref-daev">Daevanion plans (buy order)</h2><div class="tw"><table><thead><tr><th>Board</th><th>Order</th><th>Points</th></tr></thead><tbody>' +
           ''.join(f'<tr><td>{v["name"]} ({v["lvl"]})</td><td>{", ".join(E(x[1]) for x in v["steps"])}</td><td class="num">{v["steps"][-1][3] if v["steps"] else 0}</td></tr>' for b, v in DP[cls].items()) +
           '</tbody></table></div><p class="note">Plans follow the skills top players level highest, mixed with the Unique stat nodes, using the cheapest connected path on each board.</p></section>'
           f'<section><h2 id="{P}-ref-sources">Sources</h2><ul><li>Skills, specs and Daevanion boards: <a href="https://questlog.gg/aion-2/en/db/skills/{cls}" target="_blank" rel="noopener">questlog.gg</a></li>'
           f'<li>{total} top-ranked Taiwan {name}s from the Nightmare, Transcendence and Abyss leaderboards (pulled 4 Oct 2026)</li>'
           f'<li>Play note: creators collected on <a href="https://couga54.github.io/aion2-guides/en/{cls}/" target="_blank" rel="noopener">couga54\'s {name} guide</a>, summarized in our words</li>'
           '<li>Global route and gear-up: Aragon (see <a href="#sources">Sources &amp; credits</a>)</li></ul></section>')
    view = (f'<!-- ======================= {name.upper()} ======================= -->\n<div data-view="{cls}" hidden>\n  <div class="subtabs" role="tablist" aria-label="{name} sections"><button role="tab" data-sub="guide" aria-selected="true">Guide</button><button role="tab" data-sub="reference" aria-selected="false">Reference</button></div>\n'
            f'<div data-sub-panel="guide">\n<section>{guide}</section>\n</div>\n<div data-sub-panel="reference" hidden>\n{ref}\n</div>\n</div>\n')
    return view


views = ''.join(gen(c) for c in T)
open('out/full_views.html', 'w', encoding='utf8').write(views)
print(len(views))
