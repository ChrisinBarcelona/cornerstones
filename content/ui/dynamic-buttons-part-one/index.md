# Dynamic Buttons Part One

### Intro:

This is an easy lesson but **the first thing** is that it requires understanding three key principals.

- **Text Property**
- **Appearance Booleans**
- **Swaps**

**The second thing** you have to understand is that the parent component and the child component are very different. The rule is that the parent is where you load in the properties and the child is what you use.

On the right hand panel of Figma you will see two very different CSM’s: for all parents and children

![Parent.jpg](Parent.jpg)

This is the parent

![Child.jpg](Child.jpg)

The is the child

That being said, let’s get into it.

1. Use the text element and write out the word ‘Button’
    
    ![Screenshot 2026-01-06 at 15.59.33.png](Screenshot_2026-01-06_at_15.59.33.png)
    
    Screenshot 2026-01-06 at 15.59.33.png
    
2. Press `Shift + A` to wrap an auto layout frame around the text. Change the title to Button
    
    ![Screenshot 2026-01-06 at 15.59.55.png](Screenshot_2026-01-06_at_15.59.55.png)
    
3. Add a stroke to the button
    
    ![Screenshot 2026-01-06 at 16.01.59.png](Screenshot_2026-01-06_at_16.01.59.png)
    
4. Open the actions panel from the bottom of Figma and run **Phosphors Icons**

![Screenshot 2026-01-06 at 16.02.47.png](Screenshot_2026-01-06_at_16.02.47.png)

Screenshot 2026-01-06 at 16.02.47.png

1. Import **8 Icons**
- House
- User Circle
- Gear
- PlusCircle
- ArrowCircleUp
- ArrowCircleDown
- ArrowCircleRight
- ArrowCircleLeft

![Screenshot 2026-01-06 at 16.05.25.png](Screenshot_2026-01-06_at_16.05.25.png)

1. Select all icons and create ’**Multiple Components’**. Be careful not to make just one component or a component set.
    
    ![Screenshot 2026-01-06 at 16.08.31.png](Screenshot_2026-01-06_at_16.08.31.png)
    

![Screenshot 2026-01-06 at 16.09.41.png](Screenshot_2026-01-06_at_16.09.41.png)

1. Pressing `Command + G` on mac or `Control + G` on windows, make two groups, changing the name on the left hand panel to
- Navbar Icons
- Orientation Icons
    
    ![Screenshot 2026-01-06 at 16.11.18.png](Screenshot_2026-01-06_at_16.11.18.png)
    
1. Drop an Icon from each set before and after the text
    
    ![Screenshot 2026-01-06 at 16.13.48.png](Screenshot_2026-01-06_at_16.13.48.png)
    
2. Turn to a component
    
    This concludes the build. Now we will apply the text property.
    
    ![Screenshot_2026-01-06_at_16.14.52.png](Screenshot_2026-01-06_at_16.14.52.png)
    
    This concludes the build. Now we will apply the text property.
    
    ### Apply Text Property
    
    This means we specifically target the text on the **parent.**
    
    **10. Press the ‘Apply variable/property’**
    
    ![Screenshot 2026-01-06 at 16.18.25.png](Screenshot_2026-01-06_at_16.18.25.png)
    
3. Press the **+** icon which will make a new variable/property
    
    ![Screenshot 2026-01-06 at 16.18.33.png](Screenshot_2026-01-06_at_16.18.33.png)
    
4. Create the following property:
- Name: **Label**
- Value: **Continue**

![Screenshot 2026-01-06 at 16.22.41.png](Screenshot_2026-01-06_at_16.22.41.png)

1. You will know you have **successfully applied the property if** the word ‘Button’ has changed to ‘Continue’

![Screenshot 2026-01-06 at 16.23.58.png](Screenshot_2026-01-06_at_16.23.58.png)

It’s important to know that you have applied the text property to the parent component. The child component will look like this:

![Parent component has a frame tag with 4 purple diamonds. Child has no frame tag title.](Screenshot_2026-01-06_at_16.25.37.png)

Parent component has a frame tag with 4 purple diamonds. Child has no frame tag title.

### Appearance Booleans

⚠️ Working on the parent component ⚠️

1. Select the text element. We are going to apply another property but this time it will be on the appearance.

![Screenshot 2026-01-06 at 16.28.18.png](Screenshot_2026-01-06_at_16.28.18.png)

1. Press the plus Icon and make the following property.

![Screenshot 2026-01-06 at 16.29.17.png](Screenshot_2026-01-06_at_16.29.17.png)

![Screenshot 2026-01-06 at 16.29.42.png](Screenshot_2026-01-06_at_16.29.42.png)

1. Test on the child component to make sure the appearance boolean has been applied correctly.
    
    ![Screenshot 2026-01-06 at 16.30.53.png](Screenshot_2026-01-06_at_16.30.53.png)
    
2. Repeat this process on both icons until you are left with this property panel on the child element.

![Screenshot 2026-01-06 at 16.35.06.png](Screenshot_2026-01-06_at_16.35.06.png)

### Swaps

This is the last part of the exercise. We are going to apply a swap property to both icons, again, ⚠️ Working on the parent component ⚠️

1. Select the Back Icon and create instance swap property

![Screenshot 2026-01-06 at 16.37.21.png](Screenshot_2026-01-06_at_16.37.21.png)

1. Give the name ‘**Back Icon**’

![Screenshot 2026-01-06 at 16.38.05.png](Screenshot_2026-01-06_at_16.38.05.png)

1. Repeat the process on the front icon but calling the swap property **‘- Front Icon’**

![Screenshot 2026-01-06 at 16.39.07.png](Screenshot_2026-01-06_at_16.39.07.png)

The child component should look a little something like this:

![Screenshot 2026-01-06 at 16.40.11.png](Screenshot_2026-01-06_at_16.40.11.png)

1. Select the parent and switch the order on properties

![Screenshot 2026-01-06 at 16.42.03.png](Screenshot_2026-01-06_at_16.42.03.png)

Order on child element should look like this:

![Screenshot 2026-01-06 at 16.42.34.png](Screenshot_2026-01-06_at_16.42.34.png)

## All Done!

![Screenshot 2026-01-06 at 16.43.54.png](Screenshot_2026-01-06_at_16.43.54.png)
