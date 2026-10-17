title: Colour Values
promise: How screens make colour, and the formats you'll use to hand colour from Figma to code.
duration: 15 minutes
topics:
- How screens make colour: light and RGB
- HEX: the designer's everyday format
- RGB and RGBA in CSS
- HSL: tints and shades the easy way
- CMYK: why print looks different
- Grayscale and gradients
---
@title
# Colour Values
How screens make colour, and the formats you'll use to hand colour from Figma to code.
---
@split
## Colour is light

![The visible light spectrum, from violet at 400 nanometres to red at 700](Visible-Light-Spectrum.png)

Everything you design is seen as **light**.

Screens make every colour by mixing three lights: **red, green and blue**.

Colour values are just a precise way of writing down how much of each.
---
@cards
## Five formats you'll meet

- **HEX** `#FF0000`: the everyday format in Figma and CSS
- **RGB** `rgb(255, 0, 0)`: red, green and blue from 0 to 255
- **HSL** `hsl(0, 100%, 50%)`: hue, saturation, lightness
- **CMYK** `0, 100, 100, 0`: ink for print only
- **Named** `red`: handy in code, too limited for design
---
@split
## HEX

![Pure red, green and blue as HEX: #FF0000, #00FF00, #0000FF](HEX_Values.png)

A hash and **six characters**: `#RRGGBB`.

Each pair is one light, from `00` (off) to `FF` (full).

`#FF0000` = full red, no green, no blue.
---
@split
## Mixing light

![Yellow, cyan and magenta made by mixing two lights at full strength](RGBValues-2.png)

Light mixes **additively**: add lights together and you get brighter colours.

- Red + green = **yellow** `#FFFF00`
- Green + blue = **cyan** `#00FFFF`
- Red + blue = **magenta** `#FF00FF`
- All three = **white** `#FFFFFF`
---
@split
## RGB and RGBA

![Figma's colour picker switched to RGB: 0, 255, 0](Screenshot_2024-05-18_at_10.40.50.png)

The same three lights as numbers from **0 to 255**: `rgb(0, 255, 0)`.

Add a fourth value, **alpha**, for transparency: `rgba(0, 255, 0, 0.5)` is 50% see-through.

Figma's picker switches between formats from the dropdown.
---
@split
## HSL

![Pure red, green and blue written in HSL](HEX_Values-2.png)

**Hue** (0–360° around the colour wheel), **saturation** (0–100%) and **lightness** (0–100%).

Its superpower: change only the **lightness** to make tints and shades of one colour for a design system.

`hsl(24, 100%, 50%)` → `hsl(24, 100%, 85%)`
---
@statement
If your colours look dull, you're probably in CMYK.

CMYK is for print: ink **subtracts** light from white paper, so it can't reach the brightest screen colours.
---
@split
## Grayscale

![A grayscale ramp from black #000000 to white #FFFFFF](RGBValues-1.png)

When red, green and blue are **equal**, you get a grey.

That's why mid-fi wireframes are grey: no colour to distract from layout and function.
---
@split
## Gradients

![Sho Shibuya's sunrise painted over a New York Times front page](sho-shibuya-nyt-sunrise_june-7-2020.jpg)

A smooth blend between two or more colours.

Every morning the artist **Sho Shibuya** paints the sunrise over the front page of *The New York Times*: a gradient as a diary.

Figma offers linear, radial, angular and diamond gradients.
---
@text
## Handing colour to a developer

Your developer can paste any of these straight into CSS:

`color: #FF6100;`
`color: rgb(255, 97, 0);`
`color: hsl(23, 100%, 50%);`
`color: rgba(255, 97, 0, 0.5);`

Pick **one format for the whole project** and save every colour as a Figma style or variable.
---
@exercise
## Crack the code

1. What colour is `#00FF00`?
2. Write pure blue in RGB.
3. Mix red and green light at full strength: what HEX do you get?
4. Your brand orange is `hsl(24, 100%, 50%)`. Write a lighter tint.
5. The client's printed poster looks duller than the screen. Why?
---
@answers
## Check yourself

1. Pure **green**: no red, full green, no blue.
2. `rgb(0, 0, 255)`
3. `#FFFF00`, **yellow**.
4. Keep hue and saturation, raise lightness: for example `hsl(24, 100%, 80%)`.
5. Print uses **CMYK** ink, which subtracts light and can't reach bright screen colours.
