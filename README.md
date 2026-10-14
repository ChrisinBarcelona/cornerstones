# cornerstones
It's notes for me to teach my stuents - UX LEarning resource for Barcelona Code School

A static website: `index.html` lists every lecture, and each lecture opens at `lectures/<slug>.html`.

## Layout

- `index.html`, `lectures/` – the generated site (open `index.html` or serve the folder)
- `assets/` – stylesheet and script
- `content/` – lecture source: one folder per page with `index.md` and its images, plus `lectures.json` (order, categories, sub-lessons)
- `tools/import_notion.py` – turns a Notion Markdown export into `content/`
- `tools/build.py` – renders `content/` into the site

## Updating

Edit `content/<slug>/index.md` (or re-export from Notion and re-import), then rebuild:

```bash
pip install markdown
python3 tools/import_notion.py "/path/to/unzipped/Private & Shared"   # only when re-importing from Notion
python3 tools/build.py
```

Preview locally with `python3 -m http.server` and open http://localhost:8000.

## Publishing

Settings → Pages → Deploy from branch `main`, folder `/ (root)`.
