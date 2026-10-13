#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""入口の掴みを検める——④（場面の型）の計測器。

**何を測るか。** 場面表（`habits-0N/構想/各話/MM_題.md`）の **「入口の掴み」** の欄の中身が、
**場面1（第一行〜最初の `＊` の手前）に、句として在るか**。

**欄の中身の分け方**——`*` を落とし、「。」で割る。

- `[0]`＝ `第一場面の第一文——…`。**〈X〉＝物の目録であるゆえ、候補から外す。**
- `[1]` 以降のうち、**註**（`この話`／`その話`／`この巻` で始まる、`反応軸` を含む、
  `→` を含む、`（` で始まる）を外したものが、**この器の「候補」である。**
- **`——` から先は、欄の中の註であるゆえ、落とす**（例＝`01-14`「名の書かれた位置に、もう一度立つ——この話の癖は…」）。
- 候補が一つも残らない話（欄が註だけ＝`01-07`）は、**分母から外す**。

**⚠ この欄の形は、巻ごと・話ごとに揃っていない。** 第一・二・四巻は「〈X〉。〈Y〉 註」の三つ、
**第三巻は〈Y〉が最後に来る**（`03-01`「…**この巻の音は、鍵の音である**（→…）。名より先に、音が来る」）、
あるいは〈Y〉が四つ目に来る（`03-10`）。
**ゆえにこの器は、「〈Y〉がどこか」を決めない。** **欄が名指しした句のどれかが、場面1に在るか**を数える。

**照合**——句読点・空白・括弧を落とした**先頭8字**が、場面1の本文（同じく記号を落としたもの）に在るか。
⚠ **8字は、私が決めた長さである。** 短い句（「名乗る」＝3字）は、その長さで切る。

**入口の第一文の型**——**行5の第一文**（最初の「。」まで）の文末が
`ある／いる／ない／無い／ている／てある／である／ままだ／ままである。` なら「物・状態」、他は「その他」。
⚠ **行5の最後の文ではない。** 「入口の第一文」ゆえ、**頭の一文**である。

    python3 入口の掴みを検める.py            # いまの本文を測る
    python3 入口の掴みを検める.py --at HEAD  # その時点の本文を測る（git show）
    python3 入口の掴みを検める.py -v         # 一話ずつ出す

⚠ **この器は、④の前後を較べるために書かれた。** ④の効果を測るものであって、
**「掴みが読み手に届いたか」を測るものではない**（それは第七段の、人による計測である）。

⚠ **この器は、材料文書 [`第七段階_第四段_娯楽_型_材料.md`](第七段階_第四段_娯楽_型_材料.md) §0-3 の数を置き換える。**
あちらの数（14/60・42/21）は、**書き残していない使い捨ての照合器**から出たもので、規則を再現できない。
**この器の規則は、上に書いたとおりである。**
"""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EX = os.path.dirname(os.path.dirname(ROOT))          # examples/
RULE = "＊"
NOTE = re.compile(r"^(この話|その話|この巻)|反応軸|→|^（")
TAIL = re.compile(r"(ある|いる|ない|無い|ている|てある|である|ままだ|ままである)。$")


def cell_of(ep):
    """「入口の掴み」の欄の中身を返す。無ければ None。"""
    vol, num = "habits-" + ep[:2], ep.split("-")[1]
    for p in sorted(glob.glob(os.path.join(EX, vol, "構想", "各話", "*.md"))):
        if not os.path.basename(p).startswith(num + "_"):
            continue
        for line in open(p, encoding="utf-8"):
            if "入口の掴み" in line:
                s = line.replace("*", "")
                if "|" in s:
                    parts = [x for x in s.split("|") if x.strip()]
                    s = parts[-1] if parts else s
                return s
    return None


def candidates(cell):
    """欄の中身から、〈X〉と註を外した「候補」を返す。"""
    out = []
    for i, x in enumerate([y.strip() for y in cell.split("。") if y.strip()]):
        if i == 0:                       # 〈X〉＝物の目録
            continue
        head = x.split("——")[0].strip()  # —— から先は註
        if not head or NOTE.search(head):
            continue
        out.append(head)
    return out


def squeeze(s):
    return re.sub(r"[。、！？\s「」『』——…（）()\[\]→]", "", s)


def load(ep, at):
    vol = "habits-" + ep[:2]
    p = glob.glob(os.path.join(EX, vol, "草稿", "draft_" + ep + "_*.md"))[0]
    if at:
        txt = subprocess.run(["git", "show", f"{at}:examples/{vol}/草稿/{os.path.basename(p)}"],
                             cwd=EX, capture_output=True, text=True).stdout
    else:
        txt = open(p, encoding="utf-8").read()
    return txt.split("\n")


def main():
    at = None
    if "--at" in sys.argv:
        at = sys.argv[sys.argv.index("--at") + 1]
    eps = sorted({os.path.basename(p)[6:11]
                  for p in glob.glob(os.path.join(EX, "habits-0*", "草稿", "draft_*.md"))})
    hit = total = 0
    no_cand, rows = [], []
    kind = {"物・状態": 0, "その他": 0}
    for ep in eps:
        cell = cell_of(ep)
        if cell is None:
            continue
        body = load(ep, at)
        try:
            end = body.index(RULE, 4)
        except ValueError:
            end = len(body)
        s1 = squeeze("。".join(body[4:end]))
        head = body[4].rstrip().split("。")[0] + "。"
        kind["物・状態" if TAIL.search(head) else "その他"] += 1
        cs = candidates(cell)
        if not cs:
            no_cand.append(ep)
            continue
        total += 1
        found = [c for c in cs if squeeze(c)[:8] and squeeze(c)[:8] in s1]
        if found:
            hit += 1
        rows.append((ep, "在" if found else "無", "／".join(c[:24] for c in cs)))
    print(f"時点: {at or 'いまの本文'}")
    print(f"欄の候補が場面1に在る話: {hit} / {total}")
    print(f"欄が註だけ（分母から外す）: {len(no_cand)} 件 {' '.join(no_cand)}")
    print(f"入口の第一文の型: {kind}")
    if "-v" in sys.argv:
        for ep, h, cs in rows:
            print(f"  {ep}  {h}  {cs}")


if __name__ == "__main__":
    main()
