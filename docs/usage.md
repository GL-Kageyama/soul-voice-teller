# Usage

How to install the layer and call the skills in order.

## Install

```bash
# install (global / in-project)
./install.sh            # ~/.claude/skills/ (callable from anywhere)
./install.sh --local    # .claude/skills/ (this repo only)
```

## The call sequence

After installing, call the skills in order in Claude Code:

```
/writer-persona        # first draw out the writer's setting (make the five-item persona)
/premise               # pass a seed and ideate
/plot-design           # make the design document (required design + optional preparation)
/fast-draft            # write the draft (introspection loop + the aesthetic of expression and restraint)
/voice-ledger          # store the voice · read it back

# preparation (optional. Before or after plot-design)
/narration-design      # detailed design of narration
/character-forge       # character design
/character-in-action   # making the character act in the scene
/character-bond        # render the relationship between two characters
/worldbuild            # world design
/world-iceberg         # documenting the unwritten world
/research-verify       # checking historical fact · period detail

# the quality of writing · revision · long-term
/prose                 # sharpen by prose style
/scene-writer          # write one scene deeply
/series-bible          # the work's bible · ledger
/revise-for-reader     # revise by the reader's experience
/entertainment         # inspect the draft against the six reaction axes and fill the weak one
/whole-work-review     # review the work as a whole — one book that closes

# delivery
/package               # wrap the finished work for the reader
/theme-song            # condense the finished work into one theme song
```

## Switching the output language

Each skill accepts a `lang` argument (e.g. `/premise lang=ja`) or reads `SOUL_VOICE_TELLER_LANG` to switch the output language (default `en`). To write in Japanese (or Chinese) by default, set it in your shell profile:

```bash
# ~/.zshenv
export SOUL_VOICE_TELLER_LANG=ja   # or zh
```

See the [Language (i18n)](../README.md) section of the README for the full resolution order and the three-layer structure.

## The writer's permanent state (persona / voice-ledger)

`persona.md` ("I write like this" — present) and `voice-ledger.md` ("I have written like this" — past) live in `$SOUL_VOICE_HOME` (see [The writer's permanent state](../README.md#the-writers-permanent-state) in the README).

### voice-ledger's growth and context

`voice-ledger.md` is **not loaded into the session context automatically**. It lives on disk and is read only when a skill asks for it:

- `premise` at ideation (call the previous work's voice into the new question)
- `fast-draft`'s safety valve (when the voice runs dry)
- the `voice-ledger` skill itself

Growth therefore costs context **only at the moment of reading** — not continuously. Reading a ~40 KB ledger costs roughly 10k tokens once; cheap per read, but a full read of a growing file becomes wasteful.

When the ledger grows (roughly past 100 KB), keep a full read cheap:

- **Index at the top** — a one-line pointer per work; read the index, open only the entry you need.
- **Archive separation** — split older works into an archive file so the daily-read file stays small.
