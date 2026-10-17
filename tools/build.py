"""Render content/ into the static site.

    index.html      Course home: the four sections, a suggested route and a search of everything
    timetable.html  The 9-week timetable board (content/timetable.json)
    ux.html         UX Theory          -> lectures/<slug>.html
    methods.html    UX methods         -> methods/<slug>.html
    ui.html         UI Theory          -> ui/<slug>.html
    figma.html      Figma tutorials    -> figma/<slug>.html   (content shared with UI: content/ui/)
    exercises.html  Exercises          -> exercises/<slug>.html

Usage:
    pip install markdown
    python3 tools/build.py
"""
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

import markdown

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SITE = "Cornerstones"
SCHOOL = "Barcelona Code School"
# The logo mark: four tiles in the section colours; the top-left "cornerstone" is a quarter circle.
LOGO_MARK = ('<svg class="logo-mark" viewBox="38 40 739 739" width="38" height="38" aria-hidden="true">'
             '<path d="M221 90H590L777 409H38Z" fill="#004ecd"/>'
             '<path d="M38 409H777L590 728H221Z" fill="#0062ff"/>'
             '<path d="M374 254H688L777 409H286Z" fill="#002b71"/>'
             '<path d="M286 409H777L688 564H374Z" fill="#003ea2"/></svg>')
FAVICON = "data:image/svg+xml," + __import__("urllib.parse").parse.quote(
    LOGO_MARK.replace('class="logo-mark" ', 'xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', ''))
LOGO = (f'{LOGO_MARK}<span class="logo-text"><span class="logo-name">Cornerstones</span>'
        f'<span class="logo-sub">UX/UI Design at {SCHOOL}</span></span>')
ASSET_V = ""  # set in main(): a content hash appended to asset URLs so browsers never mix old and new files
TAGLINE = "UX & UI learning resource for Barcelona Code School"

# Course login. Only a SHA-256 hash of "username:password" is stored, never the password itself.
# To change it:  python3 -c "import hashlib; print(hashlib.sha256(b'user:newpassword').hexdigest())"
# Changing it signs everyone out. Note: this is a browser-side gate on a static site; it keeps casual
# visitors out but is not real security (the files themselves stay publicly reachable).
LOGIN_HASH = "c5690f27953d06d990942488e4e6153a0e1116091995938ffa0bb366cda32202"

TRACKS = [
    {"id": "sprints", "out": "sprints", "index": "sprints.html", "label": "Sprint Briefs", "noun": "Brief",
     "eyebrow": "The Projects", "h1": "Sprint Briefs",
     "blurb": "The four sprints at the heart of the bootcamp, from real-world service design to your own project.",
     "intro": "The {n} sprints at the heart of the bootcamp. Each brief sets out the problem, your challenge, the goals, the scope, what to deliver and how the sprint runs day by day.",
     "chapters": {"Sprint Briefs": "Service design, a startup, a wicked problem and a project of your own."}},
    {"id": "ux", "out": "lectures", "index": "ux.html", "label": "UX Theory", "noun": "Lecture",
     "eyebrow": "UX Learning Resource", "h1": "UX Theory",
     "blurb": "The history, psychology and practice of user experience design.",
     "intro": "{n} lectures on the history, psychology and practice of UX, grouped by topic.",
     "chapters": {
         "Foundations": "Where UX comes from, what it is, and the people and roles behind it.",
         "Psychology": "How people perceive, decide and behave, and the laws and heuristics that follow.",
         "Process": "How design thinking works, from data and wicked problems to MVPs and wireframes.",
         "Business Case Studies": "Real products and businesses that got UX very right, or very wrong.",
         "Interface": "UI basics, and how people physically interact: gestures and haptics.",
     }},
    {"id": "methods", "out": "methods", "index": "methods.html", "label": "UX Methods", "noun": "Method",
     "eyebrow": "Sprint Toolkit", "h1": "UX Methods",
     "blurb": "Your bank of methods for different types of problems.",
     "intro": "Your bank of {n} methods for different types of problems. Pick and choose: there's nothing to complete here, and no sprint uses them all. Find the stage you're at, then the method that fits your problem. Each one opens with what it's for and how long it takes.",
     "chapters": {
         "Discovery": "Generative research: find out what the problem really is, and who has it.",
         "Define": "Turn research into a clear problem, a target user and a direction.",
         "Information Architecture": "Part of Define: structure the steps users take to reach their goal.",
         "Ideation": "Diverge on many ideas, decide on one, then design it from paper to high fidelity.",
         "Validation": "Test the prototype with real users and iterate on what you learn.",
         "Retrospective": "Reflect on the sprint and capture the lessons for your case study.",
         "AI Workflows": "Use AI across the sprint with you in charge: prompting, connecting tools, context and quality.",
     },
     "parent": {"Information Architecture": "Define"}},
    {"id": "ui", "out": "ui", "index": "ui.html", "label": "UI Theory", "noun": "Lecture",
     "eyebrow": "UI Learning Resource", "h1": "UI Theory",
     "blurb": "The theory behind good interfaces: colour, type, spacing, icons and systems.",
     "intro": "{n} lectures on the theory behind interfaces. For hands-on tutorials, see <a href=\"figma.html\">Figma</a>.",
     "chapters": {
         "UI Theory": "The concepts behind interfaces: colour, type, spacing, icons and systems.",
     }},
    {"id": "figma", "content": "ui", "out": "figma", "index": "figma.html", "label": "Figma", "noun": "Lesson",
     "eyebrow": "Hands-on Tutorials", "h1": "Figma",
     "blurb": "Step-by-step Figma tutorials, from your first frame to components and variables.",
     "intro": "{n} step-by-step Figma tutorials. Work through Figma Basics in order, then move on to Figma Advanced.",
     "chapters": {
         "Figma Basics": "Start here: frames, grids, nesting, Auto Layout, the 8 point grid and your first components.",
         "Figma Advanced": "Component properties and variables, the building blocks of a design system.",
     }},
    {"id": "exercises", "out": "exercises", "index": "exercises.html", "label": "Exercises", "noun": "Exercise",
     "eyebrow": "Practice", "h1": "Exercises",
     "blurb": "Briefs to practise in Figma, from one-session Daily UIs to multi-day projects.",
     "intro": "{n} briefs to practise in Figma, from one-session Daily UIs to multi-day projects.",
     "chapters": {
         "Daily UI": "Single-screen briefs for one session, rated for difficulty.",
         "Replica Challenges": "Copy real apps pixel for pixel to build fluency in Figma.",
         "UI Team Projects": "Multi-day team UI builds from a schema.",
         "AI Outputting": "Give the same brief to several AI tools, screenshot the results and judge the pros and cons.",
     }},
]
# Sections with progress tracking. Finishing every page of a sub-section earns its milestone badge; finishing every
# milestone (every page) earns the section's award; all five awards unlock the certificate. Sprints have no
# milestones: completing `need` of the four sprints wins their award, as two sprints are needed to pass. A page with sub-lessons
# counts as one item, complete only when the page and every sub-lesson are done.
PROGRESS = {
    "sprints": {"badge": "Sprints", "short": "SP", "colour": "#ff3d8b", "need": 2,
                "done": "You've completed two sprints, enough to pass. Keep going for all four!", "milestones": {}},
    "ux": {"badge": "UX Theory", "short": "UX", "colour": "#0072e3", "done": "You've finished every UX Theory lecture.",
           "milestones": {"Foundations": "🏛️", "Psychology": "🧠", "Process": "🔁", "Business Case Studies": "🔍", "Interface": "👆"}},
    "ui": {"badge": "UI Theory", "short": "UI", "colour": "#ff6100", "done": "You've finished every UI Theory lecture.",
           "milestones": {}},
    "figma": {"badge": "Figma", "short": "FG", "colour": "#ab54f7", "done": "You've finished every Figma lesson.",
              "milestones": {"Figma Basics": "🧱", "Figma Advanced": "🚀"}},
    "exercises": {"badge": "Exercises", "short": "EX", "colour": "#00aa3c", "done": "You've completed every exercise.",
                  "milestones": {"Daily UI": "✏️", "Replica Challenges": "🪞", "UI Team Projects": "🤝", "AI Outputting": "🤖"}},
}
CERTIFICATE = "UX/UI Design Bootcamp"


def badge_svg(track, size=96):
    """A section's award: a rosette with ribbons."""
    b = PROGRESS[track]
    return f"""<svg class="badge-art" viewBox="0 0 96 112" width="{size}" height="{round(size * 112 / 96)}" aria-hidden="true">
  <path d="M30 70 18 108l16-8 10 12 8-34z" fill="{b['colour']}" opacity=".75"/><path d="M66 70l12 38-16-8-10 12-8-34z" fill="{b['colour']}" opacity=".75"/>
  <circle cx="48" cy="46" r="40" fill="{b['colour']}"/><circle cx="48" cy="46" r="32" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="2" stroke-dasharray="3 4"/>
  <circle cx="48" cy="46" r="26" fill="#fff" fill-opacity=".16"/>
  <text x="48" y="54" text-anchor="middle" font-family="Bricolage Grotesque, sans-serif" font-weight="800" font-size="24" fill="#fff">{b['short']}</text>
</svg>"""


def milestone_svg(track, cat, size=56):
    """A milestone: a hexagon (like the logo) in the section's colour, with the sub-section's icon."""
    colour, icon = PROGRESS[track]["colour"], PROGRESS[track]["milestones"][cat]
    return f"""<svg class="badge-art milestone-art" viewBox="0 0 64 64" width="{size}" height="{size}" aria-hidden="true">
  <path d="M18 5h28l15 27-15 27H18L3 32z" fill="{colour}"/><path d="M3 32h58L46 59H18z" fill="#000" fill-opacity=".14"/>
  <path d="M21 11h22l12 21-12 21H21L9 32z" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="1.5"/>
  <text x="32" y="41" text-anchor="middle" font-size="24">{icon}</text>
</svg>"""


