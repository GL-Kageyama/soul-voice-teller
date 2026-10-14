---
name: entertainment
description: A revision skill that inspects the draft against the six reaction axes (感嘆 · ユーモア · 感動 · 楽しい · 恐怖 · かわいい) and fills the weak axis without breaking expression and restraint. The former structural pleasures (hook · page-turner · twist · catharsis · pacing · empathy) are reclassified as the engine (interest), the ingredients (exceed · identification), and the structure (release · flow). Adds pleasure through the concrete (action · image · sound), not explanation · naming · moral. When the draft's vessel itself forbids the axis (a rule · a record · a design decision, not the prose), a radical revision is permitted — replacing the vessel, the cast size, the dialogue density, the notes — provided the part the design record named as not-to-be-moved stays unmoved and still countable.
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
- **version**: `0.3.0`
- **category**: `writing` (revision · entertainment)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The revision skill of the three-layer model. Where revise-for-reader handles **reader experience** (immersion · reread · post-reading displacement), entertainment handles the **reactions** — the six response axes that move the reader's heart. It fills the weak axis **without breaking expression and restraint** (negative space · don't name it · no moral at the ending) — through action · image · sound, not explanation.

**That is the move when the vessel permits the axis. When it does not, the permitted move is larger.** If the axis is not weak in the prose but *forbidden by the vessel* — the line structure, a rule of the work, the size of the cast — then the revision may be **radical**: replace the vessel, add people to existing seats, grow the dialogue, cut the 註 the work carries about itself. What holds it safe is not surface restraint but **checkability**: the part the work's own design record named as 動かさないもの, and the viewpoint character's 内面, must not move — and staying unmoved has to be countable ([references/entertainment-revision.md](../references/entertainment-revision.md)).

**Source**: [references/six-response-axes.md](../references/six-response-axes.md) · [references/hook-engine.md](../references/hook-engine.md) · [references/entertainment-revision.md](../references/entertainment-revision.md) · technical catalogue §9 the reader + §4 structure.

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

**The former "six axes" (hook · page-turner · twist · catharsis · pacing · empathy) are not lost — they are reclassified.** Hook and page-turner are the **engine (interest)** — expanded in [references/hook-engine.md](../references/hook-engine.md) (未知 × 知りたさ · give → break · the four axes of the chain); twist is the *exceed* ingredient of 感嘆; the empathy hook is the *identification* ingredient of 感動; catharsis is the *structure of release*; pacing is the *flow* of 楽しい. They stay as the concrete moves below.

## Procedure

1. Read draft.md and design.md's "reader image & promise".
2. Confirm the axis the premise's promise (約束) selected — the axis the work rides.
3. **Check the vessel, before the prose.** Measure whether this vessel can carry that axis at all. If the measurement says it **cannot** — the axis is not weak, it is forbidden — read [references/entertainment-revision.md](../references/entertainment-revision.md) and follow its §1 (the four conditions for a radical revision) and §4 (the seven checks).
4. Inspect against the six axes. Find which axis is weak.
5. Fill it **through its four steps** (the whole-work arc) and **three kinds** (the scene arc), in harmony with restraint — add only the concrete (action · image · sound).
6. Catharsis by **action, not summary**: don't write "he was saved"; write one action of the moment of being saved.
7. Save the revised draft.md.

## Output

The revised `<working-dir>/draft.md`.

## Notes

- **Fill the weak axis, but don't break expression and restraint.** A release written as a moral breaks the soul.
- Add the reaction through the **concrete** (action · image · sound), not explanation.
- **The engine (interest) runs across all six axes** ([../references/hook-engine.md](../references/hook-engine.md)). Hook and twist are built by **withholding information**; the release and the flow by **the concrete of body and image**.

## When the vessel forbids the axis

The six axes assume the axis *can* land and only needs filling. Often it cannot, and the reason is measurable: in `habits`, humor landed in **1 scene out of 189**, because a checker forbade adding a sentence inside a line — a gap (ズレ) needs **two beats** ("build a prediction, then break it"), and that vessel could strike one.

**So the first question is not "which axis is weak" but "can this vessel strike two beats at all".** When it cannot, the permitted revision is **radical** — the vessel (line and sentence structure) · the size of the cast · the density of dialogue · the 註 (the notes the work carries about itself) — and **humor goes into the second beat, never into the voice.** What keeps it safe is not surface restraint but **checkability**: the record named as 動かさないもの and the viewpoint character's 内面 must not move, and that has to be countable.

The eleven principles · the eight steps · the seven checks · the seven failure modes are in [references/entertainment-revision.md](../references/entertainment-revision.md).
