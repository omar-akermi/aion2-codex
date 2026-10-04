const fs=require('fs'),path=require('path');const {JSDOM}=require('jsdom');const S=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(S,'docs/index.html'),'utf8');const errors=[];
const files={'planner_data.json':path.join(S,'docs/planner_data.json'),'planner_skills.json':path.join(S,'docs/planner_skills.json'),'builds.json':path.join(S,'docs/builds.json')};
const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://example.test/#home',pretendToBeVisual:true,beforeParse(w){w.fetch=u=>Promise.resolve({json:()=>Promise.resolve(JSON.parse(fs.readFileSync(files[u],'utf8')))});w.matchMedia=()=>({matches:false});w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=function(){};w.addEventListener('error',e=>errors.push(e.message));w.console.error=(...a)=>errors.push(a.join(' '));}});
const w=dom.window,d=w.document,sleep=ms=>new Promise(r=>setTimeout(r,ms));
setTimeout(async()=>{const out=[];
 for(const id of ['templar','ranger','sorcerer','elementalist','cleric','chanter','gladiator','assassin']){
  w.location.hash='#'+id; await sleep(60);
  const v=d.querySelector('[data-view]:not([hidden])');
  const h=v.querySelector('.chero h1');
  out.push(id+': view='+v.dataset.view+' hero='+(h&&h.id)+' toc='+d.querySelectorAll('#toc-list a').length+' gearup='+!!v.querySelector('.gu-table')+' checks='+v.querySelectorAll('.check input').length+' imgs='+v.querySelectorAll('img').length);
  const ref=v.querySelector('[data-sub="reference"]');
  if(ref){ref.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));await sleep(30);out.push('   ref toc='+d.querySelectorAll('#toc-list a').length+' first='+(d.querySelector('#toc-list a')||{}).textContent);}
 }
 w.location.hash='#rg-p2-specs'; await sleep(60); out.push('deep link view='+d.querySelector('[data-view]:not([hidden])').dataset.view+' panel guide visible='+!d.querySelector('[data-view="ranger"] [data-sub-panel="guide"]').hidden);
 console.log(out.join('\n'));console.log('ERRORS:',errors.slice(0,5));process.exit(0);},1500);