def certificate_svg(size=96):
    """The final award: a seal in the Cornerstones blues."""
    return f"""<svg class="badge-art cert-art" viewBox="0 0 96 112" width="{size}" height="{round(size * 112 / 96)}" aria-hidden="true">
  <path d="M30 70 18 108l16-8 10 12 8-34z" fill="#002b71"/><path d="M66 70l12 38-16-8-10 12-8-34z" fill="#002b71"/>
  <path d="M48 4l9 7 11-2 4 10 10 5-2 11 7 9-7 9 2 11-10 5-4 10-11-2-9 7-9-7-11 2-4-10-10-5 2-11-7-9 7-9-2-11 10-5 4-10 11 2z" fill="#0062ff"/>
  <circle cx="48" cy="46" r="27" fill="#004ecd"/><circle cx="48" cy="46" r="22" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="1.5"/>
  <path d="M37 47l8 8 15-17" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def progress_panel(track, compact=False):
    """Filled in by app.js from the student's saved progress."""
    b = PROGRESS[track]
    return f"""<div class="progress{' compact' if compact else ''}" data-track="{track}">
  <div class="progress-row"><span class="progress-label">Your progress</span><span class="progress-count">–</span></div>
  <div class="progress-bar" role="progressbar" aria-label="{b['badge']} progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span></span></div>
  {'' if compact else f'<div class="progress-badge">{badge_svg(track, 44)}<span class="progress-badge-text">Finish them all to earn the {b["badge"]} award.</span></div>'}
  {'' if compact or not b["milestones"] else '<ul class="milestones">' + "".join(milestone_item(track, c, 34) for c in b["milestones"]) + '</ul>'}
</div>"""


def milestone_item(track, cat, size):
    """A milestone badge with its name and count, linking to just that sub-section; app.js marks it earned."""
    return (f'<li class="milestone" data-milestone="{track}:{esc(cat)}"><a class="milestone-link" '
            f'href="{TRACK[track]["index"]}#category={quote(cat)}" title="Show the {esc(cat)} pages">{milestone_svg(track, cat, size)}'
            f'<span class="milestone-name">{esc(cat)}</span><span class="milestone-state">–</span></a></li>')


# The suggested route on the home page: (step, why, section id, page slug).
ROUTE = [
    ("Understand UX", "Start with the foundations: what UX really is and where it comes from.", "ux", "what-is-ux-design"),
    ("Learn Figma", "Work through Figma Basics in order, then Figma Advanced.", "figma", "choose-your-frame"),
    ("Practise every day", "Pick a Daily UI brief each session, starting with Sidebar.", "exercises", "sidebar"),
    ("Run a sprint", "Pick from the method bank whatever your sprint's problem needs. Many teams start with a Lean UX Canvas.", "methods", "lean-ux-canvas"),
    ("Build something bigger", "Finish with a replica challenge and the Stage Play team project.", "exercises", "glovo-replica-challenge"),
]
TRACK = {t["id"]: t for t in TRACKS}

# Order and categories for tracks fed by more than one source, or sharing content with another track
# ("content" in TRACKS). Every page in a content source must be listed by exactly one track.
ORDER = {
    "ux": {
        "Foundations": ["what-is-ux-design", "design-origins", "the-father-of-ux", "key-figures", "key-roles"],
        "Psychology": ["design-psychology", "mental-models", "bias", "the-bias-of-beauty", "laws-of-ux", "neilson-heuristics"],
        "Process": ["starting-point", "what-is-design-thinking", "wicked-problem", "data", "target-mvp", "stages-of-wireframes"],
        "Business Case Studies": ["bad-user-experience", "the-death-of-kodak", "a-case-of-genius"],
        "Interface": ["gestures", "haptics"],
    },
    "ui": {
        "UI Theory": ["colour-values", "atomic-design-methodology", "file-types", "spacing-grids", "typeface",
                      "style-guides", "icons", "paper-wireframes"],
    },
    "methods": {
        "Discovery": ["lean-ux-canvas", "long-term-goal", "initial-problem-statement", "solution-hypothesis", "research-goal", "research-questions", "desk-research", "site-visit", "user-survey", "user-interview", "discovery-summary"],
        "Define": ["affinity-mapping", "data-synthesis-with-ai", "problem-statement", "user-persona",
                   "competitive-analysis", "business-model-canvas", "wicked-problem-mapping", "how-might-we",
                   "pick-a-target", "user-journey-map", "service-design-blueprint", "dvf-analysis",
                   "converge-diverge", "vote"],
        "Information Architecture": ["task-flows", "sitemap"],
        "Ideation": ["crazy-8s", "crazy-8s-with-ai", "solution-sketch", "mood-board", "mood-board-with-ai",
                     "brand-pack", "style-guide", "paper-wireframes", "mid-fi", "hi-fi"],
        "Validation": ["usability-test", "create-your-script", "facilitator-format",
                       "limited-intervention-technique", "notetaker-format", "ab-test", "design-iteration"],
        "Retrospective": ["sprint-retrospective", "cataloguing-artifacts", "writing-your-case-study", "building-your-web-portfolio"],
        "AI Workflows": ["ai-guidelines", "mcp", "skills-in-claude", "connectors-in-claude", "avoiding-ai-slop", "token-economics"],
    },
    "sprints": {
        "Sprint Briefs": ["honest-greens", "locker-room", "wicked-project", "personal-project"],
    },
    "figma": {
        "Figma Basics": ["choose-your-frame", "starting-in-figma", "beginners-guide-to-grids",
                         "beginners-guide-to-nesting", "beginners-guide-auto-layout",
                         "beginners-guide-to-8-point-grid-system", "beginners-guide-to-components"],
        "Figma Advanced": ["navbar", "dynamic-buttons-part-one",
                           "dynamic-buttons-part-deux", "color-variables", "number-variables",
                           "string-variables", "variable-modes"],
    },
    "exercises": {
        "Daily UI": ["sidebar", "friends-list", "new-notification", "bottom-sheet", "sign-in", "cc-checkout",
                     "video-player", "choose-a-movie", "music-player", "home-monitor-dash", "user-profile-page",
                     "make-an-ai-interface", "product-card"],
        "Replica Challenges": ["glovo-replica-challenge", "youtube-challenge", "airbnb-replica-challenge", "balenciaga-replica-challenge"],
        "UI Team Projects": ["stage-play"],
        "AI Outputting": ["ux-x-ai"],
    },
}

# Cross-links shown at the end of a page as "Related". Each pair is linked both ways.
RELATED = [
    ("figma/navbar", "figma/dynamic-buttons-part-one"),
    ("figma/dynamic-buttons-part-one", "figma/dynamic-buttons-part-deux"),
    ("figma/color-variables", "ui/colour-values"),
    ("figma/color-variables", "figma/number-variables"),
    ("figma/number-variables", "figma/string-variables"),
    ("figma/string-variables", "figma/variable-modes"),
    ("figma/number-variables", "figma/beginners-guide-to-8-point-grid-system"),
    ("exercises/stage-play", "figma/beginners-guide-to-8-point-grid-system"),
    ("exercises/stage-play", "figma/beginners-guide-to-nesting"),
    ("exercises/stage-play", "figma/beginners-guide-auto-layout"),
    ("exercises/stage-play", "figma/beginners-guide-to-components"),
    ("exercises/stage-play", "figma/dynamic-buttons-part-one"),
    ("ui/spacing-grids", "figma/beginners-guide-to-grids"),
    ("ui/spacing-grids", "figma/beginners-guide-to-8-point-grid-system"),
    ("ui/atomic-design-methodology", "figma/beginners-guide-to-components"),
    ("ui/paper-wireframes", "ux/stages-of-wireframes"),
    ("exercises/glovo-replica-challenge", "figma/beginners-guide-to-nesting"),
    ("exercises/glovo-replica-challenge", "figma/beginners-guide-auto-layout"),
    ("exercises/glovo-replica-challenge", "figma/beginners-guide-to-components"),
    ("exercises/youtube-challenge", "figma/beginners-guide-to-nesting"),
    ("exercises/youtube-challenge", "figma/beginners-guide-auto-layout"),
    ("exercises/youtube-challenge", "figma/beginners-guide-to-components"),
    ("exercises/ux-x-ai", "exercises/make-an-ai-interface"),
    ("exercises/glovo-replica-challenge", "exercises/youtube-challenge"),
    ("exercises/airbnb-replica-challenge", "figma/beginners-guide-to-nesting"),
    ("exercises/airbnb-replica-challenge", "figma/beginners-guide-auto-layout"),
    ("exercises/airbnb-replica-challenge", "figma/beginners-guide-to-components"),
    ("exercises/airbnb-replica-challenge", "exercises/glovo-replica-challenge"),
    ("exercises/airbnb-replica-challenge", "exercises/youtube-challenge"),
    ("exercises/balenciaga-replica-challenge", "exercises/airbnb-replica-challenge"),
    ("exercises/balenciaga-replica-challenge", "figma/beginners-guide-auto-layout"),
    ("exercises/balenciaga-replica-challenge", "figma/beginners-guide-to-components"),
    ("methods/pick-a-target", "ux/target-mvp"),
    ("methods/paper-wireframes", "ui/paper-wireframes"),
    ("methods/style-guide", "ui/style-guides"),
    ("methods/style-guide", "figma/dynamic-buttons-part-one"),
    ("methods/mid-fi", "ux/stages-of-wireframes"),
    ("methods/paper-wireframes", "methods/mid-fi"),
    ("methods/mid-fi", "methods/hi-fi"),
    ("methods/site-visit", "methods/research-questions"),
    ("methods/desk-research", "methods/site-visit"),
    ("methods/desk-research", "methods/wicked-problem-mapping"),
    ("methods/affinity-mapping", "methods/data-synthesis-with-ai"),
    ("methods/affinity-mapping", "methods/discovery-summary"),
    ("methods/service-design-blueprint", "methods/user-journey-map"),
    ("methods/business-model-canvas", "methods/lean-ux-canvas"),
    ("methods/business-model-canvas", "methods/dvf-analysis"),
    ("methods/wicked-problem-mapping", "ux/wicked-problem"),
    ("methods/wicked-problem-mapping", "methods/problem-statement"),
    ("methods/dvf-analysis", "methods/vote"),
    ("methods/sitemap", "methods/task-flows"),
    ("methods/mood-board", "methods/mood-board-with-ai"),
    ("methods/mood-board", "methods/brand-pack"),
    ("methods/brand-pack", "methods/style-guide"),
    ("methods/ab-test", "methods/usability-test"),
    ("methods/cataloguing-artifacts", "methods/writing-your-case-study"),
    ("methods/writing-your-case-study", "methods/building-your-web-portfolio"),
    ("methods/sitemap", "methods/building-your-web-portfolio"),
    ("methods/sprint-retrospective", "methods/writing-your-case-study"),
    ("methods/hi-fi", "ux/stages-of-wireframes"),
    ("methods/research-goal", "methods/research-questions"),
    ("methods/crazy-8s", "methods/crazy-8s-with-ai"),
    ("methods/mood-board", "methods/style-guide"),
    ("methods/user-journey-map", "methods/task-flows"),
    ("methods/usability-test", "methods/design-iteration"),
    ("methods/usability-test", "methods/facilitator-format"),
]

