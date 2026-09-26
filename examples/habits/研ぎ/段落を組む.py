#!/usr/bin/env python3
"""段落を組む——一行一文の草稿を、自然な一行多文（段落）へ組む。

**⚠ 字は、一字も触らない。** **行の切り方だけを変える。**

いまの形——本文の一行の次は、必ず空行である（ゆえに、どの拍も一文で切れている）。
組んだ形——段落は一行であり、段落の間だけに空行が一つある。

ゆえに「組む」とは、**その行を、直前の本文行へ繋ぐ**ことである（間の空行が消える）。

台帳（マニフェスト）の形式——タブ区切り、一行一件。
**前三欄は「差し替える.py」「挿し入れる.py」と同じである**（読む者が同じに読めるように）。

    ファイルパス<TAB>行番号<TAB>組む

⚠ **「切る」は書かない**（既定である）。**ゆえに台帳は、例外だけを書く**——
   「組む」と書かれた行は、直前の行と繋がる。**台帳が短いほど、いまの形に近い。**
⚠ **組む行が一つも無い話は、行番号を `-` として「組まない」と書く**（第三欄）。
   **⚠ 空の台帳は、依然として落ちる**——**空は、書き忘れと見分けがつかない。**
   **⚠ 「組まない」は「見て、組む行が無かった」という申告である。**
⚠ 行番号は、**いまの本文の行番号**である（当てる前の）。
⚠ 同じファイルに何件も当てるときも、**行番号はすべて「当てる前」のものでよい。**

確かめること（当てる前）——① ファイルがある、② 行がある、③ その行が、いま空行でない
本文行である、④ 見出し行を狙っていない、⑤ 同じ行を二度狙っていない、
⑥ 繋ぐ先がある（直前の非空行が、見出しでない本文行である）、
⑦ **⚠ 直上が二重空行でない**——**⚠ それは著者の置いた余白である。跨ぐと消える。**
⑧ **⚠ 会話（鉤括弧）を組まない**——**⚠ 会話の行は文が一つゆえ、文の数の検査では捕まらない。**
⑨ **⚠ 既に組まれている段落を、さらに組まない**——**⚠ 複数文の行は、著者が既に組んだ段落である**
   （**組む側にも、組まれる側にも立てない**）。

確かめること（当てた後）——五つ。

1. **内容の不変**——**本文行を、空行を挟まずに連結した文字列が、前後で一バイトも違わない。**
   ⚠ **空の検査は OK と言う。** ゆえに「相手が空なら落ちる」を入れる——
   **連結した文字列が空なら、照合せずに落とす**（0 == 0 で通さない）。
2. **字数の不変**——**空白を除いた字数が、一字も動いていない。**
3. **段落の形**——**非空行の連続は 0**（段落は空行で隔てられる）。⚠ 先頭・末尾も空行でない。
4. **⚠ 連続する空行の数は、動かない**——**⚠ この作品には、著者の置いた二重空行が六箇所ある**
   （`01-13:930・933`・`01-14:804・813`・`04-17:180・183`。**うち二つは頂点の一文の前後**）。
   **⚠ 器は、それを「規律違反」と呼ばない**——2026-09-26 まで、そう呼んで止まっていた。
   **⚠ 但し、増えても減ってもいけない**ゆえ、数えて比べる。
5. **段落の数**——**本文行数 − 「組む」と書かれた件数**に、一致する。

⚠ そして、**行番号の対応表**を書き出す（旧 <TAB> 新。5-2 の入力になる）。

使い方:
    python3 段落を組む.py <台帳>                 # 当てずに、確かめるだけ
    python3 段落を組む.py <台帳> --write         # 当てる
    python3 段落を組む.py <台帳> --map <出力>    # 対応表を書き出す（当てずに）
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

WHERE = ("組む", "切る", "組まない")


def read_ledger(path: Path) -> list[tuple[Path, int, str]]:
    rows = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 3:
            raise SystemExit(
                f"台帳 {i} 行目——欄が {len(parts)} 個である（3 個でなければならない）\n"
                "   ファイル<TAB>行番号<TAB>組む|切る（⚠ 組む行が一つも無い話は、行番号を `-` として 組まない）"
            )
        f, n, where = parts
        if where not in WHERE:
            raise SystemExit(
                f"台帳 {i} 行目——第三欄が「{where}」である（組む・切る・組まない のいずれかでなければならない）")
        if where == "組まない":
            # ⚠ **組む行が一つも無い話を、明示して言うための一行である。**
            #    ⚠ 空の台帳は、依然として落ちる（**空は、書き忘れと見分けがつかない**）。
            #    ⚠ これは「見て、組む行が無かった」という申告である。行番号は `-` とする。
            if n.strip() != "-":
                raise SystemExit(f"台帳 {i} 行目——組まない の行番号は `-` である（「{n}」が書かれている）")
            rows.append((Path(f), 0, where))
            continue
        rows.append((Path(f), int(n), where))
    return rows


def is_body(line: str) -> bool:
    """本文行——空行でなく、見出しでない。"""
    return bool(line.strip()) and not line.lstrip().startswith("#")


def bun(p: str) -> int:
    """その行の文の数。⚠ 段落化の前の本文行へ掛ける（段落化のあとは、三〜四文が普通である）。"""
    return p.count("。") + p.count("？") + p.count("?") + p.count("！")


def joined_body(lines: list[str]) -> str:
    return "".join(l for l in lines if is_body(l))


def nchars(lines: list[str]) -> int:
    return sum(len(l) for l in lines if l.strip())


def blank_pairs(lines: list[str]) -> list[int]:
    """連続した空行の、前のほうの行番号（1-based）。"""
    return [i for i in range(1, len(lines)) if not lines[i - 1].strip() and not lines[i].strip()]


def check_shape(lines: list[str]) -> list[str]:
    """段落の形——連続する非空行は 0（段落は空行で隔てられる）。

    ⚠ **連続する空行を、ここで 0 と呼ばない。** **⚠ この作品には、著者の置いた二重空行がある**——
    2026-09-26 の実測で六箇所（`01-13:930・933`＝頂点の一文 `:932` の前後・`01-14:804・813`・
    `04-17:180・183`＝頂点の一文 `:182` の前後）。**⚠ それは余白の装置である。**
    ⚠ **この器は、入力に無い規律を要求していた**——ゆえに、第一巻第十三話で止まった。
    **⚠ 但し、増えても減ってもいけない**（下の、数えて比べる検査）。
    """
    bad = []
    for i in range(1, len(lines)):
        a, b = lines[i - 1], lines[i]
        if a.strip() and b.strip():
            bad.append(f"{i} 行目と {i + 1} 行目——非空行が続いている（{b[:24]}）")
    if lines and not lines[0].strip():
        bad.append("先頭が空行である")
    if lines and not lines[-1].strip():
        bad.append("末尾が空行である")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description="一行一文の草稿を、段落へ組む")
    ap.add_argument("ledger")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--map", dest="map_path", default=None, help="対応表の書き出し先（旧<TAB>新）")
    args = ap.parse_args()

    rows = read_ledger(Path(args.ledger))
    if not rows:
        print("⛔ 台帳が空である——組むものが無い")
        return 2

    # 一ファイルを一度だけ読み、そのファイルの全件を「元の本文」に照らして確かめる。
    bad: list[str] = []
    order: list[Path] = []
    grouped: dict[Path, list[tuple[int, str]]] = defaultdict(list)
    for f, n, where in rows:
        if f not in grouped:
            order.append(f)
        grouped[f].append((n, where))

    plans = []
    declared: list[Path] = []   # ⚠ 「組む行が無い」と、台帳が明示した話
    for f in order:
        items = grouped[f]
        if not f.exists():
            bad.append(f"{f}——ファイルが無い")
            continue
        lines = f.read_text(encoding="utf-8").splitlines()
        ok: list[tuple[int, str]] = []
        # ⚠ 「組まない」は、**その話について一行だけ**書ける。**他の行と混ぜない**——
        #    混ざっていたら、書き手が「組む行が無い」と「組む行がある」を同時に言っている。
        if any(w == "組まない" for _n, w in items):
            if [w for _n, w in items] != ["組まない"]:
                bad.append(f"{f.name}——「組まない」と、他の行が混ざっている")
                continue
            declared.append(f)
            plans.append((f, lines, []))
            continue
        for n, where in items:
            if not (1 <= n <= len(lines)):
                bad.append(f"{f.name}:{n}——行が無い（全 {len(lines)} 行）")
                continue
            if not is_body(lines[n - 1]):
                bad.append(f"{f.name}:{n}——本文行でない: {lines[n - 1][:32]!r}")
                continue
            if where == "組む":
                # 繋ぐ先——直前の非空行が、見出しでない本文行であること。
                j = n - 2
                while j >= 0 and not lines[j].strip():
                    j -= 1
                if j < 0:
                    bad.append(f"{f.name}:{n}——上に繋ぐ先が無い（先頭の本文行である）")
                    continue
                if not is_body(lines[j]):
                    bad.append(f"{f.name}:{n}——繋ぐ先が見出し行である: {lines[j][:32]!r}")
                    continue
                # ⚠ 直上が二重空行なら、組めない。**それは著者の置いた余白である**——
                #    跨ぐと、下の `while` が空行を全部取り除き、**余白ごと消える**（2026-09-26 に気づいた）。
                if n >= 3 and not lines[n - 2].strip() and not lines[n - 3].strip():
                    bad.append(f"{f.name}:{n}——直上が二重空行である（著者の余白を跨ぐ）")
                    continue
                # ⚠ 指示書 §2-2「会話（鉤括弧）を、他の文と組まない」を、機械で二つに割る。
                #    ⚠ **会話の行は、文が一つである**（「はい。」）ゆえ、**文の数の検査では捕まらない。**
                #    ⚠ 2026-09-26、02-06 の台帳を作った者がこれを指で見つけた——
                #    「`:359` 前田亮太が言う。」は、器の検査を素通りします、と。
                #    ⚠ 実測（2026-09-26。走査した集合＝四巻六十三話の草稿 63 本）——**鉤括弧を含む本文行は 149、
                #    うち行頭が「が 145、行頭が「でなく行末が」が 4 である**（4 件はすべて 03-06）。
                #    ⚠ ゆえに、繋げば「地の文と会話が同じ段落」という、この作品に無い形ができる。
                #    ⚠ 承認済み・案の全台帳 4,404 件を、当てる前の本文（控え）に照らして数えた——
                #    **鉤括弧を組む 0 件・鉤括弧へ組む 0 件。** **ゆえにこれは、既にある仕事を縛らない。**
                if "「" in lines[n - 1] or "」" in lines[n - 1]:
                    bad.append(f"{f.name}:{n}——会話の行を組もうとしている"
                               f"（§2-2。会話は必ず単独の段落である）: {lines[n - 1][:32]!r}")
                    continue
                if "「" in lines[j] or "」" in lines[j]:
                    bad.append(f"{f.name}:{n}——会話の行へ組もうとしている"
                               f"（§2-2。直前 {j + 1} は会話である）: {lines[j][:32]!r}")
                    continue
                # ⚠ 指示書 §91「既に組まれている段落を、さらに組まない」を、機械で二つに割る。
                #    ⚠ 段落化済みの話では、**複数文の行は、著者が既に組んだ段落である。**
                #    ⚠ ゆえに、その行は動かせない——**組む側にも、組まれる側にも、立てない。**
                #    ⚠ 2026-09-26、第二巻の五本を人に任せたところ、**三本がここを外した**
                #    （02-02 が十一件・02-04 が十六件・02-01 が一件）。**いずれも「読み方」として申告された。**
                #    **⚠ 文面は一義的ゆえ、人の読みに委ねず、器の側で止める。**
                if bun(lines[n - 1]) != 1:
                    bad.append(f"{f.name}:{n}——複数文の行を組もうとしている"
                               f"（この行は {bun(lines[n - 1])} 文＝既に組まれた段落である）: {lines[n - 1][:32]!r}")
                    continue
                if bun(lines[j]) != 1:
                    bad.append(f"{f.name}:{n}——複数文の行へ組もうとしている"
                               f"（直前 {j + 1} は {bun(lines[j])} 文＝既に組まれた段落である）: {lines[j][:32]!r}")
                    continue
            ok.append((n, where))
        seen = [n for n, _w in ok]
        if len(set(seen)) != len(seen):
            dup = sorted({n for n in seen if seen.count(n) > 1})
            bad.append(f"{f.name}——同じ行を二度狙っている: {dup}")
            continue
        if ok:
            plans.append((f, lines, ok))

    if bad:
        print(f"⛔ 当てられない {len(bad)} 件——一件も当てていない")
        for b in bad:
            print("   " + b)
        return 1

    # 組む。元の本文を頭から歩き、「組む」と書かれた行を直前の本文行へ足す。
    results = []
    for f, lines, ok in plans:
        merge = {n for n, w in ok if w == "組む"}
        out: list[str] = []
        # 旧の行番号 → 新の行番号（本文行のすべてについて、必ず一件書く）
        themap: list[tuple[int, int]] = []
        for i, line in enumerate(lines, 1):
            if i in merge:
                while out and not out[-1].strip():
                    out.pop()
                themap.append((i, len(out)))
                out[-1] = out[-1] + line
            else:
                out.append(line)
                if is_body(line):
                    themap.append((i, len(out)))

        # 確かめる——① 内容の不変（⚠ 空なら落ちる）
        before, after = joined_body(lines), joined_body(out)
        if not before:
            bad.append(f"{f.name}——本文が空である（照合せずに落とす）")
            continue
        if before != after:
            bad.append(f"{f.name}——連結した本文が、前後で違う（この器の欠陥）")
            continue
        # 確かめる——② 字数の不変
        if nchars(lines) != nchars(out):
            bad.append(f"{f.name}——空白を除いた字数が動いた（{nchars(lines)} → {nchars(out)}）")
            continue
        # 確かめる——③ 段落の形
        shape = check_shape(out)
        if shape:
            bad.append(f"{f.name}——段落の形が壊れている")
            bad.extend("    " + s for s in shape[:5])
            continue
        # ⚠ 確かめる——③b 連続する空行の数は、入力と同じであること。
        #    **⚠ この作品には、著者の置いた二重空行が六箇所ある**（頂点の一文の前後など）。
        #    **⚠ 器は、それを「規律違反」と呼ばない。****但し、増えても減ってもいけない。**
        if len(blank_pairs(out)) != len(blank_pairs(lines)):
            bad.append(f"{f.name}——連続する空行の数が動いた"
                       f"（{len(blank_pairs(lines))} → {len(blank_pairs(out))}）")
            continue
        # 確かめる——④ 段落の数
        n_before = sum(1 for l in lines if is_body(l))
        n_after = sum(1 for l in out if is_body(l))
        if n_after != n_before - len(merge):
            bad.append(f"{f.name}——段落が {n_after} になった（{n_before - len(merge)} のはずである）")
            continue
        results.append((f, lines, out, ok, merge, themap))

    if bad:
        print(f"⛔ 組めない {len(bad)} 件——一件も当てていない")
        for b in bad:
            print("   " + b)
        return 1

    import statistics

    for f, lines, out, ok, merge, themap in results:
        n_before = sum(1 for l in lines if is_body(l))
        n_after = sum(1 for l in out if is_body(l))
        print(f"■ {f.name}")
        if f in declared:
            # ⚠ 黙って何もしない、が、いちばん危ない。**「見て、組む行が無かった」と、声に出す。**
            print(f"   ⚠ この話は、組む行が無い**（台帳が、そう言っている）**——"
                  f"本文 {n_before} 行・段落 {n_before} 個のまま。**一行も動かさない。**")
            print(f"   ⚠ これは「繋ぎ漏れ」ではない（指示書 §1 の密度の註）。"
                  f"**段落化済みの話では、著者が既に段落を作っている。**")
        else:
            print(f"   本文 {n_before} 行 → 段落 {n_after} 個（−{len(merge)}）")
            print(f"   全体 {len(lines)} 行 → {len(out)} 行（−{len(lines) - len(out)}）")

        # ⚠ 場面ごとに見る。**⚠ 但し、勾配は規範でも目標でもない**（計画 §8-3 の裁定——「場面ごとに決める」）。
        #    ⚠ 2026-09-26 まで、ここは「第二巻の実測 1.62 / 1.42 / 1.33」を並べていた。
        #    **⚠ それは、この段の物差しであるかのように読める**——**著者は、そう決めていない。**
        #    ⚠ ゆえに、数を出すだけにする。**比べる相手を、器が差し出さない。**
        # ⚠ 文の数え方は、上の `bun` に一本化した（2026-09-26。**二箇所に書くと、片方だけ直る**）。

        sec, buf, rows = None, [], []
        for line in out:
            if line.lstrip().startswith("## "):
                if sec:
                    rows.append((sec, buf))
                sec, buf = line.strip(), []
            elif is_body(line):
                buf.append(line)
        if sec:
            rows.append((sec, buf))

        print("   場面ごと——文/段落（⚠ 比べる相手は無い。§8-3——場面ごとに読んで決める）")
        for sec, ps in rows:
            ns = [bun(p) or 1 for p in ps]
            one = sum(1 for n in ns if n == 1) / len(ns)
            print(
                f"     {sec}  段落 {len(ps):>4}  文/段落 {statistics.mean(ns):.2f}"
                f"  字/段落 {statistics.mean([len(p) for p in ps]):.1f}  一文 {one:.0%}"
            )
        sizes = sorted(len(l) for l in out if is_body(l))
        ns = [bun(p) or 1 for p in out if is_body(p)]
        print(f"   全体  文/段落 平均 {statistics.mean(ns):.2f}"
              f"  字/段落 中央値 {statistics.median(sizes):.0f} 平均 {statistics.mean(sizes):.1f}"
              f"  最長 {max(sizes)} 字")
        # ⚠ 申し送りを、器から促す。**勾配を決めた理由は、機械で見えない。人が読む**（指示書 §1）。
        print("   ⚠ この数を、その話の申し送りに書く（なぜ、そう決めたかを一行）。器は理由を持てない。")
        print()

    if args.map_path:
        # ⚠ 「組まない」と申告された話は、**対応表を書かない**。
        #    ⚠ 番号が一字も動かないゆえ、引く先が無い（**恒等の対応表は、貼り直しの材料にならない**）。
        #    ⚠ そして、控えも取られない——**控えの無い対応表は、`対応表を検める.py` が正しく落とす。**
        #    ⚠ ゆえに「この話は動かさなかった」の記録は、**台帳の「組まない」の一行が持つ。**
        moved = [(f, tm) for f, _l, _o, _ok, _m, tm in results if f not in declared]
        Path(args.map_path).write_text(
            "".join(f"{f}\t{o}\t{n}\n" for f, tm in moved for o, n in tm),
            encoding="utf-8",
        )
        n_map = sum(len(tm) for _f, tm in moved)
        print(f"〔対応表〕{n_map} 件を {args.map_path} へ書き出した。"
              + (f"⚠ 組まない {len(declared)} 話は、書いていない。" if declared else ""))

    if not args.write:
        print("〔確かめのみ〕当てるには --write を付ける。")
        return 0

    # ⚠ 当てる前に、いまの本文を控える。
    #    草稿は git で追跡されているが、**未コミットの変更が十三本ある**（2026-09-26 実測）。
    #    ゆえに git だけでは、この段の前後を戻せない。控えは、この器が自分で取る。
    BACKUP = Path(__file__).resolve().parent / "段落化の控え"
    BACKUP.mkdir(exist_ok=True)
    # ⚠ 「組まない」と申告された話は、**控えも取らず、書きもしない**——
    #    ⚠ 一字も動かないゆえ、控えは「この段の前の本文」という**嘘の記録**になる。
    #    ⚠ そして控えだけ在って対応表が無いと、`対応表を検める.py` が正しく落ちる（噛み合わない）。
    moving = [(f, l, o, ok, m, tm) for f, l, o, ok, m, tm in results if f not in declared]
    for f, lines, _out, _ok, _m, _tm in moving:
        (BACKUP / f.name).write_text("\n".join(lines) + "\n", encoding="utf-8")

    for f, _lines, out, _ok, _m, _tm in moving:
        f.write_text("\n".join(out) + "\n", encoding="utf-8")

    print(f"✅ {len(moving)} 本を組んだ" + (f"（⚠ 組まない {len(declared)} 話は、触っていない）" if declared else ""))
    print(f"〔控え〕組む前の本文を {BACKUP.name}/ へ取った（{len(moving)} 本）。")
    print("⚠ 以後、この段より下の引用（NN-NN:NNN）は、対応表で引き直す（§5-2）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
