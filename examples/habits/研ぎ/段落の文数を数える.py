#!/usr/bin/env python3
"""段落の文数を数える——組んだあとの草稿を、段落ごとの文数で数える。

⚠ **なぜ、この器が要るか**（計画 §11-11 の穴）。

`段落を組む.py` は、段落の数・文/段落・字/段落を出すが、**段落の文数の分布は出さない**。
ゆえに「**一つの段落が四文を超えたら、それは組みすぎである**」（指示書 §1）を、
**機械で見る者がいない。** **⚠ 台帳を書く者が、各自で即席の照合器を書いていた**——
**⚠ そして、そのうち二つが在り得ない数を出した**
（**03-09 は「一文 128・文/段落 1.0」・03-15 も同じ形。古い accumulator を読んだ**）。
**⚠ 空の検査は OK と言う**（**相手が空なら落ちる、を入れていない器は、0==0 で通る**）。

ゆえに、ここに一本だけ置く。**⚠ 読み取り専用である。草稿を書かない。**

    python3 段落の文数を数える.py <草稿> [<草稿> ...]
    python3 段落の文数を数える.py --strict <草稿>   # 五文以上が一つでもあれば exit 1

**数え方**

- **本文行**——空行でなく、見出し（`#` で始まる）でもない行。**⚠ 組んだあとの草稿では、
  複数文を含む行がある**（**ゆえに、本文行数と文の総数は一致しない**）。
- **段落**——空行で切った、本文行のかたまり。
- **文**——段落のなかの `。？！` の数。**⚠ 鉤括弧のなかも数える**（**会話は一文である**）。
  **⚠ `——` で始まる一声の行も、末尾に句点があれば一文である。**
  **⚠ 句点で終わらない行は、文として数えない**（**数え落としではない。数え方をここに書く**）。

**⚠ この器が見ないもの**——**その組み方が、その話の拍として正しいか。** それは人が読む。
"""

from __future__ import annotations

import argparse
import statistics
import sys
from pathlib import Path

# 段落の文数の目安。**⚠ 規則ではなく、この作品の勾配である**（計画 §8-3 と同じ扱い）。
#
# **⚠ 2026-09-26 の実測**（走査した集合＝当てた四十六話の全段落）。
# **⚠ 五文以上の段落は 57 箇所ある**——**⚠ 第一巻 29・第二巻 28・第三巻 0・第四巻 0。**
#   - **第一巻の 29 は、すべてこの台帳が組んだものである**（第一巻の草稿は一行一文ゆえ、
#     段落はすべて組んだ結果である。当てる前の複数文の行は二つだけ）。
#   - **第二巻の 28 は、すべて著者が既に書いた段落である**（当てる前から五文以上。
#     02-09 に最長 7 文・02-10 に 6 文がある。計画の申し送り(d)と同じものである）。
#   - **第三巻・第四巻は 0**——**⚠ この二巻の台帳は、四文で止めている。**
# **⚠ ゆえに「四文を超えたら組みすぎ」は、第三巻・第四巻では真であり、第一巻では偽である。**
# **⚠ 第一巻は承認済みであるゆえ、戻さない**（申し送り——計画 §11-14）。
# **⚠ 五文ちょうど 47・六文以上 10**（**六文以上は第一巻 2・第二巻 8。すべて上の 57 の内側**）。
CAP = 4


def is_body(line: str) -> bool:
    s = line.strip()
    return bool(s) and not s.startswith("#")


def is_scene(line: str) -> str | None:
    s = line.strip()
    if s.startswith("## "):
        return s
    return None


def bun(text: str) -> int:
    """⚠ 句点の数で数える。**⚠ 読点は数えない**（指示書 §1——判定は字数ではない）。"""
    return sum(text.count(c) for c in "。？！")


