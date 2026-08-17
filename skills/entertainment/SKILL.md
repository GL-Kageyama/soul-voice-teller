---
name: entertainment
description: A revision skill that inspects the draft against the six reaction axes (感嘆 · ユーモア · 感動 · 楽しい · 恐怖 · かわいい) and fills the weak axis without breaking expression and restraint. The former structural pleasures (hook · page-turner · twist · catharsis · pacing · empathy) are reclassified as the engine (interest), the ingredients (exceed · identification), and the structure (release · flow). Adds pleasure through the concrete (action · image · sound), not explanation · naming · moral.
argument-hint: '(optional) the path to draft.md. If omitted, find draft.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# entertainment — the reactions, without breaking restraint

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/entertainment lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja`. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `entertainment`
- **version**: `0.2.0`
- **category**: `writing` (revision · entertainment)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The revision skill of the three-layer model. Where revise-for-reader handles **reader experience** (immersion · reread · post-reading displacement), entertainment handles the **reactions** — the six response axes that move the reader's heart. It fills the weak axis **without breaking expression and restraint** (negative space · don't name it · no moral at the ending) — through action · image · sound, not explanation.

**Source**: [references/six-response-axes.md](../references/six-response-axes.md) · technical catalogue §9 the reader + §4 structure.

## The six response axes

The draft is inspected against the **six reaction axes** — the six routes to "面白い (interesting)". The full table (mechanism × failure mode), the axis test, and the four steps / three kinds live in [references/six-response-axes.md](../references/six-response-axes.md).

| axis | reaction | mechanism (正体) |
|---|---|---|
| 感嘆 (admiration) | a groan — "I've been had" | exceed prediction × make it feel inevitable |
| ユーモア (humor) | a laugh | gap (ズレ) × safe recovery |
| 感動 (emotion) | tears, a tight chest | identification × confirmation of a value |
| 楽しい (fun) | pleasant, exhilarating | positive emotion × flow |
| 恐怖 (fear) | on edge, cold sweat | a threat shown × no escape |
| かわいい (cuteness) | "precious", protective | protectiveness × lovability |

**The former "six axes" (hook · page-turner · twist · catharsis · pacing · empathy) are not lost — they are reclassified.** Hook and page-turner are the **engine (interest)**; twist is the *exceed* ingredient of 感嘆; the empathy hook is the *identification* ingredient of 感動; catharsis is the *structure of release*; pacing is the *flow* of 楽しい. They stay as the concrete moves below.

## Procedure

1. Read draft.md and design.md's "reader image & promise".
2. Confirm the axis the premise's promise (約束) selected — the axis the work rides.
3. Inspect against the six axes. Find which axis is weak.
4. Fill it **through its four steps** (the whole-work arc) and **three kinds** (the scene arc), in harmony with restraint — add only the concrete (action · image · sound).
5. Catharsis by **action, not summary**: don't write "he was saved"; write one action of the moment of being saved.
6. Save the revised draft.md.

## Output

The revised `<working-dir>/draft.md`.

## Notes

- **Fill the weak axis, but don't break expression and restraint.** A release written as a moral breaks the soul.
- Add the reaction through the **concrete** (action · image · sound), not explanation.
- **The engine (interest) runs across all six axes.** Hook and twist are built by **withholding information**; the release and the flow by **the concrete of body and image**.
