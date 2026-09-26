#!/usr/bin/env python3
"""引用を貼り直す——段落化で動いた行番号を、記録の側で引き直す。

**⚠ この器は、`貼り直し.py` の代わりではない。** **⚠ あれは「同じ行番号の内側で引用を引き直す」器である**
（読点の解放は行を動かさなかったゆえ、それで足りた）。**⚠ 段落化は、行番号そのものを動かす。**

**⚠ ゆえに、この器は「内容で引く」ことをしない。** **⚠ 対応表だけで引く。**
**⚠ 内容では引けない**——**同じ文が二度現れる本文である**（`段落を組む.py` の冒頭）。

対応表の形式——`段落を組む.py --map` が書き出すもの。タブ区切り、一行一件。

    草稿の絶対パス<TAB>旧の行番号<TAB>新の行番号

**⚠ 本文行のすべてが、一件ずつ入っている**（**組んだ行も、組まなかった行も**）。
**⚠ ゆえに、引けない番号があるなら、それは本文行を指していない**（見出し行・範囲の外）。

する こと——**リポジトリ全体の `*.md` から `NN-NN:NNN` を見つけ、`NNN` を対応表で引き直す。**
**⚠ 「本文 N」は、引かない**（**計画 §4-2。⚠ 顔が三つあり、どれかは機械で見えない**）。
**⚠ それは、⑤の別の手である。**

**⚠ `--bare` を付けたときだけ、四つ目の顔（裸の `:NNN`）のうち、直前の指し先から話が割れるものを引く**
（**計画 §4-4。⚠ 実測——5,248 件のうち 1,597 件・30% だけである。⚠ 既定は、切ったまま**）。

**⚠ 引けない番号は、書き換えずに「引けない」として報告する**（`貼り直し.py` と同じ流儀）。

当てた後に確かめる——二つ。

1. **一件も、黙って落ちていない**——**走査した件数 = 書き換えた件数 + 引けなかった件数。**
   **⚠ 空の検査は OK と言う**——**走査が 0 件なら、照合せずに落とす**（0 == 0 で通さない）。
2. **`NN-NN:` の部分が、一字も動いていない**——**動くのは `:NNN` だけである。**

使い方:
    python3 引用を貼り直す.py <対応表> [<対応表> ...]              # 当てずに、数える
    python3 引用を貼り直す.py <対応表> ... --write                 # 当てる
    python3 引用を貼り直す.py <対応表> ... --root <ディレクトリ>    # 走査する根（既定はリポジトリ）
"""

import argparse
import re
import sys
from pathlib import Path

# ⚠ 境界に `\b` を使わない——2026-09-26 に踏んだ。
#    ⚠ この作品の引用は `` `draft_03-01:99` `` の形を取る。**`_` は語の字である**ゆえ、
#    `\b` は `_` と `0` のあいだに境界を立てず、**その引用を丸ごと落とす。**
#    **⚠ 実測——この一つの誤りで、1,413 件のうち 95 件が黙って落ちた**（0 件ではない。**静かに減る**）。
#    ⚠ ゆえに、境界は「数字でないこと」で書く。
CITE = re.compile(r"(?<![0-9])(0[1-9]|[1-9][0-9])-([0-9]{2}):([0-9]+)(?![0-9])")
DRAFT = re.compile(r"draft_(\d{2}-\d{2})_")

# ⚠ 四つ目の顔——**話を書かない略記**である（`` `draft_03-02:581`・`:603` `` の `:603`）。
#    ⚠ これは引ける（直前の引用と同じ話である）が、**道の引用（`話割り.md:252`）と混ざる**。
#    ⚠ ゆえに、既定では**引かない。数えて、申し送る**——**黙って落とさないためである。**
BARE = re.compile(r"(?<![\w:/]):([0-9]+)(?![0-9])")

