"""Import a Notion "Markdown & CSV" export into content/.

Usage:
    python3 tools/import_notion.py "/path/to/unzipped/Private & Shared" [more export dirs...]

Recognises these exports and splits them into the site's tracks:
  - "Cornerstones"  -> ux         (UX lectures)
  - "Bootcamp UI"   -> ui         (UI Starter Pack + UI Theory lectures)
                    -> exercises  (Replica challenges + Daily UI briefs)
  - "Google Sprint" + "Team Sprint" databases -> methods (UX Methods; pass both exports at once)
  - "Master"        -> ui         (later Figma guides + UI Theory: Typeface, Case Studies)

Each export writes content/<track>/<slug>/index.md (+ optimised images) and its own
index, content/<track>.json (or content/<track>.<part>.json when a track has several
sources). Re-importing an export replaces only the pages that export made.
Order and categories within each track are set in tools/build.py (ORDER). Notion hash suffixes are stripped, internal links become
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
    "Interface": ["gestures", "haptics"],
    "Case Studies": ["bad-user-experience", "a-case-of-genius", "the-death-of-kodak"],
    "Research": ["non-directive-interview-technique", "interviewer-format", "interview-taking-notes"],
    "Career": ["portfolio", "scripts"],
}
# UX lectures taken off the site (What is UI Design and its parts now live in UI Lectures and Figma).
UX_REMOVED = {"what-is-ui-design"}
# Bootcamp UI: these hub pages become UI lecture categories; every other link is an exercise.
UI_GROUPS = {"UI Starter Pack": "Figma Guides", "UI Theory": "UI Theory"}
# Templates and duplicates, left out wherever they appear.
EXCLUDE = {"Daily UI: Template", "Boiler Plate", "Key Figures: Walt Disney (1)"}
# Bootcamp UI pages replaced by newer versions in the Master export (Typeface, Dynamic Buttons Part One).
UI_REPLACED = {"Typography", "07. UI Guidelines: Dynamic Button"}

# UX Methods: one bank of methods drawn from the Google Sprint and Team Sprint databases, by chapter.
# Briefs (Talk To Me, Sprint Brief) and sprint introductions are left out. Where both sprints have the same
# method, the fuller Team Sprint version is used; these were dropped as duplicates:
#   Google Sprint: Competitive Analysis, Hi-Fi, Paper Wireframes, User Persona, Sprint Retrospective,
#                  Validate Problem Statement (= Problem Statement), Make A Map (= User Journey Map),
#                  Validate (= Usability Test), Conduct Interviews (one line), User Stories (brief-specific)
#   Team Sprint:   Mid-Fi (an unedited copy of Lo-Fi)
METHOD_CHAPTERS = [
    ("Discovery", [("Team Sprint", "Lean UX Canvas"), ("Google Sprint", "Long Term Goal"),
                   ("Team Sprint", "Research Goal"), ("Team Sprint", "Research Questions"),
                   ("Team Sprint", "User Survey"), ("Team Sprint", "User Interview"),
                   ("Team Sprint", "Discovery Summary")]),
    ("Define", [("Team Sprint", "Problem Statement"), ("Team Sprint", "User Persona"),
                ("Team Sprint", "Competitive Analysis"), ("Google Sprint", "How Might We"),
                ("Team Sprint", "Pick a Target"), ("Team Sprint", "User Journey Map"),
                ("Google Sprint", "Converge / Diverge"), ("Google Sprint", "Vote")]),
    ("Information Architecture", [("Team Sprint", "Task Flows")]),
    ("Ideation", [("Google Sprint", "Crazy 8’s"), ("Google Sprint", "Crazy 8’s with AI"),
                  ("Google Sprint", "Solution Sketch"), ("Team Sprint", "Mood Board"), ("Team Sprint", "Style Guide"),
                  ("Team Sprint", "Paper Wireframes"), ("Team Sprint", "Lo-Fi"), ("Team Sprint", "Hi-Fi")]),
    ("Validation", [("Team Sprint", "Usability Test"), ("Google Sprint", "Create your Script"),
                    ("Google Sprint", "Facilitator Format"), ("Google Sprint", "Limited Intervention Technique"),
                    ("Google Sprint", "Notetaker Format"), ("Team Sprint", "Design Iteration")]),
    ("Retrospective", [("Team Sprint", "Sprint Retrospective")]),
]
# Notion database properties written at the top of each page; not content.
PROPERTY_RE = re.compile(r"\A\s*(?:(?:Activity Number|Created by|Day|Sprint Phase|Status|Parent item|Sub-item|Student[^:\n]*):[^\n]*\n\s*)+")


def clean_title(text):
    return re.sub(r"\*\*|__", "", text).strip()


def short_title(title):
    """Drop series prefixes: '03. UI Guidelines: Beginner's Guide to Grids' -> 'Beginner's Guide to Grids'."""
    title = re.sub(r"^\d+\s*[.:]\s*UI (?:Guidelines|Theory)\s*[:.]\s*", "", title)
    title = {"TypeFace": "Typeface"}.get(title, title)
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
    # A table followed directly by text (no blank line) swallows it; separate them.
    for i in range(len(out) - 1, 0, -1):
        if out[i - 1].startswith("|") and out[i].strip() and not out[i].startswith("|"):
            out.insert(i, "")
    return "\n".join(out)


def fix_bold(text):
    """Tidy Notion's bold artefacts: drop empty '****' and split a bold run that spans two paragraphs."""
    text = text.replace("****", "")
    # "**- item**": bold wrapped around a list marker; move it inside.
    text = re.sub(r"(?m)^(\s*)\*\*- (.+?)\*\*\s*$", r"\1- **\2**", text)
    # A heading whose bold run continues onto the next line ("## **5. Buttons\nExercise →**"): drop the markers.
    text = re.sub(r"(?m)^(#+ )\*\*([^*\n]+)\n([^*\n]+)\*\*$", r"\1\2\n\n\3", text)
    # "**bold.***" closing bold and italic together trips up Markdown; spell the bold out.
    text = re.sub(r"(?<!\*)\*\*([^*\n]+)\*\*\*", r"<strong>\1</strong>*", text)
    paras = text.split("\n\n")
    for i in range(len(paras) - 1):
        if paras[i].count("**") % 2 and paras[i + 1].count("**") % 2:
            paras[i] = paras[i].rstrip() + "**"
            paras[i + 1] = "**" + paras[i + 1].lstrip()
    return "\n\n".join(paras)


