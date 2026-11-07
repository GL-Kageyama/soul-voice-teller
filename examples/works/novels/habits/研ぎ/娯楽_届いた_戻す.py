#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""娯楽_届いた_戻す——当てた案のうち、**要らないものだけ**を、元の一行へ戻す。

⚠ **なぜ要るか。** 娯楽の段の案は、**四人の読者が書いた**（[`第七段階_第四段_娯楽_届いたかを測る_第二層.md`](第七段階_第四段_娯楽_届いたかを測る_第二層.md) §4-1）。
**機械の検査は、色語・匂い・閉じた形・禁則語・一行性を見る**——だが**見ないものが二つある**。
**①その一句が、その場面で既に確立している事実と食い違っていないか。②その行が、場面末・章末であるか。**
**これは人が読む**（`台帳を検める.py` の末尾が、そう書いている）。
**ゆえに、当てたあとに人の読みが入り、⛔ が出た行だけを、ここで戻す。**

⚠ **戻すのは「当てた一行」だけである。** 器は `差し替える.py` と同じ——
**一行を、一行に置き換える。行数は動かない。**

⚠ **この器は、戻す先を「当てたときの台帳」から取る。** ゆえに**台帳が無ければ戻せない**。
**戻す先を推測しない**（推測すれば、本文が静かに壊れる）。

使い方:
    python3 娯楽_届いた_戻す.py --all > 娯楽_届いた_戻す.tsv              # 全部を戻す
    python3 娯楽_届いた_戻す.py --only 03-07:363 01-01:121 > …            # 選んで戻す
    python3 娯楽_届いた_戻す.py --only-file /tmp/戻す.txt > …             # 一行一件の鍵の一覧から
    python3 娯楽_届いた_戻す.py --check                                   # いまの本文が、当てたまま／戻した／どちらでもない、のどれか
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE.parent.parent
SWAP = HERE / "娯楽_届いた_差し替え.tsv"


def read_swap(path: Path) -> list[tuple[str, str, str, str]]:
    """(パス, 行番号, 当てる前, 当てた後)"""
    out = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 4:
            sys.exit(f"⛔ 台帳 {i} 行目——欄が {len(parts)} 個である（4 個でなければならない）")
        out.append(tuple(parts))          # type: ignore[arg-type]
    return out


def key_of(rel: str, n: str) -> str:
    """`habits-03/草稿/draft_03-07_….md` + `363` → `03-07:363`"""
    return f"{Path(rel).name.split('_')[1]}:{n}"


def current(rel: str, n: str) -> str:
    p = EXAMPLES / rel
    return p.read_text(encoding="utf-8").split("\n")[int(n) - 1]


def main() -> int:
    ap = argparse.ArgumentParser(description="当てた案を、元の一行へ戻す")
    ap.add_argument("--all", action="store_true", help="台帳の全部を戻す")
    ap.add_argument("--only", nargs="*", default=[], help="戻す鍵（例 03-07:363）")
    ap.add_argument("--only-file", help="鍵を一行一件で書いたファイル")
    ap.add_argument("--check", action="store_true",
                    help="いまの本文が、当てたときの台帳と一致するかだけを見る")
    ap.add_argument("--ledger", default=str(SWAP))
    a = ap.parse_args()

    rows = read_swap(Path(a.ledger))

    if a.check:
        # ⚠ **三つに分ける。** 台帳の4欄目は「当てた後」、3欄目は「当てる前」である。
        #    ゆえに本文がどちらか一方に一致すれば、その行は**どちらの状態かが分かる**。
        #    ⚠ 二つに分けていたときは、**戻した行がすべて「⛔」として鳴った**——
        #    **戻すのは決定である**（`娯楽_届いた_戻した.tsv`）。⛔ と混ぜてはならない。
        on, off, bad = [], [], []
        for rel, n, old, new in rows:
            got = current(rel, n)
            k = key_of(rel, n)
            if got == new:
                on.append(k)
            elif got == old:
                off.append(k)
            else:
                bad.append((k, old, new, got))
        print(f"—— {len(rows)} 件を照合した（当てたまま {len(on)}／戻した {len(off)}／"
              f"どちらでもない {len(bad)}）。")
        for k in off:
            print(f"↩ {k}——戻してある（本文は、当てる前の一行である）")
        for k, old, new, got in bad:
            print(f"⛔ {k}——本文が、当てた後にも当てる前にも一致しない")
            print(f"     当てる前 {old}")
            print(f"     当てた後 {new}")
            print(f"     本文     {got}")
        return 1 if bad else 0

    want: set[str] | None = None
    if a.only_file:
        want = {l.strip() for l in Path(a.only_file).read_text(encoding="utf-8").splitlines()
                if l.strip() and not l.lstrip().startswith("#")}
    elif a.only:
        want = set(a.only)
    if not a.all and want is None:
        sys.exit("⛔ `--all` か `--only` か `--only-file` のどれかを付ける"
                 "（**戻す先を推測しない**ゆえ、どれも無ければ、何もしない）")

    out, hit = [], set()
    for rel, n, old, new in rows:
        k = key_of(rel, n)
        if want is not None and k not in want:
            continue
        hit.add(k)
        # ⚠ 戻す向き——いまの本文（＝当てた後）を、当てる前へ。
        out.append("\t".join([rel, n, new, old]))

    if want is not None and hit != want:
        miss = sorted(want - hit)
        sys.exit(f"⛔ 台帳に無い鍵が {len(miss)} 件ある（**その鍵では戻せない**）:\n  " + "\n  ".join(miss[:10]))

    print(f"# 娯楽_届いた_差し替え.tsv から作った、**戻す**向きの4欄台帳。"
          f"`cd examples` から当てる（パスは examples/ からの相対）。")
    print(f"# 件 {len(out)}。**⚠ 当てる前へ戻すゆえ、`差し替える.py` の検算は"
          f"「いまの本文＝当てた後」を要求する。**")
    for l in out:
        print(l)
    return 0


if __name__ == "__main__":
    sys.exit(main())
