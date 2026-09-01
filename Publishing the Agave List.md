# Publishing the Agave List

How the online agave menu gets on the web, and how to update it later. Same setup as [[Publishing the Whiskey List]].

## How the pieces connect

```
Printed menu QR  →  lnk.bio/CarnivalBar  →  "Agave List" button  →  mrpaulsagave.netlify.app
```

The QR points at the **link page**, never at the menu directly. If the menu ever moves hosts, you edit one button on the link page and every printed menu still works.

## How it deploys

**The site builds itself from GitHub. Nothing is dragged anywhere.**

This folder is a git repo pushed to `github.com/WilliamBrown555/MrPaulsagave`, and the Netlify project watches its `main` branch. Push to `main` and the live site updates on its own, usually inside a minute.

Netlify settings, as verified Sept 2026 — you should not need to touch these:

| Setting | Value |
|---|---|
| Repository | `github.com/WilliamBrown555/MrPaulsagave` |
| Production branch | `main` |
| Auto publishing | On |
| Base directory | `/` |
| Build command | *empty* |
| Publish directory | `Agave Website` |

**The empty build command matters.** Netlify does not run `build_agave.py`. It takes whatever `Agave Website/index.html` you committed and serves it. So the rebuilt file has to be committed alongside the source change, or you'll push a source edit that never reaches the page.

## Updating the list

Ask Claude for a rebuild, or do it by hand:

1. Edit the bottle data in `source/build_agave.py` — prices must match [[Agave List]]
2. `cd source && python3 build_agave.py`
3. Run the price check in `source/README.md`. It compares the built page against [[Agave List]] and should print five empty lists
4. Commit **both** the source change and the rebuilt `Agave Website/index.html`
5. `git push origin main`
6. Watch the **Deploys** tab. The published commit should move to the one you just pushed

Same URL every time. The QR and the link tree never change.

### If the push is blocked

A Claude cloud session can clone this repo but can't push unless `WilliamBrown555/MrPaulsagave` has been added to that session's authorized sources — otherwise the git proxy returns 403. Add it, or have Claude hand you a patch and apply it here with `git am`, then push from this machine.

A cloud session also can't reach `api.netlify.com` or `*.netlify.app` at all — the sandbox proxy refuses both — so it can't deploy or even load the live page to check it. Anything Netlify has to happen in a browser.

### The manual drop, if you ever need it

**Deploys** tab → drag the `Agave Website` folder onto the drop zone at the bottom. This still works, and it is the right move only if GitHub is down and something must go live now.

Understand the cost: a dropped deploy publishes a build the repo has no record of, so the live site and `main` disagree until the next push quietly overwrites it. Get the change into `main` afterwards.

*(For the record, the original setup was a manual drop at `app.netlify.com/drop`, claimed to the same account as the whiskey list and renamed to `mrpaulsagave`. That's history — the project has been repo-linked since.)*

## Add it to the link page

On **lnk.bio/CarnivalBar**, add a button pointing at `https://mrpaulsagave.netlify.app/`.
Suggested label: **The Agave List** or **Agave List — 45 Bottles**.

Put it next to the whiskey button.

## What's on the page

All 45 bottles from [[Agave List]], in the same three sections and the same alphabetical order as the printed half-fold.

**Maiz Nation Añejo is not on this page** — it's a Mexican whiskey made from heirloom Oaxacan corn, not an agave spirit, so it was pulled. It's still listed under Other Agave in [[Agave List]] and on the printed half-fold; pull it there too on the next reprint, or move it to the whiskey list.

Online-only additions (deliberately not in print):

- **ABV** for every bottle
- **Where it was distilled** — the house, the town and the state
- **What agave and where it grew** — Blue Weber / Los Altos, Espadín / Santiago Matatlán, and so on
- A short flag line where it matters — tahona-crushed, clay-pot still, destilado de agave
- Search across bottle, distillery, town and agave; jump-to-section chips

### Half pours

A half pour is offered only on bottles at or above `HALF_POUR_MIN`, set to **25** at the top of `build_agave.py`. Ten of the forty-five qualify. It's a rule, not a list — change the one number and rebuild.

Every bottle keeps both prices in the data and in [[Agave List]]; the page just doesn't print the half on the cheap ones. Bottles under the line render an empty Half cell rather than shifting left, so every full price stays under the **Full** column header.

### The look

Burgundy `#8c2830` is sampled off the printed PDF and doesn't change. The ground is **"Antique" `#DCD0B3`** — chosen Sept 2026 off a ladder of seven warmer papers, because the printed sheet's `#f3f1ee` read as glare on a screen.

So the web list is **deliberately a warmer, dimmer paper than the printed half-fold**. That's a decision, not drift — don't "fix" it back.

If the ground is ever changed again, four things move with it or the page breaks in ways that are easy to miss: the sticky search bar's fade gradient (`--ground-0`), the search field background (`--inputbg`), the `theme-color` meta tag, and the fill of the inline SVG favicon. The small greys (`--muted`, `--faint`, `--ag`) are also tuned to this ground — dim the paper further without darkening them and the distillery lines are the first thing to go soft. `source/README.md` has the details.

## Two things to check before you send people to it

1. **Sol2Noches is sotol**, not mezcal or raicilla — flagged on the page.
2. **El Popo Avila Reposado's 44%** comes from the brand's blanco spec repeated on the reposado page. Worth a text to the importer to confirm.

Also worth confirming with a bottle in hand: which **5 Sentidos** pechuga is open (Mole Poblano vs Mole Negro — different mezcalero, different state, different ABV), which **La Luna** expression is open, and the batch ABVs on **Real Minero** and **Rey Campero**.

Batch-strength bottles used to carry a **◇** next to the ABV. That marker and its footnote came off the menu in Sept 2026 — those bottles now print their ABV plain, and the number still moves on restock.

## Related

- [[Agave List]]
- [[The Whiskey List]]
- [[Publishing the Whiskey List]]
- [[Brand Colors]]
