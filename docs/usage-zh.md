# 用法

层的安装方法，以及按顺序调用技能的步骤。

## 安装

```bash
# 安装（全局 / 项目内）
./install.sh            # ~/.claude/skills/（从任何项目可调用）
./install.sh --local    # .claude/skills/（仅本仓库）
```

## 调用顺序

安装后，在 Claude Code 中按顺序调用技能：

```
/writer-persona        # 先引出写作者的设定（做五项 persona）
/premise               # 传入种子并构思
/plot-design           # 做设计书（必需构思＋可选预备）
/fast-draft            # 写草稿（内省循环＋流露与克制的美学）
/voice-ledger          # 存声 · 回读

# 预备（可选。plot-design 之前或之后）
/narration-design      # 叙述的详细设计
/character-forge       # 人物设计
/character-in-action   # 人物在场景中的活用
/worldbuild            # 世界设计
/world-iceberg         # 未写世界的资料化
/research-verify       # 史实 · 时代考据的对照

# 写作质量 · 改稿 · 长期
/prose                 # 以文体打磨
/scene-writer          # 深写一个场景
/series-bible          # 作品圣经 · 账本
/revise-for-reader     # 以读者体验改稿
```

## 切换输出语言

每个技能都接受 `lang` 参数（例如 `/premise lang=ja`）或读取 `SOUL_VOICE_TELLER_LANG` 来切换输出语言（默认 `en`）。要默认以中文（或日文）输出，请在 shell 配置文件中设置环境变量：

```bash
# ~/.zshenv
export SOUL_VOICE_TELLER_LANG=zh   # 或 ja
```

详见 [README](../README-zh.md) 的「语言（i18n）」一节。
