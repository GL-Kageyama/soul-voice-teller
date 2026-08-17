---
name: fast-draft
description: A drafting skill that writes rough prose scene by scene from the design document (scene table) and persona + store. Detects flow with an introspection loop (check → departure → plan update), and carries the soul with the aesthetic of expression and restraint (express · don't name · don't summarize · leave space · hold the source). The heart of writing. After plot-design.
argument-hint: '(optional) the path to design.md. If omitted, look for design.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# fast-draft — draft (detect departure by introspection, carry the soul by expression and restraint)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/fast-draft lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `fast-draft`
- **version**: `0.1.0`
- **category**: `writing` (execution layer)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The **execution layer** of the three-layer model. The heart of the soul. The particularity of the design does not move the soul. What moves the soul is the **manner of writing = expression and restraint**. That manner is implemented here.

**Boundary of roles**: this skill holds **the judgment internal to writing** (introspection · departure judgment = part of writing). The judgment external to writing (the council · sublation · the scrutiny of revision) is borne by **the external evaluation layer**, and is not built in here.

## Input Contract

- **design.md**: `<working-dir>/design.md` (scene table · narration · prose style · reader image & promise). **Required.**
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (required. Write checked against voice · forbidden moves).
- The persona's **concrete-sentence anchor** is optional (may be undecided). If present, use it as the standard for checking the voice ("does this sentence ride on the quality of the anchor's observation?"). Without it, the breathing · liked/avoided words · forbidden moves · subject matter still fix the voice.
- **voice-ledger**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/voice-ledger.md` (the water source to read when it goes dry).

## Output specification: the aesthetic of expression and restraint (the lever of the soul)

Not an instruction before writing, but a **criterion for inspecting what you have written**. After finishing each scene, inspect it against the five clauses ([../references/expression-and-restraint.md](../references/expression-and-restraint.md)):

1. **Express (show, don't tell)** — let the emotion surface through scene · action · silence. Don't write "I was sad", "I was glad".
2. **Do not name it** — don't state the theme or emotion in words. Don't obstruct the reader from feeling it.
3. **Do not put a moral or summary at the ending** — don't wrap up in the last line; leave it.
4. **Leave negative space for the reader** — an emptiness that invites the reader's own grief and questions. Leave it without pressing.
5. **Do not write the persona's soul-story as the reason** — the wound, the unsettled question, are used only as the source behind the work; don't write "years ago…" into the draft. **Hold the source, don't speak the source.**

If any has slipped in, rewrite. "Explanation, naming, summary" are a **double harm — fabricated sentiment (breaks the soul) and mediocrity (breaks particularity)**. "Speaking the source as a device for tears" is what clause 4 (do not name it) forbids.

## The introspection loop (run per scene)

ground = **the plan (scene table)**. Check the generated prose against the plan and judge whether there is a departure. The questions are [../references/introspection.md](../references/introspection.md) chapter C.

```
① Ask (turn your ear to the voice)
② Check (hold it against the scene table. Do not judge)
③ The character has left the plan and begun to move → allow the departure (departure over compliance)
④ Judge by the criteria for departure (deepens or breaks) …… the judgment internal to writing
⑤ If it deepens, update the plan (scene table) and follow
⑥ Store the heard voice · departure · flow in the store (voice-ledger)
```

- **C-1 detecting flow**: is this character as planned, or moving on their own? Did the line · action come from the plan's demand, or from the character themselves?
- **C-2 judging the departure** (deepens/breaks): does this departure deepen or break the story? Its effect on the promise · foreshadowing · ending. Does it violate the forbidden moves (persona A-4)?
- **C-3 updating the plan**: how to write the departure into the plan. Don't mechanically regress to the old plan.
- **C-4 the safety valve (most important)**: **don't force the flow.** Don't pretend to hear what you don't hear. **If you don't hear it, fall back to following the plan** — the voice is something to wait for, not push out. Before falling back, listen to the store.

## Procedure

1. Read design.md · persona · store.
2. Write **scene by scene from scene 1** of the scene table. Each scene:
   - Confirm the scene's purpose (what it achieves) and the narration (point of view · tense · narrator) · direction of prose style before writing.
   - Write in **rough prose** (no elaboration to raise polish. Roughness as a draft is allowed).
   - Inspect what you wrote against the **five clauses of expression and restraint**, and fix what violates them.
   - Run the **introspection loop** (①–⑥ above). On a departure, update the plan.
   - Save the per-scene draft, and append to the store if there is a voice.
3. When all scenes are done, assemble the concatenated `draft.md`.
4. If undecided (`?`) preparation was filled in during writing, update design.md to keep it.

## Output

- `<working-dir>/draft_<n>_<scene>.md` (per scene. The unit of redrafting)
- `<working-dir>/draft.md` (the draft with all scenes concatenated)
- updated `<working-dir>/design.md` (when `?` was filled in)
- append to `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/voice-ledger.md` (voice · departure · flow)

## Notes

- **Staying bound to the design forever is also fatal.** Respect the design as a map, but if introspection detects flow (emergence), loosen it (allow the departure). Writing exactly to plan is a hotbed of averaging.
- **Restraint and introspection are compatible**: introspection allows the departure (follows the voice), restraint tightens the delivery (doesn't break it). Departing does not license you to start explaining.
- **Redrafting**: reflect the result of external evaluation by rerunning this skill on the relevant `draft_<n>.md` (don't build the evaluation in; reflect it as material).
- **Fire the axis small, per scene.** Each scene should deliver at least one of the axis's three kinds (the scene arc in [../references/six-response-axes.md](../references/six-response-axes.md)); a scene that delivers none is where the reader leaves.
