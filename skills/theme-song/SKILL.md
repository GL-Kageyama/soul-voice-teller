---
name: theme-song
description: A delivery skill that condenses a finished work into one theme song — the full song set to hand to Suno or a similar music generator: the song title, structured lyrics, the style of music (genre · tempo · mood · instrumentation), the vocal direction, the song description, and the placement in the story. It is grounded in the whole work (the theme + the scenes where emotion surfaces) and follows the same expression-and-restraint: the lyrics sing the soul without naming it, stop before the reveal, and are written to be sung, not read.
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
- **version**: `0.1.0`
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

## One soul, two doors

The theme song and the package are two doors to the same soul, not different souls. If `package.md` exists, the song's title · chorus · style must be consistent with the package's title · catch copy · synopsis — same promise, same tone, same voice.

## Procedure

1. Read draft.md, premise.md (theme · core question), series-bible.md (disclosure level), persona (voice), and package.md if present.
2. Survey the whole work — theme, structure, the scenes where emotion surfaces, the reveal — and decide which single moment the song sings. A theme song is one moment of the soul, not a plot summary.
3. Draw the song's core line — the one hook that carries the theme without naming it. Everything below derives from it.
4. Write the six deliverables in order: title → lyrics (structure tags) → style of music → vocal → song description → placement & intent.
5. Check each against the four rules: sing without lying · promise what you deliver · stop before the reveal · restraint carries into the lyric.
6. Check the whole set for "one soul, two doors" — does it open onto the same work as the package?
7. Save `<working-dir>/theme-song.md`.

## Output

`<working-dir>/theme-song.md` — the song set (title / lyrics / style of music / vocal / song description / placement & intent).

## Notes

- **The ground is the work's soul — the theme and the scene where emotion rises — not the reader's first impression.** Package handles the reader; the song handles the soul.
- **series-bible's disclosure level is the boundary.** The song never sings the reveal or the ending.
- **The lyric is the work's voice in song, not marketing.** It is the work's soul compressed into a few singable lines.
- **Lyrics are in the work's language; the style-of-music tags are English.** The `lang` argument changes only this skill's own prose.
- **A lyric that over-explains has already broken the fifth rule (源を語らない).** The shorter the line, the more restraint it needs.