# ⚠ `--bare` を付けたときだけ、**直前の指し先から話を割る**（計画 §4-4 の実測）。
#    ⚠ 指し先とは、`NN-NN:NNN` か、`…*.md` の形である。**行のなかで、いちばん近いものを採る。**
#    ⚠ 実測（2026-09-26。リポジトリ全体の *.md 740 ファイル、裸の `:NNN` は 5,248 件）——
#      **直前が `NN-NN:NNN` であるもの 1,597 件（30%）**・直前が別の文書であるもの 1,463 件（28%）・
#      行に指し先が無いもの 2,188 件（42%）。
#    ⚠ ゆえに、この旗で引けるのは、**三割だけである**。**残りは、人が読む。**
#    ⚠ 既定は、切ったままである（**裁定を受けていない**）。
DOCREF = re.compile(r"[^\s`（(「]*\.md")

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}


def read_maps(paths: list[Path]) -> tuple[dict[tuple[str, int], int], list[str]]:
    """対応表を読む。(話, 旧) → 新 の辞書と、読めなかった行の報告。"""
    table: dict[tuple[str, int], int] = {}
    bad: list[str] = []
    for p in paths:
        if not p.exists():
            bad.append(f"{p}——対応表が無い")
            continue
        n = 0
        for i, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            parts = raw.split("\t")
            if len(parts) != 3:
                bad.append(f"{p.name}:{i}——欄が {len(parts)} 個である（3 個でなければならない）")
                continue
            f, old, new = parts
            m = DRAFT.search(Path(f).name)
            if not m:
                bad.append(f"{p.name}:{i}——ファイル名から話が読めない: {Path(f).name}")
                continue
            key = (m.group(1), int(old))
            if key in table and table[key] != int(new):
                bad.append(f"{p.name}:{i}——{key} が二度、違う値で書かれている")
                continue
            table[key] = int(new)
            n += 1
        print(f"  {p.name}——{n} 件")
    return table, bad


