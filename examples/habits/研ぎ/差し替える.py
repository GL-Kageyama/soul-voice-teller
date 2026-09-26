#!/usr/bin/env python3
"""差し替える——指定した一行だけを、指定した一行に置き換える。

この段で本文にしてよいことは、**一行を別の一行に置き換えることだけ**である。
行を増やすことも、減らすことも、ほかの行に触ることも許されない。

そこで、当てる前に「その行が、いま、その文であること」を確かめ、
当てたあとに「行数が変わっていないこと」「変わったのが、その行だけであること」を確かめる。

台帳（マニフェスト）の形式——タブ区切り、一行一件:

    ファイルパス<TAB>行番号<TAB>いまの文<TAB>置き換える文

使い方:
    python3 差し替える.py <台帳>            # 当てずに、確かめるだけ
    python3 差し替える.py <台帳> --write    # 当てる
"""

import argparse
import sys
from pathlib import Path


def read_ledger(path: Path) -> list[tuple[Path, int, str, str]]:
    rows = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 4:
            raise SystemExit(f"台帳 {i} 行目——欄が {len(parts)} 個である（4 個でなければならない）")
        f, n, old, new = parts
        rows.append((Path(f), int(n), old, new))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="指定した一行だけを置き換える")
    ap.add_argument("ledger")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    rows = read_ledger(Path(args.ledger))
    if not rows:
        print("⛔ 台帳が空である——当てるものが無い")
        return 2

    # 一ファイルを一度だけ読み、そのファイルの全件を「元の本文」に照らして確かめる。
    # 二度読むと、二件目が一件目の結果に当たる。読むのは一度きりである。
    bad = []
    order: list[Path] = []
    grouped: dict[Path, list[tuple[int, str, str]]] = {}
    for f, n, old, new in rows:
        if f not in grouped:
            order.append(f)
            grouped[f] = []
        grouped[f].append((n, old, new))

    plans = []
    for f in order:
        items = grouped[f]
        if not f.exists():
            bad.append(f"{f}——ファイルが無い")
            continue
        lines = f.read_text(encoding="utf-8").splitlines()
        ok = []
        for n, old, new in items:
            if not (1 <= n <= len(lines)):
                bad.append(f"{f.name}:{n}——行が無い（全 {len(lines)} 行）")
                continue
            if lines[n - 1] != old:
                bad.append(f"{f.name}:{n}——いまの文が違う\n    台帳: {old}\n    本文: {lines[n - 1]}")
                continue
            if new == old:
                bad.append(f"{f.name}:{n}——置き換え後の文が、置き換え前と同じである")
                continue
            if "\n" in new or "\n" in old:
                bad.append(f"{f.name}:{n}——文に改行が入っている")
                continue
            ok.append((n, old, new))
        # 同じ行を二度、狙っていないか
        ns = [n for n, _o, _w in ok]
        if len(set(ns)) != len(ns):
            bad.append(f"{f.name}——同じ行を二度狙っている: {sorted(ns)}")
            continue
        if ok:
            plans.append((f, lines, ok))

    if bad:
        print(f"⛔ 当てられない {len(bad)} 件——一件も当てていない")
        for b in bad:
            print("   " + b)
        return 1

    count = sum(len(ok) for _f, _l, ok in plans)
    for f, _lines, ok in plans:
        print(f"■ {f.name}")
        for n, old, new in sorted(ok):
            print(f"   {n}行目  − {old}")
            print(f"          ＋ {new}")

    if not args.write:
        print()
        print(f"〔確かめのみ〕{len(plans)} 本 / {count} 件。当てるには --write を付ける。")
        return 0

    # 当てる。行数は動かさない——一対一の置換である。
    for f, lines, ok in plans:
        before = len(lines)
        for n, _old, new in ok:
            lines[n - 1] = new
        assert len(lines) == before, f"{f.name}——行数が動いた"
        f.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print()
    print(f"✅ {len(plans)} 本 / {count} 件を当てた")
    return 0


if __name__ == "__main__":
    sys.exit(main())
