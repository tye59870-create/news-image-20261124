# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/tye59870-create/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/tye59870-create/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A single front page for Tuesday 24 November 2026. The lead is Jensen
Huang's return as Nvidia chief executive — shares up 31% on the day —
with four more stories below it: Ukraine's sea drones sinking a Russian
corvette off Libya, Iran claiming missiles that can reach Europe, the
evacuation of a Manchester arena show, and Kim Jong Un ignoring Trump's
overtures. A ticker along the bottom carries the rest of the day.

## How to run

```sh
python3 main.py            # writes /output/entry.png
python3 main.py --out x.png   # write somewhere else instead
```

`build_image.py` draws the page with Pillow (no network, no input
files). The finished PNG is stored in the repository as `entry.png.b64`
so the tree stays plain text; `main.py` decodes it, checks it is a
1024×1024 PNG under 1 MiB, and writes it out. Running it twice writes
the same bytes both times.

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
