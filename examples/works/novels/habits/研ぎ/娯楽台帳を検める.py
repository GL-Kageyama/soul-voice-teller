#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""娯楽台帳を検める——**五つの検査**を、22欄の台帳に掛ける。

⚠ なぜ要るか。この台帳は、**機械の欄と、人の欄の両方を持つ**（[`台帳を作る.py`](台帳を作る.py)）。
機械の欄は器が作るゆえ間違えようがないが、**人の欄は、四人が別々に書く。**
**四つの書き方が、一つの表に合わさる。** 合わさったときに壊れるのは——
**値域**（`掴んでいるか` に `○` 以外の何かが混ざる）と、
**根拠**（引いた逐語が、その行に無い）と、**欄が消えること**である。

⚠ **この器は、点数を付けない。** 出すのは**違反**と**註**だけである。
台帳が「娯楽が届いたか」をどう言っているかは、**人が読む。**

検査:
  1. **形**——ヘッダが 15＋7 に一致し、行数が草稿の場面の数に一致する
  2. **空欄ゼロ**——22欄のどこにも空が無い（`空ファイルは内容でない`）
  3. **値域**——`掴んでいるか`・`実現した軸`・`三種`・`ズレの有無`・`器`・`案` の形
  4. **逐語**——`器`・`ズレの有無`・`案` が引く `(:NNN)` の行番号がその場面の中に在り、
     **その行に、引いた句が逐語で在る**（⚠ 引けない行は、書いてはならない）
  5. **設計との突き合わせ**——`設計の軸`・`設計の三種` が、**いまの場面表**と一致する

使い方:
    python3 娯楽台帳を検める.py 娯楽台帳.tsv
    python3 娯楽台帳を検める.py 娯楽台帳.tsv --v        # 違反を一行ずつ
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent          # examples/habits/研ぎ
EXAMPLES = HERE.parent.parent                   # examples/
DRAFTS = "habits-0*/草稿/draft_*.md"

MACHINE = ["話", "場面", "行", "字数", "段落", "文", "会話",
           "設計の軸", "設計の三種", "設計の位相",
           "入口の判定", "①設計の字を持つ", "②第一段落の割合", "最良の段落",
           "章末の形"]
READER = ["実現した軸", "三種", "掴んでいるか", "器（与えた／欠けさせた）",
          "設計との差", "ズレの有無", "案"]

COL = MACHINE + READER
ENTRANCE4 = ("入口の判定", "①設計の字を持つ", "②第一段落の割合", "最良の段落")

AXES = ["ユーモア", "楽しい", "感嘆", "感動", "恐怖", "かわいい"]
THREE = {
    "感嘆": ["へえ", "なるほど", "うまい"],
    "ユーモア": ["クスッ", "ニヤリ", "ぷっ"],
    "感動": ["じんわり", "胸が熱い", "こみ上げる"],
    "楽しい": ["心地よい", "ワクワク", "ぞくぞく"],
    "恐怖": ["ゾクッ", "ヒヤッ", "ぞわり"],
    "かわいい": ["かわいい", "守りたい", "尊い"],
}
ALL_THREE = {k for v in THREE.values() for k in v}
GRAB = ["○", "△", "×"]
DASH = "—"

# ⚠ 引用の形は二つある——`器` は `〈句〉(:123)`、`案` は `123: 〈文〉 → 〈文〉`。
CITE = re.compile(r"(.{1,80}?)[（(]:(\d+)[）)]")
PLAN = re.compile(r"^(\d+):\s*(.+?)\s*→")


def norm(q: str) -> str:
    """引用の側の飾りを落とす——`与:`／`欠:`／`有（` と、鉤括弧。

    ⚠ 落とすのは**飾りだけ**である。**句そのものは一字も動かさない**——
       動かせば、この検査は「引いた句が逐語で在るか」を測らなくなる。
    """
    q = q.strip()
    for pref in ("与:", "与：", "欠:", "欠：", "有（", "有("):
        if q.startswith(pref):
            q = q[len(pref):]
            break
    return q.strip().strip("「」『』（）() 　")


