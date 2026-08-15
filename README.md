**Language:** English | [日本語](README-ja.md) | [中文](README-zh.md)

# soul-voice-teller

<p align="center">
  <img src="assets/repo-hero.png" width="100%" alt="soul-voice-teller">
</p>

**To write is to carry the soul.** —— a layer of novel-writing skills.

With 15 skills — five (`writer-persona` reflecting the writer's (human's) soul, voice, and preferences, `premise` for ideation, `plot-design` for design, `fast-draft` for the draft, `voice-ledger` for storing the voice), six optional preparations, and four for prose style · revision · the ledger — the layer makes "design → draft → revision" hold up on writing skills alone.

> **Division of labor**: this layer is **writing only**. Evaluation (seeing through) a work is borne by the external evaluation layers ([novel-council-layer](../novel-council-layer/) / [wisdom-council-layer](../wisdom-council-layer/) / [elevate-draft-engine](../elevate-draft-engine/)).

## The core proposition

- **To write is to carry the soul.**
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

## Documentation

- [Usage](docs/usage.md) — install and the call sequence, switching the output language
- [The 15 skills](docs/skills.md) — the reference of what each skill does (input → output)
- [実証](docs/実証.md) — the empirical evidence behind the design (Japanese)

## The writer's permanent state

- `${SOUL_VOICE_HOME}/persona.md` —— "I write like this" (present tense · portrait). Made by writer-persona
- `${SOUL_VOICE_HOME}/voice-ledger.md` —— "I have written like this" (past tense · diary). Accumulated by voice-ledger
- The location is a **dedicated folder (private git repository)** the user makes inside their workspace, pointed to by the `SOUL_VOICE_HOME` environment variable (if unset, `~/.soul-voice-teller/`). writer-persona's first step is to prompt this folder's creation

> **persona / voice-ledger are per-writer state, not included in the repository (not fixed)** — because many different people use it. There is no default persona the skills refer to. The persona in `examples/sample/` is a demo sample, not the skills' default.

## Repository layout

- `skills/{name}/SKILL.md` — the 15 skills (en canonical) + `SKILL-ja.md` / `SKILL-zh.md` per language
- `references/` — the operational principles (introspection · restraint · voice-store, en canonical; `references/ja/`, `references/zh/` mirrors)
- `docs/` — usage & the skill reference ([usage.md](docs/usage.md) / [skills.md](docs/skills.md)) plus anything generic (evidence · rationale · design notes)
- `locales/` — display strings (`en` canonical, `ja` / `zh` mirror)
- `examples/<work>/` — the artifacts per work
- `install.sh` — symlink install (global / local / uninstall)

## Language (i18n)

Three languages — **en / ja / zh** — in the three-layer structure:

1. **Locale JSON** — `locales/{en,ja,zh}.json` (display strings)
2. **Language-specific prompts** — `skills/{name}/SKILL-{lang}.md` + `references/{lang}/*.md`
3. **Mirror tree** — `README-{lang}.md` / `CLAUDE-{lang}.md`

Language resolution: the `lang` argument > the `SOUL_VOICE_TELLER_LANG` environment variable > **en** (default). An unsupported language warns and falls back to `en`. To write in Japanese (or Chinese) by default, see [Usage](docs/usage.md).

The **source concepts (内省 / 余白 / 間)** are Japanese, and are re-derived — not translated word-for-word — into English (introspection / negative space / restraint) and Chinese (内省 / 留白 / 含蓄). The prose-family skills (`prose` / `scene-writer` / `revise-for-reader`) are re-implemented in each language's prose tradition.

## License

MIT ([LICENSE](LICENSE))
