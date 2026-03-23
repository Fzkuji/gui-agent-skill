# gui-observe 设计文档

> 最后更新：2026-03-24

## 核心原则

**先看再做。每个操作必须有视觉依据。**

## 三种视觉方法的分工

### 为什么需要三种方法

单一方法不够：
- OCR 看不到没有文字的图标按钮（三点菜单、关闭按钮）
- GPA 检测到位置但不知道是什么（label 始终是 null）
- image tool 能理解语义但给不了精确坐标

三者互补：
- OCR → 坐标 ✅ + 语义 ✅（文字本身就是语义）
- GPA → 坐标 ✅ + 语义 ❌（需要结合 OCR 或 image tool 识别）
- image tool → 坐标 ⛔ + 语义 ✅（理解页面结构和含义）

### 为什么 image tool 不能提供坐标

LLM 视觉模型看到的是压缩后的图片，内部没有像素级别的空间推理能力。它说"按钮在右上角"是模糊的语义描述，不是 (1200, 50) 这样的精确坐标。实测误差通常 > 50px，在密集 UI 里会点错元素。

### detect_all 统一入口

`detect_all(img_path)` 同时调用 GPA + OCR，返回合并去重的结果。

设计决策：
- **GPA 是必须的底线** — 纯 Python + YOLO，任何平台都能跑
- **OCR 是可选增强** — Mac 有 Apple Vision（最准），其他平台以后可接 Tesseract/PaddleOCR
- OCR 失败时 graceful degradation：只用 GPA 结果，不报错

## Phase 1 / Phase 2 渐进式观察

### 为什么区分两个阶段

Phase 1（全量观察）每次调用 image tool 分析截图，消耗 ~3000 token。如果对一个已经操作过 20 次的页面每次都跑 Phase 1，token 浪费严重。

Phase 2（快速观察）跳过 image tool，只用 OCR + GPA 的文字输出让 LLM 直接判断。在熟悉的页面上这就够了。

### 何时降级回 Phase 1

- OCR/GPA 输出看不懂（不认识的页面）
- 操作后结果不符合预期
- 出现弹窗、错误页面等异常

## 坐标系统

Mac Retina 屏幕：物理像素 = 逻辑像素 × 2
- 截图（screencapture）：3024 × 1964 物理像素
- 点击（pynput）：1512 × 982 逻辑像素
- OCR 返回的坐标：已转换为逻辑像素（detect_text 内部 ÷2）
- GPA 返回的坐标：物理像素，需要 ÷2
- detect_all 返回：全部是物理像素，调用方根据 retina 参数决定是否 ÷2

远程 VM（OSWorld）：1920 × 1080，无 Retina，坐标 1:1。
