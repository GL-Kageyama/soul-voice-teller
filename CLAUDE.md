**Language:** English | [日本語](CLAUDE-ja.md) | [中文](CLAUDE-zh.md)

# soul-voice-teller

## Project Identity

This is a layer of **novel-writing skills**. It is composed of 21 skills: the five (`writer-persona` reflecting the writer's (human's) soul, voice, and preferences, `premise` for ideation, `plot-design` for design, `fast-draft` for the first draft, `voice-ledger` for storing the voice), `steady-draft` for the everyday writing (the next episode, or fleshing out / expanding an episode), plus seven optional preparations (`narration-design` / `character-forge` / `character-in-action` / `character-bond` / `worldbuild` / `world-iceberg` / `research-verify`), the quality-of-writing · revision · long-term skills (`prose` / `scene-writer` / `series-bible` / `revise-for-reader` / `entertainment` / `whole-work-review`), and the delivery skills `package` (wrapping the finished work for the reader) and `theme-song` (condensing it into one theme song).

## The core proposition (placed at the top)

**To write is to carry the soul.**

- Avoiding "average prose that belongs to no one" (particularity) is **not the aim**. Moving the reader's heart and leaving something in memory (the soul) is the aim; particularity is one **means** toward it.
- This inversion is proven ([docs/実証.md](docs/実証.md)).

## The three-layer model

```
writer layer (permanent)   writer-persona ──→ soul-story · voice · forbidden moves · aesthetic sense (heard by introspection = checked against real experience)
                           voice-ledger ──→ store the heard voice, read it back (ideation · escaping a stall · updating persona)
design layer (per work)    premise → plot-design ──→ the required design (the design document, revised against the promise + voice; for a serialized work, broken into chapters and episodes)
                           preparation (optional) narration-design / character-forge / character-in-action / character-bond / worldbuild / world-iceberg / research-verify
execution layer            fast-draft ──→ rough prose (detect departure by introspection and update the plan · deliver by the aesthetic of expression and restraint)
                           steady-draft ──→ the next episode of an ongoing work (grounded in persona + design + ledger; write back to the ledger)
                           quality of writing prose / scene-writer ／ revision revise-for-reader / entertainment / whole-work-review ／ long-term series-bible ／ delivery package / theme-song
```

The operation that runs through all three layers is **introspection** (hearing the voice). Introspection is "**checking against**" — observation against a ground.

## The five grounds of introspection (what it is checked against)

| question layer | ground (what it is checked against) |
|---|---|
| A the writer's setting (writer-persona) | **the writer's real experience** — the works this writer has written, the questions they actually carry, the forbidden moves. The AI asks the human and holds the answers. **The AI does not fabricate its own "wound"** |
| B ideation (premise) | **persona + the store** — voice · aesthetic sense (HOW) are checked, subject matter (WHAT) may waver (pulling too close makes every work the same) |
| C design (plot-design) | **premise (the promise · the reaction axis · the core question) + persona (voice · aesthetic sense · forbidden moves)** — the design is checked against the promise and the voice, and revised |
| D the draft loop (fast-draft) | **the plan (scene table)** — the generated prose is checked against the plan to judge whether there is a departure |
| E the everyday draft (steady-draft) | **persona + the design (構想) + the ledger (台帳) + the previous drafts** — the next episode is checked against the accumulated record, and what changed is written back |

**Introspection without a ground is not observation.** Mark the ground in every question; a question without a ground is not called "introspection" ([references/introspection.md](references/introspection.md)).

## The aesthetic of expression and restraint (the master lever of the soul)

