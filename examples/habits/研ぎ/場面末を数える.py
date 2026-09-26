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
import sys

HERE = pathlib.Path(__file__).resolve().parent
BACKUP = HERE / "段落化の控え"
SENT = "。？！?"
VOLS = [("01", "第一巻"), ("02", "第二巻"), ("03", "第三巻"), ("04", "第四巻")]


def kuten(p: str) -> int:
    return p.count("。")


def bun(p: str) -> int:
    return sum(p.count(c) for c in SENT)


def scene_finals(text: str):
    """[(場面名, 最後の本文行), ...]。見出し `## N` で切り、空行と見出しを飛ばす。"""
    out, cur, last = [], None, None
    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith("## "):
            if cur is not None:
                out.append((cur, last))
            cur, last = s[3:].strip(), None
            continue
        if not s or s.startswith("#") or s == "---":
            continue
        if cur is None:
            continue
        last = s
    if cur is not None:
        out.append((cur, last))
    return [(n, t) for n, t in out if t]


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
