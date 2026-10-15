#!/usr/bin/env python3
"""独白 `（…）` の全数一覧と、語の並びの重なりを見る器。

    python3 独白の一覧.py            # 話ごとの数と、全数を印字
    python3 独白の一覧.py --骨        # 句読点の骨が同じものを、組にして出す
    python3 独白の一覧.py --近い      # 生の字面が近い組を出す

## なぜ要るか

独白は 2026-10-15 の会話劇 Upgrade で入った、**この作品に初めて現れた記号**である。
担き手は一話ずつ独立に書く——ゆえに、**同時に走った二話が同じ手に落ちる**。

    〔実測〕`01-04`「（あとが、二つある。）」と `01-09`「（あと、二つである。）」
    〔実測〕`03-14`「（この棚に、置く。）」と `03-15`「（上のほうへ、書く。）」

**⛔ 禁じるのは形ではなく語である**（作法 §1 原則12）。だが、**語だけ違って型が同じ**なら、
読者には同じ手の二度目に見える。**ゆえに、型の重なりも見る。**

## 二つの見方

- **骨**——句読点と括弧だけ残し、他の字を `・` に置き換えたもの。
  `（上のほうへ、書く。）` → `（・・・・・、・・。）`
  ⚠ これは**候補を挙げるだけの道具**である。短い独白ほど、偶然同じ骨になる。
- **近い**——字面そのものの `difflib` ratio。0.70 以上を組にする。

⚠ どちらも**判定ではない**。人が読んで、同じ手かどうかを決める。
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
DRAFT = WORK / "草稿"
MONO_RE = re.compile(r"^（.*）$")


def collect():
    """[(話, 行番号, 独白の文)]"""
    out = []
    for p in sorted(DRAFT.glob("draft_*.md")):
        num = p.name.split("_")[1]
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
            s = line.strip()
            if MONO_RE.match(s):
                out.append((num, i, s))
    return out


def skeleton(s):
    """句読点・括弧だけ残し、他の字を `・` に。数字と英字も `・` に畳む。"""
    keep = "（）、。！？…「」"
    return "".join(c if c in keep else "・" for c in s)


def groups(rows, key):
    d = {}
    for num, i, s in rows:
        d.setdefault(key(s), []).append((num, i, s))
    return {k: v for k, v in d.items() if len(v) > 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--骨", action="store_true")
    ap.add_argument("--近い", action="store_true")
    a = ap.parse_args()

    rows = collect()
    by_ep = {}
    for num, _, _ in rows:
        by_ep[num] = by_ep.get(num, 0) + 1
    print(f"■ 独白 {len(rows)}行／{len(by_ep)}話（63話のうち）")
    if not (a.骨 or a.近い):
        for num, i, s in rows:
            print(f"  {num}:{i}\t{s}")
        print("\n  話ごとの数——" + "  ".join(
            f"{k}:{v}" for k, v in sorted(by_ep.items())))

    if a.骨:
        g = groups(rows, skeleton)
        print(f"\n■ 骨が同じ組 {len(g)}組（⚠ 候補であって判定ではない）")
        for k, v in sorted(g.items(), key=lambda kv: -len(kv[1])):
            eps = {n for n, _, _ in v}
            if len(eps) < 2:          # 同じ話の中の重なりは、担き手が自分で見た
                continue
            print(f"\n  {k}")
            for n, i, s in v:
                print(f"    {n}:{i}  {s}")

    if a.近い:
        print("\n■ 字面が近い組（ratio ≥ 0.70・別の話どうし）")
        n = 0
        for x in range(len(rows)):
            for y in range(x + 1, len(rows)):
                nx, ix, sx = rows[x]
                ny, iy, sy = rows[y]
                if nx == ny:
                    continue
                r = difflib.SequenceMatcher(None, sx, sy).ratio()
                if r >= 0.70:
                    n += 1
                    print(f"  r={r:.2f}  {nx}:{ix} {sx}   ×   {ny}:{iy} {sy}")
        if not n:
            print("  （なし）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
