#!/usr/bin/env python3
"""配置を組む——設計の入口を、第一段落へ**移す**案を、**差し替えの対**として組む（読み取り専用）。

⚠ **この器は、文を書かない。** 出すのは**対**だけである——
   いま入口にある段落（`p1`）と、設計の入口の字を持っている段落（`pk`）を、
   **中身ごと入れ替える**（`p1` に `pk` の中身、`pk` に `p1` の中身）。

⚠ **なぜ「移す」が「差し替え」で足りるか。** 段落化のあと、**段落＝物理的な一行**である。
   ゆえに対は**同じ行番号の、一行ずつの置き換え**になる——**行数は一行も動かない**。
   `差し替える.py` がそのまま受ける形（`path<TAB>行番号<TAB>いまの文<TAB>置き換える文`）で出す。
   **ゆえに、行を動かす器（`移す.py`）は作らない。**

⚠ **なぜ、挿入ではないか。** 挿入すれば、同じことを二度書くことになる
   （`第七段階_第三段_prose_指示書.md` §4-2 が禁じている）。**移すのである。**

⚠ **第四巻は組まない。** A5（人称・内面）の再確認まで、第四巻の当ては停止している
   （`第七段階_第四段_設計の改定_裁定材料.md` §8）。⚠ 第四巻は②が 54% で、**この器の主な顧客である**——
   ゆえに、裁定が出たら `--volumes 04` で組む。

⚠ **この器は、対の良し悪しを決めない。** 出すのは**在り処**である。
   ⚠ 検品 §5 の実測——**設計の第一文が第一段落に在るのに弱いと判定された話が 4 つある**
     （`01-02`・`01-06`・`03-11`・`03-12`）。**ゆえに、入口を前へ置くだけでは足りない。**
     この案は、**必要条件を満たすだけである。**

使い方:
    python3 配置を組む.py                      # 巻 01〜03 の「後ろ」を、対で出す
    python3 配置を組む.py --volumes 04          # 第四巻を組む（裁定ののち）
    python3 配置を組む.py --manifest 当てる.tsv # `差し替える.py` が受ける四欄を書く
    python3 配置を組む.py --list                # 判定を、在も含めて全部出す
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(fname: str, name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / fname)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


sc = load("場面表を検める.py", "sc")

TITLE_RE = sc.TITLE_RE
HEAD_RE = sc.HEAD_RE
RULE_RE = sc.RULE_RE


def scene1_numbered(text: str):
    """第一場面の段落を、(行番号, 文) で返す——`場面表を検める.py` と同じ切り方で。

    ⚠ **切り方を写している。** あちらが変われば、こちらも変えねばならない——
       ⚠ ゆえに、下の `main` が**両者の段落数を突き合わせる**（片方だけ直せば、落ちる）。
    """
    lines = text.split("\n")
    if any(HEAD_RE.match(l.strip()) for l in lines):
        out, started = [], False
        for i, ln in enumerate(lines, start=1):
            s = ln.strip()
            if HEAD_RE.match(s):
                if started:
                    break
                started = True
                continue
            if started and s and not s.startswith("#"):
                out.append((i, s))
        return out
    out = []
    for i, ln in enumerate(lines, start=1):
        s = ln.strip()
        if RULE_RE.match(s):
            break
        if s and not s.startswith("#") and not TITLE_RE.match(s):
            out.append((i, s))
    return out


def counts_of(paras, ks):
    """段落ごとに、設計の字を何字持つか。"""
    return [len(ks & sc.kanji(t)) for _, t in paras]


def entrance_kanji(path: Path):
    """場面表の「入口の掴み」のうち、`第一場面の第一文——` と名指された句の漢字。"""
    cell = sc.entrance_row(path)
    if cell is None:
        return None, None
    e = next((x for x in sc.clauses(cell) if sc.FIRST_RE.match(x[0])), None)
    if e is None:
        return cell, None
    body = sc.FIRST_RE.match(e[0]).group(1)
    return cell, sc.kanji(body)


def main() -> int:
    ap = argparse.ArgumentParser(description="設計の入口を第一段落へ移す、差し替えの対を組む")
    ap.add_argument("--volumes", default="01,02,03", help="対象の巻（既定 01,02,03）")
    ap.add_argument("--manifest", metavar="TSV", help="`差し替える.py` が受ける四欄を書く")
    ap.add_argument("--ledger", metavar="TSV", help="人が読む台帳（印つき）を書く")
    ap.add_argument("--list", action="store_true", help="「在」も含めて、判定を全部出す")
    a = ap.parse_args()

    vols = tuple(v.strip() for v in a.volumes.split(",") if v.strip())
    D = sc.drafts()
    pairs, skipped = [], []

    for v, f in sc.tables():
        if v not in vols:
            continue
        p = Path(f)
        key = f"{v}-{p.name.split('_')[0]}"
        if key not in D:
            sys.exit(f"⛔ 場面表に、本文が無い——{key}")

        cell, ks = entrance_kanji(p)
        if cell is None:
            skipped.append((key, "「入口の掴み」の欄が無い"))
            continue
        if not ks:
            skipped.append((key, "「第一場面の第一文——」と名指された句が無い"))
            continue

        dpath = Path(D[key])
        text = dpath.read_text(encoding="utf-8")
        if not text.strip():
            sys.exit(f"⛔ 空の草稿がある——{dpath}")
        paras = scene1_numbered(text)

        # ⚠ 切り方の突き合わせ——`場面表を検める.py` と、段落数が一致しなければ落ちる。
        plain = sc.scene1_paragraphs(text)
        if [t for _, t in paras] != plain:
            sys.exit(f"⛔ 段落の切り方が、`場面表を検める.py` と食い違う——{key}"
                     f"（この器 {len(paras)} 段落 / あちら {len(plain)} 段落）")
        if not paras:
            sys.exit(f"⛔ 第一場面の段落が、一行も読めない——{key}")

        m = sc.measure([t for _, t in paras], ks)
        if m is None:
            skipped.append((key, "漢字が無い"))
            continue

        held = len(ks & sc.kanji("".join(t for _, t in paras)))   # 第一場面が持っている字
        cnt = counts_of(paras, ks)
        rec = {"話": key, "判定": m["判定"], "①": m["持"], "②": m["一"],
               "最良の段落": m["最良の段落"], "段落数": len(paras),
               "p1の字": cnt[0], "最良の字": max(cnt), "持": held,
               # ⚠ **絶対パスで書く。** 台帳の流儀である（`第四巻_差し替え台帳_0613.tsv`）——
               #   相対で書くと、`差し替える.py` をどの置き場から走らせるかで、パスが壊れる。
               #   **この器が一度、リポジトリ根からの相対で書いて、七件とも「ファイルが無い」になった。**
               "第一段落": paras[0][1], "ファイル": str(dpath.resolve())}

        k = m["最良の段落"]
        # ⚠ **対にする条件を、名指しする。**
        #   ① 最良が第一段落でないこと（さもなければ、差し替えは何も動かさない）
        #   ② 最良が、第一場面の持っている字の八割以上を持つこと（＝設計の入口が、そこに固まっている）
        #   ③ **最良が、いまの入口より、二字以上多く持つこと**——⚠ これが無いと、
        #      `03-10`（いまの入口 3 字・最良 4 字）のような**改悪の疑い**を、対と並べてしまう。
        #      **僅差の差し替えは、動かす理由にならない。**
        #
        # ⚠ **そして、①に届かない話が、いちばん多い。** 設計の「入口の句」は
        #   **漢字三〜十三字しか持たない**（実測）ゆえ、**八割の閾値が、ごく小さい分母で動く。**
        #   `02-03` の入口は「傘立ての前に立ち、数を確かめる」＝**五字**で、どの段落も三字まで。
        #   **これは「入口が遅い」ではなく「設計の数文字が、段落に散っている」である。**
        #   ⚠ ゆえに、**理由を三つに割る**——混ぜれば、別の欠陥を同じ名で呼ぶことになる。
        top = max(cnt)
        near = cnt[k] / held if k is not None else 0.0
        if k not in (None, 0) and near >= sc.FULL and cnt[k] - cnt[0] >= 2:
            # ⚠ **導入の順序**——これを検めないと、対は「動かせる」と嘘をつく。
            #   いまの入口が**物を導入している**とき（「床がある。」）、入れ替える先の段落が
            #   **その物を名指している**ことがある（`04-07`「毛が落ちている。**床の上にある。**」）。
            #   入れ替えれば、**まだ名乗られていない物を、名指す段落が第一段落になる。**
            #   ⚠ ここは**字の重なり**で見る。**意味ではない**——ゆえに、印であって、判定ではない。
            shared = sc.kanji(paras[0][1]) & sc.kanji(paras[k][1])
            rec.update({"p1行": paras[0][0], "p1文": paras[0][1],
                        "pk行": paras[k][0], "pk文": paras[k][1], "k": k,
                        "導入": sorted(shared)})
            pairs.append(rec)
        elif m["判定"] == "後ろ" and k not in (None, 0) and cnt[k] - cnt[0] < 2:
            skipped.append((key, f"**僅差**——いまの入口 {cnt[0]} 字 / 最良 {cnt[k]} 字"
                                 f"（{k} 段落目・持 {held} 字）。**差し替えは、動かす理由にならない**"))
        elif m["判定"] == "後ろ":
            skipped.append((key, f"**一点に寄らない**——どの段落も八割に届かない"
                                 f"（最大 {top} 字 / 持 {held} 字・{len(paras)} 段落に散る）。"
                                 f"**動かす先が無い。ゆえに差し替えは、何も動かさない**"))
        else:
            skipped.append((key, f"在（いまの入口 {cnt[0]} 字 / 最良 {top} 字・持 {held} 字）"))

    if not pairs and not a.list:
        sys.exit(f"⛔ 対が一本も組めなかった（巻 {','.join(vols)}）——走査の鍵が掛かっていない")

    print(f"走査した集合——`examples/habits-0{{{' '.join(vols)}}}/構想/各話/*.md` と、その草稿。"
          f"読んだのは「入口の掴み」の欄と、第一場面の段落だけである。")
    print(f"⚠ **この器は、文を書かない。** 出すのは**差し替えの対**である——"
          f"段落化のあと段落＝一行ゆえ、**対は同じ行番号の、一行ずつの置き換え**になる。**行数は動かない。**")
    print(f"⚠ **必要条件を満たすだけである。** 検品 §5——入口が第一段落に在っても弱い話が 4 つある"
          f"（`01-02`・`01-06`・`03-11`・`03-12`）。")
    print()

    for v in vols:
        sub = [r for r in pairs if r["話"].startswith(v)]
        allv = [r for r in skipped if r[0].startswith(v)]
        print(f"【habits-{v}】対 {len(sub)} 本" + (f"・組まなかった {len(allv)} 話" if a.list else ""))
        for r in sub:
            print(f"  ■ {r['話']}  ②={100*r['②']:.0f}%  第一場面 {r['段落数']} 段落"
                  f"・最良は {r['k']} 段落目"
                  f"（**いまの入口 {r['p1の字']} 字 → {r['pk行'] and r['最良の字']} 字**）")
            print(f"      {r['p1行']:>4d} 行目（いまの入口）——{r['p1文']}")
            print(f"      {r['pk行']:>4d} 行目（設計の入口）——{r['pk文']}")
            if r["導入"]:
                print(f"           ⚠ **導入の順序**——入れ替える先が、いまの入口の字を名指している"
                      f"（{'・'.join(r['導入'])}）。入れ替えれば、**まだ名乗られていない物を、"
                      f"第一段落が名指す**。**字の重なりであって、意味ではない。**")
        if a.list:
            for key, why in allv:
                print(f"  · {key}  ——{why}")
        print()

    print(f"—— 対 {len(pairs)} 本（巻 {', '.join(vols)}）。"
          f"⚠ **当てるのは、著者の承認ののちである。**")
    if skipped and not a.list:
        print(f"   ⚠ 組まなかった——{len(skipped)} 話"
              f"（`--list` で全部出る）")

    if a.ledger:
        out = Path(a.ledger)
        cols = ["話", "②第一段落の割合", "第一場面の段落数",
                "いまの入口の行", "いまの入口の文", "設計の在り処の段落", "設計の在り処の行",
                "設計の在り処の文", "設計の字", "持っている字", "導入の順序の印", "当てる", "備考"]
        with out.open("w", encoding="utf-8") as f:
            f.write("\t".join(cols) + "\n")
            for r in pairs:
                why = ("⛔ 入れ替えれば、まだ名乗られていない物を、第一段落が名指す"
                       if r["導入"] else "")
                f.write("\t".join(str(x) for x in [
                    r["話"], f"{100*r['②']:.0f}%", r["段落数"],
                    r["p1行"], r["p1文"], r["k"], r["pk行"], r["pk文"],
                    r["最良の字"], r["持"],
                    "・".join(r["導入"]) if r["導入"] else "（印なし）",
                    "—", why]) + "\n")
        print(f"   人の台帳を書いた——{out}（{len(pairs)} 行）")

    if a.manifest:
        out = Path(a.manifest)
        with out.open("w", encoding="utf-8") as f:
            f.write("# 配置の対——`差し替える.py` が受ける四欄\n")
            f.write("# ⚠ 対ごとに二行。**同じ行番号の、一行ずつの置き換えである。行数は動かない。**\n")
            for r in pairs:
                f.write(f"{r['ファイル']}\t{r['p1行']}\t{r['p1文']}\t{r['pk文']}\n")
                f.write(f"{r['ファイル']}\t{r['pk行']}\t{r['pk文']}\t{r['p1文']}\n")
        print(f"   `差し替える.py` が受ける四欄を書いた——{out}（{2*len(pairs)} 行）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
