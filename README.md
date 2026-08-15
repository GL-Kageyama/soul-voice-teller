**Language:** English | [日本語](README-ja.md) | [中文](README-zh.md)

# soul-voice-teller

**To carry the soul is the aim; anti-generic is the means.** —— a layer of novel-writing skills.

With 15 skills — the first wave of five (`writer-persona` reflecting the writer's (human's) soul, voice, and preferences, `premise` for ideation, `plot-design` for design, `fast-draft` for the draft, `voice-ledger` for storing the voice), six optional preparations (wave 2), and four for prose style · revision · the ledger (wave 3) — the layer makes "design → draft → revision" hold up on writing skills alone.

> **Division of labor**: this layer is **writing only**. Evaluation (seeing through) a work is borne by the external evaluation layers ([novel-council-layer](../novel-council-layer/) / [wisdom-council-layer](../wisdom-council-layer/) / [elevate-draft-engine](../elevate-draft-engine/)).

## The core proposition

- **To carry the soul is the aim, anti-generic is the means.** Non-averageness (particularity) is a means, not the aim.
- **The human is the author, the AI is a drafting device, the persona is a mirror of the human's preferences.**
- **Introspection is "checking against", not "fabrication".** Introspection without a ground (what it is checked against) is not observation.
- **The aesthetic of restraint is the master lever of the soul**: don't explain emotion · don't name it · don't summarize · leave space.

## The three-layer model

```
writer layer (permanent)   writer-persona ──→ the soul-story · voice · forbidden moves · aesthetic sense (checked against real experience)
                           voice-ledger ──→ store the heard voice, read it back
design layer (per work)    premise → plot-design ──→ the required design (the design document)
execution layer            fast-draft ──→ rough prose (detect departure by introspection · deliver by the aesthetic of restraint)
external (evaluation layer) evaluation · sublation ──→ material for redrafting
```

## The 15 skills (wave 1〜3)

