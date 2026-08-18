---
name: plot-design
description: Builds a design document (required design + optional preparation) from premise and persona. Fixes the logline, narration, prose style, scene table, and reader image & promise as the required design, and allows character / world / foreshadowing to be left blank. This is fast-draft's input specification itself. After premise, before fast-draft.
argument-hint: '(optional) the path to premise.md. If omitted, look for premise.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# plot-design — design (build fast-draft's input specification)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/plot-design lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `plot-design`
- **version**: `0.1.0`
- **category**: `writing` (design layer · per work)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The back stage of the **design layer** in the three-layer model. It expands what premise fixed — "what it asks · in what prose · for whom" — into the granularity at which fast-draft can **write**. The design document is fast-draft's **input specification itself**.

## Input Contract

- **premise**: `<working-dir>/premise.md` (required).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (required. Checked so the choice of narration · prose style · reader image does not become "a choice no one made").

## Procedure

1. Read premise and persona.
2. Fix the **required design** (the format below). This exists so that before fast-draft writes a single sentence, "who tells what", "in what prose", and "for whom" are already decided:
   - **logline** — carried over from premise
   - **narration** — point of view (first/second/third person) · tense · narrator (who tells it, and from what distance)
   - **direction of prose style** — the direction of the prose, checked against the persona's voice & brushwork
   - **reaction axis** — carried over from premise (primary · secondary); its four steps become the whole-work arc ([../references/six-response-axes.md](../references/six-response-axes.md))
   - **scene table** — each scene's reaction axis (three kinds) · purpose · who · what changes. **Write undecided items as `?` so "what is undecided" stays visible**
   - **reader image & promise** — carried over from premise, and broken down into the "distribution of the reader's time" per scene (where you grab · hold · release them)
3. **Optional preparation** (character · world · foreshadowing) **may be left blank**. It can be filled in during writing (the plan is a map, not an order). But record "that it is undecided" with `?` so consistency can be checked later.
4. Save the output to `<working-dir>/design.md`.

## Output

`<working-dir>/design.md`

```markdown
# design — the design document

## Required design (what should be fixed before fast-draft writes)

### Logline
(from premise)

### Narration
- point of view: (first / second / third person)
- tense: (present / past)
- narrator: (who · from what distance)

### Direction of prose style
(the direction of this work's prose, checked against the persona's voice)

### The reaction axis
(primary · secondary carried from premise. Its four steps become the whole-work arc — [../references/six-response-axes.md](../references/six-response-axes.md))

### Scene table
| # | scene | reaction axis (three kinds) | purpose (what it achieves) | who | what changes |
|---|---|---|---|---|---|
| 1 | (e.g. on a stormy night, the lighthouse keeper sees the wreck) | (e.g. fear · a chill) | (e.g. raise fear and conflict) | (e.g. the keeper) | (e.g. the prelude to the decision to go to the rescue) |

(undecided cells are `?`)

### Reader image & promise
(who · what experience you promise. Where in each scene you grab · hold · release the reader's time)

## Optional preparation (may be blank · filled in during writing)

### Character
(`?` allowed)

### World
(`?` allowed)

### Foreshadowing
(`?` allowed)
```

## Notes

- **The only fatal flaw is a missing required design.** Without narration (point of view · tense · narrator) · direction of prose style · reader image & promise · scene table, the draft becomes a string of averaged sentences.
- Conversely, **a blank preparation is not fatal**. Missing settings can be decided during writing. But record "undecided" with `?`.
- Particularity is the lever (not density): a single singular image · constraint · decision of voice ("thin particularity") produces more non-average prose than carefully filling in three-act structure and flaw-overcoming ("thick generality").
- **The chosen axis is designed as the whole-work arc.** The primary axis premise selected is laid out as its four steps across the scene table ([../references/six-response-axes.md](../references/six-response-axes.md)). Write, in each scene's "reaction axis (three kinds)" cell, which axis and which of its three kinds that scene fires. **In a long work you may change the axis per scene** — the primary axis carries the whole-work arc, while individual scenes fire other axes (a fear scene, a humor scene, a cute scene) so the reader's response never saturates. In a short work the primary axis's three kinds usually recur scene by scene.
- **The scene table places the hook's chain.** Where you grab · hold · release the reader's time maps to the trunk (whole-work question) and the branches (scene questions) of the hook engine ([../references/hook-engine.md](../references/hook-engine.md)); preserve the trunk's answer to the peak.
