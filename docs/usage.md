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
/fast-draft            # write the draft (introspection loop + the aesthetic of restraint)
/voice-ledger          # store the voice · read it back

# preparation (optional. Before or after plot-design)
/narration-design      # detailed design of narration
/character-forge       # character design
/character-in-action   # making the character act in the scene
/worldbuild            # world design
/world-iceberg         # documenting the unwritten world
/research-verify       # checking historical fact · period detail

# the quality of writing · revision · long-term
/prose                 # sharpen by prose style
/scene-writer          # write one scene deeply
/series-bible          # the work's bible · ledger
/revise-for-reader     # revise by the reader's experience
```

## Switching the output language

Each skill accepts a `lang` argument (e.g. `/premise lang=ja`) or reads `SOUL_VOICE_TELLER_LANG` to switch the output language (default `en`). To write in Japanese (or Chinese) by default, set it in your shell profile:

```bash
# ~/.zshenv
export SOUL_VOICE_TELLER_LANG=ja   # or zh
```

See the [Language (i18n)](../README.md) section of the README for the full resolution order and the three-layer structure.
