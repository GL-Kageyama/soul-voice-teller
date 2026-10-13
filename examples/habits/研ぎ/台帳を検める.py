#!/usr/bin/env python3
"""台帳を検める——第三段（`/prose`）の改稿案を、本文へ当てる前に、機械で見える分だけ検める。

見えるのは、次の八つである。

1. **行が在るか**——その話の、その行番号が、いまもその文であるか（一字一句）。
2. **一行であるか**——案が一行であり、行数を動かさないか。**案が、いまの文より
   文を増やしていないか。** ⚠ **巻では決めない。** 一行が二文である行が、設計された
   例外として在る——第一巻の会話（`01-07:631`「先生。この一枚名がありません。」）、
   第四巻の型（**どの話にも一つずつ**「…。それ、誰の。」の十七行）、第三巻の
   `03-01` の冒頭・`03-06`・`03-07`（のべ二百三十二行）。**ゆえに見るのは、
   いまの文との差である。**
3. **逐語**——案が、その話の本文のどこかに、既に一字一句そのまま在るか。
4. **巻をまたいだ反復**——案が、他の話にも現れるか（十二字以上）。
   三話以上に現れるなら、それは基底語である（⚠ ではなく、註として出す）。
5. **禁則語**——`検査/check.py` と同じ語群（`../README.md` の「## 禁則」から読む）。
6. **色語と匂いの語**——案が新しく持ち込んでいるか（いまの文が持っていなければ、新しい）。
   ⚠ **第四巻にだけ掛ける**（`CLOSED_VOLUMES` を見よ）。
7. **閉じた形**——「〜は、答えない。」「その、ままである。」（**この巻の話末を閉じていた型**）を、
   案が使っていないか。⚠ **「ままである」一般ではない**（`CLOSED_SHAPES` の註を見よ）。
   ⚠ **第四巻にだけ掛ける**（同上）。
8. **同じ話の中の近さ**——その話の既存の行と、語の重なりが大きすぎないか（⚠）。

見えないもの——**その案が、その話の本文に既に真であるか。** これは人が読む。

使い方:
    python3 台帳を検める.py <台帳.tsv> [<台帳.tsv> ...]
    python3 台帳を検める.py <台帳.tsv> --quiet     # ⛔ と ⚠ のある行だけを出す
"""

import argparse
import importlib.util
import re
import sys
from pathlib import Path

# ⚠ 場面の区切りは、いま `＊`（全角のアスタリスク）だけの行である——著者裁定 2026-10-13。
#   **本文行ではない**（prose_lines を見よ）。
RULE_RE = re.compile(r"^＊$")

HERE = Path(__file__).resolve().parent          # examples/habits/研ぎ
HABITS = HERE.parent                            # examples/habits
EXAMPLES = HABITS.parent                        # examples

COLOR = re.compile(r"[青緑黄茶灰銀紫桃橙]")
SMELL = re.compile(r"匂|におい|臭|香|嗅")

# ⚠ **閉じた形は、「ままである」一般ではない。**
#   出典は `第七段階_第三段_prose_指示書.md` §4-4——「**第四巻では、「〜は、答えない。」
#   「その、ままである。」を使わない**（同 §12〜§14）」。**指されているのは、
#   この巻の話末を閉じていた「型」そのものである**——`第四巻_七軸_裁定材料.md` §1-3 が
#   実測している（「話末を閉じるのは「〜、ままである。」が 17/18 話」「**「その、ままである。」は
#   37件あり、うち十五件が第三節末**」）。**§12〜§14 は、その三十七件を当てた記録である。**
#
#   ⚠ **実測（2026-10-14）——第四巻の本文に「ままである」を持つ行は 110 行ある。**
#      **そのすべてが「触ったままである」「止まったままである」「空いたままである」
#      「置かれたままである」の形であり、読点つきの「その、ままである。」は 0 件である。**
#      **ゆえに「ままである」を広く禁じれば、この器は、設計が正しいとしている用法を ⛔ と呼ぶ。**
#      **実害が出た**——2026-10-14、この規則を広く読んだ私は、娯楽の段の案のうち三件
#      （`04-02:227`「指が一本、浮いたままである。」・`04-06:51`「機械の穴が、暗いままである。」・
#      `04-15:89`「椅子の座面が、平らなままである。」）を「〜である／〜ている」へ書き換えて当てた。
#      **規則の要求ではなかった。戻した**（`娯楽_届いた_当てた.md` §5）。**「対比は両側を測る」の実例。**
CLOSED_SHAPES = re.compile(r"答えない|その、?ままである")
MIN_LEN = 12
NEAR = 0.5
ONE_SENTENCE_VOLUMES = {"01", "03", "04"}       # 一行一文が本体の巻（註を出すためだけに使う）

