---
name: entertainment
description: A skill that achieves the pleasures of entertainment (hook · page-turner · twist · catharsis · pacing · empathy) without breaking expression and restraint. It builds the grip on the reader, the pull that won't let go, the unexpected turn, and the point of emotional release through the concrete (action · image · sound), not explanation · naming · moral. Turns quiet prose into a book that can't be put down.
argument-hint: '(optional) the path to draft.md. If omitted, find draft.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# entertainment — the pleasures of entertainment, without breaking restraint

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/entertainment lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja`. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `entertainment`
- **version**: `0.1.0`
- **category**: `writing` (revision · entertainment)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The revision skill of the three-layer model. Where revise-for-reader handles **reader experience** (immersion · reread · post-reading displacement), entertainment handles the **pleasures of entertainment** (hook · page-turner · twist · catharsis · pacing · empathy). It adds pleasure **without breaking expression and restraint** (negative space · don't name it · no moral at the ending) — through action · image · sound, not explanation.

**Source**: technical catalogue §9 the reader + §4 structure (the turn · pacing).

## Input Contract

- **draft.md**: `<working-dir>/draft.md` (what to revise).
- **design.md**: `<working-dir>/design.md` (reader image & promise · direction of prose style).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (forbidden moves · voice).

## The six axes of entertainment (the sources of pleasure)

1. **Hook (the grip)** — grab the reader with the opening line. Even under restraint, the opening alone sets "what will happen" strongly.
2. **Page-turner (won't let go)** — leave the pull toward "next" at the end of a chapter. Not only the refrain; leave an unresolved question · an omen.
3. **Twist (the turn)** — betray the expectation. Make the turn of the four acts "surprising, yet inevitable".
4. **Catharsis (the release)** — make a point of emotional release. But through action · image, not a moral.
5. **Pacing (ebb and flow)** — vary length and density. Don't keep every chapter the same tone.
6. **Empathy hook** — lay the protagonist's hunger over the reader's own hunger.

## Procedure

1. Read draft.md and design.md's "reader image & promise".
2. Inspect against the six axes. Find which axis is weak.
3. Fill it **in harmony with restraint**: when adding pleasure, don't add explanation · naming · moral. Add only the concrete (action · image · sound).
4. Catharsis by **action, not summary**: don't write "he was saved"; write one action of the moment of being saved.
5. Pacing by **varying length**: avoid the same tone across chapters; raise the density only of the pivotal one.
6. Save the revised draft.md.

## Output

The revised `<working-dir>/draft.md`.

## Notes

- **Add the pleasures of entertainment, but don't break expression and restraint.** A catharsis written as a moral breaks the soul.
- Add pleasure through the **concrete** (action · image · sound), not explanation.
- **Pacing (ebb and flow)** means not equalizing length. Raise the density only of the pivotal chapter; keep the others short.
- Hook and twist are built by **withholding information**; catharsis and pacing by **the concrete of body and image**.