def read_paragraphs(path: Path) -> tuple[list[tuple[str, list[str]]], int]:
    """草稿を、場面ごとの段落へ割る。返り値は ([(場面名, [段落, ...]), ...], 本文行数)。"""
    scenes: list[tuple[str, list[str]]] = []
    cur_scene = "(見出しの前)"
    cur_par: list[str] = []
    scene_pars: list[str] = []
    body_lines = 0

    def flush_par() -> None:
        nonlocal cur_par
        if cur_par:
            scene_pars.append("\n".join(cur_par))
            cur_par = []

    def flush_scene() -> None:
        nonlocal scene_pars, cur_scene
        flush_par()
        if scene_pars:
            scenes.append((cur_scene, scene_pars))
            scene_pars = []

    for raw in path.read_text(encoding="utf-8").splitlines():
        head = is_scene(raw)
        if head is not None:
            flush_scene()
            cur_scene = head
            continue
        if is_body(raw):
            body_lines += 1
            cur_par.append(raw.strip())
        else:
            flush_par()
    flush_scene()
    return scenes, body_lines


def report(path: Path) -> tuple[int, int, list[int]]:
    scenes, body_lines = read_paragraphs(path)
    all_ns: list[int] = []
    print(f"■ {path.name}")
    print(f"   本文 {body_lines} 行")
    for name, pars in scenes:
        ns = [bun(p) for p in pars]
        all_ns.extend(ns)
        one = sum(1 for n in ns if n == 1)
        over = sum(1 for n in ns if n > CAP)
        # ⚠ **⛔ にしない**——**⚠ 五文の段落は、この作品に 57 箇所ある**（上の註を見る）。
        flag = f"  ⚠ 五文以上 {over}" if over else ""
        print(
            f"   {name}  段落 {len(pars):>4}  文 {sum(ns):>4}"
            f"  文/段落 {statistics.mean(ns):.2f}  一文 {one:>3}"
            f"  ({one / len(ns):.0%}){flag}"
        )
    if not all_ns:
        # ⚠ **空の検査は OK と言う**——**ゆえに、ここで落とす**（**戻り値を空にして、
        # ⚠ 呼び手が「五文以上 0」を「綺麗である」と読む道を、塞ぐ**）。
        print("   ⛔ 段落が一つも無い。**この草稿は、組まれていないか、読み取りに失敗している。**")
        return body_lines, 0, []
    dist = {n: sum(1 for x in all_ns if x == n) for n in range(1, CAP + 1)}
    # ⚠ **「五文以上」は、五文ちょうどではない**——**⚠ 六文以上を別に数える**。
    # ⚠ 2026-09-26、この器を書いた者がここを取り違えた（01-03 は五文以上 4 だが 3 と出た）。
    over5 = sum(1 for x in all_ns if x == CAP + 1)
    over6 = sum(1 for x in all_ns if x > CAP + 1)
    print(
        "   全体  "
        + "  ".join(f"{'一二三四'[n - 1]}文 {dist[n]}" for n in range(1, CAP + 1))
        + f"  五文 {over5}  六文以上 {over6}"
    )
    print(
        f"   文/段落 平均 {statistics.mean(all_ns):.2f}"
        f"  中央値 {statistics.median(all_ns)}  最長 {max(all_ns)} 文"
    )
    return body_lines, sum(all_ns), all_ns


def main() -> int:
    ap = argparse.ArgumentParser(description="組んだあとの草稿を、段落ごとの文数で数える")
    ap.add_argument("drafts", nargs="+", type=Path, help="組んだあとの草稿")
    ap.add_argument(
        "--strict",
        action="store_true",
        help=f"段落の文数が {CAP} を超えたら exit 1（⚠ 著者の既存の段落も同等に数える）",
    )
    args = ap.parse_args()

    rc = 0
    over_total = 0
    for i, path in enumerate(args.drafts):
        if not path.exists():
            print(f"⛔ 無い——{path}", file=sys.stderr)
            rc = 1
            continue
        if i:
            print()
        _, n_sent, ns = report(path)
        if not ns:
            # ⚠ **空を、通さない**（0==0 で通る検査にしない）。
            rc = 1
            continue
        over = sum(1 for x in ns if x > CAP)
        over_total += over
        if over:
            rc = rc or (1 if args.strict else 0)
    if over_total:
        print(
            f"\n⚠ 五文以上の段落が {over_total} 個ある。"
            f"**⚠ 指示書 §1——「一つの段落は、四文までが普通である」"
            f"（⚠ 但し、第一巻には 29・第二巻には 28 ある。あの註を見る）。**"
        )
    return rc


if __name__ == "__main__":
    sys.exit(main())
