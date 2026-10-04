# Aion 2 Codex

Class guides, global gear routes, crafting recipes and a gear / skill / Daevanion planner for **Aion 2 (global Season 1)**.
It's a single static page with no build step. Open `docs/index.html` or serve the `docs/` folder.

## What's inside

| Path | What it is |
|---|---|
| `docs/index.html` | The whole site: home, 8 class guides (Guide + Reference tabs), After level 45, Gathering & crafting, Systems, Build planner, Sources |
| `docs/img/` | Charts, Daevanion plans, class emblems, skill and item icons, banner illustrations |
| `docs/planner_data.json`, `docs/planner_skills.json` | Item, stat, skill and Daevanion data loaded by the planner |
| `docs/builds.json` | Featured builds shown in the Gladiator and Assassin guides |
| `tools/` | Python scripts that pull data from questlog.gg and generate the guides, charts and plans |
| `tests/` | Headless page tests (jsdom) |

## Run locally

The page loads its JSON with `fetch`, so serve the folder rather than opening the file directly:

```bash
python -m http.server 8000 --directory docs
```

Then open http://localhost:8000.

## Deploy on GitHub Pages

1. Push this repository to GitHub.
2. **Settings → Pages → Build and deployment**: Source = *Deploy from a branch*, Branch = `main`, folder = `/docs`.
3. The site is published at `https://<user>.github.io/<repo>/`.

`docs/.nojekyll` is included so GitHub serves the files as they are.

## Tests

```bash
npm install
npm test
```

`test_planner.js` exercises the gear, skill and Daevanion planner. `test_classes.js` opens every class guide and checks the hero, table of contents, gear-up block, checklists and Reference tab.

## Regenerating data

The scripts in `tools/` were written against a working folder that also held raw downloads: questlog.gg API dumps in `ref/`, ranked-player profiles in `cls/` and `chars/`, and generated images in `out/`. Those folders are not committed (see `.gitignore`).
- `qlapi.py` is the small questlog.gg tRPC client.
- `fetch_all.py` pulls ranked profiles per class.
- `gen_guides.py`, `gen_full.py` and `guide_text.py` build the class guides.
- `daev_plan_all.py` draws the Daevanion buy orders.

Run them from a folder with that layout and copy the results into `docs/`.

## Sources and credits

- Game data (skills, items, recipes, Daevanion boards, tier lists, ranked profiles): [questlog.gg](https://questlog.gg/aion-2/en).
- Global progression route: summarized from [couga54's AION 2 Guides](https://couga54.github.io/aion2-guides/en/progression/) (Sanya Jacuzzi's datamine, TitanTheF's sheet).
- Playtest route and gear stages: Aragon ([video](https://www.youtube.com/watch?v=zaTPBotP5ZI), [questlog build](https://questlog.gg/aion-2/en/character-builder/ConsumablesOfTheFrost)).
- Gladiator PvE build: Chef_Zhab ([video](https://www.youtube.com/watch?v=Ft4XarY_V6k)).

Creator advice is summarized in our own words, with a link back to the source.

Unofficial fan project, not affiliated with NCSOFT. AION 2, its skill and item icons and class emblems are © NCSOFT. The class banner illustrations in `docs/img/art/` are original.

## License

No license has been chosen yet. Add one (for example MIT for the code) before inviting contributions.
