---
name: revise-for-reader
description: A skill that revises the draft from the viewpoint of the reader's experience (immersion, page-turner, keeping the promise, the inducement to reread). Checked against design.md's reader image & promise, it adjusts where the reader's time is grabbed, held, and released. Does not build in sublation (the evaluation layer).
argument-hint: '(optional) the path to draft.md. If omitted, look for draft.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# revise-for-reader — revise by the reader's experience (immersion · page-turner · keeping the promise · rereading)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/revise-for-reader lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `revise-for-reader`
- **version**: `0.1.0`
- **category**: `writing` (revision)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The **revision** skill of the three-layer model. Revises the draft from the viewpoint of the "reader's experience". **Sublation (negation · preservation · elevation) is the mechanism of the evaluation layer (external)**, not built in here (design list §3-C). This skill handles only the revision of the reader's experience (§9).

**Source**: technical catalogue §9 the reader's experience + §15 revision.

## Input Contract

- **draft.md**: `<working-dir>/draft.md` (the object of revision).
- **design.md**: `<working-dir>/design.md` (the reader image & promise = the standard of revision).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (forbidden moves · voice — don't break the voice for the reader's sake).

## Procedure

1. Read draft.md and design.md's "reader image & promise".
2. Inspect from the viewpoint of the reader's experience (§9):
   - **immersion (9-1)**: the power to pull out of reality and into the time of the story
   - **curiosity (9-2)**: the pull of wanting the next
   - **page-turner (9-8)**: the power that won't let the reader put it down at a chapter/scene end
   - **promise and recovery (9-6)**: whether the contract of the opening returns at the end
   - **the inducement to reread (9-9)**: the device that makes the second read a different book
   - **the displacement after reading (9-10)**: the sense that something in life moved after reading
3. For each viewpoint, confirm that the distribution of the reader's time (where to grab · hold · release) matches design.md's promise.
4. Revise (§15): structural revision (15-2) first, then the deletion · movement · addition of scenes (15-3), then the reduction of redundancy (15-5).
5. Keep **the limit of revision (15-10)**: don't over-fix and break it. The judgment to acknowledge completion is the human's (a judgment hard to externalize).
6. Save the revised draft.md.

## Output

The revised `<working-dir>/draft.md`.

## Notes

- Revision is **"raising the reader's experience", not "fixing"**. Sublation (negation · preservation · elevation) is the evaluation layer's mechanism; don't do it here.
- The reader image & promise is **the standard of revision**. Keep the promise while leaving the inducement to reread.
- **The limit of revision** (15-10): the judgment to over-fix and break, or to acknowledge completion, is the human's. The AI goes as far as proposing candidates.
- Don't break the aesthetic of expression and restraint: revision must not add explanation · naming · summary (so that revising for the reader does not become revising that breaks the soul).
