# Accessibility

## Design for everyone

About **1.3 billion people**, roughly one in six, live with a significant disability, according to the [World Health Organization](https://www.who.int/news-room/fact-sheets/detail/disability-and-health). Add everyone who is temporarily or situationally limited, and accessibility stops being an edge case: it is most of your users, some of the time.

| Permanent | Temporary | Situational |
| --- | --- | --- |
| One arm | Arm in a cast | Holding a baby |
| Blind | Eye infection | Phone in bright sunlight |
| Deaf | Ear infection | Loud bar or train |

This way of thinking comes from Microsoft's Inclusive Design toolkit. A design that works for someone with one arm also works for a parent holding a coffee.

<aside>
📝 **Accessibility** means people with disabilities can perceive, understand, navigate and use your product. It is a design responsibility, not a developer's clean-up job at the end.

</aside>

## WCAG: the rules everyone builds to

The **Web Content Accessibility Guidelines (WCAG)**, published by the W3C, are the international standard. Most laws, including the European Accessibility Act, which applies to many digital products in the EU since June 2025, point to them. WCAG has three levels: **A** (minimum), **AA** (the usual target) and **AAA** (strictest).

Every guideline sits under four principles, known as **POUR**:

1. **Perceivable**: people can see or hear the content (text alternatives, captions, contrast).
2. **Operable**: people can use it with whatever they have (keyboard, touch, voice, enough time).
3. **Understandable**: the content and interface behave predictably and explain themselves.
4. **Robust**: it works with assistive technology such as screen readers.

## Colour and contrast

Contrast is the accessibility rule designers break most often. WCAG 2.2 at level AA asks for:

| What | Minimum contrast ratio |
| --- | --- |
| Body text | **4.5 : 1** |
| Large text (24 px regular, or about 19 px bold) | **3 : 1** |
| Icons, input borders, focus rings and other UI parts | **3 : 1** |
| Disabled controls, logos, decoration | No requirement |

Check every colour pair in a contrast checker before it goes in your style guide, not after the screens are built.

**Never use colour alone to carry meaning.** Around 1 in 12 men and 1 in 200 women have some form of colour blindness. A red border on an error field needs an icon and a message too; a green/red chart needs labels or patterns.

## Type and readability

- Body text of **16 px** or larger on mobile.
- Line height around **1.5×** the font size for paragraphs.
- Lines of roughly **45–75 characters** on desktop.
- Left-aligned text for anything longer than a sentence or two; avoid justified text and long runs of capitals or italics.
- Let text resize: layouts should survive the user's system text size being turned up to 200%.

## Touch targets and interaction

Small targets fail people with tremors, big thumbs or a moving bus.

| Guideline | Minimum target |
| --- | --- |
| WCAG 2.2 AA | 24 × 24 px (or enough space around it) |
| Apple Human Interface Guidelines | 44 × 44 pt |
| Material Design | 48 × 48 dp |

Design for the platform minimum, not the WCAG floor. On an 8-point grid, a **48 × 48** target is the easy default. Every interactive element also needs a visible **focus state** for keyboard users, and gestures such as swipe or long-press need a simple tap alternative.

## Screen readers and structure

A screen reader reads your interface out loud, in order. What you hand off decides what it says:

- **Alt text** for every meaningful image; mark decorative images as decorative.
- **Real labels** on form fields. Placeholder text disappears when you type, so it is not a label.
- **Headings in order** (H1, H2, H3) so people can jump through the page.
- **Buttons that say what they do**: "Add to cart", not "Click here".
- **Reading and focus order** annotated in your Figma file when it isn't obvious from the layout.

---

## Why it matters for UX

Accessibility is usability for everyone, pushed to its limit. The same choices that let a blind user complete checkout also help someone in sunlight, in a hurry or on a cracked screen. It is also increasingly the law, and fixing it in Figma costs a fraction of fixing it in code.

## Try it: audit a screen (30 minutes)

1. Pick one screen from your current project.
2. Run every text and icon colour pair through the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) and fix anything below AA.
3. Measure every tap target and make anything under 44 × 44 bigger, or give it more space.
4. Find every place where colour alone carries meaning, and add an icon, label or pattern.
5. Annotate the reading order and write alt text for every image on the screen.

## Media

[https://www.youtube.com/watch?v=hE83Qn-PTGA](https://www.youtube.com/watch?v=hE83Qn-PTGA)

[https://www.youtube.com/watch?v=5H1JGdqLrWo](https://www.youtube.com/watch?v=5H1JGdqLrWo)

## Resources

[WCAG 2.2 Quick Reference – W3C](https://www.w3.org/WAI/WCAG22/quickref/)

[Contrast Checker – WebAIM](https://webaim.org/resources/contrastchecker/)

[Accessibility – Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/accessibility)

[Web Accessibility Perspectives videos – W3C](https://www.w3.org/WAI/perspective-videos/)

## Key takeaways

- Disability can be permanent, temporary or situational, so accessible design helps most users some of the time.
- WCAG AA is the usual target: 4.5:1 for body text, 3:1 for large text and UI parts.
- Never let colour alone carry meaning, and keep tap targets at 44–48 px.
- Labels, alt text, heading order and focus states decide what a screen reader can do with your design.
