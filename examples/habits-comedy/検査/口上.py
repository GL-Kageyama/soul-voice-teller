#!/usr/bin/env python3
"""冒頭の口上（§0-3）を、全63話について数える器。

    python3 口上.py              # ⑴ 各話の口上を印字し、数える
    python3 口上.py --近い        # ⑵ 口上の語の並びが、話をまたいで重なっていないか
    python3 口上.py --名          # ⑶ 名の規則（第四巻に名が無いこと）
    python3 口上.py --禁則        # ⑷ 読者・二人称・呼びかけ
    python3 口上.py --札          # ⑸ カテゴリの札が、順序どおりに在るか

## 口上とは

`# 第N話「題」` の直後、**本文の第一行から連続する独白の行**である。
地の文の行が一つでも来たら、そこで口上は終わる（§0-3）。

    第1節の先頭 ─┬─ ＜場所＞ …      ← 口上（①）
                 ├─ ＜人物＞ …      ← 口上（②）
                 ├─ ＜語り手＞ …    ← 口上（③）
                 ├─ ＜癖＞ …        ← 口上（④）
                 └─ 前年度の出席簿が…  ← ここから本編

⛔ 2026-10-15——著者指示は八つ。**形は四行に落ち着いた**（①②③④）。
   ⚠ **四行の頭に、カテゴリの札が付く**（⑻「カテゴリで分けて、型を作って」）。
     **旧い二つの形も、口上として受ける**——`（…）`（段3の稿）と
     `＜…＞`（段3改・段3改dの稿）である。
     ただし**本文の独白は `（…）` のままである**——二つの記号を混ぜない。

⛔ **比べるときは、札を外す。** 札（`＜場所＞ ` など）は63話に同じゆえ、
   比べた数に同じ字が混ざる。**札は型であって、語ではない**（原則4の註）。
   ——ゆえに `--近い` は、**札を外した本文で測り、札つきでも測って、両方を出す。**

## なぜ要るか

口上は、**63話すべてに、同じ位置・同じ順で置かれる型である**（作法 §0-3）。
ゆえに二つの危険がある。

1. **型が同じゆえ、語まで同じになる。** —— 同じ語の並びの二度目は、
   読者には「同じ手の二度目」に見える（原則4 の註）。
   〔前例〕`04-05`:103 `（名は、変わる。）` と `04-09`:41 `（名は、変わる。）`（r=1.00）。
   ⛔ **これは、いま実際に起きた。** 2026-10-15、**④へ癖を切り出した瞬間、
   ③が「〈名〉は、〈職〉である。」だけになり、第二巻に五度・第三巻に五度、
   同じ一行が並んだ**（`--近い` が 29 組を返した）。
   **ゆえに ③ には、その話の「立場」を一つ入れる**——属性だけを書くと、
   型が同じぶん、語まで同じになる。
2. **名の規則は、巻ごとに違う。** 第四巻は名を置かない（「誰の声か書かない」）。
   第一〜三巻は、語り手の名を置ける（原本に既にある名）。

⚠ この器は数を出すだけである。**判定は人がする。**
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
DRAFT = WORK / "草稿"

TITLE_RE = re.compile(r"^#\s")
SCENE_RE = re.compile(r"^(?:＊|\*{1,3}|—{2,}|-{3,})$")
# ⚠ 2026-10-15——著者の指示で、区切りは `＜…＞` になり、
#   さらに**四行の頭にカテゴリの札**が付いた（`＜場所＞ …`）。
#   **旧い二つの形も、口上として受ける**（前の稿を読むため）。
#     `（…）`        ——段3の稿
#     `＜…＞`        ——段3改・段3改dの稿
#     `＜札＞ 本文`  ——いまの稿
MONO_RE = re.compile(r"^(?:（.*）|＜.*＞|＜[^＞]+＞[ 　].+)$")

# 札（カテゴリ）。**順序も見る**——型は順序まで含む。
LABELS = ["場所", "人物", "語り手", "癖"]
LABEL_RE = re.compile(r"^＜([^＞]+)＞[ 　]?")


def content(s):
    """口上の行から、**札を外した本文**を返す（札が無ければ、そのまま）。"""
    m = LABEL_RE.match(s)
    if m and m.group(1) in LABELS:
        return s[m.end():]
    return s


def wrap(s):
    """旧い形 `＜…＞` `（…）` の外側の括弧を外す（比較のため）。"""
    if s[:1] == "＜" and s[-1:] == "＞":
        return s[1:-1]
    if s[:1] == "（" and s[-1:] == "）":
        return s[1:-1]
    return s


def core(s):
    """**比べるための字面**——札も、外側の括弧も外したもの。"""
    return wrap(content(s))

# 巻ごとの語り手の名（作法 §0-3 の表。場面表の「誰が居るか」欄の先頭の者）。
NARRATOR = {"01": "碓氷", "02": "暮林", "03": "侘田", "04": None}

# ⛔ 2026-10-15——**著者が、口上で名と属性を語ることを許した。**
#   ゆえに第四巻のゲスト（鈴木和彦・大森徹・宮下遥・林沙織・関口浩一・池田絵里）は、
#   いま口上に名を持つ。**残る禁止は、さくら一人である**——
#   第四巻の設計は「作中で誰もその名を呼ばない」ゆえ、口上にも置かない。
VOL4_NAMES = ["さくら"]

# ⑷ 禁則（作法 §0-3——口上は宛先を持たない）
FORBIDDEN = ["読者", "あなた", "きみ", "君", "お前", "あんた", "みなさん", "皆さん"]


def body_lines(path):
    """本文の行だけを (行番号, 文) で返す。題名行・`＊`・空行を除く。"""
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        s = line.strip()
        if not s or TITLE_RE.match(s) or SCENE_RE.match(s):
            continue
        out.append((i, s))
    return out


def prologue(path):
    """冒頭の口上——本文の先頭から連続する独白の行。"""
    out = []
    for i, s in body_lines(path):
        if MONO_RE.match(s):
            out.append((i, s))
        else:
            break
    return out


def episodes():
    return sorted(DRAFT.glob("draft_*.md"))


def cmd_default(rows):
    print(f"■ 口上——{len(rows)}話")
    short = []
    for num, vol, r in rows:
        print(f"\n■ {num}  （{len(r)}行）")
        for i, s in r:
            print(f"    {i}: {s}")
        if len(r) < 2:
            short.append(num)
    print(f"\n  ⛔ 口上が2行に満たない話: {len(short)} {short if short else ''}")
    print(f"  ✅ 口上が在る話: {sum(1 for _, _, r in rows if len(r) >= 2)}/{len(rows)}")

    # 〔計測〕口上は ①場②人③語り手の型を63話が共有する。
    #        ゆえに語尾の一致は、欠陥ではなく、**型そのもの**である。数を控える。
    third = [r[2][1] for _, _, r in rows if len(r) > 2]
    same = sum(1 for s in third if "側である。" in s)
    print(f"\n  〔計測〕③語り手の行に「〜側である。」を持つ話: {same}/{len(third)}")
    print("  ⚠ 2026-10-15 の指示で、③ は**名・属性（職）・立場**を名乗り、")
    print("     **扱う癖は ④ へ切り出された。** ゆえに「〜側である。」の数は、")
    print("     前の稿より減った。**減ったこと自体は欠陥ではない。**")
    print("  〔計測〕行数——" + "  ".join(
        f"{n}行×{sum(1 for _, _, r in rows if len(r) == n)}話"
        for n in sorted({len(r) for _, _, r in rows})))
    tot = sum(len(s) for _, _, r in rows for _, s in r)
    print(f"  〔計測〕口上の字数（合計）: {tot}")
    print("  ⚠ 語尾の一致は型である（原則4の註）。**語の並び**は、--近い で見る。")


def _pairs(rows, key, level):
    """話をまたぐ組を、ratio の高い順に返す。key は行 → 比べる字面。"""
    allm = [(n, i, key(s)) for n, _, r in rows for i, s in r]
    hits = []
    for x in range(len(allm)):
        for y in range(x + 1, len(allm)):
            nx, ix, sx = allm[x]
            ny, iy, sy = allm[y]
            if nx == ny:
                continue
            r = difflib.SequenceMatcher(None, sx, sy).ratio()
            if r >= level:
                hits.append((r, nx, ix, sx, ny, iy, sy))
    return sorted(hits, reverse=True)


def cmd_near(rows):
    # ── 主たる見方——**口上ぜんたい**（行をつないだもの）を、話どうしで比べる。
    #    読者が受け取る単位は、行ではなく、この四行の固まりである。
    #    ⛔ 比べる字面は `core()`——**札と外側の括弧を外したもの**。
    #       札は63話に同じゆえ、混ぜると「同じ手」が札のぶんだけ薄まる。
    #       ⚠ だが**札つきでも測り、両方を出す**（数を隠さない）。
    for name, key, level in (
            ("口上ぜんたい・本文（札を外したもの）", lambda s: core(s), 0.70),
            ("⚠ 参考——口上ぜんたい・札つき", lambda s: s, 0.70)):
        blocks = [(n, "".join(key(s) for _, s in r)) for n, _, r in rows]
        print(f"■ {name}の組（ratio ≥ {level}）——{len(blocks)}話")
        hits = []
        best = (0.0, "", "", "", "")
        for x in range(len(blocks)):
            for y in range(x + 1, len(blocks)):
                nx, sx = blocks[x]
                ny, sy = blocks[y]
                r = difflib.SequenceMatcher(None, sx, sy).ratio()
                if r > best[0]:
                    best = (r, nx, sx, ny, sy)
                if r >= level:
                    hits.append((r, nx, sx, ny, sy))
        for r, nx, sx, ny, sy in sorted(hits, reverse=True):
            print(f"  r={r:.4f}  {nx}  ×  {ny}")
            print(f"        {sx}")
            print(f"        {sy}")
        if not hits:
            print("  （なし）")
        print(f"  〔最大〕r={best[0]:.4f}  {best[1]} × {best[3]}")
        if name.startswith("⚠"):
            print("  ⚠ 札（一話あたり12字——`＜場所＞ ` など）は、**63話に同じ字**である。")
            print("     ゆえに、同じ字が比べた数に混ざる。**門は、上の『本文』で読む。**")
            print("     ここは、その差そのものを見るための数である。")
        print()

    # ── 行ごと——ここは 0.85 以上だけを見る。
    #    ⛔ 口上は ①場所②人物③語り手④癖の型を、63話が共有する。
    #    ゆえに「碓氷千夏は、〜する側である。」どうしが 0.70 前後で並ぶのは、
    #    **型が同じ**という意味であって、**同じ手**という意味ではない（原則4の註）。
    #    0.85 を超えると、もはや語まで同じである。
    for name, key in (("行ごと・本文（札を外したもの）", lambda s: core(s)),
                      ("⚠ 参考——行ごと・札つき", lambda s: s)):
        print(f"■ {name}の組（ratio ≥ 0.85・別の話どうし）")
        hits = _pairs(rows, key, 0.85)
        for r, nx, ix, sx, ny, iy, sy in hits:
            print(f"  r={r:.4f}  {nx}:{ix} {sx}   ×   {ny}:{iy} {sy}")
        if not hits:
            print("  （なし）")
        print()

    # ── 余裕の帯（0.80〜0.85）。⚠ 丸めた表示が 0.85 になる組を、ここで見る。
    print("■ 余裕の帯（0.80 ≤ ratio < 0.85・札を外した本文）")
    hits = _pairs(rows, lambda s: core(s), 0.80)
    hits = [h for h in hits if h[0] < 0.85]
    for r, nx, ix, sx, ny, iy, sy in hits:
        print(f"  r={r:.4f}  {nx}:{ix} {sx}   ×   {ny}:{iy} {sy}")
    if not hits:
        print("  （なし）")

    # 語の並び（句読点と札と括弧を落とした字面）でも見る
    print("\n■ 語の並びだけが同じ組（句読点を落として一致）")
    norm = {}
    for n, _, r in rows:
        for i, s in r:
            key = re.sub(r"[、。（）]", "", core(s))
            norm.setdefault(key, []).append((n, i, s))
    g = {k: v for k, v in norm.items() if len({n for n, _, _ in v}) > 1}
    for k, v in g.items():
        print(f"  ⛔ {k}")
        for n, i, s in v:
            print(f"      {n}:{i}  {s}")
    if not g:
        print("  （なし）")


def cmd_labels(rows):
    """⑸ 型——四行の札が、順序どおりに在るか。"""
    print("■ 型——カテゴリの札（2026-10-15・著者指示⑻）")
    bad = 0
    for num, _, r in rows:
        got = [LABEL_RE.match(s).group(1)
               for _, s in r if LABEL_RE.match(s)]
        if got != LABELS:
            print(f"  ⛔ {num}  札が違う: {got}")
            bad += 1
    print("  ✅ 63話すべてが、＜場所＞＜人物＞＜語り手＞＜癖＞の順である"
          if not bad else f"  ⛔ {bad}話")
    # ④の頭——札が「癖」と言っているのに、本文が「癖は、」で始まっていないか。
    dull = [(n, s) for n, _, r in rows for _, s in r
            if LABEL_RE.match(s) and LABEL_RE.match(s).group(1) == "癖"
            and content(s).startswith("癖は、")]
    print(f"\n  〔計測〕④の本文が、まだ「癖は、」で始まる話: {len(dull)}")
    for n, s in dull:
        print(f"      {n}: {s}")


def cmd_names(rows):
    # ⛔ 名は、**口上ぜんたいで一つ**であればよい。①場の行に名は無いのが正しい——
    #    ゆえに、行ごとに名を要求してはならない（2026-10-15、最初の版の穴）。
    print("■ 名の規則——⑶（口上ぜんたいで見る）")
    bad = 0
    for num, vol, r in rows:
        text = "".join(s for _, s in r)
        if vol == "04":
            for w in VOL4_NAMES:
                if w in text:
                    print(f"  ⛔ 第四巻に名: {num} 「{w}」")
                    bad += 1
        else:
            want = NARRATOR[vol]
            if want and want not in text:
                print(f"  ⚠ 語り手の名が無い: {num} （期待「{want}」）")
    if not bad:
        print("  ✅ 第四巻の口上に、名は一つも無い")
    print(f"\n  ⚠ 語り手の名は、巻ごとに {NARRATOR} である")
    print("  ✅ 2026-10-15——著者が、口上で名と属性を語ることを許した。")
    print("     ゆえに相手の名（片山大翔・高橋由美…）は、いま口上に在る。")
    print(f"     ⛔ 第四巻で名を置かないのは、{VOL4_NAMES} だけである。")


def cmd_forbid(rows):
    print("■ 禁則——⑷（口上は宛先を持たない）")
    bad = 0
    for num, _, r in rows:
        for i, s in r:
            for w in FORBIDDEN:
                if w in s:
                    print(f"  ⛔ {num}:{i} 「{w}」 {s}")
                    bad += 1
    print("  ✅ 読者・二人称・呼びかけは、一つも無い" if not bad
          else f"  ⛔ {bad}件")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--近い", action="store_true")
    ap.add_argument("--名", action="store_true")
    ap.add_argument("--禁則", action="store_true")
    ap.add_argument("--札", action="store_true")
    a = ap.parse_args()

    rows = []
    for p in episodes():
        num = p.name.split("_")[1]
        rows.append((num, num.split("-")[0], prologue(p)))

    if a.近い:
        cmd_near(rows)
    elif a.名:
        cmd_names(rows)
    elif a.禁則:
        cmd_forbid(rows)
    elif a.札:
        cmd_labels(rows)
    else:
        cmd_default(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