# Hand-written one-line summaries, keyed "section/slug" (edit content/summaries.json).
SUMMARIES = {k: v for k, v in json.loads((CONTENT / "summaries.json").read_text(encoding="utf-8")).items()
             if not k.startswith("_")}

# A line icon for each Figma lesson (24px grid, 2px stroke, currentColor), shown on the Figma cards.
FIGMA_ICONS = {
    "choose-your-frame": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M10.5 18.5h3"/><path d="M3 6V3h3M21 6V3h-3M3 18v3h3M21 18v3h-3"/>',
    "starting-in-figma": '<path d="M12 20l7-7-3-3-7 7z"/><path d="M16 10l-1.5-5.5L4 2l2.5 10.5L12 14"/><path d="M4 2l6.5 6.5"/><circle cx="11.5" cy="9.5" r="1.5"/>',
    "beginners-guide-to-grids": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18M15 3v18"/>',
    "beginners-guide-to-nesting": '<rect x="3" y="3" width="18" height="18" rx="2.5"/><rect x="7.5" y="7.5" width="9" height="9" rx="1.5"/>',
    "beginners-guide-auto-layout": '<rect x="4" y="3" width="16" height="4.5" rx="1.5"/><rect x="4" y="16.5" width="16" height="4.5" rx="1.5"/><path d="M12 9.5v5M10 11l2-1.5 2 1.5M10 13l2 1.5 2-1.5"/>',
    "beginners-guide-to-8-point-grid-system": '<circle cx="5" cy="5" r="1.3"/><circle cx="12" cy="5" r="1.3"/><circle cx="19" cy="5" r="1.3"/><circle cx="5" cy="12" r="1.3"/><circle cx="12" cy="12" r="1.3"/><circle cx="19" cy="12" r="1.3"/><circle cx="5" cy="19" r="1.3"/><circle cx="12" cy="19" r="1.3"/><circle cx="19" cy="19" r="1.3"/>',
    "beginners-guide-to-components": '<path d="M12 2.5l3 3-3 3-3-3z"/><path d="M12 15.5l3 3-3 3-3-3z"/><path d="M5.5 9l3 3-3 3-3-3z"/><path d="M18.5 9l3 3-3 3-3-3z"/>',
    "navbar": '<rect x="3" y="3" width="18" height="18" rx="2.5"/><path d="M3 16h18"/><circle cx="7.5" cy="18.5" r=".8"/><circle cx="12" cy="18.5" r=".8"/><circle cx="16.5" cy="18.5" r=".8"/>',
    "dynamic-buttons-part-one": '<rect x="2.5" y="6" width="16" height="7" rx="3.5"/><path d="M14 14l1.5 7 2-3 3 2.5 1-1.5-3-2.5 3-1.5z"/>',
    "dynamic-buttons-part-deux": '<rect x="3" y="3" width="18" height="5" rx="2.5"/><rect x="3" y="9.5" width="18" height="5" rx="2.5"/><rect x="3" y="16" width="18" height="5" rx="2.5"/>',
    "color-variables": '<path d="M12 3a9 9 0 1 0 0 18c1.5 0 2-1 2-2 0-1.5-1.5-2-1.5-3.5S13.5 13 15 13h2.5c2 0 3.5-1.5 3.5-3.5C21 6 17 3 12 3z"/><circle cx="7.5" cy="11.5" r="1.2"/><circle cx="10" cy="7.5" r="1.2"/><circle cx="15" cy="7.5" r="1.2"/>',
    "number-variables": '<rect x="2.5" y="8" width="19" height="8" rx="1.5"/><path d="M6.5 8v3M10 8v2M13.5 8v3M17 8v2"/>',
    "string-variables": '<path d="M4 7V5h11v2M9.5 5v14M7.5 19h4"/><path d="M15 12h6M18 12v7M16.5 19h3"/>',
    "variable-modes": '<rect x="2.5" y="7" width="19" height="10" rx="5"/><circle cx="16.5" cy="12" r="3.2"/><path d="M6.5 10.5v3M5 12h3"/>',
}


