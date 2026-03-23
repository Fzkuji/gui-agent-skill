# gui-report 设计文档

> 最后更新：2026-03-24

## 核心目的

追踪每个 GUI 任务的性能数据：时间、token 消耗、操作次数。用于：
- 对比不同策略的效率
- 发现性能瓶颈（哪步最慢？哪步 token 最多？）
- Benchmark 结果量化

## 当前状态

⚠️ **gui-report 目前未被正式使用过。** auto-tick 机制在后台计数（screenshots、ocr_calls 等），但 `start` 和 `report` 从未在实际任务中正式调用。没有历史数据，没有 data 目录。

## 设计

### auto-tick 机制

各函数内部自动计数，不需要 LLM 手动调用：
- `learn_from_screenshot()` → screenshots++, learns++, ocr_calls++, detector_calls++
- `record_page_transition()` → transitions++, clicks++, ocr_calls++, detector_calls++

只有 `image_calls`（LLM 看截图的次数）需要手动 tick，因为 image tool 的调用在 LLM 层面，不在 app_memory.py 里。

### 计数器

| Counter | 自动 | 含义 |
|---------|------|------|
| screenshots | ✅ | 截图次数 |
| clicks | ✅ | 点击次数 |
| learns | ✅ | learn_from_screenshot 调用次数 |
| transitions | ✅ | 状态转移记录次数 |
| ocr_calls | ✅ | OCR 调用次数 |
| detector_calls | ✅ | GPA-GUI-Detector 调用次数 |
| image_calls | ❌ 手动 | LLM 视觉分析次数 |

### Token 追踪

通过读取 OpenClaw 的 sessions.json 获取任务开始和结束时的 token 数，计算差值。

### 待解决问题

1. **从未正式调用**：需要在主 SKILL.md 的流程中强制要求 start/report
2. **没有持久化数据目录**：需要创建 data/ 目录存储历史报告
3. **和 workflow 的分层验证整合**：Level 0/1/2 的调用次数也应该追踪
4. **Benchmark 模式**：OSWorld 等 benchmark 应该自动产出 per-task 报告

## 理想流程

```
任务开始 → tracker start
  → 操作中各计数器自动 tick
  → 包括 workflow 的 level 0/1/2 验证次数
任务结束 → tracker report
  → 输出：时间、token 消耗、操作次数、成功率
  → 保存到 data/<timestamp>.json
```
