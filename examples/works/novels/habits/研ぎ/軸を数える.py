#!/usr/bin/env python3
"""軸を数える——四巻六十三話の場面表の「反応軸」欄を、機械で数える（読み取り専用）。

⚠ この器が答える問いは、一つである——
   **設計が各話に配った反応軸は、六軸のどれであり、その三種のどれであるか。**

⚠ なぜ要るか。**本文が「説明ばかり」に見えるのは、入口の軸が偏っているからである**
   （`構想/design.md:189`「掴むのは話の入口（多くは楽しい・心地よい）」）。
   その偏りは、**設計の側の欄に既に書かれている。**ゆえに、本文を読む前に数えられる。

⚠ 数え方は `検査/check.py` と同じ物差しに合わせない——**この器は本文を読まない。**
   読むのは `habits-0*/構想/各話/*.md`（場面表）の表だけである。

⚠ **欄は、見出しの名で引く。** 欄番号を直に書かない——**第四巻は「内面」の欄を持たない**
   （`構想/design.md:245` の決定は第一〜第三巻に当たる）。番号で引くと、第四巻だけ別の欄を読む。
   → [`../../../../.claude/projects/.../memory/scan-key-must-match-the-field.md`]
   **「走査の鍵は、その欄に掛ける。」**

⚠ **三種の名は、正本から読む。** `references/ja/6つの反応軸.md` の表を引く——
   ここに書き写すと、正本が動いたとき、この器だけが古い名を持ち続ける。

使い方:
    python3 軸を数える.py                 # 軸の分布と、三種の分布
    python3 軸を数える.py --list          # 六十三話の軸セルを、逐語で出す
    python3 軸を数える.py --off-list      # 三種の一覧に無い名だけを出す
"""

import argparse
import glob
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # examples/habits/研ぎ
HABITS = HERE.parent                            # examples/habits
EXAMPLES = HABITS.parent                        # examples
REPO = EXAMPLES.parent                          # soul-voice-teller
AXES_DOC = REPO / "references" / "ja" / "6つの反応軸.md"

SPLIT = "・"


def axis_reference():
    """正本の「場面の三種」表を読む。{軸: [三種, ...]} と、宣言された軸の順を返す。"""
    if not AXES_DOC.exists():
        sys.exit(f"⛔ 正本が無い——{AXES_DOC}")
    text = AXES_DOC.read_text(encoding="utf-8")
    # 「| 感嘆 | へえ ・ なるほど ・ うまい |」の形の行だけを拾う。
    row = re.compile(r"^\|\s*([^\s|]+)\s*\|\s*([^|]+?)\s*\|\s*$")
    table = {}
    order = []
    for line in text.split("\n"):
        m = row.match(line.strip())
        if not m:
            continue
        axis, types = m.group(1), m.group(2)
        if axis in ("軸", "---"):
            continue
        parts = [t.strip() for t in types.split(SPLIT) if t.strip()]
        # 三種の表は、ちょうど三つ。四工程の表は「→」を含むゆえ、ここで落ちる。
        if len(parts) == 3 and "→" not in types:
            table[axis] = parts
            order.append(axis)
    if not table:
        sys.exit(f"⛔ 三種の表が読めなかった——{AXES_DOC}")
    return table, order


def scene_rows(path):
    """場面表の表から、(場面番号, 反応軸セル) を返す。

    ⚠ 欄は、見出し行で「反応軸」の位置を探してから引く。番号を直に書かない。
    """
    lines = path.read_text(encoding="utf-8").split("\n")
    col = None
    out = []
    for line in lines:
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if col is None:
            if "反応軸" in cells:
                col = cells.index("反応軸")
            continue
        # 場面の行——第一欄が番号である。
        if not cells or not re.fullmatch(r"\d+", cells[0]):
            continue
        if col >= len(cells):
            continue
        out.append((int(cells[0]), cells[col]))
    return out


def parse_cell(cell):
    """「楽しい・心地よい（掴む）」→ ('楽しい', '心地よい', '掴む')。

    ⚠ 括弧の中は位相（掴む／置かせる／解放しない）である。軸ではない。
    """
    phase = ""
    m = re.search(r"[（(]([^）)]*)[）)]", cell)
    if m:
        phase = m.group(1).strip()
        cell = cell[: m.start()] + cell[m.end():]
    cell = cell.strip().strip("*").strip()
    parts = [p.strip() for p in cell.split(SPLIT) if p.strip()]
    axis = parts[0] if parts else ""
    sub = parts[1] if len(parts) > 1 else ""
    return axis, sub, phase


