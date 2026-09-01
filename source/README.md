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

- **half / full** — the two pour prices, as plain numbers. Must match [[Agave List]].
- **abv** — a string with the `%` on it, so `"50.5%"` works.
- **batch** — `1` puts a ◇ next to the ABV, meaning the bottle is filled at batch strength and the number moves on restock. Use it for single-village mezcal and anything bottled undiluted. `0` otherwise.
- **house** — who made it and where. Distillery or mezcalero, then town, then state.
- **agave** — what it was made from and where that grew.
- **flag** — the small burgundy line under the entry. Leave it `""` for most bottles; it's for things worth calling out (tahona-crushed, additive-free, clay-pot still, destilado de agave). Don't repeat what the bottle name already says — El Guel Sotol doesn't need a "Sotol" flag, Sol2Noches does.

Sections stay alphabetical, matching the printed half-fold. Add a bottle in the right alphabetical spot rather than at the end.

## Checking a rebuild against the printed list

Prices are the thing that goes wrong. This compares the built page to `../Agave List.md` and prints anything that doesn't line up:

```python
import re
src = open('../Agave List.md', encoding='utf-8').read()
ref = {m.group(1).strip().lower(): (int(m.group(2)), int(m.group(3)))
       for m in re.finditer(r'^(.+?) - (\d+) / (\d+)\s*$', src, re.M)}
page = open('../Agave Website/index.html', encoding='utf-8').read()
got = {m.group(1).replace('&#x27;', "'").strip().lower(): (int(m.group(2)), int(m.group(3)))
       for m in re.finditer(r'<span class="nm">(.*?)</span>.*?'
                            r'<span class="p1">(\d+)</span><span class="sl">/</span>'
                            r'<span class="p2">(\d+)</span>', page, re.S)}
print('missing from page:', sorted(set(ref) - set(got)))
print('on page but not in the list:', sorted(set(got) - set(ref)))
print('price mismatches:', [(k, ref[k], got[k]) for k in set(ref) & set(got) if ref[k] != got[k]])
```

All three should print empty. If a bottle shows up as missing from the page, check it wasn't dropped on purpose — Maiz Nation Añejo was pulled from both in Aug 2026 for being a corn whiskey.

## Notes on the build

- **No outside requests.** No web fonts, no CDN, no images — the page is one file that renders the same on bar wifi as on your desk. It uses Helvetica/Arial, which is what the printed menu is set in. Don't add a Google Fonts link.
- **Colors** are sampled off the printed PDF: burgundy `#8c2830` on cream `#f3f1ee`.
- The search box matches on bottle name, house, town, agave and flag — all of it is packed into each row's `data-n` attribute at build time.

## Related

- [[Publishing the Agave List]]
- [[Agave List]]
- [[Publishing the Whiskey List]]
