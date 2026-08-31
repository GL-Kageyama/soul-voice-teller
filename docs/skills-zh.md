# 20 个技能

每个技能做什么（输入 → 输出）的参考。调用方式见 [用法](usage-zh.md)。

## 主线

| 技能 | 职责 | 输入 → 输出 |
|---|---|---|
| `writer-persona` | 用对谈引出写作者的设定（A 问句 · 依据 = 人的真实经验） | 对谈 → `${SOUL_VOICE_HOME}/persona.md`（灵魂故事 / 审美 / 声音与笔触 / 禁忌 / 题材偏好） |
| `premise` | 构思（B 问句 · 依据 = persona＋声音库） | 种子＋persona＋声音库 → `<作品>/premise.md`（一句话梗概 / 核心问句 / 主题 / 体裁的约定 / 文体的方向 / 读者形象与约定） |
| `plot-design` | 设计书（fast-draft 的输入规格），对照约定＋声音来修订（C 问句 · 依据 = premise＋persona）。连载作品把弧展开为章立て・话割り | premise＋persona＋声音库 → `<作品>/design.md`（必需构思＋章立て・话割り＋可选预备） |
| `fast-draft` | 草稿（流露与克制的美学＋内省循环） | 设计＋persona＋声音库 → `<作品>/draft_*.md`＋计划更新＋供声音库存的声音 |
| `voice-ledger` | 存声、回读 | 声音（构思 / 设计 / 草稿 / 文思 / 禁忌 / 评价的回响） → `${SOUL_VOICE_HOME}/voice-ledger.md` |

## 可选预备

从 plot-design 按需调用。留空也能写。

| 技能 | 职责 | 输入 → 输出 |
|---|---|---|
| `narration-design` | 叙述的详细设计（视角类型 · 可靠度 · 距离 · 时态 · 嵌套 · 语体） | 设计 → design.md 的「叙述」细化 |
| `character-forge` | 人物设计（欲望 · 伤口 · 声音 · 变化弧 · 内在冲突） | 设计＋premise＋persona → design.md 的「人物」细化 |
| `character-in-action` | 让人物设定在场景中生效（分阶段披露 · 让设定动起来） | 设计 → 向场景表追加联动点 |
| `character-bond` | 描绘两人之间的关系（关系的轴 · 反转／镜像 · 转折点 · 双向 · 身体化） | 设计＋草稿 → 两人关系的细化 |
| `worldbuild` | 世界设计（舞台 · 规则 · 内在一致 · 设定⇔故事的连接） | 设计＋premise＋persona → design.md 的「世界」细化 |
| `world-iceberg` | 未写世界的资料化程度（按触及概率） | 设计 → 追加资料清单 |
| `research-verify` | 史实 · 时代考据 · 专业知识的对照（排除错误） | 设计/草稿 → 错误＋订正清单 |

## 写作质量 · 改稿 · 长期

| 技能 | 职责 | 输入 → 输出 |
|---|---|---|
| `prose` | 以文体打磨（节奏 · 语感 · 无可替代的声音） | 文/场景＋persona → 重写后的文字 |
| `scene-writer` | 深写一个场景（留白的设计 · 见而示之 · 场景的接缝） | 设计＋persona → draft_<n>_<场景>.md |
| `series-bible` | 作品圣经（集中管理设定 · 伏笔 · 连载的账本） | 作品的产物 → series-bible.md |
| `revise-for-reader` | 以读者体验改稿（沉浸 · 翻页感 · 约定 · 重读） | 草稿＋设计 → 改稿后的 draft.md |
| `entertainment` | 不破坏克制地增添娱乐的快感（钩子 · 翻页 · 反转 · 宣泄 · 节奏 · 共情） | 草稿＋设计 → 改稿后的 draft.md |
| `whole-work-review` | 把作品作为「整体」来重看——是否作为一本书闭合（结构的连贯性 · 伏笔回收 · 密度分配 · 重复 · 世界观词语的依赖 · 克制的平衡） | 草稿＋series-bible → 改稿后的 draft.md |

## 送达

| 技能 | 职责 | 输入 → 输出 |
|---|---|---|
| `package` | 把完成的作品包装给读者（标题＋副标题 · 宣传语 · 简介 · 图像提示词 · 标签），对照读者的第一印象 | 草稿＋premise＋series-bible＋persona → `<作品>/package.md` |
| `theme-song` | 把完成的作品凝缩为一首主题曲（曲名 · 带结构的歌词 · 曲风指定 · 声乐 · 歌曲说明 · 位置），对照作品的灵魂（主题＋情感升起的场景） | 草稿＋premise＋series-bible＋persona → `<作品>/theme-song.md` |
