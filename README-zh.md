**Language:** [English](README.md) | [日本語](README-ja.md) | 中文

# soul-voice-teller

**以承载灵魂为目的，反套路（anti-generic）是手段。**—— 小说写作技能的一层。

由 15 个技能构成——第一波五个（`writer-persona` 映照写作者（人）的灵魂、声音与偏好，`premise` 构思，`plot-design` 设计，`fast-draft` 草稿，`voice-ledger` 存声），六个可选预备（第二波），以及文体 · 改稿 · 账本的四个（第三波）——让「设计 → 草稿 → 改稿」仅凭写作技能即可成立。

> **分工**：本层**只负责写作**。对作品的评价（看穿）由外部的评价层承担（[novel-council-layer](../novel-council-layer/) / [wisdom-council-layer](../wisdom-council-layer/) / [elevate-draft-engine](../elevate-draft-engine/)）。

## 核心主张

- **以承载灵魂为目的，反套路（anti-generic）是手段。**非平均（个别性）是手段，不是目的。
- **人是作者，AI 是草稿装置，persona 是人偏好的镜子。**
- **内省是「对照」，不是「捏造」。**没有依据（对照对象）的内省，不是观察。
- **克制的美学是灵魂的主杠杆**：不解释情感 · 不点名 · 不总结 · 留白。

## 三层模型

```
写作者层（持久）    writer-persona ──→ 灵魂故事 · 声音 · 禁忌 · 审美（对照人的真实经验）
                   voice-ledger ──→ 存下听到的声音，再回读
构思层（每部作品）  premise → plot-design ──→ 必需的构思（设计书）
执行层             fast-draft ──→ 粗稿（以内省察觉偏离 · 以克制的美学送达）
外部（评价层）      评价 · 扬弃 ──→ 改稿的素材
```

## 15 个技能（第一～三波）

| 技能 | 职责 | 输入 → 输出 |
|---|---|---|
| `writer-persona` | 用对谈引出写作者的设定（A 问句 · 依据 = 人的真实经验） | 对谈 → `${SOUL_VOICE_HOME}/persona.md`（灵魂故事 / 审美 / 声音与笔触 / 禁忌 / 题材偏好） |
| `premise` | 构思（B 问句 · 依据 = persona＋声音库） | 种子＋persona＋声音库 → `<作品>/premise.md`（一句话梗概 / 核心问句 / 主题 / 体裁的约定 / 文体的方向 / 读者形象与约定） |
| `plot-design` | 设计书（fast-draft 的输入规格） | premise＋persona → `<作品>/design.md`（必需构思＋可选预备） |
| `fast-draft` | 草稿（克制的美学＋内省循环） | 设计＋persona＋声音库 → `<作品>/draft_*.md`＋计划更新＋供声音库存的声音 |
| `voice-ledger` | 存声、回读 | 声音（构思 / 草稿 / 文思 / 禁忌 / 评价的回响） → `${SOUL_VOICE_HOME}/voice-ledger.md` |

**第二波（可选预备）**—— 从 plot-design 按需调用。留空也能写

| 技能 | 职责 | 输入 → 输出 |
|---|---|---|
| `narration-design` | 叙述的详细设计（视角类型 · 可靠度 · 距离 · 时态 · 嵌套 · 语体） | 设计 → design.md 的「叙述」细化 |
| `character-forge` | 人物设计（欲望 · 伤口 · 声音 · 变化弧 · 内在冲突） | 设计＋premise＋persona → design.md 的「人物」细化 |
| `character-in-action` | 让人物设定在场景中生效（分阶段披露 · 让设定动起来） | 设计 → 向场景表追加联动点 |
| `worldbuild` | 世界设计（舞台 · 规则 · 内在一致 · 设定⇔故事的连接） | 设计＋premise＋persona → design.md 的「世界」细化 |
| `world-iceberg` | 未写世界的资料化程度（按触及概率） | 设计 → 追加资料清单 |
| `research-verify` | 史实 · 时代考据 · 专业知识的对照（排除错误） | 设计/草稿 → 错误＋订正清单 |

**第三波（写作质量 · 改稿 · 长期）**

