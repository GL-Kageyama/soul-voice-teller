#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""娯楽台帳_第二層_後_束ねる——四人が書いた「人の欄」を、台帳の骨へ戻す。

**なぜ、この器が要るか。** 台帳（[`台帳を作る.py`](台帳を作る.py)）は**機械の15欄しか作らない**。
**人の7欄は、四人が巻ごとに別々の TSV へ書いた**（`娯楽台帳_第二層_後_0N.tsv`）。
**この器は、それを (話, 場面) で合流させるだけである。**

⚠ **合流の鍵は「話＋場面」である**（[[scan-key-must-match-the-field]]——
   鍵は、その欄の字そのものに掛ける。`話` は `NN-NN`、`場面` は `1`/`2`/`3`）。

⚠ **この器は、値を一字も直さない。** 直すのは検める器（`娯楽台帳を検める.py`）の仕事である。

使い方:
    python3 娯楽台帳_第二層_後_束ねる.py            # 確かめだけ（書かない）
    python3 娯楽台帳_第二層_後_束ねる.py --write    # 台帳を書き換える
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "娯楽台帳_第二層_後.tsv"
VOLS = ["01", "02", "03", "04"]
READER = ["実現した軸", "三種", "掴んでいるか", "器（与えた／欠けさせた）",
          "設計との差", "ズレの有無", "案"]


def read_tsv(p):
    lines = [ln for ln in p.read_text(encoding="utf-8").split("\n") if ln.strip()]
    hdr = lines[0].split("\t")
    return hdr, [ln.split("\t") for ln in lines[1:]]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--base", default=str(BASE))
    a = ap.parse_args()

    base_hdr, base_rows = read_tsv(Path(a.base))
    if base_hdr[0] != "話" or base_hdr[1] != "場面":
        sys.exit("骨のヘッダが違う")

    human = {}
    for v in VOLS:
        p = HERE / f"娯楽台帳_第二層_後_{v}.tsv"
        if not p.exists():
            sys.exit(f"無い: {p.name}")
        hdr, rows = read_tsv(p)
        # ⚠ 読者のファイルのヘッダは `話`＋`場面`＋7欄＝**9欄**である（手引き §3 のとおり）。
        #    ゆえに、比べるのは `hdr[2:]` である——**一度 `hdr[1:]` と書いて、四人とも落ちた**
        #    （第一巻の読者が申告してくれた）。器の側の欠陥であって、読者の側ではない。
        if hdr[:2] != ["話", "場面"] or hdr[2:] != READER:
            sys.exit(f"{p.name}——ヘッダが違う: {hdr}")
        for r in rows:
            key = (r[0], r[1])
            if key in human:
                sys.exit(f"鍵が重なる: {key}（{p.name}）")
            human[key] = r[2:9]

    print(f"骨——{len(base_rows)} 行")
    print(f"人が書いた——{len(human)} 行（" +
          "・".join(f"{v}:{sum(1 for k in human if k[0].startswith(v + '-'))}" for v in VOLS) + "）")

    missing = [k for k in ((r[0], r[1]) for r in base_rows) if k not in human]
    stray = [k for k in human if k not in {(r[0], r[1]) for r in base_rows}]
    print(f"骨に在って、人が書いていない——{len(missing)} 行" + (f"（例 {missing[:5]}）" if missing else ""))
    print(f"人が書いて、骨に無い——{len(stray)} 行" + (f"（例 {stray[:5]}）" if stray else ""))

    out = []
    for r in base_rows:
        k = (r[0], r[1])
        out.append(r[:15] + human.get(k, [""] * 7))

    widths = {len(r) for r in out}
    print(f"欄の数——{widths}（{len(base_hdr)} であること）")

    if missing or stray:
        print("⛔ 合流しない鍵がある。書かない。")
        return 1

    if not a.write:
        print("（確かめのみ。書くには --write）")
        return 0

    text = "\t".join(base_hdr) + "\n" + "\n".join("\t".join(r) for r in out) + "\n"
    BASE.write_text(text, encoding="utf-8")
    print(f"✅ 書いた——{BASE.name}（{len(out)} 行）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
