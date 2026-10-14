"""Import a Notion "Markdown & CSV" export into content/.

Usage:
    python3 tools/import_notion.py "/path/to/unzipped/Private & Shared"

Recognises two exports and splits them into the site's three tracks:
  - "Cornerstones"  -> ux         (UX lectures)
  - "Bootcamp UI"   -> ui         (UI Starter Pack + UI Theory lectures)
                    -> exercises  (Replica challenges + Daily UI briefs)

Each track gets content/<track>/<slug>/index.md (+ optimised images) and
content/<track>.json. Notion hash suffixes are stripped, internal links become
<slug>.html, and large images are resized with macOS `sips`.
Unzip exports with `ditto -x -k export.zip dest` – plain `unzip` mangles curly quotes.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
MAX_DIM = 1600
HASH_RE = re.compile(r"\s+(?:[0-9a-f]{32})$")
LINK_RE = re.compile(r"(!?)\[((?:[^\[\]]|\[[^\]]*\]\([^)]*\))*)\]\(((?:[^()\s]|\([^()]*\))+)\)")
IMAGE_EXT = (".avif", ".webp", ".png", ".jpg", ".jpeg", ".gif", ".heic")

# UX lectures, grouped for the index sidebar.
UX_CATEGORIES = {
    "Foundations": ["design-origins", "starting-point", "what-is-ux-design", "the-father-of-ux",
                    "key-figures", "key-roles"],
    "Psychology": ["the-bias-of-beauty", "bias", "mental-models", "design-psychology", "laws-of-ux",
                   "neilson-heuristics"],
    "Process": ["data", "what-is-design-thinking", "wicked-problem", "stages-of-wireframes", "target-mvp"],
    "Interface": ["what-is-ui-design", "gestures", "haptics"],
    "Case Studies": ["bad-user-experience", "a-case-of-genius", "the-death-of-kodak"],
    "Research": ["non-directive-interview-technique", "interviewer-format", "interview-taking-notes"],
    "Career": ["portfolio", "scripts"],
}
# Bootcamp UI: these hub pages become UI lecture categories; every other link is an exercise.
UI_GROUPS = {"UI Starter Pack": "Figma Guides", "UI Theory": "UI Theory"}
EXCLUDE = {"Daily UI: Template"}


def clean_title(text):
    return re.sub(r"\*\*|__", "", text).strip()


def short_title(title):
    """Drop series prefixes: '03. UI Guidelines: Beginner's Guide to Grids' -> 'Beginner's Guide to Grids'."""
    title = re.sub(r"^\d+\.\s*UI Guidelines\s*[:.]\s*", "", title)
    title = re.sub(r"^Daily UI:\s*", "", title)
    return re.sub(r"\s+", " ", title).strip()


def slugify(text):
    text = re.sub(r"['’]", "", text.lower())
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def file_slug(md_path):
    return slugify(HASH_RE.sub("", md_path.stem))


def has_alpha(path):
    out = subprocess.run(["sips", "-g", "hasAlpha", str(path)], capture_output=True, text=True).stdout
    return "hasAlpha: yes" in out


def copy_image(src, dest_dir):
    """Copy an image into dest_dir, resizing/re-encoding big ones. Returns the new file name."""
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", src.name).strip("-") or "image"
    ext = src.suffix.lower()
    dest = dest_dir / name
    if ext in (".png", ".jpg", ".jpeg", ".heic"):
        to_jpeg = ext == ".heic" or (ext == ".png" and src.stat().st_size > 400_000 and not has_alpha(src))
        if to_jpeg:
            dest = dest.with_suffix(".jpg")
        cmd = ["sips", "-Z", str(MAX_DIM)]
        if to_jpeg or ext in (".jpg", ".jpeg"):
            cmd += ["-s", "format", "jpeg", "-s", "formatOptions", "80"]
        r = subprocess.run(cmd + [str(src), "--out", str(dest)], capture_output=True)
        # sips always re-encodes; keep the original if that made it bigger.
        if ext != ".heic" and (r.returncode != 0 or (dest.suffix == src.suffix and dest.stat().st_size > src.stat().st_size)):
            shutil.copyfile(src, dest)
    else:
        shutil.copyfile(src, dest)
    return dest.name


def fix_tables(text):
    """Notion writes multi-line cells as raw newlines; join them back into one row."""
    out, buf = [], None
    for line in text.split("\n"):
        if buf is not None:
            buf += "<br>" + line.strip()
            if line.rstrip().endswith("|"):
                out.append(buf)
                buf = None
        elif line.startswith("|") and not line.rstrip().endswith("|"):
            buf = line.rstrip()
        else:
            out.append(line)
    if buf is not None:
        out.append(buf)
    return "\n".join(out)


def fix_bold(text):
    """Tidy Notion's bold artefacts: drop empty '****' and split a bold run that spans two paragraphs."""
    paras = text.replace("****", "").split("\n\n")
    for i in range(len(paras) - 1):
        if paras[i].count("**") % 2 and paras[i + 1].count("**") % 2:
            paras[i] = paras[i].rstrip() + "**"
            paras[i + 1] = "**" + paras[i + 1].lstrip()
    return "\n\n".join(paras)


def read_page(md_path):
    lines = md_path.read_text(encoding="utf-8").split("\n")
    title = clean_title(lines[0][2:]) if lines and lines[0].startswith("# ") else ""
    return title, "\n".join(lines[1:]).strip("\n")