# ⚠ **色語・匂い・閉じた形（答えない／ままである）は、第四巻の規則である。**
#   出典は二つ——`第七段階_第三段_prose_指示書.md`:222-224
#   （「**第四巻は、この二つが既に閉じている**」・「**第四巻では**、……を使わない」）と、
#   `第四巻_締めの連_差し替え指示.md`:68。
#
#   ⚠ **全巻へ掛けると、第一〜第三巻に偽の ⛔ が出る。** 実測——本文で色語を持つ行は
#     **一巻 17・二巻 43・三巻 5・四巻 1**。第一〜第三巻の地の文は、色を普通に使う
#     （`01-01:187`「罫が引いてある。薄い緑である。」／`02-01:95`「二つとも青である。」）。
#     **README の禁則（八つの語群）に、色語は入っていない**——ゆえに全巻の禁則ではない。
#   ⚠ ここを巻で切らないと、**この器は、設計が許している語を ⛔ と呼ぶ**。
CLOSED_VOLUMES = {"04"}


def inner_periods(s: str) -> int:
    """その行が持つ文の数 − 1。末尾の句点は数えない。"""
    return s.count("。") - (1 if s.endswith("。") else 0)


def load_check_module():
    """検査器を読み込む（禁則の語群は、README から読む一個所に保つ）。"""
    path = HABITS / "検査" / "check.py"
    spec = importlib.util.spec_from_file_location("habits_check", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def draft_path(vol: str, ep: str) -> Path:
    d = EXAMPLES / f"habits-{vol}" / "草稿"
    hits = sorted(d.glob(f"draft_{vol}-{ep}_*.md"))
    if not hits:
        raise SystemExit(f"⛔ 本文が見つからない: {vol}-{ep}")
    return hits[0]


def body_lines(path: Path) -> list[str]:
    """行番号つきの本文。空行も見出しも、番号を食う（台帳と同じ物差し）。"""
    return path.read_text(encoding="utf-8").splitlines()


def ends_of(path: Path) -> tuple[set[int], int | None]:
    """**場面末の行番号の集合**と、**章末の行番号**を返す。

    ⚠ **なぜ器が、これを出すか。** 娯楽の段の案は「その行へ一句足す」形である。
        **足した一句が、場面の結びの一打のうしろに来れば、その一打は結びでなくなる。**
        **章末も同じである**（`whole-work-review`——「反復句が変化しなくなったら、それはループである」）。
        ⚠ **これは ⛔ ではない。** **意図してやることもある**（結びへ具体を一つ置く）。
        **だが、意図したかどうかは、人が読まねば分からない。**
        **ゆえに、器は「ここは場面末である」とだけ言う**（2026-10-14、第三巻で
        `03-07:363`「歩数はまだ足りない。」のうしろへ「名簿が、少しだけ開いている。」が
        入り、`:309`「閉じたままである。」と食い違った。**あれは、器が黙っていたから起きた**）。
    """
    ls = body_lines(path)
    scenes: set[int] = set()
    last = None
    for i, l in enumerate(ls, 1):
        s = l.strip()
        if not s or s.startswith("#"):
            continue
        if RULE_RE.match(s):            # 場面の区切り——その手前の本文行が、場面末である
            if last is not None:
                scenes.add(last)
            last = None
            continue
        last = i
    if last is not None:                # ⚠ 最後の場面末は、章末でもある
        scenes.add(last)
    return scenes, last


def prose_lines(path: Path) -> list[str]:
    """本文行だけ。空行・見出し・**場面の区切り（`＊`）**を除く。

    ⚠ 区切りは `＊` だけの行である——著者裁定 2026-10-13。**本文行ではない**——
      数えると、この一文字が全話に現れる「文」として逐語の索引に載る。
    """
    out = []
    for l in body_lines(path):
        s = l.strip()
        if s and not s.startswith("#") and not RULE_RE.match(s):
            out.append(s)
    return out


def bigrams(s: str) -> set[str]:
    return {s[i:i + 2] for i in range(len(s) - 1)}


def build_index(files: list[Path]) -> dict[str, set[str]]:
    idx: dict[str, set[str]] = {}
    for f in files:
        ep = f.name.split("_")[1]
        for s in prose_lines(f):
            idx.setdefault(s, set()).add(ep)
    return idx


def read_ledger(path: Path, ):
    rows = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.strip() == "（なし）":
            continue
        parts = raw.split("\t")
        if len(parts) != 7:
            raise SystemExit(
                f"⛔ {path.name} {i} 行目——欄が {len(parts)} 個である（7 個でなければならない）\n   {raw[:120]}")
        rows.append((path.name, i, parts))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="改稿案の台帳を、本文へ当てる前に検める")
    ap.add_argument("ledgers", nargs="+")
    ap.add_argument("--quiet", action="store_true", help="⛔ と ⚠ のある行だけを出す")
    # ⚠ **娯楽の段（第四段）の案は、文を一つ足す形である。**
    #    「足すのは具体（行為・映像・音）だけ」（`skills/entertainment/SKILL-ja.md`）——
    #    **具体を足せば、文は増える。** ゆえに、増加そのものは違反ではない。
    #    ⚠ **だが、鳴らさないのではなく、別のことを鳴らす**——増えた先の文数である
    #    （`段落化_著者への申し送り.md` §10・§19）。
    ap.add_argument("--add-sentences", action="store_true",
                    help="文の増加を ⛔ にしない（娯楽の段の案のため）。代わりに、"
                         "当てたあとの文数を註に出す")
    # ⚠ **娯楽の案は「いまの文へ一句足す」形ゆえ、その話の既存行と必ず近くなる**
    #    （案は、いまの文そのものを含む）。**測れば必ず鳴る検査は、検査ではない。**
    ap.add_argument("--no-near", action="store_true",
                    help="「同じ話の中の近さ」（検査8）を切る。娯楽の段の案のため")
    args = ap.parse_args()

    check = load_check_module()
    kinzoku = check.load_kinzoku()
    # 語 -> 分類名（同じ語が二つの語群に在れば、両方を持つ）
    word2group: dict[str, list[str]] = {}
    for gname, words in kinzoku.items():
        for w in words:
            word2group.setdefault(w, []).append(gname)

    flat = [f for v in ["habits-01", "habits-02", "habits-03", "habits-04"]
            for f in sorted((EXAMPLES / v / "草稿").glob("draft_*.md"))]
    idx = build_index(flat)

    rows = []
    for led in args.ledgers:
        rows += read_ledger(Path(led))

    print(f"台帳 {len(args.ledgers)} 本 / 案 {len(rows)} 件")
    # ⚠ **掛けなかった検査を、黙らない。** 黙れば「空の検査はOKと言う」の型になる——
    #   検査が走っていないことが、合格に見える。
    vols = sorted({v for _, _, (v, *_rest) in rows})
    off = [v for v in vols if v not in CLOSED_VOLUMES]
    if off:
        print(f"⚠ 色語・匂い・閉じた形（答えない／ままである）の検査は、"
              f"**巻 {', '.join(sorted(CLOSED_VOLUMES))} にだけ掛けた**。"
              f"巻 {', '.join(off)} には掛けていない——この三つは第四巻の規則である"
              f"（`第七段階_第三段_prose_指示書.md`:222-224・`第四巻_締めの連_差し替え指示.md`:68）。"
              f"**ゆえに、この三つについて、巻 {', '.join(off)} の ✅ は「合格」ではない。**")
    print()

    bad = warn = 0
    for src, lineno, (vol, ep, n, old, new, view, ground) in rows:
        try:
            p = draft_path(vol, ep)
            lines = body_lines(p)
        except SystemExit as e:
            print(f"⛔ {src}:{lineno}  {e}")
            bad += 1
            continue
        flags: list[str] = []
        notes: list[str] = []

        # 1. 行が在るか
        try:
            k = int(n)
        except ValueError:
            flags.append(f"⛔ 行番号が数でない: {n!r}")
            k = -1
        if k >= 0:
            if not (1 <= k <= len(lines)):
                flags.append(f"⛔ 行が無い（全 {len(lines)} 行）")
            elif lines[k - 1] != old:
                flags.append(f"⛔ いまの文が違う\n      台帳: {old}\n      本文: {lines[k - 1]}")

        # 2. 一行であるか
        if "\n" in new or "\n" in old:
            flags.append("⛔ 文に改行が入っている")
        if new == old:
            flags.append("⛔ 案が、いまの文と同じである")
        if inner_periods(new) > inner_periods(old):
            if args.add_sentences:
                n_new = inner_periods(new) + 1
                if n_new >= 5:
                    notes.append(
                        f"註 当てると、この行は {n_new} 文になる（⚠ 第五段の規律は"
                        f"「五文以上を新しく作らない」——`段落化_著者への申し送り.md` §10）")
                else:
                    notes.append(f"註 当てると、この行は {n_new} 文になる"
                                 f"（いまは {inner_periods(old) + 1} 文）")
            else:
                flags.append(
                    f"⛔ 案が、いまの文より文を増やしている"
                    f"（{inner_periods(old) + 1} 文 → {inner_periods(new) + 1} 文）")
        if vol in ONE_SENTENCE_VOLUMES and inner_periods(old) >= 1:
            notes.append(f"註 この行は、もともと文が {inner_periods(old) + 1} つである（この巻では例外）")

        # 2''. 場面末・章末——⚠ 註である（`ends_of` を見よ）
        if k >= 0 and 1 <= k <= len(lines):
            se, ce = ends_of(p)
            if ce is not None and k == ce:
                notes.append("註 **この行は、この話の最後の本文行である**（章末）——"
                             "足した一句は、章末の一打の**うしろ**に来る")
            elif k in se:
                notes.append("註 **この行は、この場面の最後の本文行である**（場面末）——"
                             "足した一句は、場面の結びの一打の**うしろ**に来る")

        mine = prose_lines(p) if k >= 0 else []

        # 3. 逐語
        if new in set(mine) and new != old:
            flags.append("⛔ この話の本文に、既に一字一句そのまま在る")

        # 4. 巻をまたいだ反復
        if len(new) >= MIN_LEN:
            others = idx.get(new, set()) - {f"{vol}-{ep}"}
            if len(others) >= 3:
                notes.append(f"註 基底語（{len(others)} 話に現れる）: {''.join(sorted(others))}")
            elif others:
                flags.append(f"⚠ 他の話にも現れる: {''.join(sorted(others))}")

        # 5. 禁則語
        for w, groups in word2group.items():
            if w in new and w not in old:
                flags.append(f"⛔ 禁則語を持ち込んでいる: 「{w}」（{'／'.join(groups)}）")

        # 6. 色語・匂いの語——⚠ 第四巻にだけ掛ける（`CLOSED_VOLUMES` を見よ）
        if vol in CLOSED_VOLUMES:
            m = COLOR.search(new)
            if m and not COLOR.search(old):
                flags.append(f"⛔ 色語を、新しく持ち込んでいる: {m.group(0)}")
            m = SMELL.search(new)
            if m and not SMELL.search(old):
                flags.append(f"⛔ 匂いの語を、新しく持ち込んでいる: {m.group(0)}")

        # 7. 閉じた形——⚠ 第四巻にだけ掛ける（同上）
        if vol in CLOSED_VOLUMES:
            m = CLOSED_SHAPES.search(new)
            if m and not CLOSED_SHAPES.search(old):
                flags.append(f"⛔ 閉じた形を使っている: {m.group(0)}")

        # 8. 同じ話の中の近さ——⚠ `--no-near` で切れる（娯楽の段の案のため）
        pb = set() if args.no_near else bigrams(new)
        near = []
        for l in mine:
            if l == old or l == new:
                continue
            lb = bigrams(l)
            if not lb or not pb:
                continue
            j = len(pb & lb) / len(pb | lb)
            if j >= NEAR:
                near.append((j, l))
        near.sort(reverse=True)
        if near:
            flags.append("⚠ この話の既存行と近い: "
                         + " / ".join(f"「{l}」（{j:.2f}）" for j, l in near[:3]))

        if not flags and not notes:
            if not args.quiet:
                print(f"✅ {vol}-{ep}:{k}  − {old}\n                ＋ {new}   〔観点{view}〕")
                print(f"      根拠 {ground}")
                print()
            continue

        if flags:
            bad += sum(1 for f in flags if f.startswith("⛔"))
            warn += sum(1 for f in flags if f.startswith("⚠"))
            print(f"■ {vol}-{ep}:{k}   〔観点{view}〕")
            print(f"   − {old}")
            print(f"   ＋ {new}")
            print(f"   根拠 {ground}")
            for f in flags:
                print("   " + f)
            for nt in notes:
                print("   " + nt)
            print()
        else:
            if not args.quiet:
                print(f"■ {vol}-{ep}:{k}   〔観点{view}〕  ✅ 機械で見える範囲では、問題なし")
                print(f"   − {old}")
                print(f"   ＋ {new}")
                for nt in notes:
                    print("   " + nt)
                print()

    print(f"—— 案 {len(rows)} 件。⛔ {bad} 件・⚠ {warn} 件。**⚠ と ✅ は、採用の可否ではない。**")
    print("   **その案が、その話の本文に既に真であるかは、人が読む。**")
    return 0


if __name__ == "__main__":
    sys.exit(main())
