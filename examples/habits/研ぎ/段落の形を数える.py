#!/usr/bin/env python3
"""段落化のあとの草稿を、手順⑦（第四段の検品を段落の形でやり直す）のために測る。

読み取り専用である。草稿を書かない。

出すもの——一話ごとに、
  * 場面ごとの段落数・文数・文/段落
  * 場面1の第一段落（入口の掴み——文数と全文）
  * 場面3の最終段落（解放しない——文数と全文）
  * 最長の段落（文数と全文）
  * 五文以上の段落の数

⚠ 空の草稿は exit 1（空の検査は OK と言う、を避ける）。
"""
import argparse
import glob
import pathlib
import re
import sys

SENT = "。？！?"

# ⚠ 場面を切る印は、いま `＊`（全角のアスタリスク）だけの行である——著者裁定 2026-10-13。
#   **区切りである。一話に二つ。** 節と節のあいだに置かれるゆえ、**最初の区切りより前が
#   第1節である**（ゆえに、区切りの数より節の数が一つ多い）。**名を持たない**——節番号は順に振る。
#   ⚠ 控え（`研ぎ/段落化の控え/`）は、まだ `## N` の**札**である。**前に置かれ、名を持つ。**
#   ゆえに両方を受ける（HEAD_RE を見よ）。
HEAD_RE = re.compile(r"^##\s*(\d+)\s*$")
RULE_RE = re.compile(r"^＊$")


def bun(p: str) -> int:
    return sum(p.count(c) for c in SENT)


def scene_blocks(lines):
    """(節名, [段落, ...]) を返す。区切りは `＊`、控えは `## N`（⚠ 置き方が逆である）。"""
    labelled = any(HEAD_RE.match(l.strip()) for l in lines)

    if labelled:
        # 控えの形——`## N` の札。名は N、本文は札の**あと**。
        scenes, cur = [], None
        for ln in lines:
            s = ln.strip()
            m = HEAD_RE.match(s)
            if m:
                cur = (m.group(1), [])
                scenes.append(cur)
                continue
            if not s or s.startswith("#"):
                continue
            if cur is None:
                continue
            cur[1].append(s)
        return scenes

    # いまの形——`＊` の区切り。名は順、本文は区切りの**あいだ**（最初の区切りの前が第1節）。
    scenes, cur = [("1", [])], None
    for ln in lines:
        s = ln.strip()
        if RULE_RE.match(s):
            cur = (str(len(scenes) + 1), [])
            scenes.append(cur)
            continue
        if not s or s.startswith("#"):
            continue
        scenes[-1][1].append(s)
    return [x for x in scenes if x[1]]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("drafts", nargs="+")
    ap.add_argument("--longest", action="store_true", help="最長の段落も出す")
    a = ap.parse_args()

    files = []
    for pat in a.drafts:
        hit = sorted(glob.glob(pat))
        files.extend(hit if hit else [pat])

    scanned = 0
    for f in files:
        p = pathlib.Path(f)
        if not p.exists():
            print(f"⚠ 無い——{f}", file=sys.stderr)
            continue
        text = p.read_text(encoding="utf-8")
        if not text.strip():
            print(f"⚠ 空である——{f}", file=sys.stderr)
            return 1
        scanned += 1
        scenes = scene_blocks(text.split("\n"))
        total = sum(len(b) for _, b in scenes)
        print(f"■ {p.name}  段落 {total}")

        first = last = None
        longest = (0, "")
        over = 0
        for name, paras in scenes:
            buns = [bun(x) for x in paras]
            if not paras:
                continue
            n5 = sum(1 for b in buns if b >= 5)
            over += n5
            mk = f"  ⚠ 五文以上 {n5}" if n5 else ""
            print(
                f"   第{name}節  段落 {len(paras):3d}  文 {sum(buns):4d}  "
                f"文/段落 {sum(buns)/len(paras):.2f}  最長 {max(buns)}{mk}"
            )
            if first is None:
                first = paras[0]
            last = paras[-1]
            for x in paras:
                if bun(x) > longest[0]:
                    longest = (bun(x), x)

        print(f"   入口（場面1の第一段落）——文 {bun(first)}｜{first}")
        print(f"   話末（場面3の最終段落）——文 {bun(last)}｜{last}")
        if a.longest:
            print(f"   最長——文 {longest[0]}｜{longest[1]}")
        if over:
            print(f"   ⚠ 五文以上 計 {over}")
        print()

    if scanned == 0:
        print("⚠ 一本も走査していない", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
