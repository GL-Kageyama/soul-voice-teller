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


def sentences(s: str) -> list[str]:
    """文へ切る。`。` で切り、最後に残った端数も一文として返す。"""
    out, buf = [], ""
    for ch in s:
        buf += ch
        if ch == "。":
            out.append(buf)
            buf = ""
    if buf.strip():
        out.append(buf)
    return [x for x in out if x.strip()]


def lost_content(line: str, new: str) -> list[str]:
    """**案が捨てた文**を返す。

    ⚠ **この段の中心の約束は「今の内容を失わずに」である。**
       ゆえに案は、**元の行の文を一つも落としてならない**（足すのは自由）。
    ⚠ **前へ足す・真ん中へ挿すは、どちらもよい**——順序も動かさないことを勧めるが、
       **落とすことだけを ⛔ にする**（`01-06:131` は真ん中に挿しており、正しい）。
    """
    return [x for x in sentences(line) if x not in new]


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


def read_rows(allow_missing: bool = False, only: tuple = (),
              halves: tuple = HALVES) -> list[dict]:
    rows, missing = [], []
    for vol in (only or VOLS):
        for half in halves:
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
                # ⚠ **八欄が本である**（`巻/話/場面/行番号/いまの文/案/三種/根拠`）。
                #    ⚠ **七欄も受ける**——`台帳を検める.py` の形で書いてしまった読み手のため
                #      （場面を落として数える）。**黙って畳まない**——註に出す。
                if len(f) == 8:
                    vol, ep, scene, n, now, new, kind, why = (x.strip() for x in f)
                elif len(f) == 7:
                    vol, ep, n, now, new, kind, why = (x.strip() for x in f)
                    scene = "?"
                else:
                    sys.exit(f"⛔ {p.name} に七欄でも八欄でもない行がある（{len(f)} 欄）:\n  {ln[:120]}")
                rows.append({"src": p.name, "vol": vol, "ep": ep, "scene": scene,
                             "n": n, "now": now, "new": new, "kind": kind, "why": why})
    if missing:
        # ⚠ **足りないことを黙らない。** だが、**途中でも走れるようにする**——
        #    八人は別々に終わるゆえ、そろった巻から先に検める（`--allow-missing`）。
        print("⚠ 案の TSV が足りない: " + ", ".join(missing)
              + f"（読んだのは {len(rows)} 件）", file=sys.stderr)
        if not allow_missing:
            sys.exit("⛔ 全部そろってから走らせること（途中で走らせるなら `--allow-missing`）")
    return rows


# ⚠ **判定と「当てるか」は、一対一である**（`第七段階_第四段_娯楽_ユーモア_検め.md` §4）。
#    食い違いは、書き間違いとして ⛔ で止める（黙って寄せない）。
VERDICTS = {"⛔": "戻す", "△": "著者", "✅": "当てる"}


