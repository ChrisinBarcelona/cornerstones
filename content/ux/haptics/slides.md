title: Haptics
promise: Designing for the sense of touch, so people can feel an interface as well as see and hear it.
duration: 15 minutes
topics:
- What haptics are, and how they differ from sound
- Why haptics matter
- From buzz to click: a short history
- Notify, confirm, delight
- Apple's haptic vocabulary and three principles
- Specifying haptics in your designs
---
@title
# Haptics
Designing for touch: interfaces you can feel.
---
@statement
**Haptics** are the taps, clicks, pulses and vibrations a device makes so you can *feel* an interface.

From the Greek *haptikos*: "able to touch or perceive".
---
@text
## Haptic or audio?

The ding when a message sends is **audio** feedback.

The buzz in your pocket for that message, or the tiny click as you flick a picker wheel, is **haptic** feedback.

The best products design the two **together**, so a moment looks, sounds and feels like one event.
---
@cards
## Why haptics matter

- **No need to look** Apple Pay's double tap tells you the payment went through
- **Glass has no buttons** Haptics give back the certainty of a click
- **Eyes-free moments** Phones in pockets, watches on silent wrists
- **Accessibility** A signal for people who can't hear an alert or see the screen
---
@section
## From buzz to click
How haptics grew up.
---
@text
## A very short history

- **1990s** Pagers and early phones: a spinning off-centre weight. Loud, slow, blunt
- **1997** The Nintendo 64 Rumble Pak: you *feel* the crash
- **2015** Apple's Taptic Engine and the Force Touch trackpad: short, crisp taps. The trackpad "click" is simulated
- **2016** The iPhone 7 home button doesn't move, but feels like it clicks
- **2020** The PlayStation 5 DualSense: detailed haptics and triggers that push back
---
@statement
Haptics went from **buzzing** to **clicking**.

Modern haptics are short, precise and meaningful.
---
@cards
## Every haptic has a job

- **Notify** Get attention: a call, a calendar alert, a tap on the wrist to turn left
- **Confirm** Say it worked, or didn't: a payment, a fingerprint, a wrong passcode
- **Delight** Make it feel physical: a slider snapping, a picker ticking
---
@text
## How haptics feel

- **Clear:** crisp and short, like a click or tick. For buttons, toggles and selections
- **Rich:** a flutter, a thud, a bounce. For special moments, with a simpler fallback
- **Buzzy:** long and tingly, like an old pager. Avoid it

Android's advice: if the choice is between buzzy and nothing, choose **nothing**.
---
@cards
## Apple's vocabulary

- **Notification** *Success*, *warning* and *error*, for the outcome of a task
- **Impact** *Light*, *medium*, *heavy*, *soft* and *rigid*, for physical contact
- **Selection** A light tick each time a value changes
---
@cards
## Three principles

- **Causality** It's obvious what caused the feeling. Late haptics feel like faults
- **Harmony** Touch, sound and visuals feel like one event
- **Utility** Only where it adds value. Less is more
---
@statement
**Never rely on haptics alone.**

Some people switch them off, some devices have none. The experience must still work.
---
@text
## Specify them in your designs

You can't feel a Figma prototype, but you can **annotate** it.

| Moment | Haptic | Paired with |
| --- | --- | --- |
| Payment complete | iOS: notification success | Green tick, "Paid" sound |
| Wrong PIN | iOS: notification error | Field shake, red message |
| Choose a time | iOS: selection | Picker wheel moves |
---
@exercise
## Name that haptic

For each moment, give the **job** (notify, confirm or delight) and the **iOS haptic**:

1. Face ID fails when you try to pay
2. You spin a date-picker wheel
3. Your watch taps to say turn left
4. A toggle snaps on
5. An upload makes the phone vibrate non-stop until it's done

One of these shouldn't have a haptic at all. Which, and why?
---
@answers
## Check yourself

1. **Confirm:** *notification error*, paired with a shake and a message
2. **Delight:** *selection*, one tick per value
3. **Notify:** a wrist tap; Apple Maps uses different patterns for left and right
4. **Confirm and delight:** a light *impact*, in sync with the animation
5. **None.** It's long and buzzy, and breaks *utility*. Show a progress bar, then one *success* haptic when it finishes
