#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文の長さを数える——第八段階（流す）の**物差し**（読み取り専用）。

**何を測るか。** 設計は「短文（切る）と長文（流す）の配分でリズムを作る」
（`../構想/design.md:81`）と定めている。**この器は、その配分を、そのまま数える。**

**⚠ 数え方（この段の主張は、この鍵の上にしか立たない）。**

- 対象＝`examples/habits-0*/草稿/draft_*.md`（`草稿/draft.md` の合本は数えない）。
- **本文行**＝空行・`#` で始まる行・題を除いた行。**`＊` は含む**（1行1字ゆえ、**文としても数える**）。
  **段落＝この一行である。**
- **文＝`。` だけで切る。** ⚠ **`？！` では切らない**——**この作品の `！` は、文末ではない**。
  第四巻に 24個あり、**すべて四条の「！」（記名の三点）という、物を指す字である**
  （`04-16:15`「欄の中に！がある。」）。**文末の `？`・`！` は、四巻とも 0本**（〔実測 2026-10-14〕
  `grep -h "[？！]$"`＝0）。**`[。？！]` で切ると、第四巻だけが 6文、多く出る。**
  ⚠ **`検査/check.py` の `SENTENCE_END` は `[。？！]` である**——**あちらは、この器と単位が違う**
  （あちらの目的は逐語の再利用であり、`！` の側は、あちらでも見る）。
- **字数＝空白と Cf を除いた字数**（記号は数える）。
- 長文の閾値は 20／25／30／40 字。**平均と sd は、文ごとの字数の、単純なものである。**

⚠ **この鍵で、材料 §2 の数が、一字も違わず再現する**（2026-10-14 実測。本文行 2,685＋2,635＋2,256＋1,385
＝8,961は `＊` 126 を含む＝**この器の「本文行＋`＊`」と一致**。文 20,905・≥20字 94・≥25字 15・
≥30字 6・4文以上 928）。

    python3 文の長さを数える.py            # 四巻と、全体
    python3 文の長さを数える.py -v 01      # 第一巻だけ
    python3 文の長さを数える.py -v 01 --long   # 30字以上の文を、座標つきで全部
    python3 文の長さを数える.py --root <dir>   # **当てる前の木**を指して測る（`habits-0N/草稿/` を持つ木）

⚠ **この器は、本文を一度も書き換えない。**
"""
import glob
import os
import re
import statistics
import sys
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
EX = os.path.dirname(os.path.dirname(ROOT))          # examples/
RULE = "＊"
TITLE = re.compile(r"^#\s+第\d+話")
THRESHOLDS = (20, 25, 30, 40)
LONG = 30


def chars(s):
    return sum(1 for c in s if not c.isspace() and unicodedata.category(c) != "Cf")


def sentences(para):
    """⚠ **`。` だけで切る**——`！` は、この作品では文末ではない（第四巻の「！」は物を指す字）。"""
    return [x + "。" for x in re.split(r"。", para) if x.strip()]


def body_lines(path):
    out = []
    for i, line in enumerate(open(path, encoding="utf-8").read().split("\n"), start=1):
        s = line.strip()
        if not s or s.startswith("#") or TITLE.match(s):
            continue
        out.append((i, s))
    return out


def episodes(vol=None):
    out = []
    for p in sorted(glob.glob(os.path.join(EX, "habits-0*", "草稿", "draft_*.md"))):
        if os.path.basename(p) == "draft.md":
            continue
        ep = os.path.basename(p)[6:11]
        if vol is None or ep.startswith(vol):
            out.append((ep, p))
    return out


def use_root(d):
    """⚠ `--root <dir>`——**当てる前の姿**を測るため。`habits-0N/草稿/` を持つ木を指す。"""
    global EX
    EX = os.path.abspath(d)


def measure(vol=None):
    """(本文行, 文の字数の一覧, 4文以上の段落数, [(話, 行, 字数, 文)]) を返す。"""
    length, longs, paras, runs = 0, [], 0, []
    for ep, p in episodes(vol):
        for i, s in body_lines(p):
            length += 1
            ss = sentences(s)
            if len(ss) >= 4:
                paras += 1
            for x in ss:
                c = chars(x)
                runs.append(c)
                if c >= LONG:
                    longs.append((ep, i, c, x))
    return length, runs, paras, longs


def marker_count(vol=None):
    n = 0
    for _ep, p in episodes(vol):
        for line in open(p, encoding="utf-8"):
            if line.strip() == RULE:
                n += 1
    return n


def main():
    if "--root" in sys.argv:
        use_root(sys.argv[sys.argv.index("--root") + 1])
    vs = sys.argv[sys.argv.index("-v") + 1] if "-v" in sys.argv else None
    targets = [vs] if vs else ["01", "02", "03", "04", None]

    print(f"{'巻':6s} {'本文行':>6s} {'＊':>4s} {'文':>6s} {'平均':>6s} {'sd':>5s} "
          + " ".join(f"{'≥'+str(t):>5s}" for t in THRESHOLDS) + f" {'4文以上':>7s}")
    for v in targets:
        length, runs, paras, longs = measure(v)
        mean = statistics.mean(runs) if runs else 0
        sd = statistics.pstdev(runs) if runs else 0
        cnt = " ".join(f"{sum(1 for c in runs if c >= t):5d}" for t in THRESHOLDS)
        label = v if v else "全体"
        print(f"{label:6s} {length:6d} {marker_count(v):4d} {len(runs):6d} "
              f"{mean:6.1f} {sd:5.1f} {cnt} {paras:7d}")

    if "--long" in sys.argv:
        print("")
        print(f"—— {LONG}字以上の文（座標つきで、全部）")
        _l, _r, _p, longs = measure(vs)
        for ep, i, c, x in sorted(longs, key=lambda z: -z[2]):
            print(f"  {ep}:{i}  {c:3d}字  {x}")


if __name__ == "__main__":
    main()
