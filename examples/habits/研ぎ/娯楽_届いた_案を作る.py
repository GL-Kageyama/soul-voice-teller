#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""娯楽_届いた_案を作る——[`娯楽台帳.tsv`](娯楽台帳.tsv) の `案` 欄から、**当てる台帳**を作る。

⚠ **娯楽台帳の `案` は、四人が書いた。** 巻ごとに一人（[`第七段階_第四段_娯楽_届いたかを測る_第二層.md`](第七段階_第四段_娯楽_届いたかを測る_第二層.md)）。
**形は一つである**——`行番号: いまの文 → 案の文`（⚠ その形であることは、
[`娯楽台帳を検める.py`](娯楽台帳を検める.py) の値域の検査が確かめている）。

**この器は、その一欄を、二つの台帳に開く**——

1. **七欄の案台帳**（`娯楽_届いた_案.tsv`）——[`台帳を検める.py`](台帳を検める.py) に掛けるため。
   `巻 / 話 / 行番号 / いまの文 / 案 / 観点 / 根拠`
   ⚠ **観点**＝台帳の `実現した軸`・`三種`（**読者が、何を届いたと見たか**）。
   ⚠ **根拠**＝台帳の `器（与えた／欠けさせた）`（**その場面のフックの、逐語**）。
2. **四欄の差し替え台帳**（`--swap`）——[`差し替える.py`](差し替える.py) に掛けるため。
   `パス / 行番号 / いまの文 / 置き換える文`

使い方:
    python3 娯楽_届いた_案を作る.py > 娯楽_届いた_案.tsv
    python3 娯楽_届いた_案を作る.py --swap > 娯楽_届いた_差し替え.tsv
    python3 娯楽_届いた_案を作る.py --summary      # 検算だけ
