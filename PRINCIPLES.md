# Agency Pack 设计原则

## 什么是 Agency Pack

**Agency Pack** 是 Plugin 和 Skill 的组合体，为 AI agent 提供在某个领域的**完整代理能力**。

一个 Agency Pack 包含：

| 组件 | 角色 | 执行方式 |
|------|------|---------|
| **Plugin** | 确定性操作 | 框架自动执行，模型不参与 |
| **Skill** | 开放性决策 | 模型按需读取，自主判断 |
| **Memory** | 经验积累 | 两者共享，越用越聪明 |

**类比：** 一个新司机上路。
- Plugin = 车载系统自动告诉你"当前在高速/城市道路"、"限速 120"、"油量还剩 30%"
- Skill = 驾校教练教你的方法论"变道前看后视镜"、"过弯减速"
- Memory = 你自己开熟了之后的肌肉记忆

三者缺一不可，穿插配合，不是先后顺序。

## Plugin vs Skill

```
Plugin（确定性）              Skill（开放性）
─────────────                ─────────────
代码执行                      文本指导
答案唯一                      解法多样
不需要模型想                   需要模型判断
框架自动触发                   模型决定是否使用
环境事实                      操作策略
"你在 Linux 上"              "截图 → OCR → 找按钮 → 点击"
```

**判断标准：** 如果一个操作的正确做法只有一种，用 Plugin。如果有多种做法需要根据情况选择，用 Skill。

## 穿插配合

Plugin 和 Skill 在任务执行中**交替出现**：

```
→ Plugin: 检测到 Linux + xdotool 可用
→ Skill:  模型截图，OCR 检测到 LibreOffice Calc 打开
→ Skill:  模型决定先关闭 text editor
→ Plugin: 用 wmctrl -c 关闭窗口（确定性命令）
→ Skill:  模型 OCR 找到 Name Box 在 (91, 184)
→ Plugin: 用 pyautogui.click(91, 184) 点击（确定性坐标）
→ Skill:  模型决定输入 "Ming Pavilion"
→ Plugin: 用 xdotool type（确定性输入方式）
→ Skill:  模型截图验证，判断是否成功
→ ...
```

**不是**"先跑完所有 Plugin，再开始 Skill"。是**该确定时确定，该判断时判断**。

## 密度变化

Plugin 和 Skill 的使用密度会自然变化：

| 阶段 | Plugin 密度 | Skill 密度 | 原因 |
|------|-----------|-----------|------|
| 任务开始 | 高 | 低 | 模型不了解环境，需要大量确定性信息 |
| 任务中期 | 中 | 高 | 模型在做具体操作，偶尔遇到确定性问题 |
| 任务后期 | 低 | 中 | 模型有 memory，两者都需要的少了 |
| 同类任务再来 | 很低 | 低 | 几乎全靠 memory，只在新情况出现时需要 |

## 设计指南

### Plugin 设计
- **只做确定性的事** — 答案不唯一就不该是 Plugin
- **注入精简** — 最小信息集，不浪费 token
- **随时可调** — 不只在开头，中途遇到确定性问题也调用
- **不替代思考** — 告诉模型"你有 xdotool"，不告诉模型"你应该点这里"

### Skill 设计
- **提供方法论** — "截图→OCR→找坐标→点击"，不是"点击 (500, 300)"
- **留决策空间** — 模型可能找到更好的做法
- **可触发 Plugin** — 流程中遇到确定性步骤，调用 Plugin 能力
- **积累记忆** — 学到的经验减少未来的依赖

### Memory 设计
- **Plugin 和 Skill 共享** — 环境信息和操作经验存在同一个 memory 里
- **越用越少依赖** — memory 丰富后，Plugin 注入和 Skill 指导都可以更简短

---

## 样例：GUI Agency Pack

以下是一个完整的 Agency Pack 示例，展示 Plugin、Skill、Memory 如何在一个简单任务中穿插配合。

### 任务：在 LibreOffice Calc 中输入一个人名

### 文件结构

```
gui-agency-pack/
├── plugin/
│   ├── openclaw.plugin.json
│   └── index.ts              # before_prompt_build hook
├── skills/
│   └── gui-agent/
│       └── SKILL.md           # 视觉检测+操作方法论
└── memory/
    └── apps/
        └── libreoffice-calc/
            └── components.json
```

### 执行流程

**1. Plugin 自动注入（框架执行，模型不参与）**

```typescript
// plugin/index.ts
api.on("before_prompt_build", async () => ({
    prependSystemContext: `
## GUI Platform Context
Platform: Linux (aarch64), Display: X11
Text input: xdotool type --delay 20 "text"
Mouse click: pyautogui.click(x, y)
Window management: wmctrl -a "title" / wmctrl -c "title"
Shortcuts: Ctrl+S (save), Ctrl+W (close file), Ctrl+Q (quit app)
Cell navigation: Click Name Box → type cell ref (e.g. "A2") → Enter
Number as text: prefix with apostrophe ('28208580)
`
}));
```

模型收到这段内容时，**已经知道了平台和工具**，不需要自己去检测。

**2. Skill 指导（模型读取后自主执行）**

SKILL.md 告诉模型：
```
## 操作流程
1. 截图 → 下载到本地
2. OCR (detect_text) → 获取所有文本 + 坐标
3. 识别目标元素 → 确定点击坐标
4. 执行操作 → 通过 VM execute API
5. 再次截图 → 验证结果
```

模型根据这个方法论**自己决定**：先 OCR 找到 Name Box，坐标是 (91, 184)。

**3. 交替执行**

```
[Plugin 注入] 模型知道在 Linux 上，用 xdotool type
[Skill 指导] 模型截图 → OCR 找到 Name Box 在 (91, 184)
[Skill 决策] 模型决定先点击 Name Box
[Plugin 工具] 通过 VM API 执行: pyautogui.click(91, 184)
[Skill 指导] 模型截图验证 → Name Box 被选中了
[Skill 决策] 模型决定输入 "A2" 导航到目标单元格
[Plugin 工具] 通过 VM API 执行: xdotool type "A2" + Enter
[Skill 指导] 模型截图验证 → A2 被选中了
[Skill 决策] 模型决定输入人名
[Plugin 工具] 通过 VM API 执行: xdotool type "Ming Pavilion"
[Skill 指导] 模型截图验证 → 文字出现在 A2 中 ✅
[Memory 保存] 记录: Name Box 位置 (91, 184), xdotool type 有效
```

**4. Memory 积累**

下次再遇到 LibreOffice Calc 任务时：
- Plugin 仍然注入平台信息（确定性，每次都需要）
- Skill 的 OCR 步骤可以跳过 Name Box 检测（memory 里已经有坐标了）
- 模型直接用记忆中的方法操作，效率更高

### 关键观察

- Plugin 在**第 1 步和每次具体操作时**都参与了（注入环境 + 提供工具命令）
- Skill 在**每次需要观察和判断时**参与了（截图、OCR、决策、验证）
- 两者**不是先后，而是交替**
- Memory **跨越两者**，记录环境信息和操作经验