- What moves the soul is not the particularity of the design, but **the manner of writing = expression and restraint**.
- Built into fast-draft as its **output specification**: let the emotion surface through scene and act, then don't explain it · don't name it · don't put a moral or summary at the ending · leave space for the reader ([references/expression-and-restraint.md](references/expression-and-restraint.md)).
- But restraint needs a **source** for "what it restrains". The source is SOURCE (checking = the writer's real experience). Restraint (MANNER) is necessary, not sufficient.

## Who writes (the framing · fixed first)

**The human is the author, the AI is a drafting device, the persona is a mirror of the author.**

- The persona's soul and voice are **the human's (user's)**. The AI is a mirror that draws them out, holds them, and reflects them in dialogue — not the author.
- This makes the introspection of the A/B questions "checking", not "fabrication".

## Directory Conventions

- `skills/{name}/SKILL.md` — each skill's canonical source (21). All callable independently. `SKILL-ja.md` / `SKILL-zh.md` are the per-language mirrors
- `.claude/skills/` — symlinks for in-project discovery (`./install.sh --local`)
- `~/.claude/skills/` — the global install target (`./install.sh`, callable from anywhere)
- `.claude-plugin/` — the plugin distribution definition
- `references/` — the operational principles the skills cite (en canonical: introspection · expression and restraint · six response axes · hook engine · voice-store; `references/ja/` · `references/zh/` mirrors)
- `docs/` — a place to put anything generic (evidence · rationale · design notes. Separated from the rules themselves)
- `locales/` — i18n display strings (`en` canonical; `ja` / `zh` mirror)
- `examples/<work>/` — the artifacts per work (premise.md / design.md / draft_*.md)
- The writer's permanent state lives in a **dedicated folder (a local folder is fine; a git repository is recommended)** the user makes inside their workspace: `persona.md` (I write like this = present tense) and `voice-ledger.md` (I have written like this = past tense). Pointed to by `SOUL_VOICE_HOME` (falling back to `~/.soul-voice-teller/` if unset). writer-persona's first step is to prompt this folder's creation. **It is per-writer state, not included in the soul-voice-teller repository (not fixed)** — because many different people use it. There is no default persona the skills refer to; always read the one in `SOUL_VOICE_HOME`.

## The judgment internal to writing vs external evaluation (the distinction)

| kind | example | the layer it belongs to |
|---|---|---|
| **the judgment internal to writing** (part of writing) | introspection · departure judgment (deepens/breaks) · detecting flow | **writing skills** (held by fast-draft / steady-draft / plot-design) |
| **external evaluation** (judgment on what is written) | the council · sublation (negation/preservation/elevation) · revision | **the evaluation layer** (external) |

"Don't build in the evaluation mechanism" means "don't build in the **external** evaluation mechanism". The **noticing** of a departure is allowed to fast-draft, steady-draft, and plot-design as part of introspection. What should be handed off is the **scrutiny · sublation** of a departure, not the noticing of it.

## Language (i18n)

Three languages — **en / ja / zh** — in the three-layer structure, **en-canonical**.

1. **Locale JSON** — `locales/{en,ja,zh}.json`
2. **Language-specific prompts** — `skills/{name}/SKILL-{lang}.md` + `references/{lang}/*.md`
3. **Mirror tree** — `README-{lang}.md` / `CLAUDE-{lang}.md`

Language resolution: the `lang` argument > the `SOUL_VOICE_TELLER_LANG` environment variable > **en** (default). An unsupported language warns and falls back to `en`.

The **source concepts (内省 / 余白 / 間)** are Japanese, re-derived — not translated word-for-word — into English (introspection / negative space / restraint) and Chinese (内省 / 留白 / 含蓄). The prose-family skills (`prose` / `scene-writer` / `revise-for-reader`) are re-implemented in each language's prose tradition.

### i18n baseline (fixed policy)

en/ja/zh multi-language support is the default for all changes from now on. New or changed skill bodies, references, and templates are resolved through the three-layer mechanism (`SKILL-{lang}.md` / locale JSON / the mirror tree), and user-facing text is output in the resolved language.

## What not to build (explicit exclusions)

- Evaluation loops · sublation — borne by the external layers. Not built in.
- Proofreading · grammar checks, genre templates, a Python engine · subagents (this layer is skill-type).

## Evidence

What the lever of the soul is — the results of each experiment (E1/E4 · E5 · E2 · E2b) and the remaining main fortress (SOURCE) — are gathered in [docs/実証.md](docs/実証.md).
