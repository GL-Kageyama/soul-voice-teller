#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""娯楽_ユーモア_案を作る——八人が書いた八欄の案を、**当てる台帳**へ開く。

⚠ **この段（ユーモア）の案は、これまでと形が違う。**
[`第七段階_第四段_娯楽_ユーモア_材料.md`](第七段階_第四段_娯楽_ユーモア_材料.md) §0-2——
**一行の内側で、文を増やしてよい。ただし差し替えた後の行が四文以下であること。**
ゆえに案は、「行の一部を引いて後ろへ一句足したもの」ではなく、
**その行の、差し替え後の全文**である。

**入力**——八本の TSV（巻ごとに二人、話で割った）。八欄:

    巻 / 話 / 場面 / 行番号 / いまの文 / 案 / 三種 / 根拠

⚠ **`#` で始まる行と、見出し行は読み飛ばす。**

**出力**（標準出力。既定は両方の検算のみ）——

1. `--swap`——[`差し替える.py`](差し替える.py) の**四欄**台帳。
   `パス / 行番号 / いまの文 / 置き換える文`（パスは `examples/` からの相対）
2. `--ledger`——[`台帳を検める.py`](台帳を検める.py) の**七欄**台帳。
   `巻 / 話 / 行番号 / いまの文 / 案 / 観点 / 根拠`

**この器が検めること**（出す前に、必ず）——

- **いまの文が、その行と一致するか**（一致しなければ、行に合わせて組み立てる——`fit`。⚠ 組み立てた件数は黙らず stderr へ出す）。
- **差し替え後の文数が、元より増えているか**（この段の目的そのもの。⚠ **増えていない案は、この段の案ではない**——②③で既に打った「入れ替え」である）。
- **差し替え後の文数が、四文以下か**（`研ぎ` の規則——五文以上の段落を作らない）。
- **同じ行に、二つの案が当たっていないか。**
- **案が、いまの文と同一でないか**（空回り）。

使い方:
    python3 娯楽_ユーモア_案を作る.py --summary
    python3 娯楽_ユーモア_案を作る.py --swap  > 娯楽_ユーモア_差し替え.tsv
    python3 娯楽_ユーモア_案を作る.py --ledger > 娯楽_ユーモア_案.tsv
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE.parent.parent

VOLS = ("01", "02", "03", "04")
HALVES = ("a", "b")

# ⚠ 文の数え方——**`台帳を検める.py` の `inner_periods` と、一字も違えず同じ物差しである。**
#   あちらは `s.count("。") - (1 if s.endswith("。") else 0)` を返す（文数 − 1）。
#   ⚠ **これは言語学の文の数ではない。** 鉤括弧の行（`「同じです。」`）は
#      末尾が `」` ゆえ **2 文**と数えられる。**それでよい**——
#      この段で要るのは、**前と後で同じ物差し**であることだけである。
#   ⚠ **器はこれを ⛔ にしない**（実測）。`--add-sentences` のときは ⚠ 註を出すだけである。
#      ゆえに**四文以下の上限は、この器が守る**（`over`）。
def count_sentences(s: str) -> int:
    """文数。`台帳を検める.py` の `inner_periods(s) + 1` と同じ値である。"""
    return s.count("。") + (0 if s.endswith("。") else 1)


def draft_path(vol: str, ep: str) -> Path:
    d = EXAMPLES / f"habits-{vol}" / "草稿"
    hits = sorted(d.glob(f"draft_{vol}-{ep}_*.md"))
    if not hits:
        sys.exit(f"⛔ 本文が見つからない: {vol}-{ep}")
    if len(hits) > 1:
        sys.exit(f"⛔ 本文が複数ある: {vol}-{ep} —— {[h.name for h in hits]}")
    return hits[0]


def draft_rel(vol: str, ep: str) -> str:
    return f"habits-{vol}/草稿/{draft_path(vol, ep).name}"


def line_of(vol: str, ep: str, n: int) -> str:
    lines = draft_path(vol, ep).read_text(encoding="utf-8").splitlines()
    if not 1 <= n <= len(lines):
        sys.exit(f"⛔ 行が無い: {vol}-{ep}:{n}（この話は {len(lines)} 行）")
    return lines[n - 1]


def fit(line: str, now: str, new: str) -> str | None:
    """案の「いまの文」が、行の**一部**であるとき、行に合わせて組み立てる。

    ⚠ **この段では、これが当たるのは誤りである**（案は行の全文であるはず）。
       ゆえに組み立てた件数は、必ず stderr へ出して、人が読む。
    ⚠ 足した一句は、**行の末尾へ置く**——元の文の順序を動かさないためである。
    """
    if line == now:
        return new
    if not new.startswith(now) or now not in line:
        return None
    return line + new[len(now):]


