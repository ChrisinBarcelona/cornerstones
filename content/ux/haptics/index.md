# Haptics

![A human finger and a robot finger about to touch](651736f9958f4d4ac42eeb21_image_-2-.jpg)

**Haptics** is designing for the sense of touch: the taps, clicks, pulses and vibrations a device makes so that you can *feel* an interface, not just see and hear it. The word comes from the Greek *haptikos*, "able to touch or perceive".

Haptics are easy to confuse with sound. The ding when a message sends, or the beep when the microwave finishes, is **audio** feedback. The buzz in your pocket for that message, or the tiny "click" you feel when you flick a picker wheel, is **haptic** feedback. The best products design the two together, so a moment looks, sounds and feels like one single event.

## Why haptics matter

- **Feedback without looking.** Nielsen's first usability heuristic, *visibility of system status*, says people should always know what the system is doing. A haptic confirms an action even when your eyes are somewhere else: Apple Pay's double tap when a payment goes through, or the buzz when a timer ends.
- **Glass has no buttons.** A touchscreen is a flat sheet of glass. There is no key travel and no click, so it is hard to know whether a touch "landed". Nielsen Norman Group points out that touch typing is impossible without tactile cues. Haptics give some of that physical certainty back.
- **Eyes-free moments.** Phones live in pockets and watches sit on wrists. NN/g recommends that most guiding interactions on a smartwatch use haptics, because watches are often on silent and people are busy doing something else. Their example: a guitarist who preferred his metronome app to vibrate rather than beep.
- **Accessibility.** Vibration helps people who can't hear an alert or can't see the screen. It must never be the *only* signal, though: some people switch haptics off, some devices have none, and some users are sensitive to vibration.

## From buzz to click: a very short history

| Year | Moment | Why it mattered |
| --- | --- | --- |
| 1990s | Pagers and early phones | A small motor with an off-centre weight (an **ERM** motor) spins up and buzzes: loud, slow and blunt. |
| 1997 | Nintendo 64 Rumble Pak | Games make you *feel* a crash or an explosion. |
| 2015 | Apple Watch and the Force Touch trackpad | A **linear actuator** (Apple calls it the Taptic Engine) makes short, crisp taps. On the trackpad, the "click" is entirely simulated: the glass barely moves. |
| 2016 | iPhone 7 home button | The physical button is replaced by a solid button that feels like it clicks, thanks to haptics. |
| 2020 | PlayStation 5 DualSense | Rich, detailed haptics and triggers that push back. |

The lesson: haptics went from *buzzing* to *clicking*. Modern haptics are short, precise and meaningful, not a long vibration.

## The three jobs of a haptic

Android's design guidelines sort haptics into three jobs. Every haptic you design should do one of them.

| Job | What it does | Examples |
| --- | --- | --- |
| **Notify** | Get attention for something that needs it | An incoming call, a text, a calendar alert, a tap on the wrist to turn left |
| **Confirm** | Tell the user an action worked, or didn't | A payment succeeds, a fingerprint is accepted or rejected, a wrong passcode |
| **Delight** | Make an interaction feel physical and satisfying | A slider snapping into place, ticks as you scroll a picker, a pull-to-refresh that "catches" |

## How haptics feel

Android also describes three qualities of haptic:

- **Clear:** crisp, clean and short, like a mechanical click or tick. Use these for buttons, toggles and selections.
- **Rich:** expressive textures, such as a flutter, a heavy thud or a bounce. Good for special moments, but not every device can play them, so always plan a simpler fallback.
- **Buzzy:** noisy, long and tingly, like an old pager. Avoid it for touch feedback. Android's advice is that if the choice is between a buzzy haptic and none, choose **none**.

## Apple's haptic vocabulary

iPhone apps share a small set of standard haptics, so they feel the same across the system. Designers should know them by name:

- **Notification:** *success*, *warning* and *error*, for the outcome of a task. Think of a payment going through or a form failing.
- **Impact:** *light*, *medium* and *heavy* (also *soft* and *rigid*), to suggest physical contact: something landing, snapping or colliding.
- **Selection:** a light tick each time a value changes, like the clicks you feel spinning a date-picker wheel.

