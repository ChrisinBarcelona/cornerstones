# Beginner’s Guide to Prototyping

## What you'll build

A clickable prototype of a three-screen flow that you can test on your phone: tap a card, open its detail screen, open a bottom sheet over it and come back. Prototypes are how you test a design with real people before anyone writes code.

## Before you start

- You've finished [Beginner’s Guide to Components](beginners-guide-to-components.html)
- Three screens from your project, built from components, in iPhone 16 frames
- The Figma app on your phone (optional, for testing on a real device)
- About 1 hour

## Let's go

Everything in this guide happens in the **Prototype** tab of the right-hand panel. Switch to it, select a layer, and a small **+** appears on its edge. Drag that **+** onto another frame and you have made a **connection**: the blue arrow, or "noodle", that tells Figma what happens when someone interacts.

Every connection has three parts:

| Part | Question it answers | Examples |
| --- | --- | --- |
| **Trigger** | What does the user do? | On tap, On drag, While hovering, After delay |
| **Action** | What happens? | Navigate to, Back, Open overlay, Scroll to, Change to |
| **Animation** | How does it move? | Instant, Dissolve, Move in, Push, Smart animate |

Watch one of these first if you prefer to see it done:

[https://www.youtube.com/watch?v=-op0gbWrmCY](https://www.youtube.com/watch?v=-op0gbWrmCY)

[https://www.youtube.com/watch?v=1ucLq6JTxac](https://www.youtube.com/watch?v=1ucLq6JTxac)

## Step by step

1. **Set a starting point.** Select your first screen. In the Prototype tab, click **+** next to **Flow starting point** and give the flow a name, such as "Browse".
2. **Navigate forward.** Select a card on the first screen, drag its **+** onto the detail screen, and set *On tap → Navigate to → Smart animate*, 300 ms, *Ease out*.
3. **Go back.** Select the back arrow on the detail screen, add an interaction and set *On tap → Back*. Back always returns to wherever the user came from.
4. **Open an overlay.** Build the bottom sheet as its own frame. Connect a button on the detail screen to it with *On tap → Open overlay*, position **Bottom center**, tick **Close when clicking outside** and **Add background behind overlay**, and animate it with *Move in* from the bottom.
5. **Make it scroll.** Make the detail frame taller than the screen, select it, and under **Overflow** choose **Vertical**. Select the navigation bar and set its position to **Fixed** so it stays put while the content scrolls.
6. **Make a component interactive.** Open your button component set. Connect the *Default* variant to the *Pressed* variant with *While pressing → Change to*. Every instance of that button now reacts on its own, on every screen.
7. **Smart animate a change.** Duplicate a screen, move or resize one layer, keep its **layer name** the same, and connect the two with *Smart animate*. Figma animates every layer whose name matches.
8. **Present and test.** Click the **Play** button in the toolbar to present the flow. To try it on a phone, open the file in the Figma app, or share the prototype link and open it in your phone's browser.
9. **Share it.** Click **Share prototype**, set who can view, and copy the link for your usability test.

## Tips

- Name your frames clearly ("01 Home", "02 Detail"): those are the names you'll pick from in every dropdown.
- Keep animations between **200 and 400 ms**. Slower feels sluggish; faster feels broken.
- Only prototype the paths your test needs. A prototype is a test tool, not the finished app.
- If Smart animate jumps instead of moving, the layer names don't match.

## Well done!

You can now:

- Connect frames with triggers, actions and animations
- Use Back, overlays and scrolling to make a flow feel real
- Make components interactive and animate changes with Smart animate
- Present and share a prototype for testing

**Next:** [Navbar](navbar.html)
