#!/usr/bin/env python3
"""対応表を検める——`段落を組む.py --map` の出力が、貼り直しに耐えるかを確かめる。

**⚠ 貼り直しは、戻せない段である**（§5-1。**控えを取るが、記録の側は戻らない**）。
**⚠ ゆえに、使う前に、対応表そのものを検める。**

確かめること——六つ。

1. **欄が三つである**（道・旧・新）。
2. **旧の番号が、重複しない**（**本文行は、一度しか出てこない**）。
3. **新の番号が、旧の順に、広義単調増加である**（**組んだ行は、直前の新の番号と同じになる**）。
4. **控え（`段落化の控え/`）の本文行と、旧の番号の集合が一致する**——
   **⚠ 一件でも欠けたら落ちる。⚠ 余っても落ちる。**
5. **いまの草稿の本文行と、新の番号の集合が一致する。**
6. **⚠ 空の検査は OK と言う**——**対応表が空なら、照合せずに落とす。**

**⚠ そして、引き直した先が、本当に同じ文を指すかを、一件ずつ照合する**（**⑦**）——
**旧の本文行と、新の本文行が、一字も違わないこと。**

使い方:
    python3 対応表を検める.py 段落化_01-*.tsv
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
BACKUP = HERE / "段落化の控え"


def is_body(line: str) -> bool:
    return bool(line.strip()) and not line.lstrip().startswith("#")


def main() -> int:
    ap = argparse.ArgumentParser(description="対応表が貼り直しに耐えるかを確かめる")
    ap.add_argument("maps", nargs="+")
    args = ap.parse_args()

    bad: list[str] = []
    total = 0
    for m in args.maps:
        p = Path(m)
        if not p.exists():
            bad.append(f"{p}——対応表が無い")
            continue
        rows = []
        for i, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            parts = raw.split("\t")
            if len(parts) != 3:
                bad.append(f"{p.name}:{i}——欄が {len(parts)} 個である")
                continue
            f, old, new = parts
            if not old.isdigit() or not new.isdigit():
                bad.append(f"{p.name}:{i}——番号でない: {old!r} {new!r}")
                continue
            rows.append((Path(f), int(old), int(new)))
        if not rows:
            bad.append(f"{p.name}——空である（照合せずに落とす）")
            continue
        total += len(rows)

        # ② 旧が重複しない
        seen = [o for _f, o, _n in rows]
        if len(set(seen)) != len(seen):
            dup = sorted({n for n in seen if seen.count(n) > 1})
            bad.append(f"{p.name}——旧の番号が重複している: {dup[:8]}")
            continue

        # ③ 新が広義単調増加
        news = [n for _f, _o, n in rows]
        if any(news[i] < news[i - 1] for i in range(1, len(news))):
            w = [i for i in range(1, len(news)) if news[i] < news[i - 1]][:3]
            bad.append(f"{p.name}——新の番号が戻っている（{len(w)} 箇所。最初は {w[0]} 番目の行）")
            continue

        f = rows[0][0]
        if len({str(r[0]) for r in rows}) != 1:
            bad.append(f"{p.name}——一本の対応表が、複数のファイルを持つ")
            continue
        if not f.exists():
            bad.append(f"{p.name}——草稿が無い: {f}")
            continue
        now = f.read_text(encoding="utf-8").splitlines()

        bak = BACKUP / f.name
        if not bak.exists():
            bad.append(f"{p.name}——控えが無い: {bak.name}")
            continue
        was = bak.read_text(encoding="utf-8").splitlines()

        # ④ 旧の集合 = 控えの本文行
        old_body = {i for i, l in enumerate(was, 1) if is_body(l)}
        if set(seen) != old_body:
            miss = sorted(old_body - set(seen))[:5]
            extra = sorted(set(seen) - old_body)[:5]
            bad.append(f"{p.name}——旧の集合が控えと違う（欠け {len(old_body - set(seen))} 件 {miss}・余り {len(set(seen) - old_body)} 件 {extra}）")
            continue

        # ⑤ 新の集合 = いまの草稿の本文行
        new_body = {i for i, l in enumerate(now, 1) if is_body(l)}
        if set(news) != new_body:
            miss = sorted(new_body - set(news))[:5]
            extra = sorted(set(news) - new_body)[:5]
            bad.append(f"{p.name}——新の集合がいまの草稿と違う（欠け {len(new_body - set(news))} 件 {miss}・余り {len(set(news) - new_body)} 件 {extra}）")
            continue

        # ⑦ 引き直した先が、同じ文を指すか
        #    新の段落は、複数の旧の行を連結したものである。ゆえに——
        #    「同じ新の番号を持つ旧の行を連結したもの」＝「新のその行」であるはずである。
        bynew: dict[int, list[int]] = defaultdict(list)
        for _f, o, n in rows:
            bynew[n].append(o)
        diff = []
        for n, olds in bynew.items():
            joined = "".join(was[o - 1] for o in sorted(olds))
            if joined != now[n - 1]:
                diff.append(n)
        if diff:
            bad.append(f"{p.name}——⚠ 引き直した先の文が違う（{len(diff)} 段落。最初は新 {diff[0]}）")
            continue

        print(f"  ✅ {p.name}——{len(rows)} 件（本文行 {len(old_body)} → 段落 {len(new_body)}）")

    print()
    if bad:
        print(f"⛔ {len(bad)} 件")
        for b in bad:
            print("   " + b)
        return 1
    if total == 0:
        print("⛔ 一件も読めなかった——照合せずに落とす")
        return 2
    print(f"✅ {len(args.maps)} 本・{total} 件——貼り直しに耐える")
    return 0


if __name__ == "__main__":
    sys.exit(main())