def main() -> int:
    ap = argparse.ArgumentParser(description="段落化で動いた行番号を、記録の側で引き直す")
    ap.add_argument("maps", nargs="+")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--root", default=None, help="走査する根（既定は、この器の二つ上）")
    ap.add_argument("--bare", action="store_true",
                    help="裸の :NNN も、直前の指し先から話を割って引く（⚠ 三割だけ引ける。既定は切る）")
    args = ap.parse_args()

    # ⚠ 既定の根は、リポジトリの根である。**この器の置き場から数えない**——
    #    `親.parent.parent` は `examples/` であり、**リポジトリ全体ではなかった**（2026-09-26 に踏んだ）。
    if args.root:
        root = Path(args.root).resolve()
    else:
        root = Path(__file__).resolve().parent
        while root != root.parent and not (root / ".git").exists():
            root = root.parent
        # ⚠ 遡りきって `.git` が無いなら、**走査しない。**
        #    ⚠ 2026-09-26 に踏んだ——この器を `/tmp` に写して走らせたら、遡りが `/` で止まり、
        #    **黙って 20,065 ファイルを走査した**（結果は変わらなかったが、そうとは限らない）。
        if not (root / ".git").exists():
            print(f"⛔ リポジトリの根が見つからない——{root} まで遡ったが `.git` が無い。"
                  f"⚠ `--root` で走査する根を明示する（**黙って根まで走査しない**）")
            return 1
    print(f"■ 対応表を読む")
    table, bad = read_maps([Path(m) for m in args.maps])
    if bad:
        print(f"⛔ 対応表が読めない——{len(bad)} 件")
        for b in bad:
            print("   " + b)
        return 1
    if not table:
        print("⛔ 対応表が空である——引ける番号が一つも無い")
        return 2
    print(f"  引ける番号——{len(table)} 件（{len({k[0] for k in table})} 話）")
    print()

    files = sorted(p for p in root.rglob("*.md") if not (SKIP_DIRS & set(p.parts)))
    print(f"■ 走査する——{root} の *.md、{len(files)} ファイル")

    scanned = 0       # ⚠ `NN-NN:NNN` を走査した数
    hit = 0           # ⚠ 引けた数（両方の顔の合計）
    hit_cite = 0
    bare_seen = 0     # ⚠ 裸のうち、直前の指し先から話が割れたもの
    bare_skip = 0     # ⚠ 割れなかったもの（道の引用・指し先が無い）
    miss: list[tuple[Path, int, str, int, str]] = []   # 第五欄は、顔（cite / bare）
    plans: list[tuple[Path, str, int]] = []  # (ファイル, 新しい本文, 書き換えた件数)
    for p in files:
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        found = list(CITE.finditer(text))
        edits: list[tuple[int, int, str, str]] = []   # (始, 終, 置き換える文, そこにあるはずの文)
        n = 0

        # ⚠ 一つの顔——`NN-NN:NNN`。**話と行番号を持っているゆえ、機械で引ける。**
        scanned += len(found)
        for m in found:
            key = (f"{m.group(1)}-{m.group(2)}", int(m.group(3)))
            if key in table:
                edits.append((m.start(), m.end(), f"{key[0]}:{table[key]}", m.group(0)))
                n += 1
                hit += 1
                hit_cite += 1
            else:
                miss.append((p, m.start(), m.group(0), key[1], "cite"))

        # ⚠ 四つ目の顔——裸の `:NNN`。**`--bare` のときだけ、直前の指し先から話を割る**（計画 §4-4）。
        #    ⚠ 行のなかで、いちばん近い指し先が `NN-NN:NNN` であるときだけである。
        #    ⚠ 別の文書（`話割り.md:252`）であるとき、および指し先が無いときは、引かない。
        if args.bare:
            for lm in re.finditer(r"[^\n]+", text):
                line, base = lm.group(0), lm.start()
                refs = [(base + x.start(), x.group(0), "cite") for x in CITE.finditer(line)]
                refs += [(base + x.start(), x.group(0), "doc") for x in DOCREF.finditer(line)]
                refs.sort()
                for b in BARE.finditer(line):
                    pos = base + b.start()
                    if any(s <= pos < e for s, e, _r, _o in edits):
                        continue          # 既に `NN-NN:NNN` として引いた。
                    prev = [r for r in refs if r[0] < pos]
                    cm = CITE.fullmatch(prev[-1][1]) if prev and prev[-1][2] == "cite" else None
                    if cm is None:
                        bare_skip += 1
                        continue
                    bare_seen += 1
                    key = (f"{cm.group(1)}-{cm.group(2)}", int(b.group(1)))
                    if key in table:
                        # ⚠ `b.end()` は**行の頭からの数**である。`pos`（=`base + b.start()`）と違い、
                        #    足し忘れると**置き換える範囲の終わりが千行ぶん手前を指す**（2026-09-26 に踏んだ）。
                        edits.append((pos, base + b.end(), f":{table[key]}", b.group(0)))
                        n += 1
                        hit += 1
                    else:
                        miss.append((p, pos, b.group(0), int(b.group(1)), "bare"))

        if not edits:
            continue
        edits.sort()
        # ⚠ 確かめる①——置き換える範囲が、**その引用そのものを指している**こと。
        #    ⚠ 2026-09-26 に踏んだ——裸の顔の `b.end()` に行頭からの数を足し忘れ、
        #    **置き換える範囲の終わりが千行ぶん手前を指した**（本文は 282,487 字から 1,564,049 字へ膨れた）。
        #    ⚠ 重なりの検査は、これを**見逃す**——終わりが小さいゆえ、重ならない。
        #    ⚠ そして「伸びの合計」で見るのは**恒等式である**——実際に測って、鳴らないことを確かめた
        #    （再構成が `text[last:s]` を取る以上、伸びは見込みと必ず一致する。**足したが、外した**）。
        #    **⚠ 鳴らない検査は、置かない。**
        for s, e, _r, was in edits:
            if text[s:e] != was:
                print(f"⛔ {p}——引き直す範囲が、その引用を指していない（この器の欠陥）"
                      f"／{was} を {s}:{e} で引こうとした（そこにあるのは {text[s:e]!r}）")
                return 1
        if any(edits[i][0] < edits[i - 1][1] for i in range(1, len(edits))):
            print(f"⛔ {p}——引き直す範囲が重なった（この器の欠陥）")
            return 1
        out, last = [], 0
        for s, e, r, _was in edits:
            out.append(text[last:s])
            out.append(r)
            last = e
        out.append(text[last:])
        new = "".join(out)
        # ⚠ 確かめる②——`NN-NN:` の部分が、一字も動いていないこと。
        if [x.group(0).split(":")[0] for x in CITE.finditer(new)] != [
            x.group(0).split(":")[0] for x in found
        ]:
            print(f"⛔ {p}——`NN-NN:` の部分が動いた（この器の欠陥）")
            return 1
        if n:
            plans.append((p, new, n))

    n_cite_miss = sum(1 for *_x, k in miss if k == "cite")
    n_bare_miss = sum(1 for *_x, k in miss if k == "bare")
    print(f"  走査した `NN-NN:NNN`——{scanned} 件。うち、引けた {hit_cite}・引けない {n_cite_miss}")
    if args.bare:
        print(f"  裸の `:NNN`——話が割れた {bare_seen} 件。うち、引けた {bare_seen - n_bare_miss}・"
              f"引けない {n_bare_miss}。⚠ 割れなかった {bare_skip} 件は、引いていない")
    print(f"  引けた——合計 {hit} 件")
    print()

    if miss:
        print(f"■ 引けない番号——{len(miss)} 件（書き換えない。人が読む）")
        seen = set()
        for p, _pos, raw, _num, _k in miss:
            k = (p.name, raw)
            if k in seen:
                continue
            seen.add(k)
            print(f"   {p.relative_to(root)}——{raw}")
            if len(seen) >= 25:
                print(f"   …ほか {len(miss) - len(seen)} 件")
                break
        print()

    # ⚠ 四つ目の顔を、数えて申し送る。**黙って落とさないためである。**
    bare = 0
    for p in files:
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        bare += len(BARE.findall(text))
    if bare:
        if args.bare:
            print(f"⚠ 話を書かない略記（`:NNN`）——{bare} 件。"
                  f"**うち、直前の指し先から話が割れたもの {bare_seen} 件・割れなかったもの {bare_skip} 件。**")
            print(f"    ⚠ 割れなかったものは、道の引用（`話割り.md:252`）か、行に指し先が無いものである。**人が読む。**")
        else:
            print(f"⚠ 話を書かない略記（`:NNN`）——{bare} 件。**この器は引かない**（既定）。")
            print(f"    ⚠ 道の引用（`話割り.md:252`）と混ざるゆえ、機械では切れない。")
            print(f"    ⚠ `--bare` を付けると、**直前の指し先から話が割れるものだけ**を引く"
                  f"（**実測——5,248 件のうち 1,597 件・30%。計画 §4-4**）。")
        print()

    # ⚠ 確かめる①——一件も、黙って落ちていない。
    if scanned != hit_cite + n_cite_miss:
        print(f"⛔ 走査 {scanned} ≠ 引けた {hit_cite} + 引けない {n_cite_miss}——黙って落ちたものがある")
        return 1
    if args.bare and bare_seen != (bare_seen - n_bare_miss) + n_bare_miss:
        print("⛔ 裸の数が合わない（この器の欠陥）")
        return 1
    if scanned == 0:
        print("⛔ 引用が 0 件である——照合せずに落とす（0 == 0 で通さない）")
        return 1
    print(f"✅ `NN-NN:NNN` 走査 {scanned} = 引けた {hit_cite} + 引けない {n_cite_miss}"
          + (f"／裸 割れた {bare_seen} = 引けた {bare_seen - n_bare_miss} + 引けない {n_bare_miss}"
             + f"／割れず {bare_skip}" if args.bare else ""))

    if not args.write:
        print("〔確かめのみ〕当てるには --write を付ける。")
        return 0

    # ⚠ 当てる前に、いまの文書を控える。**引用を持つ文書は、草稿ではない**——
    #    ゆえに控えは、研ぎ/引用の控え/ へ、道を平らにして取る。
    BACKUP = Path(__file__).resolve().parent / "引用の控え"
    for p, new, n in plans:
        rel = p.relative_to(root)
        dst = BACKUP / str(rel).replace("/", "__")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    for p, new, _n in plans:
        p.write_text(new, encoding="utf-8")

    print(f"✅ {len(plans)} ファイルを書き換えた（{hit} 件）")
    print(f"〔控え〕書き換える前の文書を {BACKUP.name}/ へ取った。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