"""

import argparse
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE.parent.parent

PLAN = re.compile(r"^(\d+):\s*(.+?)\s*→\s*(.+)$")
DASH = "—"


def draft_path(vol: str, ep: str) -> Path:
    d = EXAMPLES / f"habits-{vol}" / "草稿"
    hits = sorted(d.glob(f"draft_{vol}-{ep}_*.md"))
    if not hits:
        sys.exit(f"⛔ 本文が見つからない: {vol}-{ep}")
    return hits[0]


def draft_rel(vol: str, ep: str) -> str:
    """差し替え台帳のパスは、**examples/ からの相対**である（`差し替える.py` の流儀）。"""
    return f"habits-{vol}/草稿/{draft_path(vol, ep).name}"


def line_of(vol: str, ep: str, n: int) -> str:
    """その行。⚠ 空行も見出しも数える（台帳と同じ物差し）。"""
    return draft_path(vol, ep).read_text(encoding="utf-8").splitlines()[n - 1]


def fit(line: str, now: str, new: str) -> str | None:
    """案の「いまの文」が、行の**一部**であるとき、行に合わせて組み立てる。

    ⚠ **四人の案は、長い行の一部を引いていることがある**（実測——140件のうち 12件）。
        案を書いた者は、行の**どこか**を引いて、そのうしろへ一句足した。
    ⚠ **足した一句は、行の末尾へ置く。** 引いた部分の直後へ挿すのではない——
        **元の文の順序を動かさないためである**（「内容を失わずに」）。
        ⚠ 台詞の行（`03-12:221`「「同じです。」」）では、直後へ挿すと**鉤括弧の内側が伸びる**。
        行末へ置けば、地の文が台詞のあとに付く——それが案の意図である。
    """
    if line == now:
        return new
    if not new.startswith(now) or now not in line:
        return None
    return line + new[len(now):]


def main() -> int:
    ap = argparse.ArgumentParser(description="娯楽台帳の案を、当てる台帳へ開く")
    ap.add_argument("--swap", action="store_true",
                    help="差し替える.py の四欄台帳で出す")
    ap.add_argument("--summary", action="store_true", help="検算だけを出す")
    ap.add_argument("--ledger", default="娯楽台帳.tsv")
    a = ap.parse_args()

    raw = [ln for ln in Path(a.ledger).read_text(encoding="utf-8").split("\n") if ln.strip()]
    rows = list(csv.reader(raw, delimiter="\t"))
    hdr, body = rows[0], rows[1:]
    i = {c: k for k, c in enumerate(hdr)}
    V = lambda r, c: r[i[c]]

    out, odd, vols, fitted = [], [], {}, []
    for r in body:
        p = V(r, "案")
        if p == DASH:
            continue
        m = PLAN.match(p)
        if not m:
            odd.append(f"{r[0]}-{r[1]}: {p[:80]}")
            continue
        key = r[0]                      # 01-01
        vol, ep = key[:2], key[3:]
        n, now, new = m.group(1), m.group(2).strip(), m.group(3).strip()
        # ⚠ **案の「いまの文」が、行の一部であることがある**（実測——140件のうち 12件）。
        #    台帳を検める.py は**完全一致**を要するゆえ、そのままでは ⛔ になる。
        #    **行に合わせて組み立てる**（`fit`）——そして、**組み立てたことを黙らない**。
        line = line_of(vol, ep, int(n))
        if line != now:
            f = fit(line, now, new)
            if f is None:
                odd.append(f"{key}-{r[1]}: 行 {n} に合わせられない——{now[:60]}")
                continue
            fitted.append((f"{key}-{r[1]}", n, now, line, f))
            now, new = line, f
        vols[vol] = vols.get(vol, 0) + 1
        view = f"{V(r, '実現した軸')}・{V(r, '三種')}〔{V(r, '掴んでいるか')}〕"
        ground = V(r, "器（与えた／欠けさせた）")
        if a.swap:
            out.append("\t".join([draft_rel(vol, ep), n, now, new]))
        else:
            out.append("\t".join([vol, ep, n, now, new, view, ground]))

    if odd:
        sys.exit("⛔ 案の形が違う行が " + str(len(odd)) + " 件ある:\n  " + "\n  ".join(odd[:5]))

    # ⚠ **組み立てた件数を、黙らない。** 四巻の読者が引いた「いまの文」が行の一部であった件は、
    #    器が行全体へ組み立てた。**その一つ一つを、人が読めるように出す**——
    #    ⚠ stderr へ出す（標準出力の台帳を汚さないため）。
    if fitted:
        print(f"⚠ 案の「いまの文」が行の一部であった——{len(fitted)} 件。"
              f"行に合わせて組み立てた:", file=sys.stderr)
        for at, n, now, line, f in fitted:
            print(f"  {at} :{n}", file=sys.stderr)
            print(f"    行: {line}", file=sys.stderr)
            print(f"    引: {now}", file=sys.stderr)
            print(f"    案: {f}", file=sys.stderr)

    if a.summary:
        print(f"案——{len(out)} 件（うち、行に合わせて組み立てた {len(fitted)} 件）")
        for v in sorted(vols):
            print(f"  第{v}巻  {vols[v]}")
        return 0

    # ⚠ 見出し行は `#` で始める——`台帳を検める.py` も `差し替える.py` も `#` の行を読み飛ばす。
    #   **付けなければ、この見出しが「案」として読まれ、⛔ を出す**（実測）。
    #   ⚠ 既存の台帳（`娯楽_ズレ_案.tsv`）と同じ流儀へ揃える。
    if a.swap:
        print("# 娯楽台帳.tsv（22欄）の `案` 欄から作った、差し替える.py 用の4欄台帳。"
              "パスは examples/ からの相対ゆえ、`cd examples` から当てる。")
        print(f"# 件 {len(out)}（うち、行に合わせて組み立てた {len(fitted)} 件）。")
    else:
        print("# 娯楽_届いた_案.tsv——娯楽台帳.tsv（22欄）の `案` 欄を、"
              "台帳を検める.py に掛ける7欄へ開いたもの。")
        print(f"# 件 {len(out)}（うち、行に合わせて組み立てた {len(fitted)} 件）。"
              "**観点＝読者が見た軸・三種〔掴んでいるか〕／根拠＝その場面の器の逐語。**")
        print("#" + "\t".join(["巻", "話", "行番号", "いまの文", "案", "観点", "根拠"]))
    for line in out:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
