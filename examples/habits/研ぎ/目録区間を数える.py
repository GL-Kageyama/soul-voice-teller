#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""目録区間を数える——**全場面**の「目録行が続く区間」を数え、台帳にする（読み取り専用）。

**なぜ、この器が要るか。** [`入口の流れを検める.py`](入口の流れを検める.py) の本命は
**`区間`**（目録行が 4 行以上続く）である。**⚠ 但し、あの器は場面1しか見ていない。**
**ゆえに「98区間」は「場面1の98区間」であって、作品全体の数ではない。**
**一手を当てる前に、範囲を測る。**

### 物差しは、`入口の流れを検める.py` と**同じ**である（一字も変えない）

- **目録行**——行内の**すべての文**の文末が
  `ある／いる／ない／無い／ている／てある／である／ままだ／ままである。` のいずれかである行。
- **区間**——目録行が **4 行以上**続く区間。
- **文の切り方**——`[。？！]` で切る。**字数は、非空白・Cf を除く。**

### 場面の切り方

**草稿の本文行**（空行・`#` の見出し・`＊` を除いた行）を、**`＊` の位置で区切る**。
**⚠ `＊` は、一話に二つ・題の直下には置かない**（場面区切りの規則）。

    python3 目録区間を数える.py            # 巻ごと・場面ごとの要約
    python3 目録区間を数える.py -v         # 区間を、一つずつ実物で出す
    python3 目録区間を数える.py --tsv     # 区間の台帳（タブ区切り）を、標準出力へ
    python3 目録区間を数える.py --at HEAD # その時点の本文（git show）

⚠ **この器は、本文を一字も触らない。**
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
TAIL = re.compile(r"(ある|いる|ない|無い|ている|てある|である|ままだ|ままである)。$")
RUN_MIN = 4


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
    return os.path.basename(p), txt.split("\n")


def scenes(body):
    """本文行を `＊` で区切る。戻り＝[ [(行番号, 文), …], … ]（場面の順）。"""
    out, cur = [], []
    for i, line in enumerate(body, start=1):
        s = line.strip()
        if not s or s.startswith("#") or TITLE.match(s):
            continue
        if s == RULE:
            out.append(cur)
            cur = []
            continue
        cur.append((i, s))
    out.append(cur)
    return [sc for sc in out if sc]


def runs(flags, minimum=RUN_MIN):
    out, a = [], 0
    while a < len(flags):
        if not flags[a]:
            a += 1
            continue
        b = a
        while b < len(flags) and flags[b]:
            b += 1
        if b - a >= minimum:
            out.append((a, b))
        a = b
    return out


def collect(at=None):
    eps = sorted({os.path.basename(p)[6:11]
                  for p in glob.glob(os.path.join(EX, "habits-0*", "草稿", "draft_*.md"))})
    rows = []
    for ep in eps:
        fname, body = load(ep, at)
        for si, sc in enumerate(scenes(body), start=1):
            flags = [all(TAIL.search(x) for x in sentences(p)) for _, p in sc]
            for a, b in runs(flags):
                rows.append({
                    "話": ep, "場面": si, "ファイル": fname,
                    "行": f"{sc[a][0]}-{sc[b-1][0]}",
                    "長さ": b - a,
                    "場面の行数": len(sc),
                    "行数": [sc[k][0] for k in range(a, b)],
                    "文": [sc[k][1] for k in range(a, b)],
                })
    return rows


def main():
    at = None
    if "--at" in sys.argv:
        at = sys.argv[sys.argv.index("--at") + 1]
    rows = collect(at)

    if "--tsv" in sys.argv:
        hdr = ["話", "場面", "行", "長さ", "ファイル"]
        print("\t".join(hdr))
        for r in rows:
            print("\t".join([r["話"], str(r["場面"]), r["行"], str(r["長さ"]), r["ファイル"]]))
        return 0

    print(f"時点: {at or 'いまの本文'}")
    print(f"区間（目録行が {RUN_MIN} 行以上続く）: 計 {len(rows)}"
          f"  その行数 {sum(r['長さ'] for r in rows)}")
    print(f"最長の区間: {max((r['長さ'] for r in rows), default=0)} 行")
    print()
    print("■ 場面ごと")
    for si in (1, 2, 3):
        s = [r for r in rows if r["場面"] == si]
        print(f"  場面{si}——区間 {len(s):3d}  その行数 {sum(r['長さ'] for r in s):4d}"
              f"  最長 {max((r['長さ'] for r in s), default=0):2d} 行")
    print()
    print("■ 巻ごと・場面ごと")
    print(f"  {'巻':<5}{'場面1':>8}{'場面2':>8}{'場面3':>8}{'計':>8}")
    for v in ("01", "02", "03", "04"):
        c = [len([r for r in rows if r["話"].startswith(v + "-") and r["場面"] == si])
             for si in (1, 2, 3)]
        print(f"  {v:<5}{c[0]:>8}{c[1]:>8}{c[2]:>8}{sum(c):>8}")
    print()
    print("■ 長さの分布")
    for L in range(RUN_MIN, max((r["長さ"] for r in rows), default=0) + 1):
        n = sum(1 for r in rows if r["長さ"] == L)
        if n:
            print(f"  {L:2d} 行——{n:3d} 区間")
    if "-v" in sys.argv:
        print()
        for r in sorted(rows, key=lambda r: (-r["長さ"], r["話"])):
            print(f"--- {r['話']} 場面{r['場面']}（{r['長さ']} 行／{r['行']}）")
            for n, t in zip(r["行数"], r["文"]):
                print(f"    {n:4d}: {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