# Row icons for the other sections (Lucide, ISC licence): content/icons.json, by section and page slug.
TRACK_ICONS = {k: v for k, v in json.loads((CONTENT / "icons.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}


def row_icon(track, slug, size=24):
    """The icon tile shown in place of a page's number in a section's list, or "" if the page has none."""
    if track == "figma":
        return figma_icon(slug, size)
    icon = TRACK_ICONS.get(track, {}).get(slug)
    if not icon:
        return ""
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icon["svg"]}</svg>')


def figma_icon(slug, size=24):
    paths = FIGMA_ICONS.get(slug)
    if not paths:
        return ""
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')


# Quick definitions for the Definition box on UX method pages (edit content/definitions.json).
DEFINITIONS = {k: v for k, v in json.loads((CONTENT / "definitions.json").read_text(encoding="utf-8")).items()
               if not k.startswith("_")}

# Method sections shown in the quick-reference card or folded away, matched on heading text.
METHOD_DROP = ("stage",)                    # repeats the chapter, which the page already shows
# Media (the videos) is never folded: watching them matters.
METHOD_FOLD = ("extra notes", "resources", "tips", "checklist", "summary", "template", "ai assist")

YOUTUBE_RE = re.compile(
    r'<p><a href="(https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/)|youtu\.be/)([\w-]{11})[^"]*)">[^<]*</a></p>')
FIGMA_RE = re.compile(r'<p><a href="(https://(?:www\.figma\.com/embed\?|embed\.figma\.com/)[^"]+)">[^<]*</a></p>')
LECTURE_LINK_RE = re.compile(r'<p><a href="([a-z0-9-]+)\.html">(.*?)</a></p>')
IMG_P_RE = re.compile(r'<p>(<img [^>]+>)</p>')
IMG_RE = re.compile(r'<img alt="([^"]*)" src="([^"]+)"\s*/?>')
H_RE = re.compile(r'<h([1-3]) id="([^"]+)">(.*?)</h\1>')
TAG_RE = re.compile(r"<[^>]+>")
ASIDE_RE = re.compile(r"<aside>\s*(.*?)\s*</aside>", re.S)
# Difficulty stars: a "**Difficulty:** ⭐️⭐️⭐️" line (Daily UI template) or the older "## Difficulty Level ⭐️⭐️" heading.
DIFFICULTY_RE = re.compile(r"^(?:#+\s*Difficulty Level|\*\*Difficulty:\*\*)\s*(.*)$", re.M)

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


ICON_TRACKER = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6l2 2 3-3M4 13l2 2 3-3M12 7h8M12 14h8M12 20h8M5 20h2"/></svg>'
ICON_LOGOUT = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 4h4v16h-4M10 8l-4 4 4 4M6 12h11"/></svg>'


def gate(prefix):
    """Inline head script: send visitors who haven't signed in to the login page, remembering where they were."""
    return (f"<script>try{{if(localStorage.getItem('cs-auth')!=='{LOGIN_HASH}')"
            f"location.replace('{prefix}login.html?next='+encodeURIComponent(location.pathname+location.search+location.hash))}}"
            f"catch(e){{}}</script>")


def course_chips(prefix):
    """One small coloured tab per tracked section; app.js fills in the counts."""
    return "".join(
        f'<a class="cp-chip t-{k}" data-chip="{k}" href="{prefix}{TRACK[k]["index"]}" title="{esc(b["badge"])}">'
        f'<span class="cp-fill"></span><span class="cp-name">{esc(TRACK[k]["label"])}</span><b class="cp-count">0/0</b></a>'
        for k, b in PROGRESS.items())


def page(title, description, body, depth, active):
    prefix = "../" * depth
    links = "".join(
        f'<a href="{prefix}{t["index"]}"{" aria-current=page" if t["id"] == active else ""}>{t["label"]}</a>' for t in TRACKS)
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/svg+xml" href="{FAVICON}">
{gate(prefix)}
<script>try{{var t=localStorage.getItem('cs-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Figtree:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="{prefix}assets/style.css?v={ASSET_V}">
<link rel="stylesheet" href="{prefix}assets/theme.css?v={ASSET_V}">
</head>
<body class="t-{active}">
<header class="nav">
  <div class="nav-inner">
    <a class="brand logo" href="{prefix}index.html" aria-label="Cornerstones, UX/UI Design at {SCHOOL}, home">{LOGO}
    </a>
    <nav class="nav-links">{links}<a href="{prefix}timetable.html"{" aria-current=page" if active == "timetable" else ""}>Timetable</a></nav>
    <button class="icon-btn" id="tracker-open" type="button" aria-label="Open your progress tracker" aria-expanded="false" aria-controls="tracker">{ICON_TRACKER}</button>
    <button class="icon-btn" id="theme-toggle" type="button" aria-label="Toggle colour theme">{ICON_SUN}</button>
    <button class="logout-btn" id="logout" type="button" aria-label="Log out" data-login="{prefix}login.html">{ICON_LOGOUT}<span>Log out</span></button>
  </div>
  <div class="course-bar" role="progressbar" aria-label="Course progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span></span></div>
  <div class="course-row"><button type="button" class="course-label" id="course-open" aria-controls="tracker" aria-label="Open your progress tracker">Course progress · <b id="course-pct">0%</b> complete</button>
    <nav class="course-chips" aria-label="Progress by section">{course_chips(prefix)}</nav>
    <a class="mini-badges" id="mini-badges" href="{prefix}index.html#badges-title" aria-label="Your badges"></a></div>
</header>
{body}
<footer class="foot"><div class="foot-inner"><span>{SITE} · {TAGLINE}</span><span class="mono">Notes by Chris Kelly</span></div></footer>
<div class="celebrate" id="celebrate" hidden role="dialog" aria-modal="true" aria-labelledby="celebrate-title">
  <div class="celebrate-card"><div class="celebrate-badge"></div><div class="eyebrow">Badge unlocked</div>
  <h2 id="celebrate-title"></h2><p class="celebrate-text"></p>
  <div class="celebrate-actions"><a class="login-submit celebrate-link" href="{prefix}certificate.html" hidden>See your certificate</a>
  <button type="button" class="login-submit" id="celebrate-close">Nice!</button></div></div>
</div>
<script src="{prefix}assets/progress-data.js?v={ASSET_V}"></script>
<script src="{prefix}assets/app.js?v={ASSET_V}"></script>
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
    # Attachments (zip, pdf…) live next to the page's markdown, not next to the HTML.
    body = re.sub(r'href="(?![a-z]+:|#|\.\./)([^"/]+\.(?!html")[a-z0-9]+)"', rf'href="../content/{track}/{slug}/\1" download', body)
    body = IMG_P_RE.sub(r'<figure class="media">\1</figure>', body)
    # A stitched, scrolling screenshot (name.tall.webp) scrolls inside a phone-sized frame.
    body = re.sub(r'<figure class="media">(<img [^>]*src="[^"]+\.tall\.[a-z]+"[^>]*>)</figure>',
                  r'<figure class="media tall"><div class="tall-frame" tabindex="0">\1</div>'
                  r'<figcaption>Scroll inside the screen to see all of it</figcaption></figure>', body)
    body = YOUTUBE_RE.sub(
        lambda m: f'<figure class="video"><iframe src="https://www.youtube-nocookie.com/embed/{m.group(2)}" title="YouTube video" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe></figure>',
        body)

    def figma(m):
        embed = html.unescape(m.group(1))
        u = urlparse(embed)
        if u.netloc == "embed.figma.com":  # new style: the file path is in the URL itself
            file_url = f"https://www.figma.com{u.path}"
            embed = re.sub(r"embed-host=[^&]+", "embed-host=share", embed)
        else:
            file_url = parse_qs(u.query).get("url", [""])[0]
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
    # Two or more images in a row become a gallery grid (click any one to see it full size).
    body = re.sub(r'(?:<figure class="media"><img [^>]+></figure>\s*){2,}',
                  lambda m: f'<div class="gallery">{m.group(0)}</div>\n', body)
    body = re.sub(r"(<hr\s*/?>\s*)+$", "", body.strip())
    body = re.sub(r"<p>\s*(\*\*\*\*)?\s*</p>", "", body)
    # Notion section headings start with an emoji ("🪜 Stage"); give it room, and leave it out of the contents list.
    body = re.sub(r'(<h[23] id="[^"]+">)([^\w<\s(]+)\s*', r'\1<span class="h-icon">\2</span>', body)
    toc = [(lvl, hid, re.sub(r"^[^\w(]+", "", plain(txt))) for lvl, hid, txt in H_RE.findall(body)]
    toc = [x for x in toc if x[2]]
    return body, toc


def md_plain(s):
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return re.sub(r"[*_`]|<[^>]+>", "", s).strip()


def method_goal(text):
    """The 'Goal / Learning outcome' section of a method, as up to four short points."""
    m = re.search(r"^#+ [^\n]*(?:Goal\s*/|Learning [Oo]utcome)[^\n]*\n(.*?)(?=^#|\Z)", text, re.M | re.S)
    if not m:
        return []
    block = m.group(1)
    items = [md_plain(i) for i in re.findall(r"^\s*(?:[-*]|\d+\.)\s+(.+)$", block, re.M)]
    if not items:
        para = md_plain(" ".join(block.split()))
        items = [para] if para else []
    # "By the end of this activity, students will have …" is the same on every page; keep what follows.
    lead = (r"^(?:By the end of this (?:activity|exercise),?\s*)?(?:students\s+)?(?:you\s+)?"
            r"(?:should have,?\s*)?(?:students\s+)?(?:will\s+)?(?:have\s+|be able to\s+)?")
    items = [re.sub(lead, "", i, flags=re.I) for i in items]
    return [i[:1].upper() + i[1:] for i in items if i][:4]


def fold_sections(body, drop, fold, remove=()):
    """Split at h2s: trim the heading and first paragraph of 'drop' sections, delete 'remove' sections,
    and fold 'fold' sections into <details>."""
    out = []
    for part in re.split(r'(?=<h2 id=")', body):
        m = re.match(r'<h2 id="[^"]+">(.*?)</h2>\s*', part, re.S)
        name = re.sub(r"^[^\w(]+", "", plain(m.group(1))) if m else ""
        key = name.lower()
        if m and remove and key.startswith(remove):
            continue
        if m and key.startswith(drop):
            rest = re.sub(r"^<p>.*?</p>\s*", "", part[m.end():], count=1, flags=re.S)
            out.append(rest)
        elif m and any(key.startswith(f) for f in fold) and part[m.end():].strip():
            out.append(f'<details class="more"><summary>{esc(name)}</summary>\n{part[m.end():]}</details>\n')
        else:
            out.append(part)
    return "".join(out)


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
    quote = re.search(r"^> *(\S.{39,})$", text, re.M)
    if quote:
        b = re.sub(r"[*_`]", "", quote.group(1)).strip()
        return b if len(b) <= 180 else b[:177].rsplit(" ", 1)[0] + "…"
    return ""


def load():
    """Load every track and compute per-page stats."""
    data = {}
    for t in TRACKS:
        d = {"categories": [], "lectures": [], "subpages": []}
        src = t.get("content", t["id"])
        for f in [CONTENT / f"{src}.json"] + sorted(CONTENT.glob(f"{src}.*.json")):
            part = json.loads(f.read_text(encoding="utf-8"))
            d["categories"] += [c for c in part["categories"] if c not in d["categories"]]
            d["lectures"] += part["lectures"]
            d["subpages"] += part["subpages"]
        if t["id"] in ORDER:
            by = {l["slug"]: l for l in d["lectures"]}
            listed = [s for slugs in ORDER[t["id"]].values() for s in slugs]
            claimed = {s for x in TRACKS if x.get("content", x["id"]) == src and x["id"] in ORDER
                       for slugs in ORDER[x["id"]].values() for s in slugs}
            missing = set(by) - claimed
            if missing or set(listed) - set(by):
                raise SystemExit(f"ORDER[{t['id']!r}] is out of date. Not listed: {sorted(missing)}; "
                                 f"no such page: {sorted(set(listed) - set(by))}")
            d["categories"] = list(ORDER[t["id"]])
            d["lectures"] = []
            for cat, slugs in ORDER[t["id"]].items():
                for slug in slugs:
                    by[slug]["category"] = cat
                    d["lectures"].append(by[slug])
            for i, l in enumerate(d["lectures"], 1):
                l["number"] = i
            # Sub-pages go with whichever track has their parent.
            d["subpages"] = [sp for sp in d["subpages"] if sp["parent"] in set(listed)]
        elif t.get("chapters"):
            d["lectures"].sort(key=lambda l: d["categories"].index(l["category"]))
            for i, l in enumerate(d["lectures"], 1):
                l["number"] = i
        every = d["lectures"] + d["subpages"]
        by_slug = {p["slug"]: p for p in every}
        for p in every:
            p["track"] = t["id"]
            text = (CONTENT / src / p["slug"] / "index.md").read_text(encoding="utf-8")
            words = len(re.findall(r"\w+", re.sub(r"!\[[^\]]*\]\([^)]*\)|\([^)]*\)", "", text)))
            summary = SUMMARIES.get(f'{t["id"]}/{p["slug"]}')
            quote = re.search(r"^> *(\S[^\n]{39,})", text, re.M)  # sub-pages (e.g. typefaces) summarised by a one-line quote
            p["description"] = summary or (re.sub(r"[*_`]", "", quote.group(1)).strip() if quote and p["parent"] else describe(text))
            p["lede"] = not p["description"] or bool(summary)  # only show a lede when it won't repeat the first paragraph
            p["minutes"] = max(1, round(words / 200))
            p["images"] = len(re.findall(r"!\[", text))
            stars = DIFFICULTY_RE.search(text)
            p["difficulty"] = stars.group(1).count("⭐") if stars else 0
            # "Estimated Duration" / "Duration" section: first line after the heading, e.g. "30–40 minutes".
            dur = re.search(r"^#+ .*Duration\**\s*\n+\s*(?:-\s*)?([^\n]+)", text, re.M)
            p["duration"] = re.sub(r"\s*\(.*$", "", dur.group(1)).strip(" ~*") if dur else ""
            p["duration"] = re.sub(r"\s*(?:minutes?|mins?)\b\.?", " min", p["duration"], flags=re.I)
            p["duration"] = re.sub(r"\s*hours?\b", " hr", p["duration"], flags=re.I)
            if dur and ":" in dur.group(1):  # broken into stages ("Preparation: 30 min, Each test: …") – see the page
                p["duration"] = "In stages"
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
        body, toc = render_markdown(t.get("content", t["id"]), p["slug"], p["text"], by_slug)
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
        if p.get("duration"):
            meta.append(f'Takes {esc(p["duration"].lower() if p["duration"] == "In stages" else p["duration"])}')
        meta.append(f'{ICON_CLOCK}{p["minutes"]} min read')
        if p["children"]:
            meta.append(f'{len(p["children"])} sub-lessons')

        quick = ""
        if t["id"] == "methods":
            # The time is in the card, so a plain duration section is removed (staged ones stay, for the breakdown).
            body = fold_sections(body, METHOD_DROP, METHOD_FOLD,
                                 remove=("estimated duration", "duration") if p["duration"] not in ("", "In stages") else ())
            toc = [x for x in toc if f'id="{x[1]}"' in body and not re.search(rf'<details class="more">(?:(?!</details>).)*id="{x[1]}"', body, re.S)]
            goal = method_goal(p["text"])
            rows_q = [("When", f'{esc(p["category"])}: {esc(t["chapters"].get(p["category"], ""))}')]
            if p["duration"]:
                rows_q.append(("Time", esc(p["duration"].lower() if p["duration"] == "In stages" else p["duration"])))
            if goal:
                rows_q.append(("Goal", "<ul>" + "".join(f"<li>{esc(g)}</li>" for g in goal) + "</ul>"
                               if len(goal) > 1 else esc(goal[0])))
            quick = ('<div class="quickref">' + "".join(f'<div class="qr-row"><div class="qr-label">{a}</div><div class="qr-value">{b}</div></div>'
                                                        for a, b in rows_q) + "</div>\n")
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

        toc_mobile = (f'<details class="toc-mobile"><summary>On this page</summary><ol class="toc">{toc_html}</ol></details>\n'
                      if toc_html else "")
        defn = DEFINITIONS.get(f'{t["id"]}/{p["slug"]}')
        def_html = (f'<div class="definition"><div class="rail-label">Definition</div>'
                    f'<p><b>{esc(defn["q"])}</b> {esc(defn["a"])}</p></div>') if defn else ""
        body = (def_html.replace('class="definition"', 'class="definition definition-mobile"') if defn else "") + quick + toc_mobile + body
        if t["id"] in PROGRESS:
            noun_page = "exercise" if t["id"] == "exercises" else ("part" if parent else "lecture")
            parts = (f'<span class="complete-parts">This lecture has {len(p["children"])} parts. It counts as complete once '
                     f'you\'ve finished this page and all {len(p["children"])} parts: <b data-parts>0</b> of {len(p["children"])} done.</span>'
                     if p["children"] else "")
            body += f"""
<section class="complete" data-key="{t['id']}/{p['slug']}">
  <div class="complete-text"><b>Finished this {noun_page}?</b>{parts}</div>
  <button type="button" class="complete-btn" data-complete="{t['id']}/{p['slug']}" aria-pressed="false"><span class="off">Mark as complete</span><span class="on">✓ Completed</span></button>
</section>"""

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

        head_btn = (f'<button type="button" class="complete-btn head-complete" data-complete="{t["id"]}/{p["slug"]}" aria-pressed="false">'
                    '<span class="off">Mark as complete</span><span class="on">✓ Completed</span></button>') if t["id"] in PROGRESS else ""
        body_html = f"""
<main class="lecture track-{t['id']}" data-key="{t['id']}/{p['slug']}">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">{' <span class="sep">/</span> '.join(crumbs)}</nav>
    <header class="lecture-head">
      <div class="eyebrow">{esc(eyebrow)}</div>
      <div class="title-row"><h1>{esc(p['title'])}</h1>{head_btn}</div>
      {f'<p class="lede">{esc(p["description"])}</p>' if p["lede"] and p["description"] else ''}
      <div class="meta">{''.join(f'<span>{m}</span>' for m in meta)}</div>
    </header>
    <div class="lecture-grid{' no-rail' if not rail else ''}">
      {f'<aside class="rail"><div class="rail-sticky">{def_html}<div class="rail-box">{rail}</div></div></aside>' if rail else ''}
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
    parent_of = t.get("parent", {})
    chapters = t.get("chapters", {})
    for c, parent in parent_of.items():
        counts[parent] += counts[c]
    cat_links = "".join(
        f'<li{" class=sub" if c in parent_of else ""}><button type="button" data-cat="{esc(c)}"><span>{esc(c)}</span><span class="count">{counts[c]}</span></button></li>'
        for c in cats)
    is_ex = t["id"] == "exercises"
    rows = []
    for l in lectures:
        cat = l["category"]
        parent_attr = f' data-parent="{esc(parent_of[cat])}"' if cat in parent_of else ""
        if chapters and (not rows or l is next(x for x in lectures if x["category"] == cat)):
            name = f'{esc(parent_of[cat])} <span class="sep">›</span> {esc(cat)}' if cat in parent_of else esc(cat)
            rows.append(f'<li class="chapter" data-cat="{esc(cat)}"{parent_attr}><h2 class="chapter-name">{name}</h2>'
                        f'<p class="chapter-blurb">{esc(chapters.get(cat, ""))}</p></li>')
        subs = ""
        if l["children"]:
            subs = '<div class="row-subs">' + "".join(
                f'<a href="{t["out"]}/{s}.html">{esc(short(by_slug[s]["title"]))}</a>' for s in l["children"]) + "</div>"
        search = " ".join([l["title"], l["category"], l["description"]] + [by_slug[s]["title"] for s in l["children"]]).lower()
        if t["id"] == "methods":
            stats = f'<span>{ICON_CLOCK}{esc(l["duration"])}</span>' if l["duration"] else ""
        elif is_ex:
            stats = f'<span>{meter(l["difficulty"]) if l["difficulty"] else "<span class=tag>Project</span>"}</span>'
        else:
            stats = ""
        card_btn = ""
        if t["id"] in PROGRESS:  # Methods are a reference bank, so they have no completion
            parts = " ".join(f"{t['id']}/{s}" for s in l["children"])
            card_btn = (f'\n    <button type="button" class="complete-btn card-complete" data-complete="{t["id"]}/{l["slug"]}"'
                        + (f' data-with="{parts}"' if parts else "") + ' aria-pressed="false">'
                        '<span class="off">Mark as complete</span><span class="on">✓ Completed</span></button>')
        rows.append(f"""<li class="row{' no-stats' if not stats else ''}" data-key="{t['id']}/{l['slug']}" data-cat="{esc(l['category'])}"{parent_attr} data-search="{esc(search)}">
  {f'<span class="row-icon" title="{t["noun"]} {l["number"]}">{row_icon(t["id"], l["slug"])}</span>' if row_icon(t["id"], l["slug"]) else f'<span class="row-num">{l["number"]}</span>'}
  <div class="row-body">
    <div class="row-head"><a class="row-title" href="{t['out']}/{l['slug']}.html">{esc(l['title'])}</a>{f'<span class="pill" data-parts-of="{len(l["children"])}">{len(l["children"])} parts</span>' if l["children"] else ''}<span class="row-done" aria-label="Completed">✓ Done</span></div>
    <p class="row-desc">{esc(l['description'])}</p>
    {subs}{card_btn}
  </div>
  {f'<div class="row-stats">{stats}</div>' if stats else ''}
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
        side_stat = ""
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
    {progress_panel(t['id']) if t['id'] in PROGRESS else ''}
    <div class="layout">
      <aside class="sidebar">
        <div class="side-label">Category</div>
        <ul class="cats">
          {cat_links}
          <li class="cat-all"><button type="button" data-cat="" aria-pressed="true"><span>All {noun}s</span><span class="count">{len(lectures)}</span></button></li>
        </ul>
        {side_stat}
      </aside>
      <section class="listing">
        <div class="toolbar">
          <label class="search"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q" type="search" placeholder="Search {noun}s…" autocomplete="off"></label>
          <span class="showing" id="showing">Showing {len(lectures)} of {len(lectures)}</span>
          <div class="view-toggle" role="group" aria-label="Layout">
            <button type="button" data-view="list" aria-pressed="true" aria-label="List view"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button>
            <button type="button" data-view="grid" aria-pressed="false" aria-label="Grid view"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="4" width="6" height="6"/><rect x="14" y="4" width="6" height="6"/><rect x="4" y="14" width="6" height="6"/><rect x="14" y="14" width="6" height="6"/></svg></button>
          </div>
        </div>
        {f'<div class="list-head"><span></span><span></span><span class="right">{"Difficulty" if is_ex else "Time"}</span></div>' if t["id"] in ("methods", "exercises") else ""}
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


# The method bank on the home page: the kind of problem a student has, and a few methods to start from.
METHOD_BANK = [
    ("Discovery", "I don't understand the problem, or the people who have it, yet.",
     ["site-visit", "desk-research", "user-interview", "user-survey"]),
    ("Define", "I have lots of research and need to make sense of it.",
     ["affinity-mapping", "problem-statement", "user-persona", "wicked-problem-mapping"]),
    ("Information Architecture", "I need to organise pages, content or the steps of a task.",
     ["task-flows", "sitemap"]),
    ("Ideation", "I need ideas, a visual direction or something to show.",
     ["crazy-8s", "mood-board", "brand-pack", "mid-fi"]),
    ("Validation", "I need to know whether my design actually works.",
     ["usability-test", "ab-test", "design-iteration"]),
    ("Retrospective", "I need to look back and tell the story of my project.",
     ["sprint-retrospective", "cataloguing-artifacts", "writing-your-case-study"]),
    ("AI Workflows", "I want AI to help, without it taking over or making my work generic.",
     ["ai-guidelines", "avoiding-ai-slop", "skills-in-claude", "token-economics"]),
]


def method_bank(data):
    d = data["methods"]
    n = {c: sum(1 for l in d["lectures"] if l["category"] == c) for c in d["categories"]}
    tiles = []
    for cat, problem, slugs in METHOD_BANK:
        links = "".join(f'<li><a href="methods/{s}.html">{esc(d["by_slug"][s]["title"])}</a></li>' for s in slugs)
        tiles.append(f"""<li class="bank-tile">
  <span class="bank-when">When…</span>
  <p class="bank-problem">{esc(problem)}</p>
  <ul class="bank-picks">{links}</ul>
  <a class="bank-more" href="methods.html#category={quote(cat)}">{esc(cat)} · {n[cat]} methods {ICON_ARROW}</a>
</li>""")
    return f"""<section class="method-bank t-methods" aria-labelledby="bank-title">
      <div class="bank-intro">
        <div class="eyebrow">Pick and choose · not a checklist</div>
        <h2 id="bank-title">Your method bank</h2>
        <p class="bank-lede">{len(d["lectures"])} UX methods for different types of problems. Unlike the sections below, there's nothing to complete here: you won't use every method, and you shouldn't. Start from the problem in front of you and pick the method that fits.</p>
        <a class="bank-go" href="methods.html">Browse all {len(d["lectures"])} methods {ICON_ARROW}</a>
      </div>
      <ul class="bank-tiles">{''.join(tiles)}</ul>
    </section>"""


# Sprint briefs featured on the home page: kind of sprint, when it runs, and an icon for briefs without a photo.
SPRINT_META = {
    "honest-greens": ("Service Design", "Weeks 1 & 3", "🥗"),
    "locker-room": ("Lean Startup", "Weeks 2 & 4", "🏖️"),
    "wicked-project": ("High-stakes sprint", "Week 6", "🌍"),
    "personal-project": ("Personal project", "Weeks 7 & 8", "🧭"),
}


def sprint_feature(data):
    d = data["sprints"]
    cards = []
    for l in d["lectures"]:
        kind, when, icon = SPRINT_META[l["slug"]]
        num, _, name = l["title"].partition(": ")
        pics = sorted((CONTENT / "sprints" / l["slug"]).glob("*.jpg"))
        art = (f'<img src="content/sprints/{l["slug"]}/{pics[0].name}" alt="" loading="lazy">' if pics
               else f'<span class="sprint-icon" aria-hidden="true">{icon}</span>')
        cards.append(f"""<a class="sprint-card" href="sprints/{l['slug']}.html">
  <span class="sprint-art">{art}<span class="sprint-num">{esc(num)}</span></span>
  <span class="sprint-body"><span class="sprint-kind">{esc(kind)} · {esc(when)}</span>
  <span class="sprint-name">{esc(name)}</span><span class="sprint-desc">{esc(l['description'])}</span>
  <span class="sprint-go">Read the brief {ICON_ARROW}</span></span>
</a>""")
    return f"""<section class="sprint-feature t-sprints" aria-labelledby="sprints-title">
      <div class="sprint-head"><div><div class="eyebrow">The projects</div><h2 id="sprints-title">Sprint briefs</h2>
      <p class="sprint-lede">Four sprints sit at the heart of the bootcamp. Each brief sets out the problem, your challenge, the scope and how the sprint runs day by day.</p></div>
      <a class="bank-go" href="sprints.html">All sprint briefs {ICON_ARROW}</a></div>
      <div class="sprint-grid">{''.join(cards)}</div>
    </section>"""


QUOTES = json.loads((CONTENT / "quotes.json").read_text(encoding="utf-8"))["quotes"]


def quote_of_the_day():
    """A small quote above the welcome; app.js swaps in today's quote (one a day, looping)."""
    q = QUOTES[0]
    data = json.dumps(QUOTES, ensure_ascii=False).replace("</", "<\\/")
    return (f'<figure class="qotd" id="qotd"><figcaption class="qotd-label">Quote of the day</figcaption>'
            f'<blockquote class="qotd-text">“{esc(q["q"])}”</blockquote><span class="qotd-by">{esc(q["by"])}</span></figure>'
            f'<script type="application/json" id="qotd-data">{data}</script>')


def build_home(data):
    """index.html: what the course is, the method bank, the four sections, a suggested route and a search of every page."""
    cards = []
    for t in TRACKS:
        if t["id"] in ("methods", "sprints"):  # not courses to complete: they get their own features
            continue
        d = data[t["id"]]
        n = len(d["lectures"])
        cats = " · ".join(esc(c) for c in d["categories"])
        cards.append(f"""<a class="section-card t-{t['id']}" href="{t['index']}">
  <span class="section-count">{n} {t['noun'].lower()}s</span>
  <span class="section-name">{t['label']}</span>
  <span class="section-blurb">{esc(t['blurb'])}</span>
  <span class="section-cats">{cats}</span>
  {progress_panel(t['id'], compact=True) if t['id'] in PROGRESS else ''}
  <span class="section-go">Open {ICON_ARROW}</span>
</a>""")
    steps = []
    for i, (step, why, track, slug) in enumerate(ROUTE, 1):
        t, target = TRACK[track], data[track]["by_slug"].get(slug)
        if target is None:
            raise SystemExit(f"ROUTE points at missing page {track}/{slug}")
        steps.append(f"""<li class="route-step">
  <span class="route-num">{i}</span>
  <div><h3>{esc(step)}</h3><p>{esc(why)}</p>
  <a href="{t['out']}/{slug}.html">{t['label']}: {esc(target['title'])} {ICON_ARROW}</a></div>
</li>""")
    index = [{"t": p["title"], "d": p["description"], "s": t["label"], "u": f"{t['out']}/{p['slug']}.html"}
             for t in TRACKS for p in data[t["id"]]["every"]]
    badges = "".join(f"""<li class="award-card t-{k}">
  <div class="badge-item" data-track="{k}">{badge_svg(k, 72)}<span class="badge-name">{b['badge']} award</span><span class="badge-state">Locked</span></div>
  {'<ul class="milestones">' + "".join(milestone_item(k, c, 40) for c in b["milestones"]) + '</ul>' if b["milestones"]
   else f'<p class="award-note">Complete any {b["need"]} of the {len(data[k]["lectures"])} sprints to win it. You need it to pass.</p>' if b.get("need")
   else '<p class="award-note">One award for the whole section.</p>'}
</li>""" for k, b in PROGRESS.items())
    badges += f"""<li class="award-card cert-card"><a class="badge-item" data-cert href="certificate.html">{certificate_svg(72)}
  <span class="badge-name">Certificate</span><span class="cert-sub">{CERTIFICATE} · {SCHOOL}</span><span class="badge-state">Locked</span></a></li>"""
    index_json = json.dumps(index, ensure_ascii=False).replace("</", "<\\/")
    body = f"""
<main class="home course">
  <div class="wrap">
    <header class="hero hero-home">
      <div>
        <div class="eyebrow">Barcelona Code School · UX &amp; UI Bootcamp</div>
        {quote_of_the_day()}
        <h1>Welcome, student</h1>
        <p class="lede">Lectures to read, Figma lessons and briefs to practise with, plus a bank of methods to pick from in your sprints. Follow the suggested route, or see <a href="timetable.html">the nine-week timetable</a>.</p>
      </div>
      <label class="search search-all"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q-all" type="search" placeholder="Search all {len(index)} pages…" autocomplete="off"></label>
    </header>
    <ul class="cards search-results" id="results" hidden></ul>
    {sprint_feature(data)}
    {method_bank(data)}
    <section class="sections" aria-label="Sections">{''.join(cards)}</section>
    <section class="badges" aria-labelledby="badges-title">
      <h2 id="badges-title">Your badges</h2>
      <p class="route-intro">Celebrate every step. Finish every page in a sub-section to reach its <b>milestone</b>. Reach every milestone in a section to win its <b>award</b>. Win all five awards (for Sprints, two of the four sprints are enough) and {SCHOOL} awards you a <b>certificate</b> in the {CERTIFICATE}. Lectures with parts count once you've done all of their parts. Progress is saved in this browser.</p>
      <ul class="badge-shelf">{badges}</ul>
    </section>
    <section class="route">
      <h2>Suggested route</h2>
      <p class="route-intro">Not sure where to start? This is one way through. Dip into the method bank whenever your sprint needs a method.</p>
      <ol class="route-steps">{''.join(steps)}</ol>
    </section>
  </div>
</main>
<script type="application/json" id="search-index">{index_json}</script>"""
    (ROOT / "index.html").write_text(page(f"{SITE} · {SCHOOL}", TAGLINE, body, 0, "home"), encoding="utf-8")
    print(f"index.html: home, {len(index)} pages searchable")


TAG_COLOURS = 7


def tag(label, link=None, data=None):
    """A Notion-style coloured tag; linked tags point at a page on this site ("section/slug" or a section)."""
    colour = sum(map(ord, label.lower())) % TAG_COLOURS
    if not link:
        return f'<span class="tt-tag c{colour}">{esc(label)}</span>'
    track, _, slug = link.partition("/")
    if slug:
        if slug not in data[track]["by_slug"]:
            raise SystemExit(f"timetable.json links to missing page {link}")
        href = f'{TRACK[track]["out"]}/{slug}.html'
    else:
        href = TRACK[track]["index"]
    return f'<a class="tt-tag c{colour} linked" href="{href}">{esc(label)}</a>'


# Icon for each kind of timetable card (a workshop's icon depends on the tool).
TT_ICONS = {"routine-standup": "☀️", "sprint": "🚀", "project": "🧩", "checkpoint": "🏁", "lecture": "🏛️", "ui": "📐",
            "activities": "🤸", "workshop-figma": "🎨", "workshop-framer": "🖥️", "daily": "✏️", "routine-lunch": "🍔",
            "presentation": "🎤", "routine-checkout": "🌙"}


def tt_card(cid, kind, label, heading="", time="", tags="", sub="", more="", icon_key=""):
    icon = TT_ICONS.get(icon_key or kind, "")
    return f"""<article class="tt-card kind-{kind}" data-id="{cid}">
  <div class="tt-top"><span class="tt-kind">{f'<span class="tt-icon" aria-hidden="true">{icon}</span>' if icon else ''}{esc(label)}</span>{f'<span class="tt-time">{esc(time)}</span>' if time else ''}
    <label class="tt-done" title="Mark as complete"><input type="checkbox" aria-label="Mark {esc(heading or label)} as complete"></label></div>
  {f'<h4 class="tt-heading">{esc(heading)}</h4>' if heading else ''}
  {f'<div class="tt-sub">{esc(sub)}</div>' if sub else ''}
  {f'<div class="tt-tags">{tags}</div>' if tags else ''}
  {more}
</article>"""


def page_tags(keys, data):
    """Linked tags for pages on this site, by their short titles."""
    out = []
    for key in keys:
        track, slug = key.split("/")
        title = short(data[track]["by_slug"][slug]["title"]).replace("Beginner’s Guide to ", "").replace("Beginner’s Guide ", "")
        out.append(tag(title, key, data))
    return "".join(out)


def check_timetable_coverage(tt, data):
    """Every UX lecture, UI lecture, Figma lesson and exercise should be scheduled exactly once."""
    seen = []
    for w in tt["weeks"]:
        if w.get("project_exercise"):
            seen.append(w["project_exercise"])
        for d in w["days"]:
            seen += d.get("lectures", []) + d.get("ui", []) + ([d["daily"]] if d.get("daily") else [])
            seen += (d.get("workshop") or {}).get("lessons", [])
    wanted = [f"{k}/{l['slug']}" for k in ("ux", "ui", "figma", "exercises") for l in data[k]["lectures"]]
    missing = [k for k in wanted if k not in seen]
    twice = sorted({k for k in seen if seen.count(k) > 1})
    if missing or twice:
        print(f"timetable: not scheduled: {missing}; scheduled more than once: {twice}")
    return len(wanted) - len(missing)


def build_timetable(data):
    tt = json.loads((CONTENT / "timetable.json").read_text(encoding="utf-8"))
    covered = check_timetable_coverage(tt, data)
    r = tt["routine"]
    days = tt["days"]
    head = "".join(f'<div class="tt-colhead">{d} <span>Day {i}</span></div>' for i, d in enumerate(days, 1))
    weeks_html, chips = [], []
    for w_i, w in enumerate(tt["weeks"], 1):
        name = f'{w["project"]}{" – " + w["part"] if w["part"] else ""}'
        chips.append(f'<a class="tt-chip" href="#week-{w_i}"><b>Week {w_i}</b><span>{esc(w["theme"])}</span></a>')
        cols = []
        for d_i, day in enumerate(w["days"], 1):
            cid = f"w{w_i}d{d_i}"
            cards = [tt_card(f"{cid}-standup", "routine", "Stand up", time=r["standup"]["time"], icon_key="routine-standup")]
            if d_i == 1:
                about = (f'<details class="tt-about"><summary>About this sprint</summary><p>{esc(w["summary"])}</p>'
                         f'<p><b>AI in this sprint:</b> {esc(w["ai"])}</p><div class="tt-tags">{"".join(tag(t) for t in w["tools"])}</div></details>')
                cards.append(tt_card(f"{cid}-sprint", "sprint", f'Sprint {w["code"][1:]}', heading=w["theme"], sub=name, more=about))
            if d_i == 1 and w.get("project_exercise"):
                cards.append(tt_card(f"{cid}-project", "project", "Project this week", tags=page_tags([w["project_exercise"]], data)))
            if day.get("checkpoint"):
                cards.append(tt_card(f"{cid}-checkpoint", "checkpoint", "Check point", heading="Informal presentations", time="11:00"))
            if day.get("lectures"):
                cards.append(tt_card(f"{cid}-lecture", "lecture", "Lecture" + ("s" if len(day["lectures"]) > 1 else ""),
                                     tags=page_tags(day["lectures"], data)))
            if day.get("ui"):
                cards.append(tt_card(f"{cid}-ui", "ui", "UI theory", tags=page_tags(day["ui"], data)))
            cards.append(tt_card(f"{cid}-activities", "activities", "Activities",
                                 tags="".join(tag(a["label"], a.get("link"), data) for a in day["activities"])))
            if day.get("workshop"):
                ws = day["workshop"]
                kind_label = "Figma workshop" if ws["title"].startswith("Figma") else "Framer workshop"
                if ws.get("lessons"):
                    names = []
                    for key in ws["lessons"]:
                        track, slug = key.split("/")
                        lesson = short(data[track]["by_slug"][slug]["title"])
                        names.append((lesson.replace("Beginner’s Guide to ", "").replace("Beginner’s Guide ", ""), key))
                    ws_tags = "".join(tag(n, k, data) for n, k in names)
                else:
                    ws_tags = tag(ws.get("tag") or "Portfolio site", ws.get("link"), data)
                cards.append(tt_card(f"{cid}-workshop", "workshop", kind_label, tags=ws_tags,
                                     icon_key="workshop-figma" if kind_label.startswith("Figma") else "workshop-framer"))
            if day.get("daily"):
                track, slug = day["daily"].split("/")
                level = data[track]["by_slug"][slug]["difficulty"]
                cards.append(tt_card(f"{cid}-daily", "daily", data[track]["by_slug"][slug]["category"] if track == "exercises" else "Daily UI", time=f"{level}/5" if level else "",
                                     tags=page_tags([day["daily"]], data)))
            cards.append(tt_card(f"{cid}-lunch", "routine", "Lunch", time=r["lunch"]["time"], icon_key="routine-lunch"))
            if day.get("presentation"):
                cards.append(tt_card(f"{cid}-presentation", "presentation", "Presentation", heading=day["presentation"]))
            cards.append(tt_card(f"{cid}-checkout", "routine", "Check out", time=r["checkout"]["time"], icon_key="routine-checkout"))
            cols.append(f'<div class="tt-col"><div class="tt-col-label">{days[d_i - 1]} <span>Day {d_i}</span></div>{"".join(cards)}</div>')
        weeks_html.append(f"""<section class="tt-week" id="week-{w_i}">
  <details{' open' if w_i == 1 else ''}>
    <summary><span class="tt-caret" aria-hidden="true"></span><span class="tt-weekpill">Week {w_i}</span>
      <span class="tt-weekname">{esc(w["theme"])} <span>· {esc(name)}</span></span>
      <span class="tt-progress" data-week="{w_i}"></span></summary>
    <div class="tt-grid">{"".join(cols)}</div>
  </details>
</section>""")
    body = f"""
<main class="timetable">
  <div class="wrap">
    <header class="hero tt-hero">
      <div>
        <div class="eyebrow">In-Person Bootcamp · UX Day by Day</div>
        <h1>Timetable</h1>
        <p class="lede">Nine weeks covering all {covered} lectures, lessons and exercises on this site, {esc(tt["hours"])}. Every week is a sprint: a brief on Monday, a presentation on Friday.</p>
      </div>
      <div class="tt-tools">
        <span class="tt-overall" id="tt-overall"></span>
        <label class="tt-toggle"><input type="checkbox" id="tt-routine"> Show daily routine</label>
        <button type="button" class="tt-btn" id="tt-expand">Expand all</button>
      </div>
    </header>
    <nav class="tt-chips" aria-label="Weeks">{"".join(chips)}</nav>
    <p class="tt-routine-line"><b>Every day:</b> Stand up {r["standup"]["time"]} · Lunch {r["lunch"]["time"]} · Check out {r["checkout"]["time"]}</p>
    <div class="tt-board">
      <div class="tt-head">{head}</div>
      {"".join(weeks_html)}
    </div>
    <p class="tt-note">Ticks are saved in this browser only.</p>
  </div>
</main>"""
    (ROOT / "timetable.html").write_text(page(f"{SITE} · Timetable", "The nine-week UX/UI bootcamp, day by day.", body, 0, "timetable"),
                                         encoding="utf-8")
    print(f"timetable.html: {len(tt['weeks'])} weeks")


def build_certificate():
    """certificate.html: locked until every award is earned, then a printable certificate with the student's name."""
    awards = "".join(f"""<li class="badge-item" data-track="{k}">{badge_svg(k, 64)}<span class="badge-name">{b['badge']}</span>
  <span class="badge-state">Locked</span></li>""" for k, b in PROGRESS.items())
    seals = "".join(f'<li>{badge_svg(k, 54)}<span>{b["badge"]}</span></li>' for k, b in PROGRESS.items())
    body = f"""
<main class="certificate-page" data-cert-page data-state="locked">
  <div class="wrap">
    <section class="cert-locked">
      <div class="cert-lock-art">{certificate_svg(110)}</div>
      <div class="eyebrow">{SCHOOL}</div>
      <h1>Your certificate</h1>
      <p class="lede">Win all five awards to unlock your certificate in the {CERTIFICATE}. Each award comes from reaching every milestone in its section; for Sprints, complete at least two of the four sprints.</p>
      <ul class="badge-shelf cert-awards">{awards}</ul>
      <p class="cert-back"><a href="index.html#badges-title">See your milestones and awards</a></p>
    </section>
    <section class="cert-open">
      <div class="cert-controls">
        <div><div class="eyebrow">Certificate unlocked</div><h1>Congratulations!</h1>
        <p class="lede">Add your name as you'd like it to appear, then print it or save it as a PDF.</p></div>
        <label class="field cert-field"><span>Your full name</span>
          <input id="cert-name-input" type="text" autocomplete="name" maxlength="60" placeholder="e.g. Alex García"></label>
        <button type="button" class="login-submit" id="cert-print">Print or save as PDF</button>
      </div>
      <div class="cert-sheet" id="cert">
        <div class="cert-frame">
          <div class="cert-head">{LOGO_MARK.replace('width="38" height="38"', 'width="64" height="64"')}
            <div><div class="cert-school">{SCHOOL}</div><div class="cert-programme">{CERTIFICATE}</div></div></div>
          <div class="cert-kicker">Certificate of completion</div>
          <p class="cert-line">This certifies that</p>
          <div class="cert-name" id="cert-name">Your name</div>
          <p class="cert-line">has completed every UX Theory and UI Theory lecture, Figma lesson and exercise of the
            <b>{CERTIFICATE}</b> learning path, earning all five awards.</p>
          <ul class="cert-seals">{seals}</ul>
          <div class="cert-foot">
            <div><span class="cert-date" data-cert-date></span><span class="cert-caption">Date</span></div>
            <div class="cert-seal">{certificate_svg(70)}</div>
            <div><span class="cert-sign">{SCHOOL}</span><span class="cert-caption">{CERTIFICATE}</span></div>
          </div>
        </div>
      </div>
    </section>
  </div>
</main>"""
    (ROOT / "certificate.html").write_text(page(f"Certificate · {SITE}", f"Your {CERTIFICATE} certificate.", body, 0, "certificate"),
                                           encoding="utf-8")
    print("certificate.html")


def build_login():
    """login.html: the one page that isn't gated."""
    html_ = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sign in · {SITE}</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/svg+xml" href="{FAVICON}">
<script>try{{var t=localStorage.getItem('cs-theme');if(t)document.documentElement.dataset.theme=t;
if(localStorage.getItem('cs-auth')==='{LOGIN_HASH}')location.replace('index.html')}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Figtree:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="assets/style.css?v={ASSET_V}">
<link rel="stylesheet" href="assets/theme.css?v={ASSET_V}">
</head>
<body class="login-page">
<main class="login">
  <div class="login-brand logo">{LOGO}
  </div>
  <form class="login-card" id="login-form" data-hash="{LOGIN_HASH}" novalidate>
    <div class="eyebrow">Student access</div>
    <h1>Sign in to the course</h1>
    <p class="login-intro">Lectures, methods, exercises and the timetable for the UX &amp; UI bootcamp.</p>
    <label class="field"><span>Username</span>
      <input id="login-user" name="username" type="text" autocomplete="username" autocapitalize="none" spellcheck="false" required></label>
    <label class="field"><span>Password</span>
      <span class="pw"><input id="login-pass" name="password" type="password" autocomplete="current-password" required>
      <button type="button" class="pw-toggle" id="pw-toggle" aria-label="Show password" aria-pressed="false">Show</button></span></label>
    <p class="login-error" id="login-error" role="alert" hidden>That username and password don't match. Check with your teacher.</p>
    <button type="submit" class="login-submit">Sign in</button>
    <p class="login-help">Don't have the login? Ask your teacher at Barcelona Code School.</p>
  </form>
</main>
<script src="assets/app.js?v={ASSET_V}"></script>
</body>
</html>
"""
    (ROOT / "login.html").write_text(html_, encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    print("login.html")


def write_progress_data(data):
    for k, b in PROGRESS.items():
        if b["milestones"] and list(b["milestones"]) != data[k]["categories"]:
            raise SystemExit(f"PROGRESS[{k!r}] milestones {list(b['milestones'])} don't match its sub-sections {data[k]['categories']}")
    def entry(k, page):
        return {"key": f"{k}/{page['slug']}", "title": page["title"], "url": f"{TRACK[k]['out']}/{page['slug']}.html"}
    tracks = {k: {"badge": b["badge"], "done": b["done"], "short": b["short"], "label": TRACK[k]["label"], "need": b.get("need"),
                  "index": TRACK[k]["index"], "svg": badge_svg(k, 120),
                  "milestones": [{"name": c, "svg": milestone_svg(k, c, 96)} for c in b["milestones"]],
                  "items": [{**entry(k, l), "category": l["category"],
                             "children": [{**entry(k, data[k]["by_slug"][c]), "title": short(data[k]["by_slug"][c]["title"])}
                                          for c in l["children"]]}
                            for l in data[k]["lectures"]]} for k, b in PROGRESS.items()}
    (ROOT / "assets" / "progress-data.js").write_text(
        "// Generated by tools/build.py: the pages that make up each section's progress, for the tracker and badges.\n"
        "window.CS_ROOT = document.currentScript.src.replace(/assets\\/progress-data\\.js.*$/, '');\n"
        "window.CS_PROGRESS = " + json.dumps(tracks, ensure_ascii=False, separators=(",", ":")) + ";\n"
        "window.CS_CERT = " + json.dumps({"name": CERTIFICATE, "school": SCHOOL, "svg": certificate_svg(120)},
                                         ensure_ascii=False, separators=(",", ":")) + ";\n"
        "// Pages that moved section: old progress key -> new one.\n"
        "window.CS_MOVED = " + json.dumps(moved_pages(data), separators=(",", ":")) + ";\n", encoding="utf-8")


def moved_pages(data):
    """Pages shown by a track that shares another track's content used to live in that track."""
    moved = {}
    for t in TRACKS:
        src = t.get("content")
        if src and src != t["id"]:
            for p in data[t["id"]]["every"]:
                moved[f"{src}/{p['slug']}"] = f"{t['id']}/{p['slug']}"
    return moved


# Pages taken off the site: old address -> where to send visitors instead.
REMOVED = {f"lectures/{s}.html": "../ui.html" for s in ("what-is-ui-design", "icons", "colors", "typography", "grid", "design-systems")}
REMOVED["methods/lo-fi.html"] = "mid-fi.html"
REMOVED.update({
    "lectures/non-directive-interview-technique.html": "../methods/limited-intervention-technique.html",
    "lectures/interviewer-format.html": "../methods/facilitator-format.html",
    "lectures/interview-taking-notes.html": "../methods/notetaker-format.html",
    "lectures/portfolio.html": "../methods/building-your-web-portfolio.html",
    "lectures/scripts.html": "../methods/building-your-web-portfolio.html",
})
REMOVED["ui/case-studies-and-how-to-tell-a-good-story.html"] = "../methods/writing-your-case-study.html"
REMOVED["methods/process-narrative.html"] = "writing-your-case-study.html"


def write_redirects(data):
    for path, target in REMOVED.items():
        (ROOT / path).write_text(
            f'<!doctype html><meta charset="utf-8"><title>Moved</title><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={target}"><p>This page has moved to <a href="{target}">{target}</a>.</p>\n',
            encoding="utf-8")
    for old, new in moved_pages(data).items():
        o, n = old.split("/"), new.split("/")
        target = f"../{TRACK[n[0]]['out']}/{n[1]}.html"
        (ROOT / TRACK[o[0]]["out"] / f"{o[1]}.html").write_text(
            f'<!doctype html><meta charset="utf-8"><title>Moved</title><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{target}">'
            f'<p>This page has moved to <a href="{target}">{target}</a>.</p>\n', encoding="utf-8")



# ---- Page templates -------------------------------------------------------------------------------
# One format per content type, so students meet the same structure on every page of a kind. Each template
# lists its section headings in order ("keys" match the start of a heading, ignoring emoji and markup);
# "optional" sections may be left out but, when present, sit in their place. check_templates() fails the
# build when a page breaks its template, except pages listed in content/template-pending.json, which are
# still waiting to be converted. That list may only shrink: the build tells you when a pending page passes.
TEMPLATES = {
    "Method": {"level": 1, "keys": ["stage", "context", "goal / learning outcome", "main exercise", "estimated duration",
                                    "extra notes", "template", "tips", "ai assist", "media", "resources", "checklist", "summary"],
               "optional": ["extra notes", "template", "ai assist"]},
    "Sprint brief": {"level": 2, "keys": ["the brief", "the problem", "your challenge", "sprint goals", "scope", "deliverables",
                                          "how the sprint runs", "constraints and tips", "success looks like"], "optional": []},
    "Daily UI": {"level": 2, "keys": ["the brief", "deliverable", "must include", "nice to have", "inspiration", "time box",
                                      "before you submit"], "optional": []},
    "Replica challenge": {"level": 2, "keys": ["the screens", "the journey ahead", "elevating your skills", "conclusion"], "optional": []},
    "Team project": {"level": 2, "keys": ["the brief", "team roles", "directives", "deliverables", "day-by-day plan", "schema",
                                          "checklist", "assessment"], "optional": []},
    "Lecture": {"level": 2, "keys": ["why it matters for ux", "try it", "media", "resources", "key takeaways"], "optional": []},
    "Key figure": {"level": 2, "keys": ["who they are", "key contributions", "why it matters for ux"], "optional": []},
    "AI outputting": {"level": 2, "keys": ["the brief", "the tools", "how to run it", "pros and cons", "before you submit"], "optional": []},
    "Figma lesson": {"level": 2, "keys": ["what you'll build", "before you start", "well done"], "optional": []},
}


def page_template(track, page):
    """Which template a page follows."""
    cat = page.get("category") or ""
    if track == "methods":
        return "Method"
    if track == "sprints":
        return "Sprint brief"
    if track == "exercises":
        return {"Daily UI": "Daily UI", "Replica Challenges": "Replica challenge", "AI Outputting": "AI outputting"}.get(cat, "Team project")
    if track == "figma":
        return "Figma lesson"
    if page.get("parent") == "key-figures":
        return "Key figure"
    return "Lecture"


def template_problems(name, text):
    """What is missing or out of order on a page, compared with its template ([] if it complies)."""
    tpl = TEMPLATES[name]
    heads = []
    for hashes, h in re.findall(r"^(#{1,3}) (.+)$", text, re.M)[1:]:
        if len(hashes) > tpl["level"]:
            continue
        h = re.sub(r"[*_`~]", "", h)
        heads.append(re.sub(r"^[^\w]+", "", h).strip(" :").lower())
    found = []
    for h in heads:
        k = next((k for k in tpl["keys"] if h.startswith(k)), None)
        if k and k not in found:
            found.append(k)
    problems = [f"missing '{k}'" for k in tpl["keys"] if k not in found and k not in tpl["optional"]]
    order = [tpl["keys"].index(k) for k in found]
    if order != sorted(order):
        problems.append("sections out of order: " + ", ".join(found))
    return problems


def check_templates(data):
    pending_file = CONTENT / "template-pending.json"
    pending = set(json.loads(pending_file.read_text(encoding="utf-8"))["pages"]) if pending_file.exists() else set()
    broken, now_pass, tally = [], [], {}
    for track, d in data.items():
        hubs = {p.get("parent") for p in d["every"]}
        for p in d["every"]:
            if p["slug"] in hubs:
                continue  # a hub page only lists its children
            key, name = f"{track}/{p['slug']}", page_template(track, p)
            problems = template_problems(name, p["text"])
            ok, total = tally.get(name, (0, 0))
            tally[name] = (ok + (not problems), total + 1)
            if problems and key not in pending:
                broken.append(f"  {key} ({name}): " + "; ".join(problems))
            elif not problems and key in pending:
                now_pass.append(key)
    print("templates: " + ", ".join(f"{n} {ok}/{tot}" for n, (ok, tot) in tally.items()))
    if now_pass:
        print("templates: these pending pages now follow their template; remove them from content/template-pending.json:\n  "
              + "\n  ".join(now_pass))
    if broken:
        raise SystemExit("Pages that break their template (fix them, or list them in content/template-pending.json):\n"
                         + "\n".join(broken))

def main():
    global ASSET_V
    data = load()
    check_templates(data)
    write_progress_data(data)
    ASSET_V = hashlib.sha1(b"".join((ROOT / "assets" / f).read_bytes()
                                    for f in ("style.css", "theme.css", "app.js", "progress-data.js"))).hexdigest()[:10]
    for t in TRACKS:
        build_track(t, data)
    build_home(data)
    build_timetable(data)
    build_certificate()
    build_login()
    write_redirects(data)


if __name__ == "__main__":
    main()
