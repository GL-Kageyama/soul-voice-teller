#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""反復句の索引を取り、当てる前と後で較べる。

⚠ なぜ要るか。`検査/check.py` は**基底語の規則**を持つ——
`MIN_LINE_FOR_REUSE = 12` 字以上の**文**が、**ちょうど二話**に現れるときだけ鳴る。
**三話以上に現れる行は「基底語」であり、鳴らない。**
ゆえに、**新しい反復を足しても、それが三話目に達した瞬間、検査器は沈黙する。**
**「鳴っていない」ことと「無い」ことは違う。** この器は、その穴を塞ぐ。

単位＝**段落**（段落化のあとの、物理的な一行）。当てる器 `差し替える.py` が
段落→段落の差し替えであるゆえ、索引の単位も段落に合わせる。

使い方
  重複を較べる.py                     いまの索引を出す
  重複を較べる.py --save base.json    索引を保存する（基準線）
  重複を較べる.py --baseline base.json 基準線と較べ、増えた一致と減った一致を出す
  重複を較べる.py --chapters 3        三話以上だけを出す（既定 2）
  重複を較べる.py --min 8             最低字数（既定 12＝検査器と同じ）

⚠ **`--baseline` で引くときは、基準線を採ったのと同じ `--min` を渡す。**
なぜなら **`--min` は、いまの索引にしか掛からない**（`compare()` は base をそのまま読む）。
**12 字で採った基準線を 8 字で引くと、8〜11 字の句が「基準線に無い」ものとして
すべて「新しく現れた一致」に出る**（2026-10-14、`--min 8 --baseline 重複の基準線.json` が
「新 10 件」を返して踏んだ。同じ字で採り直すと 0 件である）。
**ゆえに、`--min` を変えて較べるときは、その木で `--save` し直す。**
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import pathlib
import re
import sys
from collections import defaultdict

HERE = pathlib.Path(__file__).resolve().parent
EXAMPLES = HERE.parent.parent          # examples/
DRAFTS = "habits-0*/草稿/draft_*.md"

VOL_RE = re.compile(r"habits-0(\d)/")


def chapter_id(path: str) -> tuple[str, str]:
    """(巻, 話) を返す。例＝('02', '02-14')"""
    m = VOL_RE.search(path)
    vol = m.group(1) if m else "??"
    ep = re.search(r"draft_(\d\d-\d\d)", os.path.basename(path))
    return vol, (ep.group(1) if ep else os.path.basename(path))


def paragraphs(path: str) -> list[tuple[int, str]]:
    """(行番号, 段落) を返す。行番号は 1 起点、ファイル全体の行番号である。"""
    out = []
    with open(path, encoding="utf-8") as fh:
        for i, ln in enumerate(fh, 1):
            s = ln.rstrip("\n")
            if not s.strip():
                continue
            if s.startswith("#") or s.startswith(">"):
                continue
            out.append((i, s.strip()))
    return out


def build_index(min_len: int) -> dict[str, list[str]]:
    """段落の本文 → それが現れる話の一覧（重複なし・ソート済み）。"""
    idx: dict[str, set[str]] = defaultdict(set)
    for path in sorted(glob.glob(str(EXAMPLES / DRAFTS))):
        _, ep = chapter_id(path)
        for _, text in paragraphs(path):
            if len(text) < min_len:
                continue
            idx[text].add(ep)
    return {k: sorted(v) for k, v in idx.items()}


def report(idx: dict[str, list[str]], lo: int) -> None:
    hits = {k: v for k, v in idx.items() if len(v) >= lo}
    two = {k: v for k, v in hits.items() if len(v) == 2}
    many = {k: v for k, v in hits.items() if len(v) >= 3}
    print(f"索引の総数        {len(idx)} 段落（{lo} 話以上に現れるものだけを、下に出す）")
    if lo <= 2:
        print(f"ちょうど二話      {len(two)} 種   ← 検査器 `check.py` が鳴く側")
    print(f"三話以上（基底語） {len(many)} 種   ← 検査器は**沈黙する**側")
    print()
    print("=== 三話以上に現れる段落（多い順）===")
    for text, eps in sorted(many.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:60]:
        print(f"{len(eps):3d} 話  {text}")
        print(f"        {', '.join(eps)}")
    if lo <= 2:
        print()
        print("=== ちょうど二話に現れる段落 ===")
        for text, eps in sorted(two.items(), key=lambda kv: kv[0])[:40]:
            print(f"  2 話  {text}")
            print(f"        {', '.join(eps)}")


def compare(base: dict[str, list[str]], now: dict[str, list[str]], lo: int) -> int:
    b = {k: set(v) for k, v in base.items()}
    n = {k: set(v) for k, v in now.items()}
    added, removed, spread = [], [], []
    for text, eps in n.items():
        if len(eps) < lo:
            continue
        was = b.get(text, set())
        if not was:
            added.append((text, sorted(eps)))
        elif len(eps) > len(was):
            spread.append((text, sorted(was), sorted(eps)))
    for text, eps in b.items():
        if len(eps) < lo:
            continue
        if text not in n:
            removed.append((text, sorted(eps)))
    print(f"基準線と較べる（{lo} 話以上）")
    print(f"  新しく現れた一致   {len(added)}")
    print(f"  広がった一致       {len(spread)}")
    print(f"  消えた一致         {len(removed)}")
    if added:
        print("\n=== 新しく現れた一致（⚠ 検査器は、三話目で沈黙する）===")
        for text, eps in added:
            print(f"{len(eps):3d} 話  {text}")
            print(f"        {', '.join(eps)}")
    if spread:
        print("\n=== 広がった一致 ===")
        for text, was, eps in spread:
            print(f"{len(was)} → {len(eps)} 話  {text}")
            print(f"        {', '.join(eps)}")
    if removed:
        print("\n=== 消えた一致（✅ 直った側）===")
        for text, eps in removed:
            print(f"{len(eps):3d} 話  {text}")
    return len(added) + len(spread)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="反復句の索引を取り、当てる前と後で較べる（検査器の基底語規則が隠す分を見る）")
    ap.add_argument("--min", type=int, default=12, help="最低字数（既定 12＝検査器と同じ）")
    ap.add_argument("--chapters", type=int, default=2, help="報告する最小話数（既定 2）")
    ap.add_argument("--save", metavar="FILE", help="索引を保存する（基準線）")
    ap.add_argument("--baseline", metavar="FILE", help="基準線と較べる")
    args = ap.parse_args()

    if args.baseline:
        base = json.load(open(args.baseline, encoding="utf-8"))
        now = build_index(args.min)
        n = compare(base, now, args.chapters)
        print()
        if n == 0:
            print("✅ 増えた一致は 0 件である")
        else:
            print(f"⚠ 増えた一致が {n} 件ある——**検査器は、これを一件も鳴らさない**")
        return 0

    idx = build_index(args.min)
    if args.save:
        json.dump(idx, open(args.save, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1, sort_keys=True)
        print(f"保存した {args.save}（{len(idx)} 段落）")
        return 0
    report(idx, args.chapters)
    return 0


if __name__ == "__main__":
    sys.exit(main())
