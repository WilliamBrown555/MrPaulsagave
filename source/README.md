# Agave list — source

What builds `../Agave Website/index.html`. Two files, no dependencies beyond Python 3.

| File | What it is |
|---|---|
| `build_agave.py` | The whole thing — bottle data, prices, ABV, distillery and agave lines, plus the HTML and CSS template |
| `crest.svg` | The Mr. Paul's crest, inlined into the page footer at build time |

## Rebuilding

```
python3 build_agave.py
```

Writes `Agave Website/index.html` and prints the bottle count. Then drag the `Agave Website` folder onto the deploy drop zone for the **mrpaulsagave** project on Netlify — see [[Publishing the Agave List]].

`build_agave.py` expects `crest.svg` next to it. If you move the folder, fix the `CREST = open(...)` path at the top.

## Editing bottles

Three lists near the top — `T` (Tequila), `M` (Mezcal), `O` (Other Agave). One tuple per bottle, in this order:

```python
("Arette Reposado", 8, 15, "40%", 0, "Tequila Arette · Tequila, Jalisco", "Blue Weber · Los Valles", "")
#  name             half full abv  batch  house · town, state              agave · region           flag
```

- **half / full** — the two pour prices, as plain numbers. Must match [[Agave List]]. Keep the half price on every bottle even when it won't print — see *Half pours* below.
- **abv** — a string with the `%` on it, so `"50.5%"` works.
- **batch** — kept in the data but no longer printed. It used to put a ◇ next to the ABV; that marker and its footnote came off the menu in Sept 2026, so batch-strength bottles now show their ABV plain.
- **house** — who made it and where. Distillery or mezcalero, then town, then state.
- **agave** — what it was made from and where that grew.
- **flag** — the small burgundy line under the entry. Leave it `""` for most bottles; it's for things worth calling out (tahona-crushed, clay-pot still, destilado de agave). Additive-free is *not* one of them — those flags came off in Sept 2026, so don't put them back. Don't repeat what the bottle name already says — El Guel Sotol doesn't need a "Sotol" flag, Sol2Noches does.

Sections stay alphabetical, matching the printed half-fold. Add a bottle in the right alphabetical spot rather than at the end.

## Half pours

Same rule as the whiskey list: a half pour is offered only on bottles at or above `HALF_POUR_MIN`, set to `25` at the top of `build_agave.py`. Ten of the forty-five qualify today.

It's a rule, not a list — change the one number and rebuild, and nothing else needs touching. Every bottle keeps both prices in the data and in [[Agave List]]; the build just doesn't print the half. Bottles under the line render an empty Half cell rather than shifting left, so every full price stays under the **Full** column header.

## Checking a rebuild against the printed list

Prices are the thing that goes wrong. This compares the built page to `../Agave List.md` and prints anything that doesn't line up:

```python
import re
# read the threshold out of the script rather than importing it — importing
# build_agave would rebuild the page as a side effect
HALF_POUR_MIN = int(re.search(r'^HALF_POUR_MIN\s*=\s*(\d+)',
                              open('build_agave.py', encoding='utf-8').read(), re.M).group(1))
src = open('../Agave List.md', encoding='utf-8').read()
ref = {m.group(1).strip().lower(): (int(m.group(2)), int(m.group(3)))
       for m in re.finditer(r'^(.+?) - (\d+) / (\d+)\s*$', src, re.M)}
page = open('../Agave Website/index.html', encoding='utf-8').read()
# p1 is empty on bottles under HALF_POUR_MIN, so half comes back as None there.
got = {m.group(1).replace('&#x27;', "'").strip().lower():
           (int(m.group(2)) if m.group(2) else None, int(m.group(3)))
       for m in re.finditer(r'<span class="nm">(.*?)</span>.*?'
                            r'<span class="p1">(\d*)</span><span class="sl">/?</span>'
                            r'<span class="p2">(\d+)</span>', page, re.S)}
print('missing from page:', sorted(set(ref) - set(got)))
print('on page but not in the list:', sorted(set(got) - set(ref)))
print('full-price mismatches:',
      [(k, ref[k][1], got[k][1]) for k in set(ref) & set(got) if ref[k][1] != got[k][1]])
print('half-price mismatches:',
      [(k, ref[k][0], got[k][0]) for k in set(ref) & set(got)
       if got[k][0] is not None and ref[k][0] != got[k][0]])
print('half shown/hidden wrongly:',
      [k for k in set(ref) & set(got)
       if (got[k][0] is not None) != (ref[k][1] >= HALF_POUR_MIN)])
```

All five should print empty. If a bottle shows up as missing from the page, check it wasn't dropped on purpose — Maiz Nation Añejo was pulled from both in Aug 2026 for being a corn whiskey.

## Notes on the build

- **No outside requests.** No web fonts, no CDN, no images — the page is one file that renders the same on bar wifi as on your desk. It uses Helvetica/Arial, which is what the printed menu is set in. Don't add a Google Fonts link.
- **Colors.** Burgundy `#8c2830` is sampled off the printed PDF and does not change. The ground no longer is: the print sheet's `#f3f1ee` read as glare on a screen, so in Sept 2026 Bill picked **"Antique" `#DCD0B3`** from a ladder of seven warmer papers. The web list is deliberately a warmer, older paper than the printed half-fold.
- **Changing the ground.** Everything derived from it lives in the `:root` block — `--panel` and `--panel-2` (row hover), `--inputbg` (search field), and `--ground-0`, which is the same colour at zero alpha and must be kept in step or the sticky header fades to the wrong shade. `--muted`, `--faint` and `--ag` are the small greys; they were darkened to hold the same contrast on this paper that `#7b7369` and `#948b80` held on the old one. Dim the ground further without darkening them and the distillery lines are the first thing to go soft.
- The search box matches on bottle name, house, town, agave and flag — all of it is packed into each row's `data-n` attribute at build time.

## Related

- [[Publishing the Agave List]]
- [[Agave List]]
- [[Publishing the Whiskey List]]