def read_verdicts(only: tuple = (), suffix: str = "") -> dict:
    """検めの TSV（五欄）を読み、`鍵 -> (判定, 当てるか, 理由)` を返す。

    ⚠ `suffix` は**二度目の回**のためである（`娯楽_ユーモア_検め_0N_2.tsv`）。
    **一度目の検めと、二度目の検めは、別のファイルでなければならない**——
    二度目の鍵は一度目の △／⛔ の鍵と**同じ**ゆえ、一つのファイルへ混ぜると
    `鍵が二度ある` で止まる（この器の検査）。
    """
    out = {}
    for vol in (only or VOLS):
        p = HERE / f"娯楽_ユーモア_検め_{vol}{suffix}.tsv"
        if not p.exists():
            sys.exit(f"⛔ 検めの TSV が無い: {p.name}\n"
                     f"   （検めが済んでから `--decisions` を付けること）")
        for i, raw in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            f = raw.split("\t")
            if f[0].strip() in ("鍵", "key"):
                continue
            if len(f) < 3:
                sys.exit(f"⛔ {p.name} {i} 行目——欄が {len(f)} 個である"
                         f"（鍵/判定/当てるか/理由/確かめた行 の五欄でなければならない）")
            key, verdict, apply_ = f[0].strip(), f[1].strip(), f[2].strip()
            if verdict not in VERDICTS:
                sys.exit(f"⛔ {p.name} {i} 行目——判定が {verdict!r} である"
                         f"（⛔／△／✅ のどれかでなければならない）")
            if apply_ != VERDICTS[verdict]:
                sys.exit(f"⛔ {p.name} {i} 行目——判定 {verdict} なのに「当てるか」が {apply_!r} である"
                         f"（{VERDICTS[verdict]} でなければならない）")
            if key in out:
                sys.exit(f"⛔ {p.name} {i} 行目——鍵 {key} が二度ある")
            out[key] = (verdict, apply_, f[3].strip() if len(f) > 3 else "")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="ユーモアの案を、当てる台帳へ開く")
    ap.add_argument("--swap", action="store_true", help="差し替える.py の四欄台帳で出す")
    ap.add_argument("--ledger", action="store_true", help="台帳を検める.py の七欄台帳で出す")
    ap.add_argument("--allow-missing", action="store_true",
                    help="八本そろっていなくても走らせる（検算だけ）")
    ap.add_argument("--decisions", action="store_true",
                    help="検めの TSV を読み、✅ の行だけを出す（⛔ と △ は出さない）")
    ap.add_argument("--vol", action="append", choices=list(VOLS),
                    help="この巻だけを扱う（巻ごとに当てるため。二度書けば二巻）")
    ap.add_argument("--round", choices=("1", "2"), default="1",
                    help="回。1＝`_0N_a/_0N_b` と `検め_0N.tsv`（既定）／"
                         "2＝`_0N_c` と `検め_0N_2.tsv`（当たらなかった場面の二度目の案）")
    a = ap.parse_args()

    only = tuple(a.vol or ())
    # ⚠ **二度目の回は、別の案ファイルと別の検めを読む**（上の `--round` を見よ）。
    halves = HALVES if a.round == "1" else ("c",)
    vsuffix = "" if a.round == "1" else "_2"
    rows = read_rows(allow_missing=a.allow_missing, only=only, halves=halves)

    # ⚠ **当てる前の検め**（第三段の教訓——順序は `案 → 検め → 当てる`）。
    #    検めが済んでいない行は、**当てない**（黙って全部当てない）。
    tally, undecided, strayed = {}, [], []
    already = []
    if a.decisions:
        verdicts = read_verdicts(only=only, suffix=vsuffix)
        keys = {f"{r['vol']}-{r['ep']}:{r['n']}" for r in rows}
        # ⚠ **逆向きも見る**——検めの鍵が、案の鍵に当たらない場合。
        #    鍵の綴りを誤れば、**その案は「未判定」として当たらない**——
        #    ゆえに、当たらない鍵は黙って捨てず、名指しで出す。
        strayed = sorted(k for k in verdicts if k not in keys)
        kept = []
        for r in rows:
            k = f"{r['vol']}-{r['ep']}:{r['n']}"
            if k not in verdicts:
                undecided.append(k)
                continue
            v = verdicts[k][0]
            per_vol_v = tally.setdefault(r["vol"], {})
            per_vol_v[v] = per_vol_v.get(v, 0) + 1
            if v == "✅":
                kept.append(r)
        rows = kept

    out, fitted, odd = [], [], []
    same, shrunk, over, dup = [], [], [], {}
    lost = []
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

        # ⚠ **当て済みの行**——当てた後は、草稿のその行が**案そのもの**になる。
        #    この判定が無いと、`fit` が足した一句を**もう一度足して**（二重にして）、
        #    「五文以上」と「fit」の偽の ⛔ を出す（2026-10-14、第一巻を当てて実測）。
        if new == line:
            already.append(f"{vol}-{ep}:{n}")
            continue

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

        for gone in lost_content(now, new):
            lost.append(f"{vol}-{ep}:{n} 捨てた文「{gone}」")

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
    if already:
        print(f"■ **当て済み**  {len(already)} 件"
              f"（草稿のその行が、既に案と一字も違わない。検算から外した）: "
              + "、".join(already[:20]) + ("…" if len(already) > 20 else ""), file=sys.stderr)

    if a.decisions:
        print("■ 検めの判定（案の側から数えた数）", file=sys.stderr)
        for v in sorted(tally):
            per = tally[v]
            print(f"    第{v}巻  " + "  ".join(f"{k} {per.get(k, 0)}" for k in ("✅", "△", "⛔")),
                  file=sys.stderr)
        print(f"■ 当てる  {len(rows)} 件（✅ のみ）"
              f"／⚠ △ と ⛔ は当てない。△ は著者が読む番である。", file=sys.stderr)
        if undecided:
            print(f"⛔ **検めが無い行**——{len(undecided)} 件。当てない: "
                  + "、".join(undecided[:20]), file=sys.stderr)
        if strayed:
            print(f"⛔ **案に当たらない鍵**——{len(strayed)} 件"
                  f"（綴りの誤りか、案の消えた行である。黙って捨てない）: "
                  + "、".join(strayed[:20]), file=sys.stderr)

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

    if lost:
        print(f"⛔ **案が、元の文を捨てている**——{len(lost)} 件"
              f"（この段の中心の約束「今の内容を失わずに」に触れる）", file=sys.stderr)
        for x in lost[:20]:
            print(f"    {x}", file=sys.stderr)

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
        return 1 if (odd or over or twodup or lost or undecided or strayed) else 0

    if odd or over or twodup or lost or undecided or strayed:
        print("⛔ あるゆえ、台帳を出さない。", file=sys.stderr)
        return 1

    if a.swap:
        print("# ユーモアの案から作った、差し替える.py 用の4欄台帳。"
              "パスは examples/ からの相対ゆえ、`cd examples` から当てる。")
        if a.decisions:
            print("# ⚠ この台帳は、**当てる前の検めを通った ✅ の行だけ**である"
                  "（⛔ と △ は入っていない）。")
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
