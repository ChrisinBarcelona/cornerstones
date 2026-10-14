"""Render content/ into the static site.

    index.html      UX lectures        -> lectures/<slug>.html
    ui.html         UI lectures        -> ui/<slug>.html
    exercises.html  Exercises          -> exercises/<slug>.html

Usage:
    pip install markdown
    python3 tools/build.py
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import markdown

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SITE = "Cornerstones"
TAGLINE = "UX & UI learning resource for Barcelona Code School"

TRACKS = [
    {"id": "ux", "out": "lectures", "index": "index.html", "label": "UX Lectures", "noun": "Lecture",
     "eyebrow": "UX Learning Resource", "h1": "Cornerstones of UX Design, in order",
     "intro": "{n} lectures and {s} sub-lessons on the history, psychology and practice of user experience design. Pick any lecture to open the full notes."},
    {"id": "ui", "out": "ui", "index": "ui.html", "label": "UI Lectures", "noun": "Lecture",
     "eyebrow": "UI Learning Resource", "h1": "UI Design, from Figma basics to theory",
     "intro": "{n} lectures on building interfaces. Figma Guides are hands-on, step-by-step tutorials to follow in order; UI Theory covers the concepts behind colour, type, spacing and systems. New to UI? Read <a href=\"lectures/what-is-ui-design.html\">What is UI Design</a> in the UX track first."},
    {"id": "exercises", "out": "exercises", "index": "exercises.html", "label": "Exercises", "noun": "Exercise",
     "eyebrow": "Practice", "h1": "Exercises & design challenges",
     "intro": "{n} briefs to practise with in Figma. Replica Challenges are long, pixel-perfect copies of real apps; Daily UI briefs are single-screen designs for one session. Each one is rated for difficulty."},
]
TRACK = {t["id"]: t for t in TRACKS}

# Cross-links shown at the end of a page as "Related". Each pair is linked both ways.
RELATED = [
    ("ui/icons", "ux/icons"),
    ("ui/typography", "ux/typography"),
    ("ui/colour-values", "ux/colors"),
    ("ui/spacing-grids", "ux/grid"),
    ("ui/spacing-grids", "ui/beginners-guide-to-grids"),
    ("ui/spacing-grids", "ui/beginners-guide-to-8-point-grid-system"),
    ("ui/style-guides", "ux/design-systems"),
    ("ui/atomic-design-methodology", "ux/design-systems"),
    ("ui/atomic-design-methodology", "ui/beginners-guide-to-components"),
    ("ui/paper-wireframes", "ux/stages-of-wireframes"),
    ("ui/choose-your-frame", "ux/what-is-ui-design"),
    ("exercises/glovo-replica-challenge", "ui/beginners-guide-to-nesting"),
    ("exercises/glovo-replica-challenge", "ui/beginners-guide-auto-layout"),
    ("exercises/glovo-replica-challenge", "ui/beginners-guide-to-components"),
    ("exercises/youtube-challenge", "ui/beginners-guide-to-nesting"),
    ("exercises/youtube-challenge", "ui/beginners-guide-auto-layout"),
    ("exercises/youtube-challenge", "ui/beginners-guide-to-components"),
    ("exercises/ux-x-ai", "exercises/make-an-ai-interface"),
    ("exercises/glovo-replica-challenge", "exercises/youtube-challenge"),
]

# Hand-written summaries where a page's first paragraph doesn't describe it well.
SUMMARIES = {
    "ui/choose-your-frame": "How to pick a Figma frame size for the device you'll design and prototype on, and why aspect ratio matters.",
    "ui/dynamic-buttons-part-one": "Build a reusable button component in Figma with text properties, appearance booleans and swaps.",
    "ui/file-types": "When to use JPG, PNG, GIF, SVG, WEBP and TIFF in interface work.",
    "exercises/glovo-replica-challenge": "Recreate the Glovo app screen by screen in Figma: by hand first, then rebuilt with Auto Layout and components.",
    "exercises/youtube-challenge": "Recreate the YouTube app screen by screen in Figma: by hand first, then rebuilt with Auto Layout and components.",
    "exercises/choose-a-movie": "Design a movie trailer intro page for a streaming service that invites people to press play.",
    "exercises/video-player": "Design a simple, instantly recognisable video player for a streaming service.",
}

YOUTUBE_RE = re.compile(
    r'<p><a href="(https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/)|youtu\.be/)([\w-]{11})[^"]*)">[^<]*</a></p>')
FIGMA_RE = re.compile(r'<p><a href="(https://www\.figma\.com/embed\?[^"]+)">[^<]*</a></p>')
LECTURE_LINK_RE = re.compile(r'<p><a href="([a-z0-9-]+)\.html">(.*?)</a></p>')
IMG_P_RE = re.compile(r'<p>(<img [^>]+>)</p>')
IMG_RE = re.compile(r'<img alt="([^"]*)" src="([^"]+)"\s*/?>')
H_RE = re.compile(r'<h([1-3]) id="([^"]+)">(.*?)</h\1>')
TAG_RE = re.compile(r"<[^>]+>")
ASIDE_RE = re.compile(r"<aside>\s*(.*?)\s*</aside>", re.S)
DIFFICULTY_RE = re.compile(r"^#+\s*Difficulty Level\s*(.*)$", re.M)

ICON_SUN = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
ICON_ARROW = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICON_IMG = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICON_EXT = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 4h6v6M20 4l-9 9M18 14v6H4V6h6"/></svg>'


def esc(s):
    return html.escape(s, quote=True)


def plain(s):
    return html.unescape(TAG_RE.sub("", s)).strip()


def short(title):
    return title.split(": ", 1)[-1]


def meter(level, out_of=5):
    return (f'<span class="meter" role="img" aria-label="Difficulty {level} of {out_of}">'
            + "".join(f'<i class="{"on" if i < level else ""}"></i>' for i in range(out_of)) + "</span>")


def page(title, description, body, depth, active):
    prefix = "../" * depth
    links = "".join(
        f'<a href="{prefix}{t["index"]}"{" aria-current=page" if t["id"] == active else ""}>{t["label"]}</a>' for t in TRACKS)
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<script>try{{var t=localStorage.getItem('cs-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<header class="nav">
  <div class="nav-inner">
    <a class="brand" href="{prefix}index.html">
      <span class="brand-mark">C</span>
      <span class="brand-text"><span class="brand-name">{SITE.upper()}</span><span class="brand-sub">UX &amp; UI at Barcelona Code School</span></span>
    </a>
    <nav class="nav-links">{links}<a href="https://github.com/ChrisinBarcelona/cornerstones">GitHub</a></nav>
    <button class="icon-btn" id="theme-toggle" type="button" aria-label="Toggle colour theme">{ICON_SUN}</button>
  </div>
</header>
{body}
<footer class="foot"><div class="foot-inner"><span>{SITE} · {TAGLINE}</span><span class="mono">Notes by Chris Kelly</span></div></footer>
<script src="{prefix}assets/app.js"></script>
</body>
</html>
"""