def links_in(md_path):
    _, body = read_page(md_path)
    return [(clean_title(m.group(2)), (md_path.parent / unquote(m.group(3))).resolve())
            for m in LINK_RE.finditer(body) if not m.group(1) and m.group(3).endswith(".md")]


class Track:
    """Imports a set of top-level Notion pages (and the pages they link to) into content/<name>/."""

    def __init__(self, name, title_slugs=False, shorten=False):
        self.name, self.title_slugs, self.shorten = name, title_slugs, shorten
        self.dir = CONTENT / name
        if self.dir.exists():
            shutil.rmtree(self.dir)
        self.dir.mkdir(parents=True)
        self.pages, self.order, self.by_path, self.items = {}, [], {}, []

    def add(self, md_path, category, link_title=""):
        slug = self.import_page(md_path, link_title=link_title)
        self.pages[slug].update(number=len(self.items) + 1, category=category)
        self.items.append(slug)

    def import_page(self, md_path, parent=None, link_title=""):
        if md_path in self.by_path:
            return self.by_path[md_path]
        orig_path = md_path
        title, body = read_page(md_path)
        title = title or clean_title(link_title)
        # A page that is nothing but a link to one sub-page (e.g. "Dynamic Button") is replaced by that sub-page.
        only = LINK_RE.fullmatch(body.strip())
        if only and not only.group(1) and only.group(3).endswith(".md"):
            md_path = (md_path.parent / unquote(only.group(3))).resolve()
            title, body = read_page(md_path)
        if self.shorten:
            title = short_title(title)
        slug = slugify(title) if self.title_slugs else file_slug(md_path)
        while slug in self.pages:
            slug += "-2"
        self.by_path[md_path] = self.by_path[orig_path] = slug
        out_dir = self.dir / slug
        out_dir.mkdir(parents=True)
        record = {"slug": slug, "title": title, "parent": parent, "children": []}
        self.pages[slug] = record
        self.order.append(slug)
        base = md_path.parent

        def repl(m):
            bang, label, target = m.groups()
            if re.match(r"[a-z]+:", target):
                return m.group(0)
            path = (base / unquote(target)).resolve()
            if not path.exists():
                return m.group(0)
            if path.suffix == ".md":
                # A link to another top-level item (or Notion's duplicate of one, like Mental Models/Data).
                top = path if path in self.top_paths else self.top_by_slug.get(file_slug(path))
                if top:
                    return f"[{clean_title(label)}]({self.import_page(top)}.html)"
                child = self.import_page(path, parent=slug, link_title=label)
                if self.pages[child]["parent"] == slug and child not in record["children"]:
                    record["children"].append(child)
                return f"[{self.pages[child]['title']}]({child}.html)"
            if bang or path.suffix.lower() in IMAGE_EXT:
                label = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", label).replace("*", "")
                return f"![{label}]({copy_image(path, out_dir)})"
            return m.group(0)

        body = LINK_RE.sub(repl, fix_bold(fix_tables(body)))
        (out_dir / "index.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
        return slug

    def save(self, categories):
        items = [self.pages[s] for s in self.items]
        subpages = [self.pages[s] for s in self.order if self.pages[s]["parent"]]
        data = {"categories": categories, "lectures": items, "subpages": subpages}
        (CONTENT / f"{self.name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{self.name}: {len(items)} pages and {len(subpages)} sub-pages")


def import_cornerstones(root_md):
    ux = Track("ux")
    category_of = {slug: cat for cat, slugs in UX_CATEGORIES.items() for slug in slugs}
    links = links_in(root_md)
    ux.top_paths = {p for _, p in links}
    ux.top_by_slug = {file_slug(p): p for p in ux.top_paths}
    for label, path in links:
        ux.add(path, category_of.get(file_slug(path), "Other"), label)
    ux.save(list(UX_CATEGORIES))


def import_bootcamp_ui(root_md):
    ui = Track("ui", title_slugs=True, shorten=True)
    ex = Track("exercises", title_slugs=True, shorten=True)
    groups, exercises = [], []
    for label, path in links_in(root_md):
        title = read_page(path)[0] or label
        if title in UI_GROUPS:
            groups.append((UI_GROUPS[title], links_in(path)))
        elif title not in EXCLUDE:
            exercises.append((label, path, title))
    ui.top_paths = {p for _, pages in groups for _, p in pages}
    ui.top_by_slug = ex.top_by_slug = {}
    for category, pages in groups:
        for label, path in pages:
            ui.add(path, category, label)
    ui.save([c for c, _ in groups])

    ex.top_paths = {p for _, p, _ in exercises}
    for label, path, title in exercises:
        ex.add(path, "Daily UI" if title.startswith("Daily UI") else "Replica Challenges", label)
    ex.save(["Replica Challenges", "Daily UI"])


def main(export_dir):
    export_dir = Path(export_dir)
    CONTENT.mkdir(exist_ok=True)
    found = False
    for pattern, fn in (("Cornerstones *.md", import_cornerstones), ("Bootcamp UI *.md", import_bootcamp_ui)):
        for root_md in export_dir.glob(pattern):
            fn(root_md)
            found = True
    if not found:
        sys.exit(f"No Cornerstones or Bootcamp UI page found in {export_dir}")


if __name__ == "__main__":
    main(sys.argv[1])
