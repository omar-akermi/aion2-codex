exec(open('draw4.py',encoding='utf8').read().split('# ---------------- journey map')[0])
cards=[(1,['Rending Blow','Leaping Slam','Keen Strike'],'Starter kit'),(3,['Mocking Blade'],'Knockdown'),(4,['Overhead Slam'],'Best skill'),(5,['Sword Aura Rampage'],'Stagger only'),
 (7,['Ankle Slice'],'Root'),(8,['Crushing Wave'],'AoE'),(9,[],'Enhancement'),(10,['Rush Strike'],'Gap closer'),(12,['Aerial Snare'],'+ Nezekan board'),
 (14,['Ruinous Blow'],'Big hit + buff'),(16,['Defiance'],'CC break'),(19,[],'First level-8 specs'),(20,[],'Zikel board'),(22,['Rage Burst',"Zikel's Blessing",'Lunge Stance'],'Stigmas'),
 (25,[],'Supply Requests'),(30,[],'Vaizel board, Daily Dungeon'),(40,[],'Triniel board'),(45,[],'Azphel, Abyss, Nightmare, Arcana, Transcendence')]
COLS=6; CWD=196; CH=128
rows=(len(cards)+COLS-1)//COLS; W=20+COLS*CWD+10; H=84+rows*(CH+10)+10
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img)
d.text((20,14),'What unlocks when: level 1 to 45',font=F(22,True),fill=TXT)
d.text((20,44),'Skills at the character level they become learnable; gold cards are systems and Daevanion boards.',font=F(14),fill=SUB)
for i,(lv,sks,cap) in enumerate(cards):
    x=20+(i%COLS)*CWD; y=78+(i//COLS)*(CH+10); sysc=not sks
    d.rounded_rectangle([x,y,x+CWD-12,y+CH],10,fill=CARD,outline=GOLD if sysc else CARD,width=2)
    d.text((x+12,y+8),'Lv',font=F(11),fill=SUB); d.text((x+12,y+20),str(lv),font=F(26,True),fill=GOLD)
    ix=x+56
    for s in sks[:3]:
        im=sk(s,38); img.paste(im,(ix,y+12),im); ix+=42
    yy=y+60
    lab=', '.join(sks) if sks else ''
    for line in textwrap.wrap(lab,26)[:2]:
        d.text((x+12,yy),line,font=F(12,True),fill=TXT); yy+=15
    for line in textwrap.wrap(cap,26)[:2]:
        d.text((x+12,yy),line,font=F(12,not sks),fill=GOLD if sysc else SUB); yy+=15
img.save('out/unlocks.png'); print(img.size)
