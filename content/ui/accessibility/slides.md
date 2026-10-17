title: Accessibility
promise: Who accessibility is for, the WCAG rules behind it, and the contrast, type, target and structure checks every screen should pass.
duration: 15 minutes
topics:
- Permanent, temporary and situational disability
- WCAG and the POUR principles
- Colour and contrast
- Type, touch targets and screen readers
---
@title
# Accessibility
Design that works for everyone, including you on a sunny day.
---
@statement
About 1.3 billion people live with a significant disability: roughly one in six.

And everyone is limited **some of the time**.
---
@cards
## Permanent, temporary, situational

- **Permanent** One arm, blind, deaf
- **Temporary** Arm in a cast, eye infection, ear infection
- **Situational** Holding a baby, bright sunlight, a loud train
---
@cards
## WCAG's four principles: POUR

- **Perceivable** People can see or hear it: alt text, captions, contrast
- **Operable** People can use it: keyboard, touch, voice, enough time
- **Understandable** It behaves predictably and explains itself
- **Robust** It works with screen readers and other assistive tech
---
@text
## Contrast at level AA

| What | Minimum |
| --- | --- |
| Body text | **4.5 : 1** |
| Large text | **3 : 1** |
| Icons, borders, focus rings | **3 : 1** |
| Disabled, logos, decoration | None |

Check colour pairs **before** they go in your style guide.
---
@statement
Never let colour alone carry meaning.

Around **1 in 12 men** has some form of colour blindness. Add an icon, a label or a pattern.
---
@text
## Type that reads

- **16 px** or larger body text on mobile
- Line height around **1.5×**
- **45–75 characters** per line on desktop
- Left-aligned, no long runs of capitals
- Survives text resized to **200%**
---
@text
## Big enough to hit

| Guideline | Minimum target |
| --- | --- |
| WCAG 2.2 AA | 24 × 24 px |
| Apple HIG | 44 × 44 pt |
| Material Design | 48 × 48 dp |

On an 8-point grid, **48 × 48** is the easy default.
---
@cards
## What a screen reader needs from you

- **Alt text** On every meaningful image
- **Real labels** Placeholders vanish when you type
- **Headings in order** H1, H2, H3, so people can jump around
- **Honest buttons** "Add to cart", never "Click here"
---
@exercise
## Spot the problem

1. Grey #999999 body text on white. Does it pass AA?
2. An error field turns red, with no other change. What's wrong?
3. A 32 × 32 px close icon on iPhone. Big enough?
4. A search field labelled only by its placeholder. Why is that a problem?
5. A carousel you can only swipe. Who gets stuck?
---
@answers
## Check yourself

1. **No.** It's about 2.8 : 1; body text needs 4.5 : 1.
2. **Colour alone** carries the meaning. Add an icon and a message.
3. **No.** Apple asks for 44 × 44 pt; make the tap area bigger.
4. The placeholder **disappears** when you type, and isn't a proper label for screen readers.
5. Keyboard, switch and screen-reader users, and anyone who can't swipe. Add **buttons**.
