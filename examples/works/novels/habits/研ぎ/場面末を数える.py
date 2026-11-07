#!/usr/bin/env python3
"""場面の最後の本文行を、段落化の前後で較べる（読み取り専用）。

目的——**段落化の台帳が「場面の最後の行を組まなかった」かを、控えと突き合わせて数える。**
指示書 §1 の 3 は、台帳を作る者に「場面の最後の行を『組む』と書かない」と命じている。
これは、その規律が守られたかどうかを、申告ではなく実物で測る器である。

⚠ 控え（`段落化の控え/`）が無い話は、段落化を当てていない。**当てていない話は数えない**
（⚠ 数えないことを、報告の行に必ず書く）。

出すもの——
  * 話ごとに、場面1・2・3 の最後の本文行を、控えと今とで並べる
  * **⚠ 組まれた場面末**——控えでは一文であり、いまは二文以上であるもの
  * いまの草稿だけでの集計（表の側の数と突き合わせるため）

⚠ 数え方は二つ出す——`。` だけの数（文の数に近い）と、`。？?！` の数（`段落化_計画` §12 の数え方）。

⚠ 一本も走査しなければ exit 1（空の検査は OK と言う、を避ける）。
"""
import argparse
import glob
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
BACKUP = HERE / "段落化の控え"
SENT = "。？！?"
VOLS = [("01", "第一巻"), ("02", "第二巻"), ("03", "第三巻"), ("04", "第四巻")]

# ⚠ 場面を切る印は、いま二つの形がある——**著者裁定 2026-10-13**。
#   * いまの草稿——`＊`（全角のアスタリスク）だけの行。**区切りである。一話に二つ。**
#     節と節のあいだに置かれるゆえ、**最初の区切りより前が第1節である。名を持たない。**
#   * 控え（`段落化の控え/`）——`## N` の見出し。**札である。場面の前に置かれる。名を持つ。**
#   ゆえに、この器は**両方を受ける**（節は、名ではなく順で突き合わせる）。
HEAD_RE = re.compile(r"^##\s*(\d+)\s*$")
RULE_RE = re.compile(r"^＊$")


def kuten(p: str) -> int:
    return p.count("。")


def bun(p: str) -> int:
    return sum(p.count(c) for c in SENT)


def scene_finals(text: str):
    """[(節番号, 最後の本文行), ...]。空行と見出しと区切りを飛ばす。

    ⚠ 二つの形を受ける（HEAD_RE を見よ）——**控えは札（`## N`）、いまは区切り（`＊`）。**
    """
    lines = text.split("\n")

    if any(HEAD_RE.match(l.strip()) for l in lines):
        # 控えの形——`## N` の札。名は N、本文は札の**あと**。
        out, cur, last = [], None, None
        for ln in lines:
            s = ln.strip()
            m = HEAD_RE.match(s)
            if m:
                if cur is not None:
                    out.append((cur, last))
                cur, last = m.group(1), None
                continue
            if not s or s.startswith("#") or s == "---":
                continue
            if cur is None:
                continue
            last = s
        if cur is not None:
            out.append((cur, last))
        return [(n, t) for n, t in out if t]

    # いまの形——`＊` の区切り。名は順（1 から）、本文は区切りの**あいだ**。
    out, num, last = [], 1, None
    for ln in lines:
        s = ln.strip()
        if RULE_RE.match(s):
            if last:
                out.append((str(num), last))
            num, last = num + 1, None
            continue
        if not s or s.startswith("#") or s == "---":
            continue
        last = s
    if last:
        out.append((str(num), last))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--joined-only", action="store_true", help="組まれた場面末だけを出す")
    a = ap.parse_args()

    scanned = backed = 0
    joined = []
    table = []
    for v, vname in VOLS:
        print(f"===== {vname}")
        n_now = n_bak = s_now = s_bak = 0
        for f in sorted(glob.glob(str(HERE / f"../../habits-{v}/草稿/draft_*.md"))):
            p = pathlib.Path(f)
            text = p.read_text(encoding="utf-8")
            if not text.strip():
                print(f"⚠ 空である——{f}", file=sys.stderr)
                return 1
            scanned += 1
            now = scene_finals(text)
            bak_p = BACKUP / p.name
            if bak_p.exists():
                backed += 1
                before = dict(scene_finals(bak_p.read_text(encoding="utf-8")))
                s_bak += len(before)
                n_bak += sum(1 for x in before.values() if kuten(x) >= 2)
            else:
                before = {}
            s_now += len(now)
            n_now += sum(1 for _, x in now if kuten(x) >= 2)
            for name, line in now:
                b = before.get(name)
                if b is None:
                    continue
                if kuten(b) <= 1 and kuten(line) >= 2:
                    joined.append((vname, p.name, name, b, line))
                    if not a.joined_only:
                        print(f"   ⚠ {p.name} 場面{name}——控え「{b}」→ いま「{line}」")
                    continue
                if not a.joined_only and b != line:
                    print(f"   {p.name} 場面{name}——控え「{b}」／いま「{line}」")
        table.append((vname, s_now, n_bak, n_now, s_bak))
        print()

    print("■ 表——場面の数と、その最後の本文行が二文以上であるものの数（⚠ 数え方は `。` の数）")
    print("| 巻 | 場面 | 控えで二文以上 | いま二文以上 |")
    print("|---|---:|---:|---:|")
    for vname, s_now, n_bak, n_now, s_bak in table:
        bak = f"{n_bak}（⚠ 控え {s_bak} 場面）" if s_bak else "**控えが無い**"
        print(f"| {vname} | {s_now} | {bak} | **{n_now}** |")
    print()

    print(f"■ 走査した話 {scanned} 本。うち控えと較べた話 {backed} 本。")
    if backed < scanned:
        print(f"⚠ 較べていない話が {scanned - backed} 本ある（⚠ 段落化を当てていない話である。数に入れていない）。")
    print(f"■ ⚠ 組まれた場面末（控え一文 → いま二文以上）——{len(joined)} 件。")
    for vname, fn, name, b, line in joined:
        print(f"   {vname} {fn} 場面{name}｜{b} → {line}")

    if scanned == 0:
        print("⚠ 一本も走査していない", file=sys.stderr)
        return 1
    if backed == 0:
        print("⚠ 控えと較べた話が一本も無い", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