| skill | role | input → output |
|---|---|---|
| `writer-persona` | draw out the writer's setting in dialogue (A questions · ground = real experience) | dialogue → `${SOUL_VOICE_HOME}/persona.md` (soul-story / aesthetic sense / voice & brushwork / forbidden moves / subject-matter preference) |
| `premise` | ideation (B questions · ground = persona + store) | seed + persona + store → `<work>/premise.md` (logline / core question / theme / genre promise / direction of prose style / reader image & promise) |
| `plot-design` | the design document (fast-draft's input specification) | premise + persona → `<work>/design.md` (required design + optional preparation) |
| `fast-draft` | the draft (the aesthetic of restraint + the introspection loop) | design + persona + store → `<work>/draft_*.md` + plan update + voices for the store |
| `voice-ledger` | store the voice, read it back | the voice (ideation / draft / flow / forbidden moves / resonance of evaluation) → `${SOUL_VOICE_HOME}/voice-ledger.md` |

**Wave 2 (optional preparation)** — called optionally from plot-design. Writing works even with blanks

| skill | role | input → output |
|---|---|---|
| `narration-design` | detailed design of narration (type of point of view · reliability · distance · tense · nesting · speech style) | design → the elaboration of design.md's "narration" |
| `character-forge` | character design (desire · wound · voice · change arc · inner conflict) | design + premise + persona → the elaboration of design.md's "character" |
| `character-in-action` | make the character setting function in the scene (staged disclosure · making the setting function) | design → append linkage points to the scene table |
| `worldbuild` | world design (setting · rules · internal consistency · the setting ⇔ story connection) | design + premise + persona → the elaboration of design.md's "world" |
| `world-iceberg` | the extent to document the unwritten world (by touching probability) | design → append the documentation list |
| `research-verify` | checking historical fact · period detail · specialist knowledge (keep errors out) | design/draft → a list of errors + corrections |

**Wave 3 (the quality of writing · revision · long-term)**

| skill | role | input → output |
|---|---|---|
| `prose` | sharpen by prose style (rhythm · sense · an irreplaceable voice) | prose/scene + persona → rewritten prose |
| `scene-writer` | write one scene deeply (the design of empty space · show, don't tell · the seams of the scene) | design + persona → draft_<n>_<scene>.md |
| `series-bible` | the work's bible (a ledger that centrally manages setting · foreshadowing · serialization) | the work's artifacts → series-bible.md |
| `revise-for-reader` | revise by the reader's experience (immersion · page-turner · promise · rereading) | draft + design → the revised draft.md |

## Usage

```bash
# install (global / in-project)
./install.sh            # ~/.claude/skills/ (callable from anywhere)
./install.sh --local    # .claude/skills/ (this repo only)
```

After installing, call the skills in order in Claude Code:

```
/writer-persona        # first draw out the writer's setting (make the five-item persona)
/premise               # pass a seed and ideate
/plot-design           # make the design document (required design + optional preparation)
/fast-draft            # write the draft (introspection loop + the aesthetic of restraint)
/voice-ledger          # store the voice · read it back

# preparation (wave 2 · optional. Before or after plot-design)
/narration-design      # detailed design of narration
/character-forge       # character design
/character-in-action   # making the character act in the scene
/worldbuild            # world design
/world-iceberg         # documenting the unwritten world
/research-verify       # checking historical fact · period detail

# the quality of writing · revision · long-term (wave 3)
/prose                 # sharpen by prose style
/scene-writer          # write one scene deeply
/series-bible          # the work's bible · ledger
/revise-for-reader     # revise by the reader's experience
```

Each skill accepts a `lang` argument (e.g. `/premise lang=ja`) or reads `SOUL_VOICE_TELLER_LANG` to switch the output language (default `en`). See **Language** below.

## The writer's permanent state

- `${SOUL_VOICE_HOME}/persona.md` —— "I write like this" (present tense · portrait). Made by writer-persona
- `${SOUL_VOICE_HOME}/voice-ledger.md` —— "I have written like this" (past tense · diary). Accumulated by voice-ledger
- The location is a **dedicated folder (private git repository)** the user makes inside their workspace, pointed to by the `SOUL_VOICE_HOME` environment variable (if unset, `~/.soul-voice-teller/`). writer-persona's first step is to prompt this folder's creation

> **persona / voice-ledger are per-writer state, not included in the repository (not fixed)** — because many different people use it. There is no default persona the skills refer to. The persona in `examples/sample/` is a demo sample, not the skills' default.

## Repository layout

- `skills/{name}/SKILL.md` — the 15 skills (en canonical) + `SKILL-ja.md` / `SKILL-zh.md` per language
- `references/` — the operational principles (introspection · restraint · voice-store, en canonical; `references/ja/`, `references/zh/` mirrors)
- `docs/` — a place to put anything generic (evidence · rationale · design notes)
- `locales/` — display strings (`en` canonical, `ja` / `zh` mirror)
- `examples/<work>/` — the artifacts per work
- `install.sh` — symlink install (global / local / uninstall)

## Language (i18n)

Three languages — **en / ja / zh** — in the three-layer structure:

1. **Locale JSON** — `locales/{en,ja,zh}.json` (display strings)
2. **Language-specific prompts** — `skills/{name}/SKILL-{lang}.md` + `references/{lang}/*.md`
3. **Mirror tree** — `README-{lang}.md` / `CLAUDE-{lang}.md`

Language resolution: the `lang` argument > the `SOUL_VOICE_TELLER_LANG` environment variable > **en** (default). An unsupported language warns and falls back to `en`.

To write in Japanese (or Chinese) by default, set it in your shell profile:

```bash
# ~/.zshenv
export SOUL_VOICE_TELLER_LANG=ja   # or zh
```

The **source concepts (内省 / 余白 / 間)** are Japanese, and are re-derived — not translated word-for-word — into English (introspection / negative space / restraint) and Chinese (内省 / 留白 / 含蓄). The prose-family skills (`prose` / `scene-writer` / `revise-for-reader`) are re-implemented in each language's prose tradition.

## License

MIT ([LICENSE](LICENSE))
