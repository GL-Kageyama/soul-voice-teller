#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""入口の流れを検める——①（軸の配り直し）の**本文側**の計測器（読み取り専用）。

**何を測るか。** 各話の**場面1**（第1行＝題のあとの本文〜最初の `＊` の手前）が、
**流れを持っているか**。軸「楽しい」の失敗モードは**退屈・飽きる**であり、
その正体は `6つの反応軸.md` の一言——**正の情動 × 流れ**である。
ゆえに測るのは、流れの**不在**の二つの形である。

### 測るもの（二つ）

1. **`幅`——行の字数が、同じ帯に収まっているか。**
   行ごとに非空白字数を出し、**幅 ±6字**の帯に収まる行が**連続する最大長**を測る（`連`）。
   ——`第七段階_第四段_入口の軸_当てた.md` §9 が「48段落が、どれも同じ長さである」と読んだ形の実測。

2. **`目録`——行の全文が、物・状態の報告で終わっているか。**
   行内の**すべての文**の文末が `ある／いる／ない／無い／ている／てある／である／ままだ／ままである。`
   のいずれかである行を**目録行**と呼ぶ。
   ⚠ **これは「説明」の代理指標である。** 物を一つずつ数える行は、この形に落ちる。

3. **`区間`——目録行が、続いているか。**
   目録行が **4 行以上**続く区間を数える（`区間`＝その数、`区間行`＝その行数）。
   ⚠ **これが、この器の本命である。** 一つずつ数える行が**一件**なのは様式である。
   **四行以上続く**と、読む側には**目録**になる（`第七段階_第四段_入口の軸_当てた.md` §9 が
   「48段落が、どれも同じ長さである」と読んだ形）。
   ⚠ **`目録`（②）は定義上、`区間`を動かす一手では動かない。**
   文末を `〜である／〜ている／〜ない` のまま、中身を具体へ変えれば、`目録行`の数は**同じ**である。
   **ゆえにこの器は、③を②と別に出す。**（一手を測るのは③であって②ではない）。

⚠ **この器は、判断をしない。** 「面白い／面白くない」は出さない（それは人が読む）。
**流れの不在を、二つの数に落とすだけである。**

### 文の切り方

`[。？！]` で切る。**記号を落とした字数**（非空白・Cf を除く）で数える——`検査/check.py` と同じ物差し。

    python3 入口の流れを検める.py            # 63話の要約
    python3 入口の流れを検める.py -v         # 一話ずつ
    python3 入口の流れを検める.py -vv        # 幅の連（10行以上）の実物も出す
    python3 入口の流れを検める.py -c         # 目録区間の実物を出す
    python3 入口の流れを検める.py --at HEAD  # その時点の本文（git show）
    python3 入口の流れを検める.py --tsv      # 一話一行の台帳

