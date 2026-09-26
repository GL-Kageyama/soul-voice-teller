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
import sys

SENT = "。？！?"


def bun(p: str) -> int:
    return sum(p.count(c) for c in SENT)


def scene_blocks(lines):
    """(場面番号, [段落, ...]) を返す。見出し '## N' で切る。"""
    scenes, cur = [], None
    for ln in lines:
        s = ln.strip()
        if s.startswith("## "):
            cur = (s[3:].strip(), [])
            scenes.append(cur)
            continue
        if not s or s.startswith("#"):
            continue
        if cur is None:
            continue
        cur[1].append(s)
    return scenes


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
                f"   ## {name}  段落 {len(paras):3d}  文 {sum(buns):4d}  "
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
