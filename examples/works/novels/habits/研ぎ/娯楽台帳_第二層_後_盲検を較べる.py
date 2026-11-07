#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""娯楽台帳_第二層_後_盲検を較べる——**同じ本文**を四人が読んだとき、答えはどれだけ動くか。

**なぜ、この器が要るか。** 第二層の計測は、一度目と二度目で大きく動いた
（`なし` 17→44・一致 163→110）。**だが、それは二つの理由のどちらでも説明できる**——
①本文が三つの段で変わったから／②読者が替わったから。
**第一巻を、答えを見せずに二人へ読ませた**（`_01A`・`_01B`）。**本文は一度目・二度目と同じ**である。
**ゆえに A と B の食い違いは、そのまま「読者の側のぶれ」である。**

⚠ **点数は付けない。** 一致の数と、その内訳だけを出す。

使い方:
    python3 娯楽台帳_第二層_後_盲検を較べる.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLS = ["実現した軸", "三種", "掴んでいるか", "設計との差", "ズレの有無"]
FILES = [
    ("一度目", HERE / "娯楽台帳.tsv"),
    ("二度目", HERE / "娯楽台帳_第二層_後.tsv"),
    ("盲検A", HERE / "娯楽台帳_第二層_後_01A.tsv"),
    ("盲検B", HERE / "娯楽台帳_第二層_後_01B.tsv"),
]
AXES = ["ユーモア", "楽しい", "感嘆", "感動", "恐怖", "かわいい", "なし"]


def read(p, vol="01"):
    """読む。⚠ **読者のファイルは 9欄で `設計の軸` を持たない**ゆえ、それは台帳から補う。"""
    lines = [ln for ln in Path(p).read_text(encoding="utf-8").split("\n") if ln.strip()]
    hdr = lines[0].split("\t")
    idx = {h: i for i, h in enumerate(hdr)}
    out = {}
    for ln in lines[1:]:
        c = ln.split("\t")
        if not c[idx["話"]].startswith(vol + "-"):
            continue
        row = {k: c[idx[k]] for k in COLS if k in idx}
        for k in COLS:
            row.setdefault(k, "")
        if "設計の軸" in idx:
            row["設計の軸"] = c[idx["設計の軸"]]
        out[(c[idx["話"]], c[idx["場面"]])] = row
    return out


def main() -> int:
    data = {}
    for name, p in FILES:
        if not p.exists():
            sys.exit(f"無い: {p.name}")
        data[name] = read(p)
        if len(data[name]) != 42:
            sys.exit(f"{name}——42 場面でない: {len(data[name])}")

    # ⚠ 読者のファイルに無い `設計の軸` は、台帳（一度目）から借りる。**台帳の機械欄ゆえ、読者に依らない。**
    ledger = data["一度目"]
    for name, _ in FILES:
        if name == "一度目":
            continue
        for k, row in data[name].items():
            row["設計の軸"] = ledger[k]["設計の軸"]

    names = [n for n, _ in FILES]
    keys = sorted(data[names[0]])

    print("■ 読んだ本文は、四人とも同じである（第一巻・42場面）")
    print("  ⚠ 一度目は娯楽の段の**前**、二度目は**後**。**盲検A・盲検Bは、二度目と同じ本文**。\n")

    print("■ 一対ごとの一致（42場面）")
    print(f"  {'欄':<14}" + "".join(f"{a[:2]}={b[:2]:<8}" for a, b in
                                     [(names[i], names[j]) for i in range(4) for j in range(i + 1, 4)]))
    pairs = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    for col in ["実現した軸", "三種", "掴んでいるか", "ズレの有無"]:
        cells = []
        for i, j in pairs:
            a, b = data[names[i]], data[names[j]]
            n = sum(1 for k in keys if a[k][col] == b[k][col])
            cells.append(f"{n:>9}")
        print(f"  {col:<14}" + "".join(cells))

    print("\n■ `ズレの有無` の読み方——四人とも同じ意味で読んだか")
    print("  （`有` を立てた場面が、`設計の軸` と `実現した軸` の食い違いと一致するか）")
    for n in names:
        d = data[n]
        both = sum(1 for k in keys
                   if d[k]["ズレの有無"].startswith("有") and d[k]["設計の軸"] != d[k]["実現した軸"])
        only_z = sum(1 for k in keys
                     if d[k]["ズレの有無"].startswith("有") and d[k]["設計の軸"] == d[k]["実現した軸"])
        only_d = sum(1 for k in keys
                     if not d[k]["ズレの有無"].startswith("有") and d[k]["設計の軸"] != d[k]["実現した軸"])
        nz = sum(1 for k in keys if d[k]["ズレの有無"].startswith("有"))
        nd = sum(1 for k in keys if d[k]["設計の軸"] != d[k]["実現した軸"])
        print(f"  {n:<6}ズレ有 {nz:>2}／軸が違う {nd:>2}／両方 {both:>2}"
              f"／ズレ有だが軸は同じ {only_z:>2}／軸は違うがズレ無 {only_d:>2}")

    print("\n■ 実現した軸——分布（`＋` で割って数える）")
    print(f"  {'軸':<10}" + "".join(f"{n:>8}" for n in names))
    for x in AXES:
        row = []
        for n in names:
            c = 0
            for k in keys:
                v = data[n][k]["実現した軸"]
                parts = ["なし"] if v == "なし" else [y.strip() for y in v.split("＋")]
                if x in parts:
                    c += 1
            row.append(f"{c:>8}")
        print(f"  {x:<10}" + "".join(row))

    print("\n■ 掴んでいるか")
    print(f"  {'印':<10}" + "".join(f"{n:>8}" for n in names))
    for x in ("○", "△", "×"):
        print(f"  {x:<10}" + "".join(f"{sum(1 for k in keys if data[n][k]['掴んでいるか'] == x):>8}"
                                     for n in names))

    print("\n■ 場面ごとの `実現した軸` が四人とも一致した場面")
    full = [k for k in keys if len({data[n][k]["実現した軸"] for n in names}) == 1]
    print(f"  四人一致——{len(full)}/42")
    fullg = [k for k in keys if len({data[n][k]["掴んでいるか"] for n in names}) == 1]
    print(f"  四人一致（掴んでいるか）——{len(fullg)}/42")
    print("  ⚠ **一致した場面だけを見て「届いた」と読まない**——四人が同じに外すこともある。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
