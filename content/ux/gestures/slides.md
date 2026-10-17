title: Gestures
promise: Gestures feel direct and natural, but they are invisible. How to design ones people can find, remember and perform.
duration: 15 minutes
topics:
- What a gesture is
- The standard touch gestures and what people expect
- Why gestures are tricky
- Eight design principles
- Gestures in spatial computing
---
@title
# Gestures
Direct, fast and natural, and completely invisible.
---
@statement
A **gesture** is a movement of the hand or body that a device understands as a command.

You don't press "Zoom in". You spread the photo apart with your fingers.
---
@image
## The standard touch gestures

![Diagrams of tap, double tap, drag, flick, pinch, spread, press, press and tap, press and drag, and rotate](touch-chart-large-opt.jpg)

*People already know these. Use them for what people expect them to do.*
---
@cards
## What people expect

- **Tap** Select, open, press
- **Long press** More options, a preview, pick it up
- **Swipe** Next page or photo; reveal actions on a list item
- **Drag** Move, reorder, adjust a slider
- **Pinch and spread** Zoom out and in
- **Edge swipe** Back, home, notifications: it belongs to the system
---
@statement
A button sits on the screen and tells you it exists.

**A gesture is invisible.**
---
@quote
> Gestural interfaces: a step backward in usability.

Don Norman and Jakob Nielsen, 2010. Gestures work only if people can discover them, remember them and predict what they'll do.
---
@cards
## Why gestures are tricky

- **Invisible** Nothing shows that a row can be swiped or a photo pinched
- **Memorised** The more custom gestures you add, the fewer people remember
- **Ambiguous** A swipe that deletes here and changes tab there causes mistakes
- **Exclusive** Two-finger gestures and long presses are hard with a tremor, or a coffee in one hand
---
@text
## Use the standards, and always offer a way out

1. **Standard gestures, standard meanings.** Pinch zooms, tap selects. Don't reinvent them.
2. **A visible alternative.** Every gesture-only action needs a button, a menu or a "…". The gesture is the shortcut.
3. **Signifiers.** A card peeking from the edge invites a swipe; a handle invites a drag; dots show there's more.
4. **Instant feedback.** Content follows the finger and settles with a clear response.
---
@text
## Make it forgiving and reachable

5. **Forgiving.** Let people cancel halfway, and offer **Undo** after delete or archive.
6. **Big targets.** At least **44 × 44 pt** (Apple) or **48 × 48 dp** (Material Design), with space between.
7. **Thumbs.** Frequent actions low on the screen; destructive ones away from where thumbs rest.
8. **No conflicts.** No horizontal swipe inside a horizontal scroller, and keep clear of the system's edges.
---
@cards
## Gestures in the wild

- **Pull to refresh** Invented in the Tweetie app, now standard almost everywhere
- **Swipe to archive** In mail apps, always paired with Undo
- **Swipe left or right** In dating apps, the gesture became the product
- **Long press an app icon** Quick actions, for those who know
---
@image
## Gestures in the air

![Apple Vision Pro hand gestures: tap, double tap, pinch and hold, pinch and drag, zoom and rotate](apple-visionos-hand-gestures-illustration.avif)

*On Apple Vision Pro, you look at something to target it, then tap your thumb and index finger together to select it.*
---
@statement
In spatial computing, everything matters **more**.

Gestures are even less visible, tire the arms, and need very clear feedback, because there's no surface to confirm a touch.
---
@exercise
## Audit this to-do app

1. **Swipe right** on a task to delete it, instantly
2. **Long press** a task to edit it; there's no other way
3. **Swipe in from the left edge** to open your lists
4. The tick to complete a task is **24 × 24 pt**
5. Tasks sit inside a week strip that **scrolls sideways**

Which principle does each break, and how would you fix it?
---
@answers
## Check yourself

1. **Not forgiving:** add Undo, or swipe to reveal a Delete button rather than deleting at once
2. **No visible alternative:** add an Edit option to a "…" menu or the task screen
3. **Conflicts with the system:** the left edge means *back* on iPhone. Use a visible Lists button instead
4. **Target too small:** at least 44 × 44 pt, even if the icon stays small
5. **Gesture conflict:** a sideways swipe on a task fights the sideways scroll. Change one of them
