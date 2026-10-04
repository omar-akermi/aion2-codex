"""Original class illustrations for the hero banners: a cloaked, rim-lit figure holding the class weapon."""
import os
os.makedirs('out/art', exist_ok=True)
COL = {'gladiator': '#e0663f', 'templar': '#6d9be0', 'assassin': '#b06ad9', 'ranger': '#6fbf6a', 'sorcerer': '#4fb7e0',
       'elementalist': '#3fc9b0', 'cleric': '#e8c860', 'chanter': '#e09a3f'}

BODY = '''
  <!-- cloak -->
  <path d="M200 132 C150 140 118 175 108 240 C96 320 90 400 70 500 L330 500 C312 400 304 320 292 240 C282 175 250 140 200 132 Z" fill="url(#cloth)" stroke="url(#rim)" stroke-width="3"/>
  <!-- inner cloak fold -->
  <path d="M200 170 C180 230 176 330 168 500 L232 500 C224 330 220 230 200 170 Z" fill="#0a0d14" opacity=".75"/>
  <!-- shoulders / pauldrons -->
  <path d="M138 176 C150 150 178 142 200 142 C222 142 250 150 262 176 C246 186 226 190 200 190 C174 190 154 186 138 176 Z" fill="#141a26" stroke="url(#rim)" stroke-width="3"/>
  <path d="M124 186 C130 166 146 158 160 160 L166 196 C150 202 134 200 124 186 Z" fill="#1a2232" stroke="url(#rim)" stroke-width="2.5"/>
  <path d="M276 186 C270 166 254 158 240 160 L234 196 C250 202 266 200 276 186 Z" fill="#1a2232" stroke="url(#rim)" stroke-width="2.5"/>
  <!-- hood + face shadow -->
  <path d="M200 58 C168 58 152 86 154 116 C156 136 170 150 200 152 C230 150 244 136 246 116 C248 86 232 58 200 58 Z" fill="url(#cloth)" stroke="url(#rim)" stroke-width="3"/>
  <path d="M200 84 C180 86 172 104 174 120 C176 134 186 142 200 143 C214 142 224 134 226 120 C228 104 220 86 200 84 Z" fill="#05070b"/>
  <!-- eyes -->
  <circle cx="190" cy="118" r="2.6" fill="CC" filter="url(#glow)"/><circle cx="210" cy="118" r="2.6" fill="CC" filter="url(#glow)"/>
  <!-- belt emblem -->
  <path d="M200 262 L212 276 L200 290 L188 276 Z" fill="CC" opacity=".85" filter="url(#glow)"/>
'''

