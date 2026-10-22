# cornerstones
UX Learning resource for Barcelona Code School

A static website. `index.html` is the course home (the five sections, a suggested route and a search of every page); each section has its own contents page:

| Section | Contents page | Pages | Source in Notion |
| --- | --- | --- | --- |
| UX Lectures | `ux.html` | `lectures/` | Cornerstones |
| UX Methods (Discovery → Retrospective) | `methods.html` | `methods/` | Google Sprint + Team Sprint databases (one bank, briefs and duplicates removed) |
| UI Lectures (UI Theory) | `ui.html` | `ui/` | Bootcamp UI → UI Theory; Master (Typeface, Case Studies) |
| Figma (Figma Basics, Figma Advanced) | `figma.html` | `figma/` | Bootcamp UI → UI Starter Pack; Master (Navbar, Dynamic Buttons, Variables). Shares `content/ui/` with UI Lectures |
| Exercises (Daily UI, Replica Challenges, Team Projects) | `exercises.html` | `exercises/` | Bootcamp UI → everything else (except Daily UI: Template); Stage Play is hand-written |

## Layout

- `assets/` – stylesheet and script
- `content/<section>/<slug>/index.md` – page text and images
- `content/<section>.json` (and `<section>.<part>.json` when a section has several sources) – the pages each import produced. `content/exercises.manual.json` lists hand-written pages such as Stage Play, which no import touches.
- `tools/import_notion.py` – turns a Notion Markdown export into `content/` (UX categories, the UI/exercise split and the UX Methods chapter list are set at the top)
- `content/timetable.json` – the 9-week timetable (`timetable.html`): each week's sprint, the activities for each day (from the bootcamp page on barcelonacodeschool.com), workshops and presentations (a checkpoint at the end of a sprint's Part One, a general audience presentation at the end of a sprint). Tags can link to a lesson or method. Every activity has its own icon, used by no other activity, in the `timetable` group of `content/icons.json`; the build stops if one is missing or shared.
- `content/summaries.json` – the one-line summary for each page, shown in the lists and at the top of the page. Edit freely.
- `tools/build.py` – renders `content/` into the site. At the top: section intros and chapter descriptions, the home page's suggested route (`ROUTE`), page order and categories for UI Lectures, Figma and Exercises (`ORDER` – a new UI or Figma page must be added to one of them) and cross-links

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

## Progress and badges

UX Lectures, UI Lectures, Figma and Exercises pages end with a **Mark as complete** button. Each section's contents page and the home page show progress, and finishing a whole section unlocks its badge. A lecture with parts counts as one item, complete only once the page and every part are done. Every ticked page moves the bars along, so a lecture with parts gives partial credit as its parts are done. The header shows overall course progress and the four badges on every page, and the checklist button in the header opens a tracker sidebar listing every lecture, lesson, part and exercise, where pages can be ticked or unticked. Progress is saved in the student's browser (`localStorage`), so it stays on that device. The sections and badges are set in `PROGRESS` in `tools/build.py`.

## Login

Every page sends visitors to `login.html` until they sign in, and the header has a Log out button. Only a SHA-256 hash of `username:password` is stored (`LOGIN_HASH` in `tools/build.py`). To change the login, generate a new hash, paste it in and rebuild; that signs everyone out:

```bash
python3 -c "import hashlib; print(hashlib.sha256(b'username:newpassword').hexdigest())"
```

This runs in the browser, so it keeps casual visitors out but is not real security: anyone who knows a file's address can still open it, and the site's files are public on GitHub. `robots.txt` and a `noindex` tag keep the site out of search engines.

## Publishing

GitHub Pages deploys `main` from the repository root: https://chrisinbarcelona.github.io/cornerstones/
