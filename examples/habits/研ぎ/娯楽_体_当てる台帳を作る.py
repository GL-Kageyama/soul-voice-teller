#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""娯楽_体_当てる台帳を作る——七欄の案を、[`差し替える.py`](差し替える.py) の四欄へ開く。

**なぜ、この器が要るか。** 案は七欄（`巻／話／行番号／いまの文／案／観点／根拠`）で書かれる
（[`台帳を検める.py`](台帳を検める.py) が読む形）。**当てる器（`差し替える.py`）は四欄**
（`パス／行番号／いまの文／置き換える文`）を読む。**ゆえに、間で一度ひらく。**

**⚠ 話の番号から、草稿のファイルを引く。** 見つからなければ、**そこで止まる**（黙って落とさない）。

    python3 娯楽_体_当てる台帳を作る.py 娯楽_体_案_01.tsv [<案.tsv> …]
"""
import glob
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE.parent.parent                 # examples/
COLS = ["巻", "話", "行番号", "いまの文", "案", "観点", "根拠"]


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    rows = []
    for p in sys.argv[1:]:
        for i, raw in enumerate(Path(p).read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            c = raw.split("\t")
            if c[0].strip() in ("巻", "vol"):        # 見出し
                continue
            if len(c) != 7:
                raise SystemExit(f"⛔ {p} {i} 行目——欄が {len(c)} 個である（7 個でなければならない）")
            d = dict(zip(COLS, c))
            if d["案"].strip() == d["いまの文"].strip():
                raise SystemExit(f"⛔ {p} {i} 行目——案が、いまの文と同じである")
            # ⚠ **`話` の欄は、二つの書き方で来る**——`NN-NN`（指示書の仕様）と、
            #    `NN`（`台帳を検める.py` の `draft_path` が `draft_{巻}-{話}` を引くため、
            #    既存の台帳はこちらで書かれている）。**どちらも受ける。**
            ep = d["話"] if "-" in d["話"] else f"{d['巻']}-{d['話']}"
            g = glob.glob(str(EXAMPLES / f"habits-{d['巻']}" / "草稿" / f"draft_{ep}_*.md"))
            if len(g) != 1:
                raise SystemExit(f"⛔ {p} {i} 行目——{ep} の草稿が {len(g)} 本見つかった")
            rows.append((g[0], int(d["行番号"]), d["いまの文"], d["案"]))

    # ⚠ 同じファイル・同じ行に二件当てない（`差し替える.py` が「いまの文が違う」を返す）
    seen = {}
    for f, n, old, new in rows:
        if (f, n) in seen:
            raise SystemExit(f"⛔ 同じ行に二件——{f} {n}")
        seen[(f, n)] = True

    out = HERE / "娯楽_体_当てる.tsv"
    with open(out, "w", encoding="utf-8") as fh:
        for f, n, old, new in rows:
            fh.write(f"{f}\t{n}\t{old}\t{new}\n")
    print(f"✅ {out.name}——{len(rows)} 件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
