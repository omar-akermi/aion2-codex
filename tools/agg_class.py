import json,glob,collections as C,statistics as st,sys
D=sys.argv[1]
skills={s['id']:s['name'] for s in json.load(open('ref/skillBuilder.getSkills.json',encoding='utf8'))}
subc={s['id']:s['subCategory'] for s in json.load(open('ref/skillBuilder.getSkills.json',encoding='utf8'))}
items={i['id']:i for i in json.load(open('ref/characterBuilder.getEquipmentItems.json',encoding='utf8'))}
idx=json.load(open(f'{D}/idx.json')); seen={}
for j in idx:
  try: d=json.load(open(j['file'],encoding='utf8'))
  except: continue
  c=d['character']; s=d.get('snapshot') or {}
  if not c.get('itemLevel') or not s.get('skills'): continue
  seen.setdefault(c['characterId'],(j,d))
print('unique',len(seen), 'boards', C.Counter(b for j,d in seen.values() for b in (d['snapshot'].get('daevanion') or {})))
def agg(chars,label):
  n=len(chars); print(f'\n######## {label} n={n}')
  if not n: return
  ilv=[c['character']['itemLevel'] for c in chars]; print('iLv',min(ilv),int(st.mean(ilv)),max(ilv))
  eq=C.Counter(); lv=C.defaultdict(list)
  sub=C.defaultdict(C.Counter); subv=C.defaultdict(list); ms=C.Counter(); msv=C.defaultdict(list); arc=C.Counter(); arcn=C.Counter()
  for c in chars:
    s=c['snapshot']
    for x in s['skills']:
      nm=skills.get(str(x['id']),str(x['id'])); lv[nm].append(x['level'])
      if x['isEquipped']: eq[nm]+=1
    for slot,e in s['equipment'].items():
      for x in (e.get('substats') or {}).values(): sub[slot][x['id']]+=1; subv[(slot,x['id'])].append(x['value'])
      for x in ((e.get('magicstone') or {}).get('substats') or {}).values(): ms[x['statId']]+=1; msv[x['statId']].append(x['value'])
    for a in (s.get('arcana') or {}).values():
      it=items.get(a['id']); arcn[it['name'] if it else '?']+=1
      for x in (a.get('subSkills') or {}).values(): arc[skills.get(x['id'],x['id'])]+=x['lvl']
  print('EQUIPPED:', ', '.join(f"{k} {100*v//n}%" for k,v in eq.most_common()))
  print('LEVELS:', ', '.join(f"{k}:{st.mean(v):.0f}" for k,v in sorted(lv.items(),key=lambda x:-st.mean(x[1]))))
  for slot in ['weapon','guarder','torso','shoulder','helmet','cape','pants','gloves','boots','necklace','leftRing','leftEarring','leftBracelet','leftBrooch']:
    print(f' {slot}:',[(k,v,round(st.mean(subv[(slot,k)]),1)) for k,v in sub[slot].most_common(6)])
  print('MANASTONES',[(k,v,round(st.mean(msv[k]),1)) for k,v in ms.most_common(12)])
  print('ARCANA sub',arc.most_common(12)); print('ARCANA sets',arcn.most_common(8))
allc=[d for j,d in seen.values()]
top=lambda t:[d for j,d in seen.values() if j['type']==t and j['page']==1 and d['character']['itemLevel']>4500]
agg(top('nightmare')+top('transcendence')+top('subjugation')+top('awakening'),'TOP PvE')
agg(top('abyss'),'TOP Abyss')