WEAPON = {
    'gladiator': '''<g transform="rotate(-28 300 300)"><rect x="292" y="60" width="18" height="300" rx="3" fill="#cfd6e4" stroke="url(#rim)" stroke-width="2"/>
      <path d="M292 60 L301 20 L310 60 Z" fill="#e8edf6"/><rect x="262" y="354" width="78" height="14" rx="4" fill="#2a2f3c" stroke="CC" stroke-width="2"/>
      <rect x="295" y="368" width="12" height="60" rx="3" fill="#3a2a22"/><circle cx="301" cy="436" r="9" fill="CC" filter="url(#glow)"/>
      <line x1="301" y1="80" x2="301" y2="340" stroke="CC" stroke-width="2" opacity=".7" filter="url(#glow)"/></g>''',
    'templar': '''<path d="M60 250 C60 205 120 190 140 196 C160 190 220 205 220 250 C220 330 160 380 140 392 C120 380 60 330 60 250 Z" transform="translate(-30 0)" fill="#1c2638" stroke="url(#rim)" stroke-width="4"/>
      <path d="M110 230 L110 330 M70 270 L150 270" stroke="CC" stroke-width="6" stroke-linecap="round" filter="url(#glow)"/>
      <g transform="rotate(18 300 260)"><rect x="294" y="110" width="13" height="210" rx="3" fill="#d6dcea"/><path d="M294 110 L300 80 L307 110 Z" fill="#eef2f8"/>
      <rect x="276" y="318" width="50" height="10" rx="3" fill="#2a2f3c" stroke="CC" stroke-width="2"/><rect x="296" y="328" width="9" height="40" fill="#3a2a22"/></g>''',
    'assassin': '''<g transform="rotate(-40 120 300)"><path d="M114 210 L122 210 L126 320 L110 320 Z" fill="#d8dde8"/><path d="M110 210 L118 170 L126 210 Z" fill="#eef1f7"/><rect x="104" y="320" width="28" height="7" rx="2" fill="CC"/><rect x="113" y="327" width="10" height="34" fill="#2b2230"/></g>
      <g transform="rotate(40 290 300)"><path d="M284 210 L292 210 L296 320 L280 320 Z" fill="#d8dde8"/><path d="M280 210 L288 170 L296 210 Z" fill="#eef1f7"/><rect x="274" y="320" width="28" height="7" rx="2" fill="CC"/><rect x="283" y="327" width="10" height="34" fill="#2b2230"/></g>
      <path d="M60 420 C120 380 150 400 200 360 C250 400 280 380 340 420" stroke="CC" stroke-width="2" fill="none" opacity=".5" filter="url(#glow)"/>''',
    'ranger': '''<path d="M300 70 C380 160 380 340 300 430" stroke="#8a6a44" stroke-width="10" fill="none" stroke-linecap="round"/>
      <path d="M300 70 C380 160 380 340 300 430" stroke="url(#rim)" stroke-width="2" fill="none"/>
      <line x1="300" y1="70" x2="300" y2="430" stroke="#cfd6e4" stroke-width="1.5"/>
      <line x1="150" y1="250" x2="350" y2="250" stroke="#d9dfe9" stroke-width="3"/><path d="M350 250 L334 242 L334 258 Z" fill="CC" filter="url(#glow)"/>
      <path d="M150 250 L140 240 M150 250 L140 260" stroke="CC" stroke-width="3"/>''',
    'sorcerer': '''<g transform="translate(250 250)"><path d="M0 0 L70 -14 L70 40 L0 54 Z" fill="#2a2140" stroke="url(#rim)" stroke-width="2"/><path d="M0 0 L-70 -14 L-70 40 L0 54 Z" transform="translate(140 0) scale(-1 1) translate(140 0)" fill="#2a2140"/>
      <path d="M0 0 L60 -10 L60 36 L0 48 Z" fill="#e9e1cf"/></g>
      <circle cx="285" cy="200" r="34" fill="CC" opacity=".35" filter="url(#glow)"/><path d="M285 160 C300 185 305 200 285 228 C265 200 270 185 285 160 Z" fill="#ffd9a0" opacity=".9" filter="url(#glow)"/>
      <circle cx="110" cy="230" r="10" fill="#9fd8ff" opacity=".8" filter="url(#glow)"/><circle cx="95" cy="280" r="6" fill="#9fd8ff" opacity=".6" filter="url(#glow)"/>''',
    'elementalist': '''<circle cx="290" cy="230" r="36" fill="url(#orb)" stroke="url(#rim)" stroke-width="2" filter="url(#glow)"/>
      <circle cx="105" cy="160" r="12" fill="#ff8a5c" opacity=".85" filter="url(#glow)"/><circle cx="330" cy="130" r="10" fill="#7fd0ff" opacity=".85" filter="url(#glow)"/>
      <circle cx="80" cy="300" r="9" fill="#9be38a" opacity=".85" filter="url(#glow)"/><circle cx="340" cy="340" r="11" fill="#e8c27a" opacity=".85" filter="url(#glow)"/>
      <path d="M105 160 C160 120 250 120 330 130 M80 300 C120 360 260 380 340 340" stroke="CC" stroke-width="1.5" fill="none" opacity=".5" stroke-dasharray="4 6"/>''',
    'cleric': '''<circle cx="200" cy="64" r="58" fill="none" stroke="CC" stroke-width="4" opacity=".8" filter="url(#glow)"/>
      <g transform="rotate(20 300 280)"><rect x="294" y="190" width="12" height="190" rx="3" fill="#6a5640"/><path d="M300 150 L330 175 L322 210 L278 210 L270 175 Z" fill="#d8c8a0" stroke="url(#rim)" stroke-width="2"/>
      <circle cx="300" cy="182" r="9" fill="CC" filter="url(#glow)"/></g>
      <path d="M90 300 L90 340 M70 320 L110 320" stroke="CC" stroke-width="5" stroke-linecap="round" opacity=".85" filter="url(#glow)"/>''',
    'chanter': '''<rect x="294" y="60" width="11" height="400" rx="4" fill="#7a5a3c" stroke="url(#rim)" stroke-width="1.5"/>
      <circle cx="300" cy="62" r="26" fill="none" stroke="#d9c08a" stroke-width="5"/><circle cx="300" cy="62" r="10" fill="CC" filter="url(#glow)"/>
      <circle cx="200" cy="250" r="150" fill="none" stroke="CC" stroke-width="1.5" opacity=".35" stroke-dasharray="2 10"/>
      <circle cx="200" cy="250" r="120" fill="none" stroke="CC" stroke-width="1" opacity=".25"/>''',
}

for cls, col in COL.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
  <defs>
    <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{col}"/><stop offset=".6" stop-color="{col}" stop-opacity=".35"/><stop offset="1" stop-color="#ffffff" stop-opacity=".2"/></linearGradient>
    <linearGradient id="cloth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2232"/><stop offset="1" stop-color="#0b0e15"/></linearGradient>
    <radialGradient id="bg" cx=".5" cy=".42" r=".55"><stop offset="0" stop-color="{col}" stop-opacity=".45"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>
    <radialGradient id="orb" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="{col}"/><stop offset="1" stop-color="#10202a"/></radialGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <ellipse cx="200" cy="230" rx="200" ry="230" fill="url(#bg)"/>
  {WEAPON[cls].replace('CC', col) if cls in ('templar', 'ranger') else ''}
  {BODY.replace('CC', col)}
  {WEAPON[cls].replace('CC', col) if cls not in ('templar', 'ranger') else ''}
</svg>'''
    open(f'out/art/{cls}.svg', 'w', encoding='utf8').write(svg)
print('ok')
