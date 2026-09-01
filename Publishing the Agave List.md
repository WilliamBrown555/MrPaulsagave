# Publishing the Agave List

How the online agave menu gets on the web, and how to update it later. Same setup as [[Publishing the Whiskey List]].

## How the pieces connect

```
Printed menu QR  →  lnk.bio/CarnivalBar  →  "Agave List" button  →  mrpaulsagave.netlify.app
```

The QR points at the **link page**, never at the menu directly. If the menu ever moves hosts, you edit one button on the link page and every printed menu still works.

## Setting it up

The whole site is one file: `Agave Website/index.html` in this folder. No images, no stylesheets, no fonts — nothing loads from outside the file, so it works on bad bar wifi.

1. Go to **app.netlify.com/drop**
2. Drag the **`Agave Website` folder** onto the drop zone — the whole folder, not the file inside it
3. It's live immediately at a random address
4. Click **Claim your site** — sign in with the same account the whiskey list is on. **Don't skip this**; unclaimed sites get deleted
5. **Site configuration → Change site name** → `mrpaulsagave`

Final URL: `https://mrpaulsagave.netlify.app`

## Add it to the link page

On **lnk.bio/CarnivalBar**, add a button pointing at `https://mrpaulsagave.netlify.app/`.
Suggested label: **The Agave List** or **Agave List — 45 Bottles**.

Put it next to the whiskey button.

## Updating the list later

Ask Claude for a rebuild, then:

1. Replace `Agave Website/index.html` with the new file
2. In Netlify: **Deploys** tab → drag the `Agave Website` folder onto the drop zone at the bottom

Same URL, updated in about 10 seconds. The QR and the link tree never change.

## What's on the page

All 45 bottles from [[Agave List]], in the same three sections and the same alphabetical order as the printed half-fold. Same burgundy-on-cream look as the print piece.

**Maiz Nation Añejo is not on this page** — it's a Mexican whiskey made from heirloom Oaxacan corn, not an agave spirit, so it was pulled. It's still listed under Other Agave in [[Agave List]] and on the printed half-fold; pull it there too on the next reprint, or move it to the whiskey list.

Online-only additions (deliberately not in print):

- **ABV** for every bottle
- **Where it was distilled** — the house, the town and the state
- **What agave and where it grew** — Blue Weber / Los Altos, Espadín / Santiago Matatlán, and so on
- A short flag line where it matters — tahona-crushed, additive-free, clay-pot still, destilado de agave
- Search across bottle, distillery, town and agave; jump-to-section chips

A **◇** next to the ABV means the bottle is filled at batch strength and the number moves on restock — same idea as BP on the whiskey list.

## Two things to check before you send people to it

1. **Sol2Noches is sotol**, not mezcal or raicilla — flagged on the page.
2. **El Popo Avila Reposado's 44%** comes from the brand's blanco spec repeated on the reposado page. Worth a text to the importer to confirm.

Also worth confirming with a bottle in hand: which **5 Sentidos** pechuga is open (Mole Poblano vs Mole Negro — different mezcalero, different state, different ABV), which **La Luna** expression is open, and the batch ABVs on **Real Minero** and **Rey Campero**.

## Related

- [[Agave List]]
- [[The Whiskey List]]
- [[Publishing the Whiskey List]]
- [[Brand Colors]]
