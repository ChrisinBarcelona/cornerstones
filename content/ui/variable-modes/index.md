# Variable Modes

## What you'll build

An interactive product page where hovering over a colour swatch switches the shoe to that colour, using variable modes and a Set variable mode interaction.

## Before you start

- You've finished [String Variables](string-variables.html)
- The shoe images (download them in step 1)
- About 45 minutes

## Let's go

1. Create a component set with 5 product images inside
    
    ![Screenshot 2025-12-22 at 12.54.08.png](Screenshot_2025-12-22_at_12.54.08.png)
    
    [Shoe Collection.zip](Shoe_Collection.zip)
    

1. Name the component set
    
    ![Screenshot 2025-12-22 at 13.07.22.png](Screenshot_2025-12-22_at_13.07.22.png)
    

1. Set the **name** and **values** for each component 
    
    ![Screenshot 2025-12-22 at 13.07.55.png](Screenshot_2025-12-22_at_13.07.55.png)
    

1. **Create** 5 colour swatches for each colour. 
    
    ![Screenshot 2025-12-22 at 13.11.35.png](Screenshot_2025-12-22_at_13.11.35.png)
    

1. Create multiple components 
    
    ![Screenshot 2025-12-22 at 13.13.39.png](Screenshot_2025-12-22_at_13.13.39.png)
    

1. Create some sort of design that you are happy with (optional)
    
    ![Screenshot 2025-12-22 at 13.15.57.png](Screenshot_2025-12-22_at_13.15.57.png)
    

7. Create a variable collection with the following modes. **Make sure it is a string!** 

| **Name** | **Shoe Colour (Default)** | **Shoe Colour (Orange)** | **Shoe Colour (Black)** | **Shoe Colour (Lime)** | **Shoe Colour (Blue)** |
| --- | --- | --- | --- | --- | --- |
| Shoe Color | Pink | Orange | Black | Lime  | Blue |

![Screenshot 2025-12-22 at 13.21.39.png](Screenshot_2025-12-22_at_13.21.39.png)

8. Switch to prototype mode, select the first colour swatch, click the add action

![Screenshot 2025-12-22 at 13.19.26.png](Screenshot_2025-12-22_at_13.19.26.png)

1. Create the following interaction design
    
    ![Screenshot 2025-12-22 at 13.27.16.png](Screenshot_2025-12-22_at_13.27.16.png)
    

While hovering → 

Action: **Set variable mode**
Collection: **Variable Collection**
Mode: **Shoe Colour (*insert the correct colour*)**

1. IMPORTANT! Attach the child instance to the variable to get them talking 
    
    ![Screenshot 2025-12-22 at 14.21.35.png](Screenshot_2025-12-22_at_14.21.35.png)
    

![Screenshot 2025-12-22 at 14.21.45.png](Screenshot_2025-12-22_at_14.21.45.png)

[https://embed.figma.com/proto/pi4ilR8QSufcObFDMI60UU/Untitled?node-id=9-92&t=pO67wR4NyYRGOZMj-1&embed-host=notion&footer=false&theme=system](https://embed.figma.com/proto/pi4ilR8QSufcObFDMI60UU/Untitled?node-id=9-92&t=pO67wR4NyYRGOZMj-1&embed-host=notion&footer=false&theme=system)

## Well done!

You can now:

- Create a variable collection with several modes
- Link component variants to a string variable
- Switch modes in a prototype with the Set variable mode action

That's the last Figma lesson. Mark it complete to reach the Figma Advanced milestone.
