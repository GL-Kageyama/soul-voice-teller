#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""娯楽台帳_第二層_後_較べる——一度目と二度目の「人の欄」を、並べる。

**なぜ、この器が要るか。** 第二層の計測は二度走った。
**一度目（2026-10-14 08:16）は、娯楽の段の案を当てる前の本文を読んだ。**
**二度目は、そのあと本文へ入った三つの段（届いた案 98件・ユーモア 120＋23件）の後を読む。**
**⚠ 同じ物差し・同じ欄である。ゆえに、数は並べてよい。**

⚠ **点数は付けない。** 数と、その内訳だけを出す。

⚠ **入口の定義は、一度目と同じである**——**第一〜三巻は場面1、第四巻は場面2**
   （`話割り.md` が、この巻の入口を場面2に置いている）。

使い方:
    python3 娯楽台帳_第二層_後_較べる.py <一度目.tsv> <二度目.tsv>
"""

import re
import sys
from pathlib import Path

AXES = ["ユーモア", "楽しい", "感嘆", "感動", "恐怖", "かわいい"]


def read(p):
    lines = [ln for ln in Path(p).read_text(encoding="utf-8").split("\n") if ln.strip()]
    hdr = lines[0].split("\t")
    idx = {h: i for i, h in enumerate(hdr)}
    out = []
    for ln in lines[1:]:
        c = ln.split("\t")
        out.append({
            "話": c[idx["話"]], "場面": c[idx["場面"]],
            "設計の軸": c[idx["設計の軸"]],
            "軸": c[idx["実現した軸"]], "三種": c[idx["三種"]],
            "掴": c[idx["掴んでいるか"]],
            "差": c[idx["設計との差"]],
            "ズレ": c[idx["ズレの有無"]],
        })
    return out


def axis_counts(rows, key="軸"):
    n = {}
    for r in rows:
        v = r[key]
        for x in (["なし"] if v == "なし" else [y.strip() for y in v.split("＋")]):
            n[x] = n.get(x, 0) + 1
    return n


def grab_counts(rows):
    n = {}
    for r in rows:
        n[r["掴"]] = n.get(r["掴"], 0) + 1
    return n


def is_entrance(r):
    return r["場面"] == ("2" if r["話"].startswith("04-") else "1")


def main() -> int:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    a, b = read(sys.argv[1]), read(sys.argv[2])
    if len(a) != len(b):
        sys.exit(f"行数が違う——{len(a)} と {len(b)}")

    print(f"■ 行数——{len(a)} と {len(b)}（一致）\n")

    print("■ 実現した軸——全体")
    ca, cb = axis_counts(a), axis_counts(b)
    print(f"  {'軸':<14}{'一度目':>7}{'二度目':>7}{'差':>7}")
    for x in AXES + ["なし"]:
        va, vb = ca.get(x, 0), cb.get(x, 0)
        mark = "  ←" if va != vb and x in ("ユーモア", "なし") else ""
        print(f"  {x:<14}{va:>7}{vb:>7}{vb - va:>+7}{mark}")

    print("\n■ ズレの有無")
    za = sum(1 for r in a if r["ズレ"].startswith("有"))
    zb = sum(1 for r in b if r["ズレ"].startswith("有"))
    print(f"  有——{za} → {zb}（{zb - za:+d}）／{len(a)}")

    print("\n■ 掴んでいるか——全体")
    ga, gb = grab_counts(a), grab_counts(b)
    print(f"  {'印':<4}{'一度目':>7}{'二度目':>7}{'差':>7}")
    for x in ("○", "△", "×"):
        print(f"  {x:<4}{ga.get(x, 0):>7}{gb.get(x, 0):>7}{gb.get(x, 0) - ga.get(x, 0):>+7}")

    print("\n■ 入口——63場面（第一〜三巻は場面1、第四巻は場面2）")
    ea = [r for r in a if is_entrance(r)]
    eb = [r for r in b if is_entrance(r)]
    print(f"  場面の数——{len(ea)} と {len(eb)}")
    print(f"  `なし`——{sum(1 for r in ea if r['軸'] == 'なし')} → "
          f"{sum(1 for r in eb if r['軸'] == 'なし')}")
    print(f"  掴んでいるか——○ {sum(1 for r in ea if r['掴'] == '○')} → "
          f"{sum(1 for r in eb if r['掴'] == '○')}／△ "
          f"{sum(1 for r in ea if r['掴'] == '△')} → {sum(1 for r in eb if r['掴'] == '△')}／× "
          f"{sum(1 for r in ea if r['掴'] == '×')} → {sum(1 for r in eb if r['掴'] == '×')}")

    print("\n■ 実現した軸——入口の63場面")
    ca2, cb2 = axis_counts(ea), axis_counts(eb)
    for x in AXES + ["なし"]:
        va, vb = ca2.get(x, 0), cb2.get(x, 0)
        if va or vb:
            print(f"  {x:<14}{va:>7}{vb:>7}{vb - va:>+7}")

    print("\n■ 設計との差——一致／不一致")
    # ⚠ 一致は、`設計との差` の文ではなく、**軸の欄そのもの**で数える
    #    （一度目の記録 §3-4 と同じ数え方である——`設計の軸` は常に一つ、`実現した軸` は `＋` を含みうる）。
    ma = sum(1 for r in a if r["設計の軸"] == r["軸"])
    mb = sum(1 for r in b if r["設計の軸"] == r["軸"])
    print(f"  一致——{ma} → {mb}／不一致——{len(a) - ma} → {len(b) - mb}")
    print("  ⚠ 数え方は、`設計の軸` と `実現した軸` の**字の一致**である（`ユーモア＋感嘆` は不一致に入る）。")

    def cross(rows):
        n = {}
        for r in rows:
            if r["設計の軸"] != r["軸"]:
                k = f"{r['設計の軸']}→{r['軸']}"
                n[k] = n.get(k, 0) + 1
        return n

    xa, xb = cross(a), cross(b)
    keys = sorted(set(xa) | set(xb), key=lambda k: (-(xa.get(k, 0) + xb.get(k, 0)), k))
    print("\n■ 不一致の内訳（`設計の軸`→`実現した軸`）")
    print(f"  {'組':<24}{'一度目':>7}{'二度目':>7}")
    for k in keys:
        print(f"  {k:<24}{xa.get(k, 0):>7}{xb.get(k, 0):>7}")

    print("\n■ 場面ごとの印——一度目 → 二度目")
    for i, x in enumerate(("1", "2", "3"), 1):
        sa = [r for r in a if r["場面"] == x]
        sb = [r for r in b if r["場面"] == x]
        print(f"  場面{x}——○ {sum(1 for r in sa if r['掴'] == '○')} → "
              f"{sum(1 for r in sb if r['掴'] == '○')} "
              f"（{len(sa)} 場面）")

    print("\n■ 巻ごと——`なし`・`ズレ有`・○・一致")
    print(f"  {'巻':<5}{'場面':>5}{'なし':>12}{'ズレ有':>12}{'○':>12}{'一致':>12}")
    for v in ("01", "02", "03", "04"):
        sa = [r for r in a if r["話"].startswith(v + "-")]
        sb = [r for r in b if r["話"].startswith(v + "-")]

        print(f"  {v:<5}{len(sa):>5}"
              f"{str(sum(1 for r in sa if r['軸'] == 'なし')) + '→' + str(sum(1 for r in sb if r['軸'] == 'なし')):>12}"
              f"{str(sum(1 for r in sa if r['ズレ'].startswith('有'))) + '→' + str(sum(1 for r in sb if r['ズレ'].startswith('有'))):>12}"
              f"{str(sum(1 for r in sa if r['掴'] == '○')) + '→' + str(sum(1 for r in sb if r['掴'] == '○')):>12}"
              f"{str(sum(1 for r in sa if r['設計の軸'] == r['軸'])) + '→' + str(sum(1 for r in sb if r['設計の軸'] == r['軸'])):>12}")

    print("\n⚠ 数え方——`実現した軸` は `＋` で割って数える（`ユーモア＋感嘆` は両方に1）。"
          "⚠ `なし` は `なし` として数える。")
    print("⚠ **巻をまたいで ○ を較べない**——読者は巻ごとに一人ゆえ、四人ぶんの判定である。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
