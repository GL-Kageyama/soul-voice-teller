---
name: package
description: A skill that wraps a finished work for the reader — the title and hooking subtitle, the catch copy (obi), the synopsis (back-cover and web lengths), the image-generation prompt, and tags/keywords. It reopens premise.md's reader image & promise and, for the first time, writes to the reader: each wrapper must hook without lying, promise what the work delivers, stop before the reveal, and carry the same restraint as the prose. The work's soul is sent ahead into the reader's first line.
argument-hint: '(optional) the path to draft.md. If omitted, find draft.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# package — wrap the finished work for the reader

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/package lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja`. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `package`
- **version**: `0.1.0`
- **category**: `delivery` (届ける · packaging)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The **delivery** skill — the terminal hand-off of the three-layer model. Where writing (fast-draft) and revision (prose / scene-writer / revise-for-reader / entertainment / whole-work-review) carry the soul **into** the work, package wraps the finished work so the reader can **receive** it. Its ground is not the writer's real experience or the plan — it is **the reader's first impression**, held in premise.md's reader image & promise.

**Source**: premise (読者像と約束) + the aesthetic of expression and restraint (源を語らない).

## Input Contract

- **draft.md**: `<working-dir>/draft.md` (the finished work — what to wrap).
- **premise.md**: `<working-dir>/premise.md` (the reader image & promise · the logline — the ground: does the wrapper reach this reader).
- **series-bible.md**: `<working-dir>/series-bible.md` (the foreshadowing table · the disclosure level — what must not be spoiled).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (voice · forbidden moves — the wrapper speaks in the work's voice).

## The ground shift

Writing's introspection checks against the writer's real experience / persona / the plan. Packaging checks against a different ground: **the reader's first impression** — the reader image & promise fixed at premise. Every wrapper (title · catch copy · synopsis · image) is asked one question against that reader: *does this make them pick it up and open it — without lying, without spoiling, without over-explaining?*

## The five deliverables

1. **Title + subtitle** — the main title (the work's name) + a hooking subtitle (the premise hook). The subtitle hooks; it does not replace the name.
2. **Catch copy (＝ the obi)** — the one line that opens the door. Short, drawn from the logline, in the work's voice.
3. **Synopsis** — two lengths: back-cover (short) and web (medium, for serialization platforms). Sets up the world, the twist, the key characters — and stops before the reveal.
4. **Image-generation prompt** — the cover + one key scene, in concrete visual terms (setting · character · color · light · composition · style), so the illustration is the work's face, not a generic cover.
5. **Tags / keywords** — the address where the target reader finds it (genre + the work's own distinguishing terms).

## The four rules of the wrapper

1. **Hook without lying** — the hook comes from the work's actual premise (the logline), not a genre promise the work betrays. Don't slap a trending genre's label on a work that is not that genre.
2. **Promise what you deliver** — the synopsis sets up what the work actually does. A wrapper that promises the genre's spectacle for a quiet story is a broken promise.
3. **Stop before the reveal** — the wrapper honors the work's staged disclosure (series-bible's foreshadowing table). It goes up to the setup, never past the reveal.
4. **Restraint carries over** — the wrapper obeys the same expression-and-restraint: don't explain the theme, don't name the emotion, leave the reader's negative space even in the catch copy. A catch copy that explains "this is a story about X" has already named it.

## One soul, many doors

Title / catch copy / synopsis / image are different doors to the same soul, not different souls. They must open onto the same work — consistent in promise, tone, and voice.

## Procedure

1. Read draft.md, premise.md (reader image & promise · logline), series-bible.md (disclosure level), persona (voice).
2. Reopen the reader image. The ground of every wrapper is this reader's first impression.
3. Draw the logline — the one sentence that is the work's hook. Everything below derives from it.
4. Write the five deliverables in order: title + subtitle → catch copy → synopsis (two lengths) → image prompt → tags.
5. Check each against the four rules: hook without lying · promise what you deliver · stop before the reveal · restraint carries over.
6. Check the whole set for "one soul, many doors" — do they all open onto the same work?
7. Save `<working-dir>/package.md`.

## Output

`<working-dir>/package.md` — the packaging set (title + subtitle / catch copy / synopsis ×2 / image prompt / tags).

## Notes

- **The ground is the reader's first impression, not the writer's experience.** This is the one place writing turns outward — from "did I carry my soul" to "can the reader receive it".
- **premise.md's reader image & promise is the ground.** Without it, "does this hook" is a guess, not an observation.
- **The wrapper is the first line of the work.** It is not marketing separate from the work — it sends the work's soul ahead, before the reader opens a single page.
- **Restraint does not end at the last page.** A catch copy that over-explains has already broken the fifth rule (源を語らない).