def render_markdown(track, slug, text, titles):
    text = DIFFICULTY_RE.sub("", text)  # shown in the page header instead
    text = ASIDE_RE.sub(lambda m: f'<div class="callout" markdown="1">\n\n{m.group(1)}\n\n</div>', text)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc", "md_in_html"],
                           extension_configs={"toc": {"slugify": lambda v, sep: re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-") or "section"}})
    body = md.convert(text)
    body = re.sub(r"<h1 [^>]*>.*?</h1>\s*", "", body, count=1)  # title is rendered in the header
    # Remaining in-body h1s (Notion "slides") become h2s.
    body = re.sub(r"<h1 (id=\"[^\"]+\")>(.*?)</h1>", r"<h2 \1>\2</h2>", body)

    def fix_img(m):
        alt, src = m.groups()
        if not re.match(r"[a-z]+:", src):
            src = f"../content/{track}/{slug}/{src}"
        alt = "" if re.search(r"\.(png|jpe?g|webp|gif|avif|heic)$", alt, re.I) or alt == "Untitled" else alt
        return f'<img alt="{alt}" src="{src}" loading="lazy" decoding="async">'

    # Pull the leading emoji of a callout into its own column.
    body = re.sub(r'(<div class="callout">\s*<p>)([^\w<\s]+)\s*', r'\1<span class="callout-icon">\2</span>', body)
    body = IMG_RE.sub(fix_img, body)
    body = IMG_P_RE.sub(r'<figure class="media">\1</figure>', body)
    body = YOUTUBE_RE.sub(
        lambda m: f'<figure class="video"><iframe src="https://www.youtube-nocookie.com/embed/{m.group(2)}" title="YouTube video" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe></figure>',
        body)

    def figma(m):
        embed = html.unescape(m.group(1))
        file_url = parse_qs(urlparse(embed).query).get("url", [""])[0]
        embed = re.sub(r"embed_host=[^&]+", "embed_host=share", embed)
        link = f'<a class="embed-link" href="{esc(file_url)}" target="_blank" rel="noopener">Open in Figma {ICON_EXT}</a>' if file_url else ""
        return (f'<figure class="video figma"><iframe src="{esc(embed)}" title="Figma file" loading="lazy" allowfullscreen></iframe></figure>{link}')

    body = FIGMA_RE.sub(figma, body)

    # Runs of standalone links to other pages become a card list.
    def card(m):
        target, label = m.groups()
        sub = titles.get(target, {})
        desc = f'<span class="card-desc">{esc(sub.get("description", ""))}</span>' if sub.get("description") else ""
        return f'<li><a class="card" href="{target}.html"><span class="card-title">{label}</span>{desc}<span class="card-go">{ICON_ARROW}</span></a></li>'

    body = re.sub(r"(?:" + LECTURE_LINK_RE.pattern + r"\s*)+",
                  lambda m: '<ul class="cards">' + "".join(card(x) for x in LECTURE_LINK_RE.finditer(m.group(0))) + "</ul>\n",
                  body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    body = re.sub(r'<p><a href="https://app\.notion\.com"></a></p>', "", body)
    body = re.sub(r"(<hr\s*/?>\s*){2,}", "<hr>\n", body)
    body = re.sub(r"(<hr\s*/?>\s*)+$", "", body.strip())
    body = re.sub(r"<p>\s*(\*\*\*\*)?\s*</p>", "", body)
    toc = [(lvl, hid, plain(txt)) for lvl, hid, txt in H_RE.findall(body) if plain(txt)]
    return body, toc


def describe(text):
    for block in re.split(r"\n\s*\n", text.split("\n", 1)[1] if "\n" in text else text):
        b = block.strip()
        if not b or b.startswith(("#", "!", "|", "---", ">", "[", "<")) or re.match(r"^(\d+\.|-|\*) ", b):
            continue
        b = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", b)
        b = re.sub(r"[*_`]", "", b).replace("\n", " ").strip()
        if len(b) < 40:
            continue
        return b if len(b) <= 180 else b[:177].rsplit(" ", 1)[0] + "…"
    return ""


def load():
    """Load every track and compute per-page stats."""
    data = {}
    for t in TRACKS:
        d = json.loads((CONTENT / f"{t['id']}.json").read_text(encoding="utf-8"))
        every = d["lectures"] + d["subpages"]
        by_slug = {p["slug"]: p for p in every}
        for p in every:
            p["track"] = t["id"]
            text = (CONTENT / t["id"] / p["slug"] / "index.md").read_text(encoding="utf-8")
            words = len(re.findall(r"\w+", re.sub(r"!\[[^\]]*\]\([^)]*\)|\([^)]*\)", "", text)))
            summary = SUMMARIES.get(f'{t["id"]}/{p["slug"]}')
            p["description"] = summary or describe(text)
            p["lede"] = not p["description"] or bool(summary)  # only show a lede when it won't repeat the first paragraph
            p["minutes"] = max(1, round(words / 200))
            p["images"] = len(re.findall(r"!\[", text))
            stars = DIFFICULTY_RE.search(text)
            p["difficulty"] = stars.group(1).count("⭐") if stars else 0
            p["text"] = text
        for p in every:
            if p["description"]:
                continue
            if p["children"]:
                names = [short(by_slug[c]["title"]) for c in p["children"]]
                p["description"] = f"{len(names)} short lessons: {', '.join(names[:4])}" + (" and more." if len(names) > 4 else ".")
            else:
                heads = [re.sub(r"[*_`#]", "", h).strip(" :") for h in re.findall(r"^#{2,3} (.+)$", p["text"], re.M)
                         if not DIFFICULTY_RE.match(h)]
                heads = [h for h in heads if h][:4]
                if heads:
                    p["description"] = "Covers " + ", ".join(heads[:-1]) + (" and " if len(heads) > 1 else "") + heads[-1] + "."
        data[t["id"]] = {**d, "every": every, "by_slug": by_slug}
    return data


def build_track(t, data):
    d = data[t["id"]]
    lectures, every, by_slug = d["lectures"], d["every"], d["by_slug"]
    out = ROOT / t["out"]
    out.mkdir(exist_ok=True)
    for old in out.glob("*.html"):
        old.unlink()

    related = {}
    for a, b in RELATED:
        related.setdefault(a, []).append(b)
        related.setdefault(b, []).append(a)

    def lookup(key):
        track, slug = key.split("/")
        p = data[track]["by_slug"].get(slug)
        if p is None:
            raise SystemExit(f"RELATED points at missing page {key}")
        return p

    reading_order = [s for l in lectures for s in [l["slug"]] + l["children"]]
    for p in every:
        body, toc = render_markdown(t["id"], p["slug"], p["text"], by_slug)
        parent = by_slug.get(p["parent"]) if p["parent"] else None
        top = parent or p
        siblings = parent["children"] if parent else []
        k = reading_order.index(p["slug"])
        prev_p = by_slug[reading_order[k - 1]] if k > 0 else None
        next_p = by_slug[reading_order[k + 1]] if k + 1 < len(reading_order) else None

        crumbs = [f'<a href="../{t["index"]}">{t["label"]}</a>',
                  f'<a href="../{t["index"]}#category={esc(top["category"])}">{esc(top["category"])}</a>']
        if parent:
            crumbs.append(f'<a href="{parent["slug"]}.html">{esc(parent["title"])}</a>')
        crumbs.append(f"<span>{esc(p['title'])}</span>")

        if parent:
            eyebrow = f'{parent["title"]} · Part {siblings.index(p["slug"]) + 1} of {len(siblings)}'
        else:
            eyebrow = f'{t["noun"]} {top["number"]:02d} · {top["category"]}'
        meta = []
        if p["difficulty"]:
            meta.append(f'Difficulty {meter(p["difficulty"])}')
        elif t["id"] == "exercises":
            meta.append("Multi-session project")
        meta.append(f'{ICON_CLOCK}{p["minutes"]} min read')
        if p["images"]:
            meta.append(f'{ICON_IMG}{p["images"]} image{"s" if p["images"] != 1 else ""}')
        if p["children"]:
            meta.append(f'{len(p["children"])} sub-lessons')

        toc_html = "".join(
            f'<li class="lvl{lvl}"><a href="#{hid}">{esc(txt)}</a></li>' for lvl, hid, txt in toc if lvl in ("2", "3"))
        rail = ""
        if toc_html:
            rail += f'<div class="rail-block"><div class="rail-label">On this page</div><ol class="toc">{toc_html}</ol></div>'
        family = p["children"] or siblings
        if family:
            owner = p if p["children"] else parent
            items = "".join(
                f'<li><a href="{s}.html"{" aria-current=page" if s == p["slug"] else ""}>{esc(short(by_slug[s]["title"]))}</a></li>'
                for s in family)
            rail += f'<div class="rail-block"><div class="rail-label">{esc(owner["title"])}</div><ol class="toc family">{items}</ol></div>'
        else:
            # Pages without sub-lessons list the rest of their category instead.
            same = [l for l in lectures if l["category"] == p["category"]]
            items = "".join(
                f'<li><a href="{l["slug"]}.html"{" aria-current=page" if l is p else ""}>{esc(l["title"])}</a></li>' for l in same)
            if len(same) > 1:
                rail += f'<div class="rail-block"><div class="rail-label">{esc(p["category"])}</div><ol class="toc family">{items}</ol></div>'

        rel = [lookup(k) for k in related.get(f'{t["id"]}/{p["slug"]}', [])]
        if rel:
            cards = "".join(
                f'<li><a class="card" href="../{TRACK[r["track"]]["out"]}/{r["slug"]}.html"><span class="card-title">{esc(r["title"])}</span>'
                f'<span class="card-desc">{TRACK[r["track"]]["label"]} · {esc(r.get("category") or data[r["track"]]["by_slug"][r["parent"]]["category"])}</span>'
                f'<span class="card-go">{ICON_ARROW}</span></a></li>' for r in rel)
            body += f'\n<section class="related"><h2 id="related">Related</h2><ul class="cards">{cards}</ul></section>'

        def pager(q, label, cls):
            if not q:
                return "<span></span>"
            return f'<a class="pager {cls}" href="{q["slug"]}.html"><span class="pager-label">{label}</span><span class="pager-title">{esc(q["title"])}</span></a>'

        body_html = f"""
<main class="lecture track-{t['id']}">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">{' <span class="sep">/</span> '.join(crumbs)}</nav>
    <header class="lecture-head">
      <div class="eyebrow">{esc(eyebrow)}</div>
      <h1>{esc(p['title'])}</h1>
      {f'<p class="lede">{esc(p["description"])}</p>' if p["lede"] and p["description"] else ''}
      <div class="meta">{''.join(f'<span>{m}</span>' for m in meta)}</div>
    </header>
    <div class="lecture-grid{' no-rail' if not rail else ''}">
      {f'<aside class="rail"><div class="rail-sticky">{rail}</div></aside>' if rail else ''}
      <article class="prose">
{body}
      </article>
    </div>
    <nav class="pagers">{pager(prev_p, "Previous", "prev")}{pager(next_p, "Next", "next")}</nav>
  </div>
</main>
<div class="lightbox" id="lightbox" hidden><img alt=""></div>"""
        (out / f"{p['slug']}.html").write_text(
            page(f"{p['title']} · {SITE}", p["description"] or TAGLINE, body_html, 1, t["id"]), encoding="utf-8")

    # Contents page for the track
    cats = d["categories"]
    counts = {c: sum(1 for l in lectures if l["category"] == c) for c in cats}
    cat_links = "".join(
        f'<li><button type="button" data-cat="{esc(c)}"><span>{esc(c)}</span><span class="count">{counts[c]}</span></button></li>'
        for c in cats)
    is_ex = t["id"] == "exercises"
    rows = []
    for l in lectures:
        subs = ""
        if l["children"]:
            subs = '<div class="row-subs">' + "".join(
                f'<a href="{t["out"]}/{s}.html">{esc(short(by_slug[s]["title"]))}</a>' for s in l["children"]) + "</div>"
        search = " ".join([l["title"], l["category"], l["description"]] + [by_slug[s]["title"] for s in l["children"]]).lower()
        if is_ex:
            level = meter(l["difficulty"]) if l["difficulty"] else '<span class="tag">Project</span>'
            stats = f'<span>{level}</span><span>{ICON_CLOCK}{l["minutes"]}m read</span>'
        else:
            stats = f'<span>{ICON_CLOCK}{l["minutes"]}m</span>'
            if l["images"]:
                stats += f'<span>{ICON_IMG}{l["images"]}</span>'
        rows.append(f"""<li class="row" data-cat="{esc(l['category'])}" data-search="{esc(search)}">
  <span class="row-num">{l['number']}</span>
  <div class="row-body">
    <div class="row-head"><a class="row-title" href="{t['out']}/{l['slug']}.html">{esc(l['title'])}</a>{f'<span class="pill">{len(l["children"])} parts</span>' if l["children"] else ''}</div>
    <p class="row-desc">{esc(l['description'])}</p>
    <div class="row-tag">[{esc(l['category'].upper())}]</div>
    {subs}
  </div>
  <div class="row-stats">{stats}</div>
</li>""")

    tabs = "".join(
        f'<a class="track-tab" href="{x["index"]}"{" aria-current=page" if x is t else ""}><span>{x["label"]}</span><span class="count">{len(data[x["id"]]["lectures"])}</span></a>'
        for x in TRACKS)
    total_min = sum(p["minutes"] for p in every)
    if is_ex:
        side_stat = ('<div class="side-stat"><div class="side-label">Difficulty</div>'
                     + "".join(f'<div class="diff-row">{meter(n)}<span class="count">{sum(1 for l in lectures if l["difficulty"] == n)}</span></div>'
                               for n in range(5, 0, -1) if any(l["difficulty"] == n for l in lectures))
                     + "</div>")
    else:
        side_stat = f'<div class="side-stat"><div class="side-label">Reading time</div><div class="big">{f"{total_min // 60}h " if total_min >= 60 else ""}{total_min % 60}m</div><div class="muted mono">across every page</div></div>'
    noun = t["noun"].lower()
    intro = t["intro"].format(n=len(lectures), s=len(d["subpages"]))
    index_body = f"""
<main class="home">
  <div class="wrap">
    <nav class="track-tabs" aria-label="Sections">{tabs}</nav>
    <header class="hero">
      <div>
        <div class="eyebrow">{t['eyebrow']}</div>
        <h1>{t['h1']}</h1>
        <p class="lede">{intro}</p>
      </div>
      <a class="hero-link" href="{t['out']}/{lectures[0]['slug']}.html">Start with {esc(lectures[0]['title'])} {ICON_ARROW}</a>
    </header>
    <div class="layout">
      <aside class="sidebar">
        <div class="side-label">Category</div>
        <ul class="cats">
          <li><button type="button" data-cat="" aria-pressed="true"><span>All {noun}s</span><span class="count">{len(lectures)}</span></button></li>
          {cat_links}
        </ul>
        {side_stat}
      </aside>
      <section class="listing">
        <div class="toolbar">
          <label class="search"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q" type="search" placeholder="Search {noun}s…" autocomplete="off"></label>
          <span class="showing mono" id="showing">Showing {len(lectures)} of {len(lectures)}</span>
          <div class="view-toggle" role="group" aria-label="Layout">
            <button type="button" data-view="list" aria-pressed="true" aria-label="List view"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button>
            <button type="button" data-view="grid" aria-pressed="false" aria-label="Grid view"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="4" width="6" height="6"/><rect x="14" y="4" width="6" height="6"/><rect x="4" y="14" width="6" height="6"/><rect x="14" y="14" width="6" height="6"/></svg></button>
          </div>
        </div>
        <div class="list-head mono"><span>#</span><span>{t['noun']}</span><span class="right">{'Difficulty' if is_ex else 'Length'}</span></div>
        <ol class="rows" id="rows">
{''.join(rows)}
        </ol>
        <p class="empty" id="empty" hidden>No {noun}s match that search.</p>
      </section>
    </div>
  </div>
</main>"""
    (ROOT / t["index"]).write_text(
        page(f"{SITE} · {t['label']}", TAGLINE, index_body, 0, t["id"]), encoding="utf-8")
    print(f"{t['index']}: {len(lectures)} {noun}s, {len(every)} pages in {t['out']}/")


def main():
    data = load()
    for t in TRACKS:
        build_track(t, data)


if __name__ == "__main__":
    main()
