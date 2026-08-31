---
name: plot-design
description: Builds a design document (required design + optional preparation) from premise and persona, and revises it against the promise + voice through a design loop (check → drift → revise). Fixes the logline, narration, prose style, scene table, and reader image & promise as the required design; for a serialized work, it also breaks the arc into chapters and episodes (what happens in each episode). Allows character / world / foreshadowing to be left blank. This is fast-draft's input specification itself. After premise, before fast-draft.
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
- **voice-ledger**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/voice-ledger.md` (read when the design loop asks for the voice; the water source).

## Procedure

1. Read premise, persona, and the store.
2. Fix the **required design** (the format below). This exists so that before fast-draft writes a single sentence, "who tells what", "in what prose", and "for whom" are already decided:
   - **logline** — carried over from premise
   - **narration** — point of view (first/second/third person) · tense · narrator (who tells it, and from what distance)
   - **direction of prose style** — the direction of the prose, checked against the persona's voice & brushwork
   - **reaction axis** — carried over from premise (primary · secondary); its four steps become the whole-work arc ([../references/six-response-axes.md](../references/six-response-axes.md))
   - **chapter breakdown (章立て)** — for a serialized/long work, expand the whole-work arc into chapters; each chapter is one unit of the arc (its reaction axis · the events that must happen · trunk/branch hook · what changes). A short work omits this.
   - **episode breakdown (話割り)** — for a serialized/long work, subdivide each chapter into posting units (one episode ≈ 2,000 chars); each episode is self-contained (its own small arc) and ends with a pull into the next. A short work omits this.
   - **scene table** — each scene's reaction axis (three kinds) · purpose · who · what changes. **Write undecided items as `?` so "what is undecided" stays visible**
   - **reader image & promise** — carried over from premise, and broken down into the "distribution of the reader's time" per scene (where you grab · hold · release them)
3. **Run the design loop** (chapter C of [../references/introspection.md](../references/introspection.md)). After a first pass, check the design against the ground — **premise (the promise · the reaction axis · the core question/trunk) + persona (voice · aesthetic sense · forbidden moves)** — and revise. Compare each choice (narration · prose direction · which axis a scene fires) against the voice — not by sublation — and discard "anyone could write" choices. On a departure, judge whether it deepens (update premise) or breaks (revise the design). On a day nothing is heard, fall back to the one-shot design.
4. **Optional preparation** (character · world · foreshadowing) **may be left blank**. It can be filled in during writing (the plan is a map, not an order). But record "that it is undecided" with `?` so consistency can be checked later. If a hidden role exists, record it here as a foreshadowing map so "who is really what" is decided before fast-draft — but it may also be filled during writing (`?`).
5. Save the output to `<working-dir>/design.md`, and append any heard voice to the store.

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

### Chapter breakdown (章立て · serialized/long works only; a short work omits this)
Each chapter = one unit of the whole-work arc. Break the arc into chapters, fixing per chapter the reaction axis · the events that must happen · the trunk/branch hook · what changes.

| chapter | reaction axis (three kinds) | the events that must happen | trunk / branch (hook) | what changes |
|---|---|---|---|---|
| 1 (title) | (e.g. emotion · a soft ache) | (e.g. …) | trunk "…" (preserve) / branch "…" | (e.g. …) |

### Episode breakdown (話割り · serialized/long works only; a short work omits this)
Subdivide each chapter into posting units (one episode ≈ 2,000 chars; one draft file per episode). Each episode is **self-contained** — its own small arc (setup · development · turn · resolution) plus an **ending pull** (a cut or question that is the promise of the next episode) — so it reads even alone.

| chapter | episode | title | what happens (ending with the pull into the next) |
|---|---|---|---|
| 1 | 1-1 | (e.g. The Sign) | (e.g. …) |

### Scene table
| # | scene | reaction axis (three kinds) | purpose (what it achieves) | who | what changes |
|---|---|---|---|---|---|
| 1 | (e.g. on a stormy night, the lighthouse keeper sees the wreck) | (e.g. fear · a chill) | (e.g. raise fear and conflict) | (e.g. the keeper) | (e.g. the prelude to the decision to go to the rescue) |

(undecided cells are `?`)

### Reader image & promise
(who · what experience you promise. Where in each scene you grab · hold · release the reader's time)

## Optional preparation (may be blank · filled in during writing)

### Character
(`?` allowed. When a character has a role, add a "Role" subheading — stake / challenge (adversary named × the adversary's resistance in stages — the active verb belongs to the character, never the adversary) / agency (the rule, with risk-taking as its core). The function is fixed by plot-design. See character-forge. *Consistency (らしさ)* is not a field — it is verified at the scene level by character-in-action.)

### World
(`?` allowed)

### Foreshadowing
(`?` allowed. When a character hides a role, this takes the form of a "foreshadowing map" — surface role → hidden role, who it's hidden from (reader / other characters), the trunk question, the disclosure (turning point), the foreshadowing list (scene · clue · disclosure degree · disclosure curve · recollection), and the 4-axis check. See character-forge / character-in-action.)
```

## Notes

- **The only fatal flaw is a missing required design.** Without narration (point of view · tense · narrator) · direction of prose style · reader image & promise · scene table, the draft becomes a string of averaged sentences.
- Conversely, **a blank preparation is not fatal**. Missing settings can be decided during writing. But record "undecided" with `?`.
- Particularity is the lever (not density): a single singular image · constraint · decision of voice ("thin particularity") produces more non-average prose than carefully filling in three-act structure and flaw-overcoming ("thick generality").
- **The chosen axis is designed as the whole-work arc.** The primary axis premise selected is laid out as its four steps across the scene table ([../references/six-response-axes.md](../references/six-response-axes.md)). Write, in each scene's "reaction axis (three kinds)" cell, which axis and which of its three kinds that scene fires. **In a long work you may change the axis per scene** — the primary axis carries the whole-work arc, while individual scenes fire other axes (a fear scene, a humor scene, a cute scene) so the reader's response never saturates. In a short work the primary axis's three kinds usually recur scene by scene.
- **The scene table places the hook's chain.** Where you grab · hold · release the reader's time maps to the trunk (whole-work question) and the branches (scene questions) of the hook engine ([../references/hook-engine.md](../references/hook-engine.md)); preserve the trunk's answer to the peak.
- **The serialized skeleton is chapter → episode → scene.** For a serialized/long work, the arc breaks into chapters (arc units), each chapter into episodes (posting units), each episode into scenes (the scene table). A chapter carries one beat of the arc; an episode is self-contained and ends with a pull; a scene is where fast-draft actually writes. The chapter/episode breakdown is **required for serialized works** and **omitted for short works** — determine which from premise (its scale and reader promise); if premise is silent, ask the user.
- **The design loop is internal judgment, not evaluation.** Revising the design against the promise + voice (the loop) is part of writing — the same category as fast-draft's departure judgment. The *scrutiny · sublation* of the design is handed off to the external evaluation layer, and is not built in here.
