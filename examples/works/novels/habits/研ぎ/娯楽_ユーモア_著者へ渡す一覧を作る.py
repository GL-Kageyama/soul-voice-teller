#!/usr/bin/env python3
"""娯楽・ユーモアの △（著者が読む番）と ⛔（戻す）を、著者が読める一覧にする。

第四段は 250 件の案を書き、当てたのは一度目 120・二度目 23 である。ここに並ぶのは、検め役が
`△`（著者が読む番）または `⛔`（戻す）と判定した **107 件**である。**当てる側が ✅ へ格上げして
いない**——案を書いた者でない者が判定する、がこの段の設計である。ゆえに一覧にして著者へ渡す。

## ⚠ 一件ずつ、いまの草稿と突き合わせる（検めの判定を写さない）

**鍵ごとに、全ラウンドの案を集めて、いまの草稿のその行と一字ずつ照合する。** 三つに分かれる——

- `✅ 既に本文にある`——いまの行が**どれかの案の文**と一致する
- `未当て`——いまの行が**案の「いまの文」**と一致する（＝元のまま）
- `⚠ どの案とも違う`——どちらでもない（別の段の案が同じ行に入ったか、行が動いた）

⚠ **`✅` は食い違いである。** 検めが `△`（著者が読む番）と言った案の一部は、**既に本文に入っている**。
理由は一行ごとに違い、いま測った限りでは**「二度目の案として書き直され、そちらが当たった」**が多い。
**ゆえに `✅` の件は、著者が読む案ではない**（もう入っている）。**著者が読むのは `未当て` である。**

## 読み方

鍵は `巻-話:行`（`01-03:203`）。**一行まるごとの差し替えである**（行は足さない・消さない）。

## 使い方

    python3 娯楽_ユーモア_著者へ渡す一覧を作る.py            # 数を出す（書かない）
    python3 娯楽_ユーモア_著者へ渡す一覧を作る.py --write    # 一覧を書く
"""

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE.parents[1]                      # …/examples
OUT = HERE / "第七段階_第四段_娯楽_ユーモア_著者へ渡す一覧.md"

# ⚠ 一度目の検めは案 `_a`／`_b` を、二度目は `_c` を読んでいる（各 TSV の頭の「読んだもの」で実測）。
#    ⚠ しかも `_c` は `_a`／`_b` の**書き直し**である（鍵の重なり＝a∩c 28・b∩c 37、実測）。
#    ゆえに**鍵ごとに全ラウンドの案を集める**——回ごとに引くと、書き直して当てた件を取りこぼす。
ROUNDS = [("一度目", "", "娯楽_ユーモア_案_0?_[ab].tsv"),
          ("二度目", "_2", "娯楽_ユーモア_案_0?_c.tsv")]
ORDER = ["一度目", "二度目"]
KIND = {"△": "著者が読む番", "⛔": "戻す（本文に入れない）"}

# ⚠ 案 TSV は**二つの形**が混ざっている（実測）。欄の位置を決め打ちしない——
#    八欄＝`巻 話 場面 行番号 いまの文 案 三種 根拠`（94+91+65 行）／
#    七欄＝`巻 話 行番号 いまの文 案 三種 根拠`（`_b` に 70 行）。欄数で分ける。
COLUMNS = {8: (3, 4, 5, 6, 7), 7: (2, 3, 4, 5, 6)}    # 欄数 → (行番号, いまの文, 案, 三種, 根拠)


def drafts() -> dict[str, Path]:
    """`01-03` → 草稿のパス。"""
    out: dict[str, Path] = {}
    for p in EXAMPLES.glob("habits-0[1-4]/草稿/draft_*.md"):
        m = re.match(r"draft_(\d\d)-(\d\d)_.+\.md$", p.name)
        if m:
            out[f"{m.group(1)}-{m.group(2)}"] = p
    return out


def proposals_all() -> dict[str, list[tuple[str, str, str, str, str]]]:
    """鍵 → [(回, いまの文, 案, 三種, 根拠), …]（**全ラウンド**）。"""
    table: dict[str, list[tuple[str, str, str, str, str]]] = {}
    for label, _sfx, pat in ROUNDS:
        for p in sorted(HERE.glob(pat)):
            for line in p.read_text(encoding="utf-8").split("\n"):
                if not line.strip() or line.startswith("#"):
                    continue
                f = line.split("\t")
                if f[0] == "巻":                     # 見出し行
                    continue
                cols = COLUMNS.get(len(f))
                if cols is None:
                    continue
                i_ln, i_now, i_new, i_kind, i_why = cols
                vol, tale, ln = f[0], f[1], f[i_ln]
                if not (vol.isdigit() and tale.isdigit() and ln.isdigit()):
                    continue
                table.setdefault(f"{vol}-{tale}:{ln}", []).append(
                    (label, f[i_now], f[i_new], f[i_kind], f[i_why]))
    return table


