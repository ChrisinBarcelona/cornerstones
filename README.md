# cornerstones
It's notes for me to teach my stuents - UX LEarning resource for Barcelona Code School

A static website. `index.html` is the course home (the four sections, a suggested route and a search of every page); each section has its own contents page:

| Section | Contents page | Pages | Source in Notion |
| --- | --- | --- | --- |
| UX Lectures | `ux.html` | `lectures/` | Cornerstones |
| UX Methods (Discovery → Retrospective) | `methods.html` | `methods/` | Google Sprint + Team Sprint databases (one bank, briefs and duplicates removed) |
| UI Lectures (Figma Basics, Components & Variables, UI Theory) | `ui.html` | `ui/` | Bootcamp UI → UI Starter Pack, UI Theory; Master |
| Exercises (Daily UI, Replica Challenges, Team Projects) | `exercises.html` | `exercises/` | Bootcamp UI → everything else (except Daily UI: Template); Stage Play is hand-written |

## Layout

- `assets/` – stylesheet and script
- `content/<section>/<slug>/index.md` – page text and images
- `content/<section>.json` (and `<section>.<part>.json` when a section has several sources) – the pages each import produced. `content/exercises.manual.json` lists hand-written pages such as Stage Play, which no import touches.
- `tools/import_notion.py` – turns a Notion Markdown export into `content/` (UX categories, the UI/exercise split and the UX Methods chapter list are set at the top)
- `content/summaries.json` – the one-line summary for each page, shown in the lists and at the top of the page. Edit freely.
- `tools/build.py` – renders `content/` into the site. At the top: section intros and chapter descriptions, the home page's suggested route (`ROUTE`), page order and categories for UI Lectures and Exercises (`ORDER` – a new page must be added there) and cross-links

## Updating

Edit `content/<section>/<slug>/index.md` (or re-export from Notion and re-import), then rebuild:

```bash
pip install markdown
ditto -x -k export.zip export/                                  # only when re-importing; plain unzip breaks curly quotes
python3 tools/import_notion.py "export/Private & Shared"        # Cornerstones, Bootcamp UI or Master export
python3 tools/import_notion.py "gs/Private & Shared" "ts/Private & Shared"   # UX Methods: both sprint exports together
python3 tools/build.py
```

Preview locally with `python3 -m http.server` and open http://localhost:8000.

## Publishing

GitHub Pages deploys `main` from the repository root: https://chrisinbarcelona.github.io/cornerstones/