def tables():
    files = []
    for v in ("01", "02", "03", "04"):
        files.extend(sorted(glob.glob(str(EXAMPLES / f"habits-{v}" / "構想" / "各話" / "*.md"))))
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="場面表の反応軸の欄を数える")
    ap.add_argument("--list", action="store_true", help="六十三話の軸セルを、逐語で出す")
    ap.add_argument("--off-list", action="store_true", help="三種の一覧に無い名だけを出す")
    a = ap.parse_args()

    ref, axis_order = axis_reference()
    all_types = {t for v in ref.values() for t in v}
    files = tables()
    if not files:
        sys.exit("⛔ 場面表が一枚も無い（空の検査は通さない）")

    rows = []          # (巻, 話, 場面, 軸, 三種, 位相, 逐語)
    for f in files:
        p = Path(f)
        vol = p.parent.parent.parent.name.replace("habits-", "")
        key = p.name.split("_")[0]                     # 01 / 02 …（話番号）
        for num, cell in scene_rows(p):
            axis, sub, phase = parse_cell(cell)
            rows.append((vol, f"{vol}-{key}", num, axis, sub, phase, cell))

    if not rows:
        sys.exit("⛔ 反応軸の欄が一行も読めなかった（走査の鍵が欄に掛かっていない）")

    if a.list or a.off_list:
        for vol, ch, num, axis, sub, phase, cell in rows:
            mark = ""
            if sub and sub not in all_types:
                mark = "  ⚠ 三種の一覧に無い"
            if a.off_list and not mark:
                continue
            print(f"{ch} 第{num}場面  [{axis}] {sub or '—'}（{phase or '—'}）{mark}")
        return 0

    n_files = len(files)
    print(f"走査した集合——{n_files} 枚の場面表（`habits-0*/構想/各話/*.md`）。"
          f"読んだのは「反応軸」の欄だけである。本文は読んでいない。")
    print(f"三種の正本——`{AXES_DOC.relative_to(REPO)}`")
    print()

    # ---------------------------------------------------------------- 軸
    print("【軸——第一場面の欄】")
    first = [r for r in rows if r[2] == 1]
    counts = {}
    for _, _, _, axis, _, _, _ in first:
        counts[axis] = counts.get(axis, 0) + 1
    for axis in axis_order + [k for k in counts if k not in axis_order]:
        if counts.get(axis):
            print(f"    {axis:8s} {counts[axis]:3d} 話   （{100*counts[axis]/len(first):.0f}%）")
    unknown = [k for k in counts if k not in axis_order]
    if unknown:
        print(f"    ⚠ 六軸に無い名——{', '.join(unknown)}")
    print()

    # ---------------------------------------------------------------- 三種
    print("【三種——第一場面の欄】（正本の三種と突き合わせる）")
    for axis in axis_order:
        subs = [r[4] for r in first if r[3] == axis]
        if not subs:
            continue
        dist = {}
        for s in subs:
            dist[s] = dist.get(s, 0) + 1
        declared = ref.get(axis, [])
        print(f"  {axis}（{len(subs)} 話）——正本の三種 {'・'.join(declared)}")
        for s, n in sorted(dist.items(), key=lambda x: -x[1]):
            mark = "" if s in declared else "   ⚠ 正本の三種に無い"
            print(f"      {s:10s} {n:3d} 話{mark}")
    print()

    # ---------------------------------------------------------------- 三場面
    print("【軸——三場面すべて】")
    dist3 = {}
    for _, _, num, axis, _, _, _ in rows:
        dist3[(num, axis)] = dist3.get((num, axis), 0) + 1
    for num in sorted({r[2] for r in rows}):
        line = "   ".join(f"{axis} {dist3[(num, axis)]}"
                          for axis in axis_order if dist3.get((num, axis)))
        print(f"    第{num}場面——{line}")
    print()

    # ---------------------------------------------------------------- ユーモア
    print("【ユーモアと、使わないと定めた二軸】")
    for axis in ("ユーモア", "恐怖", "かわいい"):
        n = sum(1 for r in rows if r[3] == axis)
        print(f"    {axis:6s} 三場面で {n} 欄")
    print()

    # ---------------------------------------------------------------- 位相
    print("【位相——括弧の中】")
    ph = {}
    for _, _, num, _, _, phase, _ in rows:
        ph[(num, phase)] = ph.get((num, phase), 0) + 1
    for num in sorted({r[2] for r in rows}):
        line = "   ".join(f"{p} {ph[(num, p)]}"
                          for p in sorted({x[5] for x in rows if x[2] == num}))
        print(f"    第{num}場面——{line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