| 技能 | 职责 | 输入 → 输出 |
|---|---|---|
| `prose` | 以文体打磨（节奏 · 语感 · 无可替代的声音） | 文/场景＋persona → 重写后的文字 |
| `scene-writer` | 深写一个场景（留白的设计 · 见而示之 · 场景的接缝） | 设计＋persona → draft_<n>_<scene>.md |
| `series-bible` | 作品圣经（集中管理设定 · 伏笔 · 连载的账本） | 作品的产物 → series-bible.md |
| `revise-for-reader` | 以读者体验改稿（沉浸 · 翻页感 · 约定 · 重读） | 草稿＋设计 → 改稿后的 draft.md |

## 用法

```bash
# 安装（全局 / 项目内）
./install.sh            # ~/.claude/skills/（从任何项目可调用）
./install.sh --local    # .claude/skills/（仅本仓库）
```

安装后，在 Claude Code 中按顺序调用技能：

```
/writer-persona        # 先引出写作者的设定（做五项 persona）
/premise               # 传入种子并构思
/plot-design           # 做设计书（必需构思＋可选预备）
/fast-draft            # 写草稿（内省循环＋克制的美学）
/voice-ledger          # 存声 · 回读

# 预备（第二波 · 可选。plot-design 之前或之后）
/narration-design      # 叙述的详细设计
/character-forge       # 人物设计
/character-in-action   # 人物在场景中的活用
/worldbuild            # 世界设计
/world-iceberg         # 未写世界的资料化
/research-verify       # 史实 · 时代考据的对照

# 写作质量 · 改稿 · 长期（第三波）
/prose                 # 以文体打磨
/scene-writer          # 深写一个场景
/series-bible          # 作品圣经 · 账本
/revise-for-reader     # 以读者体验改稿
```

每个技能都接受 `lang` 参数（例如 `/premise lang=ja`）或读取 `SOUL_VOICE_TELLER_LANG` 来切换输出语言（默认 `en`）。详见下文 **语言**。

## 写作者的持久状态

- `${SOUL_VOICE_HOME}/persona.md` ——「我这样写」（现在式 · 肖像）。由 writer-persona 制作
- `${SOUL_VOICE_HOME}/voice-ledger.md` ——「我这样写过」（过去式 · 日记）。由 voice-ledger 累积
- 位置是用户在**工作区**内另设的**专用文件夹（私有 git 仓库）**，以 `SOUL_VOICE_HOME` 环境变量指向（未设定则 `~/.soul-voice-teller/`）。writer-persona 的第一步就是促成这个文件夹的创建

> **persona / voice-ledger 是每位写作者的状态，不纳入仓库（不固定）**——因为会有许多不同的人使用它。技能并不引用任何默认 persona。`examples/sample/` 里的 persona 是演示样例，不是技能的默认值。

## 仓库布局

- `skills/{name}/SKILL.md` —— 15 个技能（en 正典）＋各语言的 `SKILL-ja.md` / `SKILL-zh.md`
- `references/` —— 运用原理（内省 · 克制 · 声音库，en 正典；`references/ja/`、`references/zh/` 镜像）
- `docs/` —— 放通用之物的地方（实证 · 理由 · 设计笔记）
- `locales/` —— 显示字符串（`en` 正典，`ja` / `zh` 镜像）
- `examples/<作品>/` —— 每部作品的产物
- `install.sh` —— 符号链接安装（全局 / 本地 / 卸载）

## 语言（i18n）

三种语言——**en / ja / zh**——以三层结构实现：

1. **本地化 JSON** —— `locales/{en,ja,zh}.json`（显示字符串）
2. **语言别提示词** —— `skills/{name}/SKILL-{lang}.md` ＋ `references/{lang}/*.md`
3. **镜像树** —— `README-{lang}.md` / `CLAUDE-{lang}.md`

语言解析顺序：`lang` 参数 ＞ `SOUL_VOICE_TELLER_LANG` 环境变量 ＞ **en**（默认）。不支持的语言会警告并回退到 `en`。

**源概念（内省 / 余白 / 間）**是日语，被重新导出——不是逐字翻译——为英语（introspection / negative space / restraint）与中文（内省 / 留白 / 含蓄）。散文系技能（`prose` / `scene-writer` / `revise-for-reader`）以各语言的散文传统重新实现。

## 许可

MIT（[LICENSE](LICENSE)）