def load(fname: str, name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / fname)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def draft_lines() -> dict[str, dict[int, str]]:
    """話 → {行番号: 本文}。⚠ 空行も数える（台帳の行番号は、ファイルの行番号である）。"""
    import glob
    out = {}
    for f in sorted(glob.glob(str(EXAMPLES / DRAFTS))):
        p = Path(f)
        key = p.name.split("_")[1]
        out[key] = {i: ln.rstrip("\n")
                    for i, ln in enumerate(p.read_text(encoding="utf-8").split("\n"), 1)}
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="娯楽台帳に、五つの検査を掛ける")
    ap.add_argument("ledger")
    ap.add_argument("--v", action="store_true", help="違反を一行ずつ出す")
    a = ap.parse_args()

    raw = [ln for ln in Path(a.ledger).read_text(encoding="utf-8").split("\n") if ln.strip()]
    rows = [ln.split("\t") for ln in raw]
    hdr, body = rows[0], rows[1:]

    bad = []          # ⛔ 違反
    note = []         # ⚠ 註（欠陥ではない）

    # ---------------------------------------------------------- 1. 形
    if hdr != COL:
        bad.append(("形", "ヘッダが違う", " / ".join(hdr)))
    if any(len(r) != len(COL) for r in body):
        bad.append(("形", "欄の数が違う行がある",
                    str([len(r) for r in body if len(r) != len(COL)][:5])))

    D = draft_lines()
    # 草稿の場面数。⚠ 台帳の「話」の集合と、草稿の集合を突き合わせる
    ent = load("娯楽を数える.py", "ent")
    scenes_of: dict[str, int] = {}
    for f in ent.draft_files():
        key = Path(f).name.split("_")[1]
        scenes_of[key] = len(list(ent.scenes(Path(f).read_text(encoding="utf-8").split("\n"))))
    got = Counter(r[0] for r in body)
    for k in sorted(set(scenes_of) | set(got)):
        if got.get(k, 0) != scenes_of.get(k, 0):
            bad.append(("形", f"{k}——場面の数が違う",
                        f"台帳 {got.get(k, 0)} / 草稿 {scenes_of.get(k, 0)}"))

    # ---------------------------------------------------------- 場面表（検査5の照合先）
    ax = load("軸を数える.py", "ax")
    design = {}
    design_three = set()
    for f in ax.tables():
        p = Path(f)
        key = f"{p.parent.parent.parent.name.replace('habits-', '')}-{p.name.split('_')[0]}"
        for num, cell in ax.scene_rows(p):
            axis, sub, _ = ax.parse_cell(cell)
            design[(key, str(num))] = (axis, sub)
            design_three |= {t.strip() for t in re.split(r"[・、/]", sub or "") if t.strip()}
    DESIGN_THREE = design_three - {""}

    # ---------------------------------------------------------- 5. 逐語の検査（使い回す）
    def check_cite(tag: str, key: str, cell: str, cols: list[str]) -> None:
        """⚠ 二つを分ける。

        ⛔ **引いた句が、その行に実在しない**——これは**捏造の側**である。
            台帳の根拠は「その行を読めば確かめられる」ことの上に立っている。
            確かめられない根拠は、根拠ではない。
        ⚠ **行が場面の外にある**（章の中では在る）——これは**註**である。
            `器` の「与える」は、**場面より手前で置かれることがある**（フックのエンジン——
            「与える → 欠けさせる」は、場面をまたいで走る）。**ゆえに、違反にしない。**
            だが**数えて出す**——どの場面が、自分の外から器を借りているかは、読む者の手がかりである。
        """
        lo, hi = (int(x) for x in (cols[2].split("-") + ["0"])[:2])   # 場面の行範囲
        for quote, num in CITE.findall(cell):
            n = int(num)
            q = norm(quote.split("／")[-1])
            line = D.get(key, {}).get(n)
            if line is None:
                bad.append((tag, f"{key} {cols[1]}——行 {n} が草稿に無い", q[:40]))
                continue
            if q and q not in line:
                bad.append((tag, f"{key} {cols[1]}——行 {n} に、引いた句が逐語で無い",
                            f"引 {q[:40]} / 実 {line[:60]}"))
            elif not (lo <= n <= hi):
                note.append(("註", f"{key} {cols[1]}——`{tag}` の行 {n} が場面の外（{cols[2]}）",
                             q[:40]))

    # ---------------------------------------------------------- 2〜5. 行ごと
    for r in body:
        key, sc = r[0], r[1]
        cell = dict(zip(COL, r))
        at = f"{key} {sc}"

        # 2. 空欄ゼロ
        for c in COL:
            if not cell[c].strip():
                bad.append(("空欄", f"{at}——`{c}` が空である", ""))
        # ⚠ 空の欄に、値域の検査は掛けない（**空欄の報告で足りる**。二重に鳴らさない）
        if any(not cell[c].strip() for c in READER):
            continue

        # 3. 値域
        ax_got = cell["実現した軸"]
        parts = [x.strip() for x in ax_got.split("＋")] if ax_got != "なし" else []
        if ax_got != "なし" and not parts:
            bad.append(("値域", f"{at}——`実現した軸` が空に近い", ax_got))
        for x in parts:
            if x not in AXES:
                bad.append(("値域", f"{at}——`実現した軸` に無い名", x))

        three = cell["三種"]
        if ax_got == "なし":
            if three != DASH:
                bad.append(("値域", f"{at}——軸が `なし` なのに三種が在る", three))
        else:
            names = {t.strip() for t in re.split(r"[・、/]", three)}
            if not (names & ALL_THREE):
                # ⚠ 設計自身が六軸の表の外の語を使っている欄がある（`静か`・`あたたかい`・
                #    `胸が痛い`・`余白`・`速い` など）。**著者の裁定材料 §3-3 が、
                #    「三種の一覧に無い名が、12欄ある」として既に記録している**——
                #    **設計の欠陥であり、読者の側の違反ではない。**
                #    ゆえに、**設計の語を写したものは註に落とす。**
                if names & DESIGN_THREE:
                    note.append(("註", f"{at}——`三種` が六軸の表の外（設計自身の語）", three))
                else:
                    bad.append(("値域", f"{at}——`三種` が六軸の三種に無い", three))
            for x in parts:
                if x in THREE and not (names & set(THREE[x])):
                    note.append(("註", f"{at}——`{x}` の三種が一つも無い（軸の名だけ）", three))

        if cell["掴んでいるか"] not in GRAB:
            bad.append(("値域", f"{at}——`掴んでいるか` が ○△× でない", cell["掴んでいるか"]))

        z = cell["ズレの有無"]
        if z != "無" and not z.startswith("有"):
            bad.append(("値域", f"{at}——`ズレの有無` が 有／無 でない", z))

        v = cell["器（与えた／欠けさせた）"]
        if v != DASH and not re.match(r"^(与:|与：|欠:|欠：|与.*／欠|—)", v):
            bad.append(("値域", f"{at}——`器` が 与／欠 の形でない", v))

        p = cell["案"]
        if p != DASH and not PLAN.match(p):
            bad.append(("値域", f"{at}——`案` が `NNN: いまの文 → 案` の形でない", p[:60]))

        # 2'. 入口の四欄——場面1にのみ在る
        if sc == "1":
            if cell["入口の判定"] not in ("在", "後ろ", "無し", DASH):
                bad.append(("値域", f"{at}——`入口の判定` の値", cell["入口の判定"]))
        else:
            for c in ENTRANCE4:
                if cell[c] != DASH:
                    bad.append(("形", f"{at}——`{c}` は場面1にしか無い", cell[c]))

        # 4. 逐語——器・ズレ・案
        check_cite("逐語", key, v, r)
        if z.startswith("有"):
            check_cite("逐語", key, z, r)
        if p != DASH:
            m = PLAN.match(p)
            if m:
                n, now = int(m.group(1)), m.group(2).strip()
                lo, hi = (int(x) for x in (r[2].split("-") + ["0"])[:2])
                line = D.get(key, {}).get(n, "")
                if not (lo <= n <= hi):
                    bad.append(("逐語", f"{at}——案の行 {n} が場面の外（{r[2]}）", now[:40]))
                elif now and now not in line:
                    bad.append(("逐語", f"{at}——案の行 {n} に、いまの文が逐語で無い",
                                f"引 {now[:40]} / 実 {line[:60]}"))

        # 5'. 設計との突き合わせ
        d = design.get((key, sc))
        if d is None:
            bad.append(("設計", f"{at}——場面表に、この場面が無い", ""))
        else:
            if cell["設計の軸"] != d[0]:
                bad.append(("設計", f"{at}——`設計の軸` が場面表と違う",
                            f"台帳 {cell['設計の軸']} / 場面表 {d[0]}"))
            if cell["設計の三種"] != d[1]:
                bad.append(("設計", f"{at}——`設計の三種` が場面表と違う",
                            f"台帳 {cell['設計の三種']} / 場面表 {d[1]}"))

        # 6. 註——○ なのに案が在る／△× なのに案が無い
        g = cell["掴んでいるか"]
        if g == "○" and p != DASH:
            note.append(("註", f"{at}——○ なのに案が在る", p[:50]))
        if g in ("△", "×") and p == DASH:
            note.append(("註", f"{at}——{g} なのに案が無い", ""))

    # ---------------------------------------------------------- 註——話の中の三種の重複
    # ⚠ 見るのは**設計の側**である（`設計の三種`）。読者の欄は、まだ空でありうる。
    #    設計が一話の三場面へ同じ三種を配っているなら、それは**飽和の設計**である
    #    （`references/ja/6つの反応軸.md`——「反応を**間隔**（途切れない）・**強度**（飽和しない）で組む」）。
    for col, tag in (("設計の三種", "設計"), ):
        per = {}
        for r in body:
            per.setdefault(r[0], []).append(r[COL.index(col)])
        for k, ts in sorted(per.items()):
            vals = [t for t in ts if t.strip() and t != DASH]
            if len(vals) < 3:
                continue
            c = Counter(vals)
            for t, n in c.items():
                if n >= len(vals):
                    note.append(("註", f"{k}——{tag}は、{len(vals)} 場面とも同じ三種である", t))

    # ---------------------------------------------------------- 出す
    print(f"台帳——{a.ledger}")
    print(f"  行 {len(body)}（{len(got)} 話）／欄 {len(hdr)}")
    print()
    kinds = Counter(k for k, _, _ in bad)
    if not bad:
        print("✅ 五つの検査とも、違反は 0 件である。")
    else:
        print(f"⛔ 違反 {len(bad)} 件——" + "／".join(f"{k} {n}" for k, n in kinds.most_common()))
        if a.v:
            for k, what, why in bad:
                print(f"    [{k}] {what}" + (f"　→ {why}" if why else ""))
    print()
    if note:
        print(f"⚠ 註 {len(note)} 件（欠陥ではない。台帳を読むときの手がかりである）")
        for k, what, why in note:
            print(f"    {what}" + (f"　→ {why}" if why else ""))
    else:
        print("⚠ 註 0 件。")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