## Principles of good haptic design

Apple's audio-haptic design team (WWDC 2019) sums it up in three principles. Android's guidelines add a few practical rules.

1. **Causality.** It should be obvious what caused the feeling. A haptic that arrives late, or for no visible reason, feels like a fault.
2. **Harmony.** Touch, sound and visuals should feel like one event: in sync, and matched in character. A big, heavy animation with a tiny tick feels wrong.
3. **Utility.** Only add a haptic where it brings real value. **Less is more**: too many vibrations become annoying, numb the hand, and lead people to switch them off completely.
4. **Match strength to importance and frequency.** Things that happen constantly, like scrolling, get the faintest tick. Important moments, like submitting a form, get something stronger.
5. **Be consistent.** Use the same haptic for the same kind of event, and match the system (keyboards, pickers, switches) so people don't have to learn a new language.
6. **Never rely on haptics alone.** Always pair them with something visible, and make sure the experience still works with haptics turned off.

## Haptics in the wild

- **Phone:** the call buzz in your pocket, keyboard clicks (an option in iOS settings), the error buzz on a wrong passcode, and selection ticks on pickers.
- **Watch:** taps on the wrist for notifications, and different tap patterns for left and right turns in Apple Maps, so you can navigate without looking.
- **Laptop:** the trackpad "click" on recent MacBooks, which is a haptic, not a moving button.
- **Games:** controller rumble, and the PlayStation 5's triggers that stiffen when you draw a bow.
- **Cars:** a steering wheel or seat that vibrates when you drift out of your lane.

## Designing haptics as a UX/UI designer

You can't feel haptics in a Figma prototype, but you can still design them.

1. **Annotate them.** Add a haptics note to your Hi-Fi screens for each moment that needs one: what triggers it, which haptic, how strong, and what sound and visual go with it.
2. **Use the platform's names.** Write "iOS: notification success" or "Android: confirm" so developers know exactly what to build.
3. **Prototype on a real device when it matters.** Tools such as ProtoPie can trigger vibration on a phone, which is the only way to judge how a haptic really feels.
4. **Know the web's limits.** The browser Vibration API works on Android but not in Safari on iPhone, so haptics on websites, including portfolio sites built in Framer, are very limited. Design for them in apps, not on the web.

**Example haptics note**

| Moment | Trigger | Haptic | Paired with |
| --- | --- | --- | --- |
| Payment complete | Payment succeeds | iOS: notification success | Green tick animation, "Paid" sound |
| Wrong PIN | Third digit mismatch | iOS: notification error | Field shake, red message |
| Choose a time | Picker value changes | iOS: selection | Picker wheel moves |

## Exercise: a haptic audit (15 minutes)

1. Open two apps you use every day and slowly use their main features.
2. Every time you **feel** something, write down the moment, its job (notify, confirm or delight) and its quality (clear, rich or buzzy).
3. Find one moment that **should** have a haptic but doesn't, and one that has a haptic it doesn't need.
4. Write a haptics note (like the table above) for three key moments in your current project.

## 🎥 Media

[https://www.youtube.com/watch?v=-hvClUdSlhA](https://www.youtube.com/watch?v=-hvClUdSlhA)

[https://www.youtube.com/watch?v=cTtc90jCULU](https://www.youtube.com/watch?v=cTtc90jCULU)

[https://www.youtube.com/watch?v=ZBLRzsmLy5w](https://www.youtube.com/watch?v=ZBLRzsmLy5w)

## 📚 Resources

[Playing haptics – Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)

[Haptics design principles – Android Developers](https://developer.android.com/develop/ui/views/haptics/haptics-principles)

[6 Types of Useful Smartwatch Interactions – Nielsen Norman Group](https://www.nngroup.com/articles/smartwatch-interactions/)

## Summary

Haptics let people **feel** an interface. Done well, they are short, crisp and meaningful: they notify, confirm or delight, they match what you see and hear, and they are used sparingly. As a designer, you choose the moments, name the haptic in your specs, and always make sure the experience works without them.
