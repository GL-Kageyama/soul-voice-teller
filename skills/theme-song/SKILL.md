---
name: theme-song
description: A delivery skill that condenses a finished work into one theme song — the full song set to hand to Suno or a similar music generator: the song title, structured lyrics, the style of music (genre · tempo · mood · instrumentation), the vocal direction, the song description, and the placement in the story. It is grounded in the whole work (the theme + the scenes where emotion surfaces) and follows the same expression-and-restraint: the lyrics sing the soul without naming it, stop before the reveal, and are written to be sung, not read. It also delivers a second lyric — the reading-safe mix — the same lines with only the words a generator is likely to mispronounce opened to kana (or otherwise pinned in sound), so a misread never becomes the sung word.
argument-hint: '(optional) the path to draft.md. If omitted, find draft.md in the working directory. Add lang=en|ja|zh to switch the skill's own output language (default en); the lyrics follow the work's language.'
---

# theme-song — condense the finished work into one theme song

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/theme-song lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja`. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

The `lang` argument governs **this skill's own prose** (the instructions, the description fields). It does **not** govern the lyric language — **the lyrics are written in the work's language** (the story's language), because the song is the work's voice.

## Skill Metadata

- **id**: `theme-song`
- **version**: `0.2.0`
- **category**: `delivery` (届ける · the song)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The second **delivery** skill — after package. Where package wraps the finished work so the reader can **receive** it, theme-song condenses it into a song so the soul can be **heard**. Its ground is not the reader's first impression (that is package's) — it is **the work's soul**: the theme fixed at premise, and the specific scene(s) where emotion surfaces in the draft.

**Source**: premise (the theme · the core question) + the aesthetic of expression and restraint (源を語らない).

## Input Contract

- **draft.md**: `<working-dir>/draft.md` (the finished work — what to sing).
- **premise.md**: `<working-dir>/premise.md` (the theme · the core question · the promise — what the song must carry).
- **series-bible.md**: `<working-dir>/series-bible.md` (the foreshadowing table · the disclosure level — what must not be sung).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (voice · forbidden moves — the song sings in the work's voice).
- **package.md** (optional): `<working-dir>/package.md` — if it exists, the song must not contradict its title · catch copy · synopsis. One soul, two doors.

## The ground shift

Package checks against the reader's first impression. The song checks against the work's soul — the theme, and the moment where emotion rises. Every deliverable (title · lyric · style · vocal · description) is asked one question against that soul: *does this carry the work's soul — without naming it, without spoiling it, and as something that can actually be sung?*

## The six deliverables (the song set)

1. **Song title** — the song's name. It does not replace the work's name. A hook that overlaps with the chorus.
2. **Lyrics** — structured with section tags (`[Intro]` / `[Verse 1]` / `[Chorus]` / `[Verse 2]` / `[Bridge]` / `[Outro]`). The lyric obeys the five rules of expression and restraint, and is written to be sung, not read.
3. **Style of music (曲調指定)** — genre · tempo · mood · era · instrumentation, as English tags a music generator parses, plus a short note. It must not betray the work's promise.
4. **Vocal direction (ボーカル指定)** — gender · timbre · manner of singing. Consistent with the work's voice.
5. **Song description (楽曲説明)** — what of the story the song sings, stopping before the reveal. Context for the generator and for a human.
6. **Placement & intent (挿入位置・使用意図)** — OP / ED / insert / ending, and where in the whole story it sits. This is what makes it *the whole work's* song.

## The four rules of the song

1. **Sing without lying** — the lyric and the style come from the work's actual theme and emotion, not a genre promise the work betrays. Don't give a quiet story a loud genre's sound.
2. **Promise what you deliver** — the emotion the song promises (lyric + style) is what the work actually delivers. A song that promises a cathartic explosion for a restrained story is a broken promise.
3. **Stop before the reveal** — the lyric and the description honor series-bible's disclosure. The song may go up to the setup, never past the reveal. Never sing the ending.
4. **Restraint carries into the lyric** — the lyric obeys the same expression-and-restraint: don't explain the theme, don't name the emotion, leave the listener's negative space. A chorus that sings "this is a story about X" has already named it.

## The lyric is meant to be sung (the craft)

Lyrics are not prose lines. They are written to be carried by a voice:

- **Syllable count & rhythm** — the line fits a melody; it can be divided into beats.
- **Rhyme & repetition** — the chorus lingers through repetition. It is the one line that should survive being heard once.
- **The chorus is the hook** — like the catch copy, it carries the theme without stating it.
- **The specific danger of the lyric medium** — the shorter the line, the louder an explanation or a naming stands out. A lyric has fewer words than prose to hide in, so restraint matters more, not less.

## The reading-safe mix (the second lyric)

A generator does not read a lyric; it **pronounces** it. A character it misreads becomes the sung word, and no listener can recover the line. So every theme song ships **two lyric blocks**:

- **The lyric** — `theme-song.md` (or the named variant), in the work's orthography. This is the canonical lyric.
- **The reading-safe mix** — `theme-song-mix.md` (or `<source-stem>-mix.md` when the lyric is a named variant, e.g. `theme-song-rock-mix.md`). The same lyric, with only the words at risk of misreading opened to kana (or, in other languages, pinned in sound).

The mix is **not a rewrite**. Same words, same lines, same order, same structure tags, same sung syllables. Only the spelling of the risky words changes. The mix is a second candidate to audition against the canonical lyric, never a correction of it. It is not a seventh deliverable — it is the same lyric in a second spelling.

### ほどほど — open the minimum

Open a word only when it has a real failure shape:

| risk | examples (Japanese lyrics) |
|---|---|
| multiple readings | 設計 (せっけい / せつけい) · 保守 (ほしゅ / まもり) · 半分 (はんぶん / はんぷん) · 開く (ひらく / あく) · 月曜日 (げつようび / つきようび — the び can drop) · 方 (かた / ほう) · 親 (おや / しん) · 鍵 (かぎ / けん) |
| rare, long, or dictionary-missing compounds | 冪等性 · 枯渇 · 扇風機 · 環境変数 · 消費電力 · 先週 |
| numbers and times | 500 → ごひゃく · 十九 → じゅうきゅう · 三百五十三 → さんびゃくごじゅうさん · 二時 → にじ |
| Latin acronyms and symbols | CPU · SLO · I/O · .env |
| a short line with no context | a one-word line, a line whose neighbors carry no grammar |
| a word whose reading changes the meaning | 開いた (あいた / ひらいた) |
| the hook the ear must get right | the theme word, the line the song turns on |

A hook can be opened in part: keep the theme word's orthography and open only the risky character (揺れ方 → 揺れかた).

Leave a word in kanji when:

- **okurigana fixes the reading** — 読まない · 知らない · 冷たい · 割り込み. The inflected form has one reading.
- **it has one reading in this context** — 部屋 · 画面 · 光 · 声 · 指. (せい · こう · し are not words here.)
- **the orthography carries the meaning** — the theme word, the title, a one-character turn (来るな → 来た), or a word that collides with a homophone when opened (二本 → にほん = 日本).
- **it is a katakana loanword** — opening it to hiragana reads as unnatural. Only Latin acronyms are opened, and to katakana (CPU → シーピーユー).
- **opening it would erase segmentation cues.** Kana boundaries are not free: the more kana, the fewer word boundaries the generator can hear.

When in doubt, **leave the word in kanji and put it in the "if you still hear it" table**. The next pass opens only the words that actually came out wrong.

### Lyrics in other languages

The same principle, at the medium's own risk points:

- **Chinese** — polyphonic characters (多音字), rare compounds, Arabic numerals, Latin acronyms. Separate ambiguous compounds with spaces, spell numbers and acronyms out, and substitute a homophone-safe word only when the meaning survives. Put pinyin disambiguation in a table beside the lyric, not in the lyric block — the generator sings what is written.
- **English** — heteronyms (read / read · live / live · lead / lead), acronyms, numbers, proper nouns. Expand numbers and acronyms into words; replace a heteronym with an unambiguous word only when the line survives. Do not put phonetic respellings in the lyric — they will be sung as written.

### The mix's rules

1. **Only the reading changes** — no synonyms, no added or removed lines, no reordering, no change to the structure tags.
2. **The canonical lyric stays canonical** — the mix never overwrites it. The two files link to each other.
3. **One at a time** — never paste both into the generator. Keep Style · Vocal · Exclude · duration identical; only the Lyrics field changes.
4. **The title does not move** — the title keeps the work's orthography. If the hook is opened (揺れ方 → 揺れかた), say so, and give the alternative of keeping the title's spelling and accepting the misreading.
5. **Mark the hypothesis** — the mix is untested until generated. The file states which words were opened, which were left, what to listen for (reading · phrasing · melody), and how to choose (one full pass each; if both miss, go all-kana or open the next table).

### What the mix file contains

1. **Source and scope** — which lyric it derives from, and that only the spelling changed.
2. **The hypothesis marker** — "untested", and the assumption about how the generator misreads.
3. **The lyric block** — pasteable, same structure tags.
4. **The opened words** — a table: word → opened form → why (the failure shape).
5. **The words left in kanji** — the boundary stakes, and why each was left.
6. **"If you still hear it"** — the likely misreading → the form to open next.
7. **How to compare** — same settings, one at a time, listening for reading · phrasing · melody.
8. **The weaknesses** — the remaining risk, the cost of kana boundaries, the lost orthography.

## One soul, two doors

The theme song and the package are two doors to the same soul, not different souls. If `package.md` exists, the song's title · chorus · style must be consistent with the package's title · catch copy · synopsis — same promise, same tone, same voice.

## Procedure

1. Read draft.md, premise.md (theme · core question), series-bible.md (disclosure level), persona (voice), and package.md if present.
2. Survey the whole work — theme, structure, the scenes where emotion surfaces, the reveal — and decide which single moment the song sings. A theme song is one moment of the soul, not a plot summary.
3. Draw the song's core line — the one hook that carries the theme without naming it. Everything below derives from it.
4. Write the six deliverables in order: title → lyrics (structure tags) → style of music → vocal → song description → placement & intent.
5. Write the reading-safe mix — open only the words with a real failure shape, keep every other word, line, and tag, and record what was opened, what was left, and the "if you still hear it" table.
6. Check each against the four rules: sing without lying · promise what you deliver · stop before the reveal · restraint carries into the lyric.
7. Check the whole set for "one soul, two doors" — does it open onto the same work as the package?
8. Save `<working-dir>/theme-song.md` and `<working-dir>/theme-song-mix.md`.

## Output

- `<working-dir>/theme-song.md` — the song set (title / lyrics / style of music / vocal / song description / placement & intent), with a one-line pointer to the mix file.
- `<working-dir>/theme-song-mix.md` — the reading-safe mix: the lyric block, the opened words, the words left in kanji, the "if you still hear it" table, the comparison procedure, and the weaknesses. Beside a named variant, name it after that variant (`<source-stem>-mix.md`). If the lyric is already written entirely in kana and no risky word remains, say so in `theme-song.md` and omit this file.

## Notes

- **The ground is the work's soul — the theme and the scene where emotion rises — not the reader's first impression.** Package handles the reader; the song handles the soul.
- **series-bible's disclosure level is the boundary.** The song never sings the reveal or the ending.
- **The lyric is the work's voice in song, not marketing.** It is the work's soul compressed into a few singable lines.
- **Lyrics are in the work's language; the style-of-music tags are English.** The `lang` argument changes only this skill's own prose.
- **A lyric that over-explains has already broken the fifth rule (源を語らない).** The shorter the line, the more restraint it needs.
- **The mix changes sound, not words.** It is a second candidate, not a correction. The canonical lyric is the one in the source file (`theme-song.md`, or the named variant).
- **Open the minimum.** A lyric opened too far loses the word boundaries the generator needs — the misreading risk is traded for a phrasing risk.
- **The title keeps the work's orthography.** Only the lyric's hook may be opened, and the mix file must say so.