def verdicts() -> list[tuple[str, str, str, str]]:
    """(回, 鍵, 判定, 理由)。⚠ 判定の**欄**で選ぶ（理由の欄の記号を数えない）。"""
    rows: list[tuple[str, str, str, str]] = []
    for label, sfx, _pat in ROUNDS:
        for p in sorted(HERE.glob(f"娯楽_ユーモア_検め_0?{sfx}.tsv")):
            for line in p.read_text(encoding="utf-8").split("\n"):
                if not line.strip() or line.startswith("#"):
                    continue
                f = line.split("\t")
                if len(f) < 4:
                    continue
                if f[1] in KIND and re.fullmatch(r"\d\d-\d\d:\d+", f[0]):
                    rows.append((label, f[0], f[1], f[3]))
    return rows


def line_of(path: Path, n: int) -> str:
    lines = path.read_text(encoding="utf-8").split("\n")
    return lines[n - 1] if 1 <= n <= len(lines) else ""


def main() -> int:
    ap = argparse.ArgumentParser(description="△と⛔を、著者が読める一覧にする")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    ds = drafts()
    if len(ds) != 63:
        sys.exit(f"⛔ 草稿が {len(ds)} 本しか無い（63 本であるはず）——組まない")

    rows = verdicts()
    if not rows:
        sys.exit("⛔ 判定が 0 件である——組まない（空の検査は通さない）")

    props = proposals_all()

    body: list[str] = []
    counts: dict[tuple[str, str], int] = {}
    states: dict[str, int] = {}
    why_applied: dict[str, int] = {}
    no_proposal: list[str] = []
    cross: dict[tuple[str, str, str], int] = {}

    for label in ORDER:
        sel = [r for r in rows if r[0] == label]
        body.append(f"\n## {label}——{len(sel)} 件\n")
        for v in ("△", "⛔"):
            sub = [r for r in sel if r[2] == v]
            counts[(label, v)] = len(sub)
            if not sub:
                continue
            body.append(f"\n### {label}・{v}（{KIND[v]}）——{len(sub)} 件\n")
            for _lab, key, _verdict, why in sorted(sub):
                got = props.get(key) or []
                path = ds.get(key[:5])
                cur = line_of(path, int(key.split(":")[1])) if path else ""
                mine = [r for r in got if r[0] == label]
                body.append(f"**`{key}`**")
                if not got:
                    body.append("- ⚠ 案が見つからない（検めの鍵が案の TSV に無い）")
                    no_proposal.append(key)
                    state = "⚠ 案なし"
                else:
                    # ⚠ 「案の文 == いまの行」で当たりとする。ただし**案が元の文と同じ行**
                    #    （＝差し替えなし）は当たりに数えない——`_c.tsv` にはそれが混じる。
                    hit = [r for r in got if r[2] == cur and r[1] != r[2]]
                    if hit:
                        state = "✅ 既に本文にある"
                        who = "＋".join(sorted({r[0] for r in hit}))
                        why_applied[who] = why_applied.get(who, 0) + 1
                        body.append(f"- 状態　**✅ 既に本文にある**（{who}の案が当たっている）")
                        body.append(f"- いま　{cur}")
                        for r in hit:
                            body.append(f"- 当たっている案（{r[0]}・{r[3]}）　{r[2]}")
                    elif any(r[1] == cur for r in got):
                        state = "未当て"
                        body.append("- 状態　**未当て**（本文は、案の元の文のまま）")
                        body.append(f"- いま　{cur}")
                    else:
                        state = "⚠ どの案とも違う"
                        body.append("- 状態　**⚠ いまの草稿が、どの案とも違う**"
                                    "（別の段の案が同じ行に入ったか、行が動いた）")
                        body.append(f"- いま　{cur}")
                    for r in (mine or got):
                        body.append(f"- この回の案（{r[0]}）　{r[2]}")
                        body.append(f"- 案の元の文　{r[1]}")
                        body.append(f"- 三種　{r[3]}")
                body.append(f"- 検めの理由（{label}）　{why}")
                body.append("")
                states[state] = states.get(state, 0) + 1
                cross[(label, v, state)] = cross.get((label, v, state), 0) + 1

    total = len(rows)
    unfilled = states.get("未当て", 0)
    head = [
        "# 第七段階 第四段（娯楽・ユーモア）——**著者が読む番**の一覧",
        "",
        "この段は 250 件の案を書き、**当てたのは一度目 120・二度目 23** である。ここに並ぶのは、",
        f"検め役が `△`（著者が読む番）または `⛔`（戻す）と判定した **{total} 件**である。",
        "**当てる側が ✅ へ格上げしていない**——案を書いた者でない者が判定する、がこの段の設計である。",
        "",
        "## ⚠ 件々を開くと、検めの判定はそのままでは読めない",
        "",
        "**一件ずつ、いまの草稿のその行を開き、鍵ごとに全ラウンドの案と一字ずつ照合した**——",
        "",
        f"- **✅ 既に本文にある——{states.get('✅ 既に本文にある', 0)} 件。** "
        "検めが `△`／`⛔` と言った**案**の鍵に、**別の回の案が当たっている**。"
        "（実測＝内訳は " + "／".join(f"**{k}の案** {v} 件" for k, v in sorted(why_applied.items())) + "。"
        "**二度目の検めは、これらを ✅「当てる」と判定している**——ゆえに**著者が読む案ではない**。）",
        f"- **未当て——{unfilled} 件。** 本文は案の元の文のまま＝**当たっていない。**",
        f"- **⚠ どの案とも違う——{states.get('⚠ どの案とも違う', 0)} 件。**",
        f"- ⚠ 案の TSV に鍵が無い——{states.get('⚠ 案なし', 0)} 件。",
        "",
        f"**⇒ 著者が読むのは `未当て` の {unfilled} 件である。**",
        "",
        "⚠ **検めの判定は「案」に対するもので、「行」に対するものではない。** ゆえに、一度目に `△`（保留）"
        "や `⛔`（却下）とされた鍵へ、**二度目の案が当たることは正常**である（一度目の ⛔ は"
        "「一度目の案を戻せ」であって「その行を元に戻せ」ではない）。**この一覧の `✅` はその形である。**",
        "",
        "---",
        "",
        f"- 一度目 `△` **{counts.get(('一度目', '△'), 0)}**・`⛔` **{counts.get(('一度目', '⛔'), 0)}**",
        f"- 二度目 `△` **{counts.get(('二度目', '△'), 0)}**・`⛔` **{counts.get(('二度目', '⛔'), 0)}**",
        "- ⚠ 当てた後で当てる側が戻した **2 件**（第三巻 `03-11:181`・`03-15:245`）は、",
        "  [`娯楽_ユーモア_戻す_03_2.tsv`](娯楽_ユーモア_戻す_03_2.tsv) にある。",
        "",
        "**読み方**——鍵は `巻-話:行`。**一行まるごとの差し替えである**（行は足さない・消さない）。",
    ]

    text = "\n".join(head) + "\n" + "\n".join(body) + "\n"

    print(f"■ 判定 {total} 件（一度目 {sum(1 for r in rows if r[0] == '一度目')}・"
          f"二度目 {sum(1 for r in rows if r[0] == '二度目')}）")
    for k in sorted(counts):
        print(f"   {k[0]}・{k[1]}——{counts[k]} 件")
    print("■ 一件ずつ突き合わせた結果（検めの判定を写していない）")
    for k in sorted(states):
        print(f"   {k}——{states[k]} 件")
    print("■ 回 × 判定 × 状態（交差表）")
    for k in sorted(cross):
        print(f"   {k[0]}・{k[1]}・{k[2]}——{cross[k]} 件")
    for k in sorted(why_applied):
        print(f"      ✅ の内訳・{k}の案が当たっている——{why_applied[k]} 件")
    danger = [k for k in cross if k[1] == "⛔" and k[2] == "✅ 既に本文にある"]
    if danger:
        print(f"⚠ 「⛔ の鍵なのに、いまの本文がどれかの案と一致する」——{sum(cross[k] for k in danger)} 件")
        print("   （⚠ 検めの判定は**案**に対するもので、**行**に対するものではない。"
              "その鍵へ別の回の案が当たっているなら、⛔ は生きている）")
    if no_proposal:
        print(f"⚠ 案の TSV に鍵が無い——{len(no_proposal)} 件: {' '.join(no_proposal[:12])}")
    print(f"■ 一覧は {len(text):,} 字")

    if not args.write:
        print("〔確かめのみ〕書くには --write を付ける。")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"✅ 書いた——{OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