⚠ **この器は、入口の場面を一度も書き換えない。**
"""
import glob
import os
import re
import subprocess
import sys
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
EX = os.path.dirname(os.path.dirname(ROOT))          # examples/
RULE = "＊"
TITLE = re.compile(r"^#\s+第\d+話")
SENT = "。？！"
TAIL = re.compile(r"(ある|いる|ない|無い|ている|てある|である|ままだ|ままである)。$")
BAND = 6          # 同じ帯と見なす字数の幅
RUN_MIN = 4       # 目録行が「続いている」と見なす最短の長さ


def chars(s):
    return sum(1 for c in s if not c.isspace() and unicodedata.category(c) != "Cf")


def sentences(para):
    return [x + "。" for x in re.split(r"[。？！]", para) if x.strip()]


def load(ep, at):
    vol = "habits-" + ep[:2]
    p = glob.glob(os.path.join(EX, vol, "草稿", "draft_" + ep + "_*.md"))[0]
    if at:
        txt = subprocess.run(["git", "show", f"{at}:examples/{vol}/草稿/{os.path.basename(p)}"],
                             cwd=EX, capture_output=True, text=True).stdout
    else:
        txt = open(p, encoding="utf-8").read()
    return txt.split("\n")


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


def catalog_runs(flags, minimum=RUN_MIN):
    """`flags`（目録行かどうか）のうち、`True` が `minimum` 以上続く区間を (長さ, 開始) で返す。"""
    out, a = [], 0
    while a < len(flags):
        if not flags[a]:
            a += 1
            continue
        b = a
        while b < len(flags) and flags[b]:
            b += 1
        if b - a >= minimum:
            out.append((b - a, a))
        a = b
    return out


def longest_run(nums, band=BAND):
    """`nums` のうち、幅 `band` に収まる連続部分の最長を (長さ, 開始位置) で返す。"""
    best = (0, 0)
    for a in range(len(nums)):
        for b in range(a, len(nums)):
            if max(nums[a:b + 1]) - min(nums[a:b + 1]) <= band:
                if b - a + 1 > best[0]:
                    best = (b - a + 1, a)
            else:
                break
    return best


def main():
    at = None
    if "--at" in sys.argv:
        at = sys.argv[sys.argv.index("--at") + 1]
    eps = sorted({os.path.basename(p)[6:11]
                  for p in glob.glob(os.path.join(EX, "habits-0*", "草稿", "draft_*.md"))})
    rows = []
    for ep in eps:
        body = load(ep, at)
        s1 = scene1(body)
        if not s1:
            continue
        nums = [chars(p) for _, p in s1]
        run, start = longest_run(nums)
        flags = [all(TAIL.search(x) for x in sentences(p)) for _, p in s1]
        cat = sum(flags)
        cats = catalog_runs(flags)
        rows.append((ep, len(s1), sum(nums), run, cat, s1[max(0, start):start + run],
                     len(cats), sum(m for m, _ in cats), cats, s1))
    print(f"時点: {at or 'いまの本文'}")
    n = len(rows)
    nrun = sum(1 for r in rows if r[3] >= 10)
    print(f"話数: {n}")
    print(f"場面1の行数: 計 {sum(r[1] for r in rows)}  平均 {sum(r[1] for r in rows)/n:.1f}")
    print(f"場面1の字数: 計 {sum(r[2] for r in rows)}  平均 {sum(r[2] for r in rows)/n:.0f}")
    print(f"同じ帯（±{BAND}字）が 10 行以上続く話: {nrun} / {n}")
    print(f"同じ帯の連の最大長: 中央値 {sorted(r[3] for r in rows)[n//2]}")
    print(f"目録行（行の全文が物・状態の報告）: 計 {sum(r[4] for r in rows)}"
          f"  場面1の行の {100*sum(r[4] for r in rows)/sum(r[1] for r in rows):.1f}%")
    print(f"目録行が {RUN_MIN} 行以上続く区間: 計 {sum(r[6] for r in rows)}"
          f"  その行数 {sum(r[7] for r in rows)}"
          f"  場面1の行の {100*sum(r[7] for r in rows)/sum(r[1] for r in rows):.1f}%")
    nlong = sum(1 for r in rows if r[8] and max(m for m, _ in r[8]) >= 8)
    print(f"  うち、8 行以上続く区間を持つ話: {nlong} / {n}"
          f"  最長の区間: {max((max((m for m, _ in r[8]), default=0) for r in rows))} 行")
    if "-v" in sys.argv or "-vv" in sys.argv or "-c" in sys.argv:
        for ep, nl, nc, run, cat, lines, ncat, ncatl, cats, _f in rows:
            print(f"  {ep}  行{nl:3d}  字{nc:5d}  連{run:3d}  目録{cat:3d}"
                  f" ({100*cat/nl:4.0f}%)  区間{ncat:2d}({ncatl:3d}行)")
    if "-vv" in sys.argv:
        for ep, nl, nc, run, cat, lines, ncat, ncatl, cats, flags in rows:
            if run >= 10:
                print(f"--- {ep} の幅の連（{run} 行）")
                for x in lines[:4]:
                    print(f"    {x}")
                print("    …")
                for x in lines[-2:]:
                    print(f"    {x}")
    if "-c" in sys.argv:
        for ep, nl, nc, run, cat, lines, ncat, ncatl, cats, s1 in rows:
            for m, a in cats:
                print(f"--- {ep} の目録区間 {m} 行")
                for n, x in s1[a:a + m]:
                    print(f"    {n}: {x}")
    if "--tsv" in sys.argv:
        print("\t".join(["話", "行数", "字数", "連", "目録行", "目録率", "区間", "区間行"]))
        for r in rows:
            print("\t".join([r[0], str(r[1]), str(r[2]), str(r[3]), str(r[4]),
                             f"{100*r[4]/r[1]:.1f}", str(r[6]), str(r[7])]))


if __name__ == "__main__":
    main()
