**Language:** [English](README.md) | [日本語](README-ja.md) | 中文

# soul-voice-teller

<p align="center">
  <img src="assets/repo-hero.png" width="100%" alt="soul-voice-teller">
</p>

**写作，是承载灵魂。**—— 小说写作技能的一层。

由 21 个技能构成——五个（`writer-persona` 映照写作者（人）的灵魂、声音与偏好，`premise` 构思，`plot-design` 设计，`fast-draft` 草稿，`voice-ledger` 存声），续写的 `steady-draft`，七个可选预备，文体 · 改稿 · 账本的六个，以及送达的两个——让「设计 → 草稿 → 改稿 → 送达」仅凭写作技能即可成立。

## 核心主张

- **写作，是承载灵魂。**
- **人是作者，AI 是草稿装置，persona 是作者的镜子。**
- **内省是「对照」——对照对象（ground）上的观察。**
- **流露与克制的美学是灵魂的主杠杆。**

## 三层模型

```
写作者层（持久）    writer-persona ──→ 灵魂故事 · 声音 · 禁忌 · 审美（对照人的真实经验）
                   voice-ledger ──→ 存下听到的声音，再回读
构思层（每部作品）  premise → plot-design ──→ 必需的构思（设计书）
执行层             fast-draft ──→ 粗稿（以内省察觉偏离 · 以流露与克制的美学送达）
                   steady-draft ──→ 进行中作品的下一话（踏着 persona＋构想＋台账 · 写回台账）
```

## 文档

- [用法](docs/usage-zh.md) — 安装方法、调用顺序，以及切换输出语言
- [21 个技能](docs/skills-zh.md) — 每个技能做什么（输入 → 输出）的参考
- [実証](docs/実証.md) — 支撑设计的实证记录（日语）

## 写作者的持久状态

- `${SOUL_VOICE_HOME}/persona.md` ——「我这样写」（现在式 · 肖像）。由 writer-persona 制作
- `${SOUL_VOICE_HOME}/voice-ledger.md` ——「我这样写过」（过去式 · 日记）。由 voice-ledger 累积
- 位置是用户在**工作区**内另设的**专用文件夹（本地文件夹即可，推荐 git 仓库）**，以 `SOUL_VOICE_HOME` 环境变量指向（未设定则 `~/.soul-voice-teller/`）。writer-persona 的第一步就是促成这个文件夹的创建

> **persona / voice-ledger 是每位写作者的状态，不纳入仓库（不固定）**——因为会有许多不同的人使用它。技能并不引用任何默认 persona。`examples/sample/` 里的 persona 是演示样例，不是技能的默认值。

> **注记——存声录的增长与上下文。** `voice-ledger.md` 不会被自动载入会话上下文——仅在需要时读取，因此只在**读取的那一刻**占用上下文。读取方式，以及如何在增长后保持全文读取轻量，参见 [usage「存声录的增长与上下文」](docs/usage-zh.md)。

## 仓库布局

- `skills/{name}/SKILL.md` —— 21 个技能（en 正典）＋各语言的 `SKILL-ja.md` / `SKILL-zh.md`
- `references/` —— 运用原理（内省 · 流露与克制 · 声音库，en 正典；`references/ja/`、`references/zh/` 镜像）
- `docs/` —— 用法与技能一览（[usage-zh.md](docs/usage-zh.md) / [skills-zh.md](docs/skills-zh.md)）＋放通用之物的地方（实证 · 理由 · 设计笔记）
- `locales/` —— 显示字符串（`en` 正典，`ja` / `zh` 镜像）
- `examples/<作品>/` —— 每部作品的产物
- `install.sh` —— 符号链接安装（全局 / 本地 / 卸载）

## 语言（i18n）

三种语言——**en / ja / zh**——以三层结构实现：

1. **本地化 JSON** —— `locales/{en,ja,zh}.json`（显示字符串）
2. **语言别提示词** —— `skills/{name}/SKILL-{lang}.md` ＋ `references/{lang}/*.md`
3. **镜像树** —— `README-{lang}.md` / `CLAUDE-{lang}.md`

语言解析顺序：`lang` 参数 ＞ `SOUL_VOICE_TELLER_LANG` 环境变量 ＞ **en**（默认）。不支持的语言会警告并回退到 `en`。要默认以中文（或日文）输出，请见 [用法](docs/usage-zh.md)。

**源概念（内省 / 余白 / 間）**是日语，被重新导出——不是逐字翻译——为英语（introspection / negative space / restraint）与中文（内省 / 留白 / 含蓄）。散文系技能（`prose` / `scene-writer` / `revise-for-reader`）以各语言的散文传统重新实现。

## 许可

MIT（[LICENSE](LICENSE)）
