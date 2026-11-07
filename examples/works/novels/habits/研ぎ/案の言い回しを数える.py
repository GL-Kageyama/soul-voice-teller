#!/usr/bin/env python3
"""案の言い回しを数える.py——第七段階の検めの穴を塞ぐ器。

なぜ要るか（2026-10-14、娯楽_ユーモアの二度目で見つけた）
--------------------------------------------------------
検めは **巻ごとに一人**で行われる。ゆえに検め役は **一行ずつ**読む。
ところが案は、別々の話へ散る。**七つの話に散った同じ型は、誰の視界にも入らない。**

実例——読点込みの `、まだ、` は、**本文63話の全文で2行しか無い**（`01-03:285`・`04-06:117`）。
ところが二度目の案65件のうち **9件**がこれを使い、**第三巻だけで7件**、
しかも書き方まで同じ型だった（「〈何か〉は、まだ、〈どこか〉にある／来ない。」）。

**検査/check.py は鳴らない。** 反復の規則は「ちょうど二話に一致するときだけ」鳴り、
三話以上は基底語として黙る。**一巻の中に7件できても、一件も出ない。**

この器は、**案の「足した一句」を全文まとめて走査**し、
**本文に稀な言い回しが、案の側で何件も使われていないか**を見る。

⚠ これは**判定器ではない**。出すのは「見るべき候補」である。
⚠ **本文の数に、当てた案の分が混ざる**（当てた後に走らせた場合）。
   ゆえに `--exclude-replaced` で差し替え TSV の「置き換える文」の行を本文から外せる。
"""
from __future__ import annotations

import argparse
import glob
import pathlib
import re
import sys
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]        # examples/habits/
EX = ROOT.parent                                           # examples/
GYOGI = ROOT / "研ぎ"


def norm(s: str) -> str:
    return s.replace("、", "").replace("，", "").replace(" ", "").replace("　", "")


def body_lines() -> list[tuple[str, int, str]]:
    out = []
    for p in sorted(glob.glob(str(EX / "habits-0*" / "草稿" / "draft_0*-*.md"))):
        key = "-".join(re.search(r"draft_(\d\d)-(\d\d)_", p).groups())
        for j, line in enumerate(pathlib.Path(p).read_text(encoding="utf-8").splitlines(), 1):
            out.append((key, j, line))
    return out


def read_tsv(path: pathlib.Path) -> tuple[list[list[str]], int]:
    """(行, 案の欄の番号) を返す。見出しが在ればその名で引き、無ければ7欄として4。"""
    rows, col = [], 4
    for ln in path.read_text(encoding="utf-8").splitlines():
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        f = ln.split("\t")
        if f[0].strip() in ("巻", "vol", "話"):
            if "案" in f:
                col = f.index("案")
            continue
        rows.append(f)
    return rows, col


def added_texts(rows: list[list[str]], col: int) -> list[tuple[str, str]]:
    """(鍵, 足した一句)。鍵は TSV の欄から作る（形は `NN-NN:NNN` を期待するが、無ければ番号だけ）。"""
    out = []
    for f in rows:
        if len(f) <= col:
            continue
        now, new = f[col - 1], f[col]
        if new.strip().startswith("当てない"):
            continue
        a = new[len(now):] if new.startswith(now) else new
        key = f"{f[0]}-{f[1]}:{f[2]}" if len(f) >= 7 and col == 4 else (
            f"{f[0]}-{f[1]}:{f[3]}" if len(f) > col else "?")
        out.append((key, a.strip()))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="案の足した一句が、本文に稀な言い回しを反復していないかを見る")
    ap.add_argument("tsvs", nargs="+", help="案の TSV（複数まとめて渡すと、案の側の数が合算される）")
    ap.add_argument("--n", default="4,5,6", help="走査する字数（既定 4,5,6）")
    ap.add_argument("--min-proposals", type=int, default=4, help="案の側でこの数以上に現れたら出す（既定 4）")
    ap.add_argument("--max-body", type=int, default=2, help="本文でこの行数以下なら『稀』とみなす（既定 2）")
    ap.add_argument("--strip-punct", action="store_true",
                    help="読点を除いた形でも走査する（⚠ 既定の走査は生の字。読点込みの型はこれでしか出ない）")
    ap.add_argument("--show-lines", action="store_true", help="当たった本文の行を出す")
    a = ap.parse_args()

    blines = body_lines()
    print(f"■ 本文——{len(set(k for k, _, _ in blines))} 話・{len(blines)} 行")

    proposals = []
    for t in a.tsvs:
        p = pathlib.Path(t)
        if not p.is_absolute() and not p.exists():
            p = GYOGI / p
        rows, col = read_tsv(p)
        got = added_texts(rows, col)
        proposals += got
        print(f"   {p.name}——案 {len(got)} 件（案の欄＝{col}）")
    print(f"■ 案——合計 {len(proposals)} 件")

    variants = [("生の字", lambda s: s)]
    if a.strip_punct:
        variants.append(("読点を除く", norm))

    for label, f in variants:
        ns = [int(x) for x in a.n.split(",")]
        # 本文の各 n-gram が、何行に現れるか
        body_cnt: Counter = Counter()
        body_where: dict[str, list[str]] = defaultdict(list)
        for key, j, line in blines:
            s = f(line)
            for n in ns:
                for i in range(len(s) - n + 1):
                    g = s[i:i + n]
                    body_cnt[g] += 1
                    if len(body_where[g]) < 6:
                        body_where[g].append(f"{key}:{j}")
        # 案の各 n-gram が、何件に現れるか
        prop_cnt: Counter = Counter()
        prop_where: dict[str, list[str]] = defaultdict(list)
        for key, text in proposals:
            s = f(text)
            seen = set()
            for n in ns:
                for i in range(len(s) - n + 1):
                    g = s[i:i + n]
                    if g in seen:
                        continue
                    seen.add(g)
                    prop_cnt[g] += 1
                    if len(prop_where[g]) < 8:
                        prop_where[g].append(key)

        hits = [(g, prop_cnt[g], body_cnt.get(g, 0)) for g in prop_cnt
                if prop_cnt[g] >= a.min_proposals and body_cnt.get(g, 0) <= a.max_body]
        hits.sort(key=lambda t: (-t[1], t[2], t[0]))

        print(f"\n■ 【{label}】案の側で {a.min_proposals} 件以上・本文で {a.max_body} 行以下")
        if not hits:
            print("   無し。")
            continue
        for g, pc, bc in hits:
            print(f"   「{g}」  案 {pc} 件 ／ 本文 {bc} 行")
            print(f"        案: {'、'.join(prop_where[g])}")
            if a.show_lines:
                print(f"        本文: {'、'.join(body_where[g]) if bc else '（本文に無い）'}")

    print("\n⚠ これは判定ではない。**見るべき候補**である。")
    print("⚠ 当てた後に走らせた場合、本文の数に**その案自身の分が混ざる**。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
