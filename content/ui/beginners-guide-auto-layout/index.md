# Beginner’s Guide Auto Layout

## What you'll build

A "Share" button with an icon and a label that resizes itself around its content, built with Auto Layout and saved as a component. Auto Layout is what makes Figma designs behave like real code.

## Before you start

- You've finished [Beginner’s Guide to Nesting](beginners-guide-to-nesting.html)
- The Phosphor Icons plugin (step 5 shows you how to find it)
- About 30 minutes

## Let's go

Auto Layout is arguably the best thing you can do if you want to engage in rapid prototyping. 

It’s a major step in understanding how to create amazing uniformity.

We’ll be depending on the 8 Point Grid System for this so please familiarise yourself with that guideline.

Auto layout is closely correlated to components building but we will get to that step shortly. For now let’s learn the basics;

Jesse Showalter is one of the best teachers on Figma I’ve seen and in this video he does an amazing job of bringing you through the process, but if you don’t want to watch it;

 

[https://www.youtube.com/watch?v=Do6HJBj984I](https://www.youtube.com/watch?v=Do6HJBj984I)

I’ll be going through the process as well;

So let’s go!

## 1. Make a Frame

Let’s make a new frame;

![Screenshot 2023-05-26 at 15.47.49.png](Screenshot_2023-05-26_at_15.47.49.png)

And change the name to Button;

![Screenshot 2023-05-26 at 15.47.57.png](Screenshot_2023-05-26_at_15.47.57.png)

Cool! Next we’ll activate **Auto layout;**

## 2. Add Auto layout

**Click the plus icon (+)**

![Screenshot 2023-05-26 at 15.51.58.png](Screenshot_2023-05-26_at_15.51.58.png)

Woo! That was easy! Let’s explain a few things;

![Screenshot 2023-05-26 at 15.51.12.png](Screenshot_2023-05-26_at_15.51.12.png)

Notice here at the bottom we are no longer seeing pixels but rather **Hug x Hug** 

Well, that’s because, with **Auto layout active**, the pixel count size will be determined by the content which we place inside the frame. 

Let’s add some text!

## 3. Add Text

So we’re going click on our frame and then click the text icon;

![Screenshot 2023-05-26 at 15.55.16.png](Screenshot_2023-05-26_at_15.55.16.png)

Or optionally click frame and 

- Text: **`T`**

and voilà! Our entire frame has wrapped around our text!

![Screenshot 2023-05-26 at 15.58.11.png](Screenshot_2023-05-26_at_15.58.11.png)

Let’s type out the word button and change padding!

## 4. Adjust Padding

![Screenshot 2023-05-26 at 15.58.23.png](Screenshot_2023-05-26_at_15.58.23.png)

Nearly there! Hover over the padding in our new Button and see that there has been **default padding added of 10px;**

![Screenshot 2023-05-26 at 16.01.52.png](Screenshot_2023-05-26_at_16.01.52.png)

Let’s change that! Navigate over to the right hand sidebar and let’s align our text content from centre;

![Screenshot 2023-05-26 at 16.03.57.png](Screenshot_2023-05-26_at_16.03.57.png)

Next we’ll change the **horizontal** padding to 16px;

![Screenshot 2023-05-26 at 16.05.14.png](Screenshot_2023-05-26_at_16.05.14.png)

And now the **vertical** padding to 8px;

![Screenshot 2023-05-26 at 16.06.12.png](Screenshot_2023-05-26_at_16.06.12.png)

Well Done! **Basically that’s it**. But let’s step a little further to comprehend some more tools. Let’s change the text and fill colour to give us a cooler look. 

Let’s Jazz it up! 😎

I’ve gone with;

Text: Roboto Regular: ‘Share’ 

Text Colour; White

Fill: #0057FF 

But it can be anything; 

![Screenshot 2023-05-26 at 16.16.07.png](Screenshot_2023-05-26_at_16.16.07.png)

We need to access the plugins library, Phosphor Icons;

## 5. Add Plugin: Phosphor Icons

Right Click to access options panel;

On Windows: 

- Right Click: **`Shift + F10`**

On Mac: 

- Right Click: **`Control + Click`**

![Screenshot 2023-05-26 at 16.19.59.png](Screenshot_2023-05-26_at_16.19.59.png)

Hover over **Plugins**;

Or optionally; Select the Plugins tab from the navigation bar;

![Screenshot 2023-05-26 at 16.24.54.png](Screenshot_2023-05-26_at_16.24.54.png)

We are looking for a plugin called **Phosphor Icons;**

![Screenshot 2023-05-26 at 16.26.16.png](Screenshot_2023-05-26_at_16.26.16.png)

Once you have found it **run the plugin**;

![Screenshot 2023-05-26 at 16.26.29.png](Screenshot_2023-05-26_at_16.26.29.png)

At this stage, you’ll see an icons panel appear; 

![Screenshot 2023-05-26 at 16.26.41.png](Screenshot_2023-05-26_at_16.26.41.png)

Let’s select the ‘share’ icon;

![Screenshot 2023-05-26 at 16.29.12.png](Screenshot_2023-05-26_at_16.29.12.png)

You’ll end up with a position like this;

![Screenshot 2023-05-27 at 10.59.01.png](Screenshot_2023-05-27_at_10.59.01.png)

## 6. Add Icon to Button Layer

You’ll see on the left hierarchical side menu, the icon has been added; 

For best practise, let’s **rename it** to ‘Share Icon’

![Screenshot 2023-05-27 at 11.03.00.png](Screenshot_2023-05-27_at_11.03.00.png)

And drag our ‘Share Icon’ into the button container;

![Screenshot 2023-05-27 at 11.03.19.png](Screenshot_2023-05-27_at_11.03.19.png)

Finally, **delete the ‘ShareNetwork’ layer**

![Screenshot 2023-05-27 at 11.06.16.png](Screenshot_2023-05-27_at_11.06.16.png)

We don’t need it! Well done!

## 7. Change Container Layout Arrangement

![Screenshot 2023-05-27 at 11.07.50.png](Screenshot_2023-05-27_at_11.07.50.png)

Voilà! You’re nearly there; let’s change the direction from **vertical** to **horizontal**;

Make sure your button layer is active;

![Screenshot 2023-05-27 at 11.08.53.png](Screenshot_2023-05-27_at_11.08.53.png)

And change from the vertical ⬇

![Screenshot 2023-05-27 at 11.08.58.png](Screenshot_2023-05-27_at_11.08.58.png)

to the horizontal ➡️

![Screenshot 2023-05-27 at 11.13.58.png](Screenshot_2023-05-27_at_11.13.58.png)

Well Done! Let’s change some properties; 

![Screenshot 2023-05-27 at 11.17.08.png](Screenshot_2023-05-27_at_11.17.08.png)

Change to;

1. ‘Share’ Icon color: White: **#FFFFFF**
2. ‘Share’ Icon size: **w15px x h17px**
3. Text weight: **Semi Bold**
4. Button corner radius: **3px**

![Screenshot 2023-05-27 at 11.23.40.png](Screenshot_2023-05-27_at_11.23.40.png)

Nearly there; let’s just **readjust** the horizontal padding from **16px to 12px**;

**Hover over the empty space** on the left to activate left padding;

![Screenshot 2023-05-27 at 11.25.30.png](Screenshot_2023-05-27_at_11.25.30.png)

and **drag your mouse away from centre** to reduce to **12px**;

![Screenshot 2023-05-27 at 11.29.04.png](Screenshot_2023-05-27_at_11.29.04.png)

**Repeat** on the right hand side;

![Screenshot 2023-05-27 at 11.29.34.png](Screenshot_2023-05-27_at_11.29.34.png)

That’s better! As you can see, you have just reset the left and right padding which are now set to **12px**;

![Screenshot 2023-05-27 at 11.32.04.png](Screenshot_2023-05-27_at_11.32.04.png)

Optionally, you could have used the **Auto layout inputs.** Both work!

## 8. Convert Button to Component

For best practise, let’s just change our button to a component 

![Screenshot 2023-05-27 at 11.40.11.png](Screenshot_2023-05-27_at_11.40.11.png)

Or On Windows:

- Convert to Component: **`Ctrl + Alt + K`**

On Mac: 

- Convert to Component: **`Option + Cmd + K`**

![Screenshot 2023-05-27 at 11.34.34.png](Screenshot_2023-05-27_at_11.34.34.png)

**And you’re all done!** 

One last thing; On the left hand panel change from Layers Mode

**Change to Assets Mode** 

![Screenshot 2023-05-27 at 11.40.47.png](Screenshot_2023-05-27_at_11.40.47.png)

**Drag your component** from your assets panel. Always Remember to Work Non Destructively 🍀; 

![Screenshot 2023-05-27 at 11.45.37.png](Screenshot_2023-05-27_at_11.45.37.png)

**Always preserve the original master component** and edit copied versions only;

## Well done!

Auto layout is a great lesson to learn in Figma. It will speed up your workflow by months and ensure  great crisp symmetry for all your assets  

 

Now why not get creative! **Go have some fun 🤗.** Make some cool components using auto layout!

You can now:

- Add Auto Layout to a frame and set its padding and direction
- Add icons with a plugin and nest them inside the button
- Convert a button to a component and use instances of it

**Next:** [Beginner’s Guide to the 8 Point Grid System](beginners-guide-to-8-point-grid-system.html)
