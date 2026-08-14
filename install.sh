#!/usr/bin/env bash
#
# soul-voice-teller installer
#
# Installs the 15 writing skills to Claude Code discovery locations so they are
# available by name.
#
# Usage:
#   ./install.sh            # Global: ~/.claude/skills/ (callable from any project)
#   ./install.sh --local    # Project: .claude/skills/ (this repo only)
#   ./install.sh --uninstall
#
# Installation uses symlinks: the canonical source stays in ./skills/, so edits
# to the repo are reflected immediately.
#
# Note: soul-voice-teller has no subagents — the skills are the writing layer's
# runbooks. The 内省 (introspection) is the writer's own self-reflection, not an
# independent evaluator, so no agents/ directory is needed.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"

MODE="global"
ACTION="install"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --local)    MODE="local" ;;
    --global)   MODE="global" ;;
    --uninstall) ACTION="uninstall" ;;
    -h|--help)
      echo "Usage: ./install.sh [--local|--global] [--uninstall]"
      echo ""
      echo "  --local      Install to .claude/ (this project only)"
      echo "  --global     Install to ~/.claude/ (default; callable from anywhere)"
      echo "  --uninstall  Remove the installed skills (default: global target)"
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

if [[ "$MODE" == "local" ]]; then
  TARGET_SKILLS_DIR="$REPO_DIR/.claude/skills"
else
  TARGET_SKILLS_DIR="$HOME/.claude/skills"
fi

if [[ "$ACTION" == "uninstall" ]]; then
  echo "==> Uninstalling soul-voice-teller skills from:"
  echo "    $TARGET_SKILLS_DIR"
  removed=0
  for skill_dir in "$SKILLS_DIR"/*/; do
    name="$(basename "$skill_dir")"
    if [[ -L "$TARGET_SKILLS_DIR/$name" || -e "$TARGET_SKILLS_DIR/$name" ]]; then
      rm -rf "$TARGET_SKILLS_DIR/$name"
      echo "    ✓ removed skill $name"
      removed=$((removed+1))
    fi
  done
  echo "==> Removed $removed component(s)."
  exit 0
fi

echo "==> Installing soul-voice-teller to:"
echo "    skills: $TARGET_SKILLS_DIR"
mkdir -p "$TARGET_SKILLS_DIR"

installed=0

for skill_dir in "$SKILLS_DIR"/*/; do
  name="$(basename "$skill_dir")"
  target="$TARGET_SKILLS_DIR/$name"
  rm -rf "$target"          # remove any previous install (symlink or file)
  ln -s "$skill_dir" "$target"
  installed=$((installed+1))
  echo "    ✓ skill $name"
done

# Verify every symlink resolves to a readable SKILL.md
failures=0
for target in "$TARGET_SKILLS_DIR"/*/; do
  if [[ -f "$target/SKILL.md" ]]; then
    :
  else
    echo "    ✗ broken: $target"
    failures=$((failures+1))
  fi
done

echo ""
if [[ $failures -gt 0 ]]; then
  echo "==> $installed installed, $failures broken symlink(s). Check $SKILLS_DIR."
  exit 1
fi

echo "==> Done: $installed skills installed."
echo ""
echo "    Callable as follows:"
echo "      /writer-persona    # 書き手設定を引き出す（persona を作る）"
echo "      /premise           # 発想（ログライン・テーマ・読者像と約束）"
echo "      /plot-design       # 設計書（必須構想＋任意下準備）"
echo "      /fast-draft        # 草稿（内省ループ＋抑制の美学）"
echo "      /voice-ledger      # 声をためる・読み返す"
echo ""
echo "    下準備（第2弾・任意）:"
echo "      /narration-design    # 語りの詳細設計"
echo "      /character-forge     # 人物設計"
echo "      /character-in-action # 人物の場面での活かし方"
echo "      /worldbuild          # 世界設計"
echo "      /world-iceberg       # 未描の世界の資料化"
echo "      /research-verify     # 史実・時代考証の照合"
echo "    書く質・改稿・長期（第3弾）:"
echo "      /prose             # 文体で研ぐ"
echo "      /scene-writer      # 1場面を深く書く"
echo "      /series-bible      # 作品聖典・台帳"
echo "      /revise-for-reader # 読者体験で改稿"
echo ""
echo "    Note: restart Claude Code or run /skills once to reload the listing."
