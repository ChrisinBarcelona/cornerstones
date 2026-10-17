title: Nielsen's Heuristics
promise: The ten rules of thumb that catch most usability problems before users ever see them, and give your team a shared language for design reviews.
duration: 20 minutes
topics:
- Jakob Nielsen and the 10 heuristics
- How to use them: designing, reviewing, testing
- The ten heuristics, one by one
- A quick heuristic evaluation
---
@title
# Nielsen's Heuristics
Ten rules of thumb for usable interfaces.
---
@split
## Jakob Nielsen

![Jakob Nielsen and Don Norman](image_-4-.jpeg)

Dr Jakob Nielsen (left, with Don Norman) co-founded the **Nielsen Norman Group**.

In 1994 he published his **10 usability heuristics**, refined from earlier work with Rolf Molich.
---
@statement
They're called **heuristics** because they're rules of thumb, not strict rules.

They've held up for three decades: desktop, phones, watches and AI chat.
---
@cards
## How to use them

- **While designing** Run through the list before you hand over a screen
- **To review** A heuristic evaluation: go through heuristic by heuristic and rate each problem's severity
- **Alongside testing** They catch common problems cheaply. Only real users show you real behaviour
---
@text
## 1. Visibility of system status

Always keep users informed about what's going on, with feedback in a reasonable time.

*A progress bar while a file uploads. "Order received, ready in about 8 minutes."*

**Ask:** after every action, does the user know it worked?
---
@text
## 2. Match with the real world

Speak the users' language, not internal jargon. Follow real-world conventions.

*A shopping "basket". "Delivery address", not "Shipping endpoint".*

**Ask:** would my users understand every label without explanation?
---
@text
## 3. User control and freedom

People make mistakes. Give them a clearly marked **emergency exit**.

*Undo after archiving an email. A clear Cancel. An X on every pop-up.*

**Ask:** can people back out of anything, easily, at any point?
---
@text
## 4. Consistency and standards

Users shouldn't wonder whether different words or actions mean the same thing. Follow platform conventions.

*The logo goes home. One style for every primary button. A magnifying glass for search.*

**Ask:** does it behave the way the rest of the web has taught people to expect?
---
@text
## 5. Error prevention

Better than a good error message: a design where the error **can't happen**.

*A date picker instead of free text. Unavailable dates greyed out. "Delete 240 photos?"*

**Ask:** where could someone slip up, and can I make it impossible?
---
@text
## 6. Recognition rather than recall

Make options visible. Don't make people remember things from one screen to the next.

*Recently viewed items. Search suggestions. The delivery address shown on the payment step.*

**Ask:** am I asking people to remember something I could simply show them?
---
@text
## 7. Flexibility and efficiency of use

Shortcuts for experts, invisible to beginners.

*Keyboard shortcuts. "Reorder" in a food app. Saved payment details.*

**Ask:** is there a faster path for everyday users that doesn't get in the way of first-timers?
---
@text
## 8. Aesthetic and minimalist design

Every extra piece of information competes with the ones that matter.

*One clear primary button per screen. Three key facts on a product card, the rest one tap away.*

**Ask:** what can I remove without losing anything people need right now?
---
@text
## 9. Recognise, diagnose and recover from errors

Plain language, no codes. Say exactly what went wrong and how to fix it.

*"That card has expired. Check the date or use another card", next to the field, not "Error 402".*

**Ask:** does every error say what, where and how to fix it?
---
@text
## 10. Help and documentation

Best if nobody needs it. If they do, make it searchable, task-focused and in concrete steps.

*A tooltip beside a tricky field. A "How does this work?" link in context.*

**Ask:** when someone's stuck, is a short answer right where they are?
---
@exercise
## Evaluate this food app

1. After you tap Pay, the screen freezes for eight seconds with no message
2. The menu calls your basket your "order manifest"
3. Removing an item asks you to confirm, but there's no undo for cancelling the whole order
4. A failed payment says only "Error 5003"
5. Your delivery address isn't shown on the final step, so you go back to check it

Which heuristic does each break? How severe is it?
---
@answers
## Check yourself

1. **#1 Visibility of system status.** Major: people tap Pay again and get charged twice
2. **#2 Match with the real world.** Minor: say "basket"
3. **#3 User control and freedom** (and #5 error prevention). Major: confirm or undo the big action, not the small one
4. **#9 Recover from errors.** Critical: people can't pay, and don't know why
5. **#6 Recognition rather than recall.** Minor: show the address with the Pay button
