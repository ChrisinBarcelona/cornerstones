"""Import a Notion "Markdown & CSV" export of the Cornerstones page into content/.

Usage:
    python3 tools/import_notion.py "/path/to/unzipped/Private & Shared"

Produces content/<slug>/index.md (+ optimised images) and content/lectures.json.
Notion hash suffixes are stripped, internal links become <slug>.html and
large images are resized with macOS `sips` (copied as-is elsewhere).
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

# Top-level lectures grouped for the index sidebar.
CATEGORIES = {
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
CATEGORY_OF = {slug: cat for cat, slugs in CATEGORIES.items() for slug in slugs}


def clean_title(text):
    return re.sub(r"\*\*|__", "", text).strip()


def slugify(text):
    text = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return text.strip("-")


def page_slug(md_path):
    stem = HASH_RE.sub("", md_path.stem)
    return slugify(stem)


def has_alpha(path):
    out = subprocess.run(["sips", "-g", "hasAlpha", str(path)], capture_output=True, text=True).stdout
    return "hasAlpha: yes" in out


def copy_image(src, dest_dir):
    """Copy an image into dest_dir, resizing/re-encoding big ones. Returns the new file name."""
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", src.name).strip("-") or "image"
    ext = src.suffix.lower()
    dest = dest_dir / name
    if ext in (".png", ".jpg", ".jpeg"):
        to_jpeg = ext == ".png" and src.stat().st_size > 400_000 and not has_alpha(src)
        if to_jpeg:
            dest = dest.with_suffix(".jpg")
        cmd = ["sips", "-Z", str(MAX_DIM)]
        if to_jpeg or ext in (".jpg", ".jpeg"):
            cmd += ["-s", "format", "jpeg", "-s", "formatOptions", "80"]
        r = subprocess.run(cmd + [str(src), "--out", str(dest)], capture_output=True)
        # sips upsizes nothing but always re-encodes; keep the original if that made it bigger.
        if r.returncode != 0 or (dest.suffix == src.suffix and dest.stat().st_size > src.stat().st_size):
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


def main(export_dir):
    export_dir = Path(export_dir)
    root_md = next(export_dir.glob("Cornerstones *.md"))
    if CONTENT.exists():
        shutil.rmtree(CONTENT)
    CONTENT.mkdir()

    pages = {}  # slug -> record
    order = []

    def import_page(md_path, parent=None, link_title=None):
        slug = page_slug(md_path)
        if slug in pages:
            return slug
        raw = md_path.read_text(encoding="utf-8")
        lines = raw.split("\n")
        title = clean_title(lines[0].lstrip("# ")) if lines and lines[0].startswith("# ") else clean_title(link_title or slug)
        body = "\n".join(lines[1:]).strip("\n")
        out_dir = CONTENT / slug
        out_dir.mkdir(parents=True)
        record = {"slug": slug, "title": title, "parent": parent, "children": []}
        pages[slug] = record
        order.append(slug)

        def repl(m):
            bang, label, target = m.groups()
            if re.match(r"[a-z]+:", target):
                return m.group(0)
            path = (md_path.parent / unquote(target)).resolve()
            if not path.exists():
                return m.group(0)
            if path.suffix == ".md":
                if page_slug(path) in top_slugs:  # e.g. Mental Models links to its own copy of Data
                    return f"[{clean_title(label)}]({page_slug(path)}.html)"
                child = import_page(path, parent=slug, link_title=label)
                if pages[child]["parent"] == slug and child not in record["children"]:
                    record["children"].append(child)
                return f"[{clean_title(label)}]({child}.html)"
            if bang or path.suffix.lower() in (".avif", ".webp", ".png", ".jpg", ".jpeg", ".gif"):
                label = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", label).replace("*", "")
                return f"![{label}]({copy_image(path, out_dir)})"
            return m.group(0)

        body = LINK_RE.sub(repl, fix_tables(body))
        (out_dir / "index.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
        return slug

    root_links = [(m.group(2), (root_md.parent / unquote(m.group(3))).resolve())
                  for m in LINK_RE.finditer(root_md.read_text(encoding="utf-8"))]
    top_slugs = {page_slug(path) for _, path in root_links}
    top = [import_page(path, link_title=label) for label, path in root_links]

    lectures = []
    for i, slug in enumerate(top, 1):
        rec = pages[slug]
        rec.update(number=i, category=CATEGORY_OF.get(slug, "Other"))
        lectures.append(rec)
    children = [pages[s] for s in order if pages[s]["parent"]]
    data = {"categories": list(CATEGORIES), "lectures": lectures, "subpages": children}
    (CONTENT / "lectures.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Imported {len(lectures)} lectures and {len(children)} sub-pages into {CONTENT}")


if __name__ == "__main__":
    main(sys.argv[1])