def read_rows() -> list[dict]:
    rows, missing = [], []
    for vol in VOLS:
        for half in HALVES:
            p = HERE / f"娯楽_ユーモア_案_{vol}_{half}.tsv"
            if not p.exists():
                missing.append(p.name)
                continue
            for ln in p.read_text(encoding="utf-8").split("\n"):
                if not ln.strip() or ln.lstrip().startswith("#"):
                    continue
                f = ln.split("\t")
                if f[0].strip() in ("巻", "vol"):
                    continue
                if len(f) != 8:
                    sys.exit(f"⛔ {p.name} に八欄でない行がある（{len(f)} 欄）:\n  {ln[:120]}")
                rows.append({"src": p.name, "vol": f[0].strip(),
                             "ep": f[1].strip(), "scene": f[2].strip(),
                             "n": f[3].strip(), "now": f[4].strip(),
                             "new": f[5].strip(), "kind": f[6].strip(),
                             "why": f[7].strip()})
    if missing:
        sys.exit("⛔ 案の TSV が足りない: " + ", ".join(missing))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="ユーモアの案を、当てる台帳へ開く")
    ap.add_argument("--swap", action="store_true", help="差し替える.py の四欄台帳で出す")
    ap.add_argument("--ledger", action="store_true", help="台帳を検める.py の七欄台帳で出す")
    a = ap.parse_args()

    rows = read_rows()

    out, fitted, odd = [], [], []
    same, shrunk, over, dup = [], [], [], {}
    per_vol, per_kind = {}, {}
    gained = []

    for r in rows:
        vol, ep, n = r["vol"], r["ep"], int(r["n"])
        try:
            line = line_of(vol, ep, n)
        except SystemExit as e:
            odd.append(f"{r['src']} {r['vol']}-{r['ep']}:{n} —— {e}")
            continue
        now, new = r["now"], r["new"]

        if now != line:
            f = fit(line, now, new)
            if f is None:
                odd.append(f"{r['src']} {r['vol']}-{r['ep']}:{n} 行に合わせられない"
                           f"——引いた文「{now[:60]}」")
                continue
            fitted.append((f"{vol}-{ep}:{n}", line, now, f))
            now, new = line, f

        before, after = count_sentences(now), count_sentences(new)
        if new == now:
            same.append(f"{vol}-{ep}:{n}")
        if after < before:
            shrunk.append(f"{vol}-{ep}:{n} {before}→{after}")
        if after > 4:
            over.append(f"{vol}-{ep}:{n} {before}→{after}")
        if after > before:
            gained.append(f"{vol}-{ep}:{n} {before}→{after}")

        key = f"{vol}-{ep}:{n}"
        dup.setdefault(key, []).append(r["src"])
        per_vol[vol] = per_vol.get(vol, 0) + 1
        per_kind[r["kind"]] = per_kind.get(r["kind"], 0) + 1

        if a.swap:
            out.append("\t".join([draft_rel(vol, ep), str(n), now, new]))
        elif a.ledger:
            view = r["kind"]
            out.append("\t".join([vol, ep, str(n), now, new, view, r["why"]]))
        else:
            print(f"{vol}-{ep}:{n}\t{now[:28]}…\t→\t{new[:60]}…")
            print(f"    {r['kind']}\t{before}文→{after}文")

    # ---- 報告（⚠ 出す前に、必ず読む）-------------------------------------------
    print("", file=sys.stderr)
    print(f"■ 案 {len(rows)} 件（{len(per_vol)} 巻）", file=sys.stderr)
    for v in sorted(per_vol):
        print(f"    第{v}巻  {per_vol[v]}", file=sys.stderr)
    print(f"    三種  " + "  ".join(f"{k} {v}" for k, v in sorted(per_kind.items())),
          file=sys.stderr)
    print(f"■ 文が増えた  {len(gained)} 件   ← **この段の目的。0 に近ければ、この段は空回りである**",
          file=sys.stderr)
    print(f"■ 文が同じ    {len(same)} 件   ← ②③で打った「入れ替え」であり、この段の案ではない",
          file=sys.stderr)
    print(f"■ 文が減った  {len(shrunk)} 件", file=sys.stderr)

    twodup = {k: v for k, v in dup.items() if len(v) > 1}
    if twodup:
        print(f"⛔ 同じ行に二つの案——{len(twodup)} 件", file=sys.stderr)
        for k, v in sorted(twodup.items()):
            print(f"    {k}  {v}", file=sys.stderr)

    if fitted:
        print(f"⚠ 案の「いまの文」が行の一部であった——{len(fitted)} 件。行に合わせて組み立てた:",
              file=sys.stderr)
        for at, line, now, f in fitted[:10]:
            print(f"    {at}", file=sys.stderr)
            print(f"      行: {line}", file=sys.stderr)
            print(f"      引: {now}", file=sys.stderr)
            print(f"      案: {f}", file=sys.stderr)
        if len(fitted) > 10:
            print(f"    …ほか {len(fitted) - 10} 件", file=sys.stderr)

    if over:
        print(f"⛔ 差し替え後が五文以上——{len(over)} 件"
              f"（⚠ **器はこれを ⛔ にしない**。この段の上限を、この器が守る）", file=sys.stderr)
        for x in over[:20]:
            print(f"    {x}", file=sys.stderr)

    if odd:
        print(f"⛔ 当てられない——{len(odd)} 件", file=sys.stderr)
        for x in odd[:20]:
            print(f"    {x}", file=sys.stderr)

    if not (a.swap or a.ledger):
        return 1 if (odd or over or twodup) else 0

    if odd or over or twodup:
        print("⛔ あるゆえ、台帳を出さない。", file=sys.stderr)
        return 1

    if a.swap:
        print("# ユーモアの案から作った、差し替える.py 用の4欄台帳。"
              "パスは examples/ からの相対ゆえ、`cd examples` から当てる。")
        print(f"# 件 {len(out)}（⚠ この段は**一行の内側で文を増やす**——"
              f"文が増えた {len(gained)}／同じ {len(same)}／減った {len(shrunk)}）。")
        print(f"# 行は動かない（置換のみ）。差し替え後の文数は四文以下（最大 "
              f"{max((count_sentences(l.split(chr(9))[3]) for l in out), default=0)}）。")
    else:
        print("# 娯楽_ユーモア_案.tsv——八人が書いた八欄を、"
              "台帳を検める.py に掛ける7欄へ開いたもの。")
        print("# 観点＝三種（クスッ／ニヤリ／ぷっ）／根拠＝四つ（型・土台・外した予測・回収）。")
        print("#" + "\t".join(["巻", "話", "行番号", "いまの文", "案", "観点", "根拠"]))
    for line in out:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
