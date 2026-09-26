#!/usr/bin/env python3
"""挿し入れる——指定した行の前か後に、一行だけを足す。

第三段の「差し替える」は、行数を動かさない。**第四段は、行数を動かす。**
足すのは具体（行為・映像・音）であり、それは既存の行の置き換えではなく、新しい一行である。

ゆえに、この器は「差し替える」と別に要る。守ることは、次の三つである。

1. **狙った行が、いま、その文であること**（当てる前）。
2. **足したのが、狙った位置だけであること**——ほかの行が、一字も動いていないこと（当てた後）。
3. **動いた行数が、足した数とちょうど合うこと**。

⚠ 本文の体裁——**本文の一行の次は、必ず空行である。**
ゆえに「前」に足すときは、空行ごと足す（二行増える）。
「後」に足すときは、文だけを足す（**もとの空行が、そのまま仕切りになる**。一行増える）。

台帳（マニフェスト）の形式——タブ区切り、一行一件。
**前三欄は「差し替える.py」と同じである**（読む者が同じに読めるように）。

    ファイルパス<TAB>行番号<TAB>いまの文<TAB>挿し入れる文<TAB>前|後

⚠ 行番号は、**いまの本文の行番号**である（当てる前の）。
⚠ 同じファイルに何件も当てるときも、**行番号はすべて「当てる前」のものでよい。**
   この器は、元の本文に照らして一度に組む（一件ずつ書き換えない）。

使い方:
    python3 挿し入れる.py <台帳>            # 当てずに、確かめるだけ
    python3 挿し入れる.py <台帳> --write    # 当てる
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

WHERE = ("前", "後")


def read_ledger(path: Path) -> list[tuple[Path, int, str, str, str]]:
    rows = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 5:
            raise SystemExit(
                f"台帳 {i} 行目——欄が {len(parts)} 個である（5 個でなければならない）\n"
                "   ファイル<TAB>行番号<TAB>いまの文<TAB>挿し入れる文<TAB>前|後"
            )
        f, n, old, new, where = parts
        if where not in WHERE:
            raise SystemExit(f"台帳 {i} 行目——第五欄が「{where}」である（前か後でなければならない）")
        rows.append((Path(f), int(n), old, new, where))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="指定した行の前か後に、一行だけを足す")
    ap.add_argument("ledger")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    rows = read_ledger(Path(args.ledger))
    if not rows:
        print("⛔ 台帳が空である——当てるものが無い")
        return 2

    # 一ファイルを一度だけ読み、そのファイルの全件を「元の本文」に照らして確かめる。
    # 一件ずつ書き換えると、二件目の行番号が一件目に食われる。読むのは一度きりである。
    bad: list[str] = []
    order: list[Path] = []
    grouped: dict[Path, list[tuple[int, str, str, str]]] = defaultdict(list)
    for f, n, old, new, where in rows:
        if f not in grouped:
            order.append(f)
        grouped[f].append((n, old, new, where))

    plans = []
    for f in order:
        items = grouped[f]
        if not f.exists():
            bad.append(f"{f}——ファイルが無い")
            continue
        lines = f.read_text(encoding="utf-8").splitlines()
        ok = []
        for n, old, new, where in items:
            if not (1 <= n <= len(lines)):
                bad.append(f"{f.name}:{n}——行が無い（全 {len(lines)} 行）")
                continue
            if lines[n - 1] != old:
                bad.append(f"{f.name}:{n}——いまの文が違う\n    台帳: {old}\n    本文: {lines[n - 1]}")
                continue
            if not new.strip():
                bad.append(f"{f.name}:{n}——挿し入れる文が空である")
                continue
            if "\n" in new or "\n" in old:
                bad.append(f"{f.name}:{n}——文に改行が入っている")
                continue
            if lines[n - 1].lstrip().startswith("#"):
                bad.append(f"{f.name}:{n}——見出し行を狙っている: {lines[n - 1]}")
                continue
            # 「後」に足すとき、次の行が空行でなければ、文が接ぎ木される。
            if where == "後":
                if n == len(lines):
                    bad.append(f"{f.name}:{n}——最終行の「後」に足そうとしている（仕切りが無い）")
                    continue
                if lines[n].strip():
                    bad.append(
                        f"{f.name}:{n}——「後」に足すが、次の行が空行でない\n"
                        f"    次の行: {lines[n]}"
                    )
                    continue
            ok.append((n, old, new, where))
        # 同じ位置を二度、狙っていないか
        keys = [(n, w) for n, _o, _n2, w in ok]
        if len(set(keys)) != len(keys):
            dup = sorted({k for k in keys if keys.count(k) > 1})
            bad.append(f"{f.name}——同じ位置を二度狙っている: {dup}")
            continue
        if ok:
            plans.append((f, lines, ok))

    if bad:
        print(f"⛔ 当てられない {len(bad)} 件——一件も当てていない")
        for b in bad:
            print("   " + b)
        return 1

    # 組む。元の本文を頭から歩き、狙われた行の前か後に足す。
    results = []
    for f, lines, ok in plans:
        before_at: dict[int, list[str]] = defaultdict(list)
        after_at: dict[int, list[str]] = defaultdict(list)
        for n, _old, new, where in ok:
            (before_at if where == "前" else after_at)[n].append(new)

        out: list[str] = []
        added: set[int] = set()
        # 足した行が、もとのどの行でもないことを、索引で言えるようにする。
        for i, line in enumerate(lines, 1):
            for new in before_at.get(i, []):
                added.add(len(out))
                out.append(new)
                added.add(len(out))
                out.append("")          # 本文の一行の次は、必ず空行である
            out.append(line)
            for new in after_at.get(i, []):
                added.add(len(out))
                out.append(new)         # もとの空行が、そのまま仕切りになる

        # 当てた後の検査——足した行を取り除けば、もとの本文に戻ること。
        restored = [l for j, l in enumerate(out) if j not in added]
        if restored != lines:
            bad.append(f"{f.name}——組んだ結果が、もとの本文に戻らない（この器の欠陥）")
            continue
        n_before = sum(len(v) for v in before_at.values())
        n_after = sum(len(v) for v in after_at.values())
        expected = len(lines) + 2 * n_before + n_after
        if len(out) != expected:
            bad.append(f"{f.name}——行数が {len(out)} になった（{expected} のはずである）")
            continue
        results.append((f, lines, out, ok, added))

    if bad:
        print(f"⛔ 組めない {len(bad)} 件——一件も当てていない")
        for b in bad:
            print("   " + b)
        return 1

    count = sum(len(ok) for _f, _l, _o, ok, _a in results)
    for f, lines, out, ok, added in results:
        print(f"■ {f.name}   {len(lines)} 行 → {len(out)} 行（＋{len(out) - len(lines)}）")
        for n, _old, new, where in sorted(ok):
            print(f"   {n}行目の{where}  ＋ {new}")
            ctx = [l for l in lines[max(0, n - 3):n]]
            if ctx:
                print(f"        前: {' / '.join(x for x in ctx if x) or '（空）'}")
        print()

    if not args.write:
        print(f"〔確かめのみ〕{len(results)} 本 / {count} 件。当てるには --write を付ける。")
        return 0

    for f, _lines, out, _ok, _added in results:
        f.write_text("\n".join(out) + "\n", encoding="utf-8")

    print(f"✅ {len(results)} 本 / {count} 件を当てた")
    print("⚠ 以後、この段より下の引用（NN-NN:NNN）は、挿し入れた数だけずれる（前は +2、後は +1）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
