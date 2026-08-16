**Language:** [English](CLAUDE.md) | [日本語](CLAUDE-ja.md) | 中文

# soul-voice-teller

## 项目定位

这是**小说写作技能**的一层。由 18 个技能构成：五个（`writer-persona` 映照写作者（人）的灵魂、声音与偏好，`premise` 构思，`plot-design` 设计，`fast-draft` 草稿，`voice-ledger` 存声），加上七个可选预备（`narration-design` / `character-forge` / `character-in-action` / `character-bond` / `worldbuild` / `world-iceberg` / `research-verify`）以及写作质量 · 改稿 · 长期技能（`prose` / `scene-writer` / `series-bible` / `revise-for-reader` / `entertainment` / `whole-work-review`）。

## 核心主张（置于最前）

**写作，是承载灵魂。**

- 避开「谁都不是的平均文字」（个别性）**不是目的**。打动读者的心、在记忆中留下些什么（灵魂）才是目的；个别性只是通向它的**手段**之一。
- 这一反转已被实证（[docs/実証.md](docs/実証.md)）。

## 三层模型

```
写作者层（持久）    writer-persona ──→ 灵魂故事 · 声音 · 禁忌 · 审美（以内省＝对照人的真实经验而听到）
                   voice-ledger ──→ 存下听到的声音，再回读（构思 · 挣脱停滞 · 更新 persona）
构思层（每部作品）  premise → plot-design ──→ 必需的构思（设计书）
                   预备（可选） narration-design / character-forge / character-in-action / character-bond / worldbuild / world-iceberg / research-verify
执行层             fast-draft ──→ 粗稿（以内省察觉偏离并更新计划 · 以流露与克制的美学送达）
                   写作质量 prose / scene-writer ／ 改稿 revise-for-reader / entertainment / whole-work-review ／ 长期 series-bible
```

贯穿三层的运作是**内省**（听见声音）。内省是「**对照**」——对照对象（ground）上的观察。

## 内省的三个依据（对照对象）

| 问句层 | 依据（对照对象） |
|---|---|
| A 写作者的设定（writer-persona） | **写作者的真实经验**——这位写作者写过的作品、实际背负的问句、禁忌。AI 问人并持有答案。**AI 不自造「伤口」** |
| B 构思（premise） | **persona＋声音库**——声音 · 审美（HOW）对照，题材（WHAT）容许摇晃（拉得过近则每部作品相同） |
| C 草稿循环（fast-draft） | **计划（场景表）**——把生成的文字与计划对照，判断是否有偏离 |

**没有依据（ground）的内省，不成其为观察。**每个问句都要标明依据；没有依据的问句不叫「内省」（[references/introspection.md](references/introspection.md)）。

## 流露与克制的美学（灵魂的主杠杆）

- 打动灵魂的不是构想的个别性，而是**写作的方式＝流露与克制**。
- 作为 fast-draft 的**输出规格**内置：让情感在情景·行为中流露，然后不解释情感 · 不点名 · 结尾不落教训或总结 · 为读者留白（[references/expression-and-restraint.md](references/expression-and-restraint.md)）。
- 但克制需要「克制什么」的**源**。源是 SOURCE（对照＝写作者的真实经验）。克制（MANNER）是必要条件，不是充分条件。

## 谁来写（框架 · 最先固定）

**人是作者，AI 是草稿装置，persona 是作者的镜子。**

- persona 的灵魂与声音是**人（用户）的**。AI 是在对谈中引出 · 持有 · 反照它的镜子——不是作者。
- 正因如此，A/B 问句的内省才成为「对照」，而非「捏造」。

## 目录约定

- `skills/{name}/SKILL.md` —— 各技能的正典源（18 个）。均可独立调用。`SKILL-ja.md` / `SKILL-zh.md` 是各语言镜像
- `.claude/skills/` —— 项目内发现的符号链接（`./install.sh --local`）
- `~/.claude/skills/` —— 全局安装目标（`./install.sh`，从任何地方可调用）
- `.claude-plugin/` —— 插件分发定义
- `references/` —— 技能引用的运用原理（en 正典：内省 · 流露与克制 · 声音库；`references/ja/` · `references/zh/` 镜像）
- `docs/` —— 放通用之物的地方（实证 · 理由 · 设计笔记。与规则本身分离）
- `locales/` —— i18n 显示字符串（`en` 正典；`ja` / `zh` 镜像）
- `examples/<作品>/` —— 每部作品的产物（premise.md / design.md / draft_*.md）
- 写作者的持久状态放在用户在**工作区**内另设的**专用文件夹（本地文件夹即可，推荐 git 仓库）**：`persona.md`（我这样写＝现在式）与 `voice-ledger.md`（我这样写过＝过去式）。由 `SOUL_VOICE_HOME` 指向（未设定则回退到 `~/.soul-voice-teller/`）。writer-persona 的第一步就是促成这个文件夹的创建。**它是每位写作者的状态，不纳入 soul-voice-teller 仓库（不固定）**——因为会有许多不同的人使用它。技能不引用任何默认 persona；始终读取 `SOUL_VOICE_HOME` 中的那个。

## 写作内部判断与外部评价（区分）

| 种类 | 例 | 所属层 |
|---|---|---|
| **写作内部判断**（写作的一部分） | 内省 · 偏离判定（深化/破坏）· 察觉文思 | **写作技能**（由 fast-draft 承担） |
| **外部评价**（对写就之物的判断） | 评议会 · 扬弃（否定/保存/更高化）· 改稿 | **评价层**（外部） |

「不内建评价机制」是指「不内建**外部**评价机制」。偏离的**察觉**作为内省的一部分允许交给 fast-draft。应移交的是偏离的**审视 · 扬弃**，而不是它的察觉。

## 语言（i18n）

三种语言——**en / ja / zh**——以三层结构实现，**en 正典**。

1. **本地化 JSON** —— `locales/{en,ja,zh}.json`
2. **语言别提示词** —— `skills/{name}/SKILL-{lang}.md` ＋ `references/{lang}/*.md`
3. **镜像树** —— `README-{lang}.md` / `CLAUDE-{lang}.md`

语言解析顺序：`lang` 参数 ＞ `SOUL_VOICE_TELLER_LANG` 环境变量 ＞ **en**（默认）。不支持的语言会警告并回退到 `en`。

**源概念（内省 / 余白 / 間）**是日语，被重新导出——不是逐字翻译——为英语（introspection / negative space / restraint）与中文（内省 / 留白 / 含蓄）。散文系技能（`prose` / `scene-writer` / `revise-for-reader`）以各语言的散文传统重新实现。

### i18n 基线（固定方针）

en/ja/zh 多语言支持是此后所有变更的默认。新增或变更的技能正文、references、模板都经三层机制（`SKILL-{lang}.md` / 本地化 JSON / 镜像树）解析，面向用户的文本以解析出的语言输出。

## 不做什么（明示排除）

- 评价循环 · 扬弃——由外部层承担。不内建。
- 校对 · 语法检查、体裁模板、Python 引擎 · 子代理（本层是技能型）。

## 实证

灵魂的杠杆是什么——各实验（E1/E4 · E5 · E2 · E2b）的结果与剩下的主堡垒（SOURCE）——汇总在 [docs/実証.md](docs/実証.md)。
