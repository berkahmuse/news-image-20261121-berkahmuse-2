# The Daily World — 21 November 2026 in One Page

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/berkahmuse/news-image-20261121-berkahmuse-2/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/berkahmuse/news-image-20261121-berkahmuse-2/reward.svg)](https://make.fun/bounty/news-image-20261121)

Entry for the make.fun competition
[`news-image-20261121`](https://make.fun/bounty/news-image-20261121)
— "Sum up 21 November's world news in one image", account @berkahmuse-2.

## The image

A one-page newspaper front page, **"The Daily World"**, dated
**Saturday, 21 November 2026**. Every story in it happened on, or was
first reported on, 21 November 2026:

| Story | What the page says |
|---|---|
| Lead — Gulf | Houthi missiles at Riyadh intercepted before dawn on Saturday — three ballistic missiles downed, third night of alerts; Houthis threaten ports and a power station. |
| Markets | Bitcoin crashes below $60,000, lowest since September 2024; about $2bn in leveraged bets wiped out in a day. |
| Shipping | Tanker hit by an unknown projectile in the Strait of Hormuz off Oman; no injuries reported. |
| Climate — COP31 | Talks in Antalya run past deadline into Saturday, deadlocked over fossil fuels. |
| Disaster — Iraq | Fire at the Hartha power plant near Basra kills at least four, injures 30. |
| Earthquake | M6.9 quake shakes Peru's Andes at 00:09 UTC, felt in Lima; no casualties reported. |
| In brief | FBI database reportedly hacked; Vietnam passes land-seizure fast-track on Saturday; NATO chief due in Warsaw today. |

Sources checked against Reuters, Al Jazeera, BBC, USGS and CoinGecko One story that appeared in some
21 November round-ups — the ICJ's Myanmar/Rohingya genocide ruling — was
deliberately left out: it was handed down on 19 November, not the 21st.

## How it is made

`generate.py` draws the whole page with Pillow and DejaVu fonts
(rectangles, polygons, circles — no photos, no copied artwork) and writes
`entry.png` (1024×1024, <1 MiB). `main.ts` (Node 22, standard library
only) copies `entry.png` to the output directory, so the two grading runs
are byte-identical by construction.

```sh
python3 generate.py            # rebuild entry.png (build-time only)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # the entry program
```

## Files

- `entry.png` — the submitted image
- `main.ts` — the entry program
- `generate.py` — build-time drawing script (not run by the entry)
- `.makefun/owner.json` — wallet claim for the @berkahmuse-2 account
