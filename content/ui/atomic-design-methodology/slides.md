title: Atomic Design Methodology
promise: Brad Frost's way of building interfaces from small parts that add up to whole pages.
duration: 15 minutes
topics:
- What a design system is
- The five stages: atoms, molecules, organisms, templates, pages
- A real example: a music app, stage by stage
- How atomic design maps onto Figma
---
@title
# Atomic Design
Build interfaces from small parts that add up to whole pages.
---
@statement
A design system is a set of standards for managing design at scale, using reusable components and patterns.

Atomic design, by Brad Frost, is a way of thinking about how those parts fit together.
---
@image
## Five stages

![Atoms, molecules, organisms, templates and pages, from smallest to largest](Untitled.png)

*From the smallest building block to a finished page. It's a mental model, not a strict process.*
---
@split
## Atoms

![Atoms of a music player: icon buttons, album art, a slider and labels](Untitled-1.png)

The **smallest building blocks**: a label, an icon, a button, a colour, an image.

On their own they don't do much, but every interface is made of them.

**In Figma:** your styles and base components.
---
@split
## Molecules

![A song row: album art, title, artist and icon buttons working together](Untitled-2.png)

A **small group of atoms** that does one job.

Album art + title + artist + a like button = one **song row**.

Molecules should do one thing well.
---
@split
## Organisms

![A Popular songs list made of repeated song rows](Untitled-3.png)

**Larger sections** built from molecules: a header, a product grid, a list of songs.

This is where the interface starts to look like a product.
---
@split
## Templates

![A page layout showing where each molecule and organism goes](Untitled-4.png)

A **page-level layout** that places organisms on the grid.

It shows the structure of the content, using placeholders.
---
@split
## Pages

![The same template filled with real content for two different artists](Untitled-5.png)

The template **filled with real content**: real images, names and data.

Pages are where you test the system, because real content breaks things placeholder content never will.
---
@cards
## Atomic design in Figma

- **Atoms** Styles, variables and base components
- **Molecules** Components made from atom instances
- **Organisms** Larger components and sections
- **Templates** Frames with Auto Layout and placeholder content
- **Pages** Final screens with real content
---
@statement
Change an atom once, and every molecule, organism and page that uses it updates.

That's why design systems are fast, and why consistency comes for free.
---
@exercise
## Take YouTube apart

![YouTube's home page on desktop](youtube-home.webp)

Find at least:

- **3 atoms**
- **3 molecules**
- **3 organisms**

Then: what's the **template**, and what makes this a **page**?
---
@answers
## Check yourself

- **Atoms:** the logo, search and mic icons, a duration badge (`2:37`), a channel avatar, the verified tick, the ⋮ menu icon
- **Molecules:** the search bar (input + button), a category chip, a nav item (icon + label), the Sign in button, a video's details (avatar, title, channel, views)
- **Organisms:** the top bar, the left navigation rail, the chip bar, the grid of videos. A video card sits on the line: some teams call it a molecule, some an organism
- **Template:** top bar + rail + chip bar + a three-column grid of video cards
- **Page:** that template filled with real videos, chosen for you