def read_page(md_path):
    lines = md_path.read_text(encoding="utf-8").split("\n")
    title = clean_title(lines[0][2:]) if lines and lines[0].startswith("# ") else ""
    return title, PROPERTY_RE.sub("", "\n".join(lines[1:])).strip("\n")


def links_in(md_path):
    _, body = read_page(md_path)
    return [(clean_title(m.group(2)), (md_path.parent / unquote(m.group(3))).resolve())
            for m in LINK_RE.finditer(body) if not m.group(1) and m.group(3).endswith(".md")]


class Track:
    """Imports a set of top-level Notion pages (and the pages they link to) into content/<name>/."""

    def __init__(self, name, part=None, title_slugs=False, shorten=False):
        self.name, self.title_slugs, self.shorten = name, title_slugs, shorten
        self.dir = CONTENT / name
        self.index = CONTENT / (f"{name}.{part}.json" if part else f"{name}.json")
        # Remove what this export imported last time; other sources in the same track are left alone.
        if self.index.exists():
            old = json.loads(self.index.read_text(encoding="utf-8"))
            for p in old["lectures"] + old["subpages"]:
                shutil.rmtree(self.dir / p["slug"], ignore_errors=True)
        self.dir.mkdir(parents=True, exist_ok=True)
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
        while slug in self.pages or (self.dir / slug).exists():
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
                return clean_title(label) if target.endswith(".md") and not bang else m.group(0)
            if path.suffix == ".md" and clean_title(read_page(path)[0] or label) in EXCLUDE:
                return ""
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
                label = " ".join(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", label).replace("*", "").split())
                return f"![{label}]({copy_image(path, out_dir)})"
            # Any other attachment (e.g. a .zip of assets) is copied next to the page.
            name = re.sub(r"[^A-Za-z0-9._-]+", "-", path.name).strip("-")
            shutil.copyfile(path, out_dir / name)
            return f"[{label}]({name})"

        body = LINK_RE.sub(repl, fix_bold(fix_tables(body)))
        (out_dir / "index.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
        return slug

    def save(self, categories):
        items = [self.pages[s] for s in self.items]
        subpages = [self.pages[s] for s in self.order if self.pages[s]["parent"]]
        data = {"categories": categories, "lectures": items, "subpages": subpages}
        self.index.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{self.name}: {len(items)} pages and {len(subpages)} sub-pages")


def import_cornerstones(root_md):
    ux = Track("ux")
    category_of = {slug: cat for cat, slugs in UX_CATEGORIES.items() for slug in slugs}
    links = links_in(root_md)
    ux.top_paths = {p for _, p in links}
    ux.top_by_slug = {file_slug(p): p for p in ux.top_paths}
    for label, path in links:
        if file_slug(path) in UX_REMOVED:
            continue
        ux.add(path, category_of.get(file_slug(path), "Other"), label)
    ux.save(list(UX_CATEGORIES))


def import_bootcamp_ui(root_md):
    ui = Track("ui", title_slugs=True, shorten=True)
    ex = Track("exercises", title_slugs=True, shorten=True)
    groups, exercises = [], []
    for label, path in links_in(root_md):
        title = read_page(path)[0] or label
        if title in UI_GROUPS:
            groups.append((UI_GROUPS[title], [(l, p) for l, p in links_in(path) if (read_page(p)[0] or l) not in EXCLUDE | UI_REPLACED]))
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


def import_master(root_md):
    ui = Track("ui", part="master", title_slugs=True, shorten=True)
    links = links_in(root_md)
    ui.top_paths, ui.top_by_slug = {p for _, p in links}, {}
    for label, path in links:
        ui.add(path, "UI Theory" if "UI Theory" in (read_page(path)[0] or label) else "Figma Guides", label)
    ui.save(["Figma Guides", "UI Theory"])


def import_methods(databases):
    """databases: {"Google Sprint": folder, "Team Sprint": folder} of database page exports."""
    pages = {}
    for name, folder in databases.items():
        for md in folder.glob("*.md"):
            pages[(name, slugify(read_page(md)[0] or HASH_RE.sub("", md.stem)))] = md
    methods = Track("methods", title_slugs=True)
    methods.top_paths, methods.top_by_slug = set(), {}
    for chapter, items in METHOD_CHAPTERS:
        for db, title in items:
            md = pages.get((db, slugify(title)))
            if md is None:
                sys.exit(f"UX Methods: '{title}' not found in the {db} export")
            methods.add(md, chapter)
    methods.save([c for c, _ in METHOD_CHAPTERS])


def main(export_dirs):
    CONTENT.mkdir(exist_ok=True)
    found = False
    databases = {}
    for export_dir in map(Path, export_dirs):
        for pattern, fn in (("Cornerstones *.md", import_cornerstones), ("Bootcamp UI *.md", import_bootcamp_ui),
                            ("Master.md", import_master), ("Master *.md", import_master)):
            for root_md in export_dir.glob(pattern):
                fn(root_md)
                found = True
        for name in ("Google Sprint", "Team Sprint"):
            if (export_dir / name).is_dir():
                databases[name] = export_dir / name
    if databases:
        if len(databases) < 2:
            sys.exit("UX Methods needs both the Google Sprint and Team Sprint exports in one run")
        import_methods(databases)
        found = True
    if not found:
        sys.exit(f"No Cornerstones, Bootcamp UI, Master or sprint database export found in {export_dirs}")


if __name__ == "__main__":
    main(sys.argv[1:])
