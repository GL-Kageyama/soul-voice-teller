#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""畳める行を数える——第八段階（流す）の**候補出し**（読み取り専用）。

**何を測るか。** 設計は「短文（切る）と長文（流す）の配分でリズムを作る」（`../構想/design.md:81`）と
定めている。本文の長文は 20,905文のうち 6文である（第八段階の材料 §2）。

**⚠ 畳む手は、行の内側で起きる。** 段落（物理的な一行）が三つ以上の文を持てば、
そのうち同型の二つ以上を**読点で一息に流す一文**へ畳める。**行は足さない。文数は減る。**
**ゆえに `差し替える.py` の段落→段落の差し替えで当たり、行番号は一行も動かない。**

**⚠ この器は、案を書かない。** 畳める行を**数えて出す**だけである（畳むのは人が書く）。

### 出すもの

- 各話の**場面1**（第1行＝題のあとの本文〜最初の `＊` の手前）の行のうち、
  **文が `MIN_SENT` 個以上ある行**を、**入口に近い順**に出す。
- 併せて、その行の文末が**同型**（`ある／いる／ない／無い／ている／てある／である／ままだ`）かを出す。
  ⚠ 同型でなくても畳めることはある（並列・対比）。**ゆえに `同型` は参考であり、判定ではない。**

### 文の切り方

**`。` だけで切る**（**記号を落とした字数**で数える）。**⚠ 2026-10-14 に `[。？！]` から揃えた**——**第四巻の `！` は文末でなく、物を指す字（四条の「！」）ゆえ、`！` で切ると第四巻にだけ偽の候補が生まれる**（`sentences()` の註を見よ）。

### ⚠ 下限（`MIN_SENT`）——**2026-10-14 に 3 から 2 へ**

**第八段階の材料 §5 は候補を「同型の短文が3つ以上続く区間」と定めた**（第一巻はそれで当てた）。
**第二巻・第三巻では、畳んだ一文が20字以上になることを条件に、「二文から」へ広げた**（**第二巻5件・第三巻7件が、元2文の行**）。
**ゆえに、この器の下限も 2 へ揃えた**——**申告の本体は `第八段階_流す_当てた_第三巻.md` §6**。

    python3 畳める行を数える.py            # 63話の要約
    python3 畳める行を数える.py -v 01      # 第一巻の候補を行番号つきで全部
    python3 畳める行を数える.py -v 01-06   # 一話だけ
    python3 畳める行を数える.py --tsv 01   # 台帳の下書き（話・行・文数・字数・同型・現文）

⚠ **この器は、本文を一度も書き換えない。**
"""
import glob
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
EX = os.path.dirname(os.path.dirname(ROOT))          # examples/
RULE = "＊"
TITLE = re.compile(r"^#\s+第\d+話")
SENT = "。"          # ⚠ **`。` だけ**——2026-10-14 に `。？！` から揃えた（下の註を見よ）
TAIL = re.compile(r"(ある|いる|ない|無い|ている|てある|である|ままだ|ままである)。$")
MIN_SENT = 2          # 「畳める」と見なす文数の下限——⚠ **2026-10-14 に 3 から 2 へ**（下の註を見よ）


def chars(s):
    return sum(1 for c in s if not c.isspace() and unicodedata.category(c) != "Cf")


def sentences(para):
    """⚠ **`。` だけで切る。**

    2026-10-14 に `[。？！]` から揃えた。**理由＝第四巻の `！` は、文末ではない。**
    第四巻の `！` は **24個あり、すべて四条の「！」（記名の三点）という、物を指す字**である
    （`04-16:15`「欄の中に！がある。」。**`！` を含む行は `draft_04-16_取らない書式.md` の22行だけ**）。
    **ゆえに `！` で切ると、「欄の中に！がある。」が2文に割れ、第四巻にだけ偽の候補が生まれる。**
    ⚠ **文末の `？`・`！` は、四巻とも 0本**（〔実測 2026-10-14〕`grep -h "[？！]$"`＝0）。
    `文の長さを数える.py` は、はじめから `。` だけである。
    """
    return [x + "。" for x in re.split(r"。", para) if x.strip()]


def load(ep):
    vol = "habits-" + ep[:2]
    p = glob.glob(os.path.join(EX, vol, "草稿", "draft_" + ep + "_*.md"))[0]
    return open(p, encoding="utf-8").read().split("\n")


def scene1(body):
    """場面1の本文行（(行番号, 文)）を返す。空行・見出し・題・`＊` を除く。"""
    try:
        end = body.index(RULE, 4)
    except ValueError:
        end = len(body)
    out = []
    for i, line in enumerate(body[:end], start=1):
        s = line.strip()
        if not s or s.startswith("#") or TITLE.match(s):
            continue
        out.append((i, s))
    return out


def episodes():
    return sorted({os.path.basename(p)[6:11]
                   for p in glob.glob(os.path.join(EX, "habits-0*", "草稿", "draft_*.md"))})


def use_root(d):
    """⚠ `--root <dir>`——**当てる前の姿**の候補を出すため。`habits-0N/草稿/` を持つ木を指す。"""
    global EX
    EX = os.path.abspath(d)


def candidates(ep):
    """(行番号, 文の数, 字数, 同型か, 現文) を、入口に近い順に返す。"""
    out = []
    for n, s in scene1(load(ep)):
        ss = sentences(s)
        if len(ss) < MIN_SENT:
            continue
        same = all(TAIL.search(x) for x in ss)
        out.append((n, len(ss), chars(s), same, s))
    return out


def main():
    if "--root" in sys.argv:
        use_root(sys.argv[sys.argv.index("--root") + 1])
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    args = [a for a in args if a != sys.argv[sys.argv.index("--root") + 1]] if "--root" in sys.argv else args
    sel = args[0] if args else None
    eps = [e for e in episodes() if sel is None or e.startswith(sel)]
    rows = []
    for ep in eps:
        for n, k, c, same, s in candidates(ep):
            rows.append((ep, n, k, c, same, s))

    if "--tsv" in sys.argv:
        print("\t".join(["話", "行", "文数", "字数", "同型", "現文"]))
        for ep, n, k, c, same, s in rows:
            print("\t".join([ep, str(n), str(k), str(c), "○" if same else "", s]))
        return

    if "-v" in sys.argv:
        for ep, n, k, c, same, s in rows:
            print(f"{ep}:{n}  文{k}  字{c:3d}  {'同型' if same else '    '}  {s}")
        return

    print(f"対象: {len(eps)} 話")
    print(f"文が {MIN_SENT} 個以上ある行（場面1の中）: 計 {len(rows)}")
    by = {}
    for ep, n, k, c, same, s in rows:
        by.setdefault(ep, []).append((n, k, c, same))
    none = [e for e in eps if e not in by]
    print(f"候補が 0 行の話: {len(none)}  {none}")
    print(f"一話あたり: 中央値 {sorted(len(v) for v in by.values())[len(by)//2]}")
    print("")
    print("話ごとの、入口にいちばん近い候補（この段は、ここへ一本ずつ置く）")
    for ep in eps:
        if ep not in by:
            continue
        n, k, c, same = by[ep][0]
        print(f"  {ep}  行{n:3d}  文{k}  字{c:3d}  {'同型' if same else '    '}")


if __name__ == "__main__":
    main()
