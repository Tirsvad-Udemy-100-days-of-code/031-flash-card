# Wireframe: Study Flash Cards

_Revision 2026-10-14: the level screen (screen 1) was added for US-001.06. It was drawn by the AI from the use case because the Product Owner gave no wireframe for it; S01 may change it._

The Product Owner gave this screen in the first prompt (the course's target screenshot). The presentation layer implements it and does not redesign it. Source use case: [UC-001](./uc.md).

## Screen 1: Choose your level

```text
+----------------------------------------------------------+   background  #B1DDC6
|   padding 50 px                                          |
|                                                          |
|              Choose your level   (Arial 40 italic)       |
|                                                          |
|                  [   100 words   ]                       |
|                  [  1000 words   ]                       |
|                  [   All words   ]                       |
|                                                          |
+----------------------------------------------------------+
```

| Element | Position | Details |
| --- | --- | --- |
| Window | whole | Same title, padding and background as the card screen |
| Title | row 0 | "Choose your level", Arial 40 italic |
| Level buttons | rows 1 to 3, one column | Labels "100 words", "1000 words", "All words"; Arial 24 bold; white background, equal width |
| After a choice | whole | The screen is replaced by screen 2 on the same window |

## Screen 2: The card

```text
+----------------------------------------------------------+   background  #B1DDC6
|   padding 50 px                                          |
|   +--------------------------------------------------+   |
|   |                                                  |   |
|   |                 Malay        (italic, 40 pt)     |   |   card image 800 x 526
|   |                                                  |   |   card_front.png (white)
|   |                 aku          (bold, 60 pt)       |   |   card_back.png  (green)
|   |                                                  |   |
|   +--------------------------------------------------+   |
|        [ X unknown ]                  [ v known ]        |   buttons: wrong.png, right.png
+----------------------------------------------------------+
```

## Layout

| Element | Position | Details |
| --- | --- | --- |
| Window | whole | Title "Flashy", padding 50 px, background `#B1DDC6` |
| Card | grid row 0, columns 0 and 1 (both) | `Canvas` 800 x 526, one image, two texts |
| Language name | centre of card, y = 150 | Arial 40 italic |
| Word | centre of card, y = 263 | Arial 60 bold |
| Unknown button | grid row 1, column 0 | `wrong.png`, no border |
| Known button | grid row 1, column 1 | `right.png`, no border |

## States

| State | Card image | Language name | Word | Text colour |
| --- | --- | --- | --- | --- |
| Front (first 3000 ms) | `card_front.png` | Malay | the Malay word | black |
| Back (after 3000 ms) | `card_back.png` | Danish | the Danish translation | white |
| Finished | `card_front.png` | (empty) | "Nothing left to learn" | black |
