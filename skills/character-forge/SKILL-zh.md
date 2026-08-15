---
name: character-forge
description: 构思人物的预备技能。定下欲望、动机、创伤、信念、变化弧线与有别于他人的声音，把 design.md 的「character」深化到 fast-draft 能「让角色以本色行动」的粒度。把内在冲突收束为一个。可选预备（没有它也能写）。在 plot-design 之后。
argument-hint: '（可选）design.md 的路径。省略时在工作目录中寻找 design.md。加 lang=en|ja|zh 切换输出语言（默认 en）。'
---

# character-forge —— 人物设计（欲望 · 创伤 · 弧线 · 声音）

## 语言模式

本技能默认以英文写作。如需以其他语言写作，请传入 `lang` 参数（例如 `/character-forge lang=zh`）或在环境中设置 `SOUL_VOICE_TELLER_LANG=zh`。解析顺序：`$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`。

- `en`（默认）：使用本文件（`SKILL.md`）与 `../references/*.md`。
- `ja`：读取 `SKILL-ja.md` 与 `../references/ja/*.md`；以日语输出。源概念（内省 / 余白 / 間）在此。
- `zh`：读取本文件（`SKILL-zh.md`）与 `../references/zh/*.md`；以中文输出（留白 / 含蓄）。

所有输出均以解析出的语言书写。

## 技能元数据

- **id**：`character-forge`
- **version**：`0.1.0`
- **category**：`writing`（构思层 · 可选预备）
- **standalone**：`true`
- **language**：`zh`（镜像于 `SKILL.md`（en）/ `SKILL-ja.md`）

## 定位

可选预备（技术目录 §2-A 人物设计）。把 plot-design 的「character」（可为空）深化到 fast-draft 能「让角色以本色行动」的粒度。没有它也能写，但角色能否成为「活生生的人」而非「角色（主角 · 对手）」在此决定。

**来源**：技术目录 §2-A（2-1〜2-16）。

## 输入约定

- **design.md**：`<工作目录>/design.md`（character 一节。空白或 `?` 亦可）。
- **premise.md**：`<工作目录>/premise.md`（核心问句 · 主题——角色的欲望 · 创伤系于主题）。
- **persona**：`${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md`（题材偏好 · 吸引你的人物与关系）。

## 步骤

1. 读入 design.md 的「character」、premise 的主题、persona 的「题材偏好」。
2. 定下每个角色的「核心」（§2-A）：
   - **欲望 · 目标（2-3）**：想要什么（表面的愿望）
   - **动机（2-4）**：为何想要（根）
   - **欠缺 · 创伤 · 弱点（2-5）**：内在的欠缺 · 过去的创伤
   - **信念 · 价值观（2-6）**：视为正确之物 · 死也会守护之物
   - **声音（2-13）**：说话方式 · 用词 · 思考习惯。有别于他人
   - **变化弧线（2-12）**：如何改变 / 如何不改变
   - **表面与内里的落差（2-16）**：外貌 · 言语与内里的错位
3. **把内在冲突收束为一个**：两个相悖的欲望 · 信念相撞之点（例：想守护 vs 想逃离）。这是变化弧线的引擎。
4. 写明角色如何系于主题（premise 的核心问句）——角色应是主题的「活论据」。
5. 写入 design.md 的「character」。未定可留作 `?`（预备容许空白）。

## 输出

design.md 的「character」之深化（欲望 · 动机 · 创伤 · 信念 · 声音 · 变化弧线 · 内在冲突 · 表面与内里的落差）。

## 注意

- **保持欲望一致**（2-3〜2-4）：表面的愿望（欲望）与根（动机）不得矛盾。若矛盾，那便是内在冲突。
- 把角色当作「人」而非「角色（2-11）」来塑造。主角 · 对手是功能；其下是创伤 · 欲望 · 信念。
- **勿将对手塑成片面的恶**（2-27）：给对手的逻辑以它自身的正当性。
- 声音须不越 persona 的「禁忌」。触碰禁忌的角色，须有理由地塑造。
