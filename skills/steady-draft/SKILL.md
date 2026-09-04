---
name: steady-draft
description: A writing skill for the everyday work: writes the next episode of an ongoing work — or fleshes out / expands an existing episode — naturally grounded in persona + the design (構想) + the ledger (台帳) + the previous drafts. After the first draft (fast-draft), this continues a serialized work one episode at a time and thickens a thin 話. Shares the introspection loop and the aesthetic of expression and restraint with fast-draft, and writes back to the ledger (foreshadowing payoff · serialization progress · prose-style drift · settings). The home base of the execution layer, next to fast-draft.
argument-hint: '(optional) the path to the work directory. If omitted, look for the design / ledger / drafts in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# steady-draft — everyday writing (continue the work, grounded in design + ledger + persona)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/steady-draft lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `steady-draft`
- **version**: `0.1.0`
- **category**: `writing` (execution layer)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The **execution layer** of the three-layer model, standing **next to fast-draft**. `fast-draft` writes the *first* draft — all scenes at once, straight after `plot-design`, checked against `design.md` (the scene table) alone. `steady-draft` writes the *next* episode of an **ongoing work** — one 話 at a time, checked against the **accumulated ground**: persona + the design (構想) + the ledger (台帳) + the previous drafts.

This is the everyday writing mode — the one you are in most of the time once a work is underway. No ceremony of premise → plot-design; you already have everything, you just write the next bit. Two uses: **write the next episode** (continue), and **flesh out / expand an episode** (make a thin 話 richer).

| command | scope | ground (checked against) |
|---|---|---|
| `fast-draft` | the first draft, all scenes at once | `design.md` (scene table) |
| **`steady-draft`** | **the next episode of an ongoing work** | **persona + 構想 + 台帳 + previous drafts** |
| `scene-writer` | one dramatic scene, deep | `design.md` + persona |

**Boundary of roles**: same as fast-draft — this skill holds **the judgment internal to writing** (introspection · departure judgment · recording what changed). The judgment external to writing (the council · sublation · the scrutiny of revision) is borne by **the external evaluation layer**, and is not built in here.

## Input Contract

- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (required. Write checked against voice · forbidden moves · aesthetic sense).
- **the design (構想)**: the per-work design set — `premise.md` · `design.md` · `章立て.md` (chapter breakdown) · `話割り.md` (episode allocation) · `characters.md` · `world.md` · `foreshadowing.md` · `narration-design.md` · `research-verify.md`. **Required.**
- **the ledger (台帳)**: the accumulated record — `series-bible.md` · `設定.md` (settings) · `文体.md` (prose style) · `伏線.md` (foreshadowing) · `連載.md` (serialization). **Required** — this is what makes steady-draft richer than fast-draft: the ground includes what has *accumulated*.
- **previous drafts**: `草稿/draft_XX-Y_話名.md` (what is already written). **Required** — to continue, not repeat. Read the immediately preceding episode(s) to pick up the thread (register · situation · the seam of the scene).
- **voice-ledger**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/voice-ledger.md` (the water source to read when it goes dry).

## The ground (what introspection is checked against)

fast-draft's ground is the plan (scene table) alone. steady-draft's ground is the **accumulated record**:

- **文体 (prose style)** — keep point of view · tense · narrator · the aesthetic of expression and restraint · the forbidden moves consistent with the record.
- **伏線 (foreshadowing)** — what has been planted must keep coming; plant what this episode should plant; don't contradict the payoff table.
- **連載 + 章立て (serialization + chapter breakdown)** — this chapter's reaction axis and required event; the episode's self-containment and its pull to the next.
- **話割り (episode allocation)** — what *this* episode must contain (its 区分け).
- **persona** — voice · forbidden moves · aesthetic sense.

Introspection without a ground is not observation. Here the ground is **台帳 + 構想 + persona**.

## Fleshing out / expanding a 話 (肉付け)

To lengthen or thicken a 話, **do not add explanation · naming · summary** — they break the soul and the particularity. Add only **concrete particulars: body · action · object · sound**. One concrete particular carries more negative space than one line of explanation. Lengthening = adding particulars, not explanation. Don't fill the negative space.

## Output specification: the aesthetic of expression and restraint (shared with fast-draft)

Identical to fast-draft. After finishing the episode, inspect it against the five clauses ([../references/expression-and-restraint.md](../references/expression-and-restraint.md)):

1. **Express (show, don't tell)** — let the emotion surface through scene · action · silence.
2. **Do not name it** — don't state the theme or emotion in words.
3. **Do not put a moral or summary at the ending** — don't wrap up in the last line; leave it.
4. **Leave negative space for the reader** — an emptiness that invites the reader's own grief and questions.
5. **Do not write the persona's soul-story as the reason** — hold the source, don't speak the source.

If any has slipped in, rewrite.

## The introspection loop (run per episode)

ground = **台帳 + 構想 + persona**. The questions are [../references/introspection.md](../references/introspection.md) chapter D.

```
① Ask (turn your ear to the voice)
② Check (hold it against the ledger + design + persona. Do not judge)
③ The character has left the plan and begun to move → allow the departure (departure over compliance)
④ Judge by the criteria for departure (deepens or breaks) …… the judgment internal to writing
⑤ If it deepens, update — the design or the ledger as appropriate — and follow
⑥ Store the heard voice · departure · flow in the store (voice-ledger)
```

- **D-1 detecting flow**: is this character as planned, or moving on their own? Did the line · action come from the plan's demand, or from the character themselves?
- **D-2 judging the departure** (deepens/breaks): its effect on the promise · foreshadowing · ending. Does it violate the forbidden moves (persona A-4)?
- **D-3 updating**: on a departure, write it back into the **ledger or the design** (not just the scene table — the accumulated record). Don't mechanically regress.
- **D-4 the safety valve (most important)**: **don't force the flow.** Don't pretend to hear what you don't hear. If you don't hear it, fall back to following the plan. Before falling back, listen to the store.

## Procedure

1. **Determine what to write.** Either the **next episode** — read `話割り.md` (the episode table) + `連載.md` (progress) + the existing `草稿/` files, find the first episode not yet written — or an **existing episode to flesh out / expand** (a thin `draft_XX-Y_話名.md`). If ambiguous, ask the user.
2. **Read the ground.** persona + 構想 + 台帳 + the immediately preceding draft(s).
3. **Write the 話** (about 2,000 characters per the serialization convention) — new, or expanded from an existing thin draft by adding concrete particulars (肉付け). Before writing, confirm from 文体 (point of view · tense · narrator), 伏線 (what must keep coming), 連載 + 章立て (this chapter's reaction axis · required event), 話割り (this episode's 区分け), and persona (voice · forbidden moves).
4. **Inspect** against the five clauses of expression and restraint, and fix what violates them.
5. **Run the introspection loop** (①–⑥). On a departure, update the design or the ledger.
6. **Save** `draft_XX-Y_話名.md`, and **write back to the ledger**:
   - 伏線 — mark payoffs as 回収, add newly planted ones.
   - 連載 — record the progress (which 話 is done) and the next promise.
   - 文体 — record any style drift (e.g. a planned whitening, a new register).
   - 設定 — add new named things / world facts.
   - Append to the store if a voice was heard.

## Output

- `<work-dir>/草稿/draft_XX-Y_話名.md` (one episode)
- updated `<work-dir>/台帳/*` (伏線 · 連載 · 文体 · 設定)
- append to `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/voice-ledger.md` (voice · departure · flow)

## Notes

- **This is the everyday mode.** Don't redo premise → plot-design. You already have the design and the record; just write the next bit.
- **Writing back to the ledger is recording, not evaluation.** Record what changed (payoff · progress · drift · new settings); don't judge the draft. The scrutiny of the draft is borne by the external evaluation layer.
- **Continue, don't repeat.** Read the preceding episode(s) to pick up the register and the seam of the scene. Don't re-establish what is already established.
- **Each episode self-contains and pulls forward.** Each 話 has a small arc (起承転結) and ends with a pull to the next. Fire the axis small per episode ([../references/six-response-axes.md](../references/six-response-axes.md)), and fire the hook small per episode ([../references/hook-engine.md](../references/hook-engine.md)) — same as fast-draft.
- **The ledger is alive.** Settings and style may shift as you write; write the shift back, don't leave the record stale.
