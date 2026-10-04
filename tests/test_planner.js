const fs = require('fs'); const path = require('path');
const { JSDOM } = require('jsdom');
const S = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(S, 'docs/index.html'), 'utf8');
const files = { 'planner_data.json': path.join(S, 'docs/planner_data.json'), 'planner_skills.json': path.join(S, 'docs/planner_skills.json'), 'builds.json': path.join(S, 'docs/builds.json') };
const errors = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://example.test/#planner', pretendToBeVisual: true,
  beforeParse(w) {
    w.fetch = (u) => Promise.resolve({ json: () => Promise.resolve(JSON.parse(fs.readFileSync(files[u], 'utf8'))) });
    w.matchMedia = () => ({ matches: false, addListener() {}, removeListener() {} });
    w.scrollTo = () => {}; w.HTMLElement.prototype.scrollIntoView = function () {};
    w.addEventListener('error', (e) => errors.push(e.message));
    w.console.error = (...a) => errors.push(a.join(' '));
  }
});
const w = dom.window, d = w.document;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const click = (el) => el.dispatchEvent(new w.MouseEvent('click', { bubbles: true }));
(async () => {
  await sleep(1500);
  const out = [];
  out.push('view planner visible: ' + !d.querySelector('[data-view="planner"]').hidden);
  out.push('slots: ' + d.querySelectorAll('.pl-slot').length);
  // equip weapon
  click(d.querySelector('[data-slot="weapon"]')); await sleep(50);
  const picks = d.querySelectorAll('[data-pick]'); out.push('weapon picks: ' + picks.length);
  click(picks[0]); await sleep(50);
  out.push('editor title: ' + d.getElementById('pl-modal-title').textContent + ' | subs lines: ' + d.querySelectorAll('[data-sub]').length + ' ms lines: ' + d.querySelectorAll('[data-ms]').length);
  click(d.querySelector('[data-act="done"]')); await sleep(50);
  out.push('weapon slot: ' + d.querySelector('[data-slot="weapon"]').textContent.trim().slice(0, 60));
  out.push('summary: ' + d.getElementById('pl-summary').textContent.slice(0, 120));
  // skills tab
  click(d.querySelector('[data-tab="skills"]')); await sleep(100);
  out.push('skill cards: ' + d.querySelectorAll('.sk-card').length);
  click(d.querySelector('.sk-card')); await sleep(50);
  const lv = d.getElementById('sk-lv'); lv.value = '10'; lv.dispatchEvent(new w.Event('input', { bubbles: true }));
  out.push('skill editor: ' + d.getElementById('sk-cost').textContent + ' | ' + d.getElementById('sk-eff').textContent + ' | specs ' + d.getElementById('sk-slots')?.textContent);
  const spec = d.querySelector('[data-spec]:not([disabled])'); if (spec) { spec.checked = true; spec.dispatchEvent(new w.Event('change', { bubbles: true })); }
  out.push('after spec: ' + d.getElementById('sk-slots')?.textContent + ' | desc: ' + d.getElementById('sk-desc').textContent.slice(0, 90));
  d.getElementById('sk-eq').checked = true;
  click(d.querySelector('[data-act="skdone"]')); await sleep(50);
  out.push('summary skills: ' + d.querySelector('#pl-tab-skills .pl-summary').textContent);
  // daevanion
  click(d.querySelector('[data-tab="daev"]')); await sleep(100);
  out.push('nodes: ' + d.querySelectorAll('.dv-n').length + ' can: ' + d.querySelectorAll('.dv-n.can').length);
  click(d.querySelector('.dv-n.can')); await sleep(50);
  out.push('owned after click: ' + d.querySelectorAll('.dv-n.own').length + ' status: ' + d.getElementById('pl-status').textContent);
  const plan = d.querySelector('[data-dv="plan"]'); if (plan) { click(plan); await sleep(50); }
  out.push('owned after plan: ' + d.querySelectorAll('.dv-n.own').length + ' | ' + d.getElementById('pl-status').textContent);
  const locked = [...d.querySelectorAll('.dv-n')].find((n) => !n.classList.contains('own') && !n.classList.contains('can') && !n.classList.contains('start'));
  if (locked) { click(locked); await sleep(20); out.push('locked click: ' + d.getElementById('pl-status').textContent); }
  out.push('daev side: ' + d.querySelector('.dv-side').textContent.slice(0, 200));
  click(d.querySelector('[data-board]:nth-child(2)')); await sleep(50);
  out.push('board 2 header: ' + d.querySelector('.dv-boardbox .pl-panel-h').textContent);
  // stats include daevanion
  click(d.querySelector('[data-tab="gear"]')); await sleep(50);
  out.push('stats has Cooldown Reduction or CDR: ' + /Cooldown|Combat Speed/.test(d.getElementById('pl-stats').textContent));
  // add stage copies daev
  click(d.querySelector('[data-add]')); await sleep(50);
  click(d.querySelector('[data-tab="daev"]')); await sleep(50);
  out.push('stage2 owned on board: ' + d.querySelectorAll('.dv-n.own').length);
  // save locally (no db)
  d.getElementById('pl-name').value = 'Test build'; click(d.getElementById('pl-save')); await sleep(50);
  out.push('save: ' + d.getElementById('pl-status').textContent);
  // class switch to brawler
  const sel = d.getElementById('pl-class'); sel.value = 'ranger'; sel.dispatchEvent(new w.Event('change', { bubbles: true })); await sleep(50);
  click(d.querySelector('[data-tab="skills"]')); await sleep(50);
  out.push('ranger skills: ' + d.getElementById('pl-tab-skills').textContent.slice(0, 80));
  click(d.querySelector('[data-tab="daev"]')); await sleep(50);
  out.push('ranger nodes: ' + d.querySelectorAll('.dv-n').length);
  // home route + featured
  w.location.hash = '#gladiator'; await sleep(100);
  out.push('gladiator view: ' + !d.querySelector('[data-view="gladiator"]').hidden + ' featured: ' + d.querySelector('[data-featured="gladiator"]').textContent.slice(0, 80));
  console.log(out.join('\n'));
  console.log('ERRORS:', errors.slice(0, 10));
  process.exit(0);
})();
