# Skill Design References

参考仓库，用于改进 GUI Agent Skills 的技能设计、文档结构和工作流编排。

---

## 1. ARIS — Auto-claude-code-research-in-sleep

- **GitHub**: https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep
- **定位**: 自主 ML 研究工作流（从选题到论文），31 个可组合 skill
- **值得借鉴的设计**:
  - **Workflow 编排**: 4 个端到端 workflow（idea-discovery → experiment-bridge → auto-review-loop → paper-writing），可单独使用也可串联
  - **跨模型协作**: Claude Code 执行 + GPT-5.4 做 adversarial review，避免 self-play 盲点
  - **Skill 结构**: 每个 skill 是独立的 `SKILL.md`，plain Markdown，任何 LLM 都能读
  - **参数传递**: 所有 pipeline 行为通过 `— key: value` 内联配置
  - **Human-in-the-loop**: 可配置的 checkpoint（`AUTO_PROCEED`），既能全自动也能逐步审批
  - **多平台适配**: 同一套 skill 适配 Claude Code / Codex CLI / OpenClaw / Cursor / Trae 等
  - **模板系统**: `templates/` 目录提供每个 workflow 的输入模板
  - **Anti-hallucination**: 论文写作 skill 从 DBLP/CrossRef 获取真实 BibTeX，不靠 LLM 生成

## 2. Orchestra Research — AI Research Skills

- **GitHub**: https://github.com/Orchestra-Research/AI-Research-SKILLs
- **定位**: 最全面的 AI 研究 skill 库，86 个 skill，22 个分类
- **值得借鉴的设计**:
  - **分类体系**: 22 个清晰分类（Model Architecture / Fine-Tuning / Post-Training / Inference / Safety / Agents / RAG 等）
  - **README 结构**: 顶部用表格总览所有分类和 skill 数量，details 折叠展示完整列表
  - **Skill 规范**: 每个 skill 标注行数 + 参考文件数（如 "462 lines + 4 refs"），量化质量
  - **安装方式**: `npx` 一键安装 + Claude Code marketplace 分类安装
  - **Autoresearch 编排**: 中央编排 skill 管理完整研究生命周期，路由到各领域 skill
  - **质量标准**: "Quality over quantity" — 每个 skill 提供专家级指导、真实代码、排错指南、production workflow
  - **Skill 结构规范**:
    ```
    skill-name/
    ├── SKILL.md           # 主文件（agent 读取）
    └── references/        # 参考资料（详细文档、API spec 等）
    ```

---

## 对 GUI Agent Skills 的启发

### 已采纳
- ✅ Skills Overview 表格（参考 Orchestra 的分类表）
- ✅ 架构按核心机制组织（参考论文的 3 个创新点）
- ✅ 中英文文档结构统一

### 可考虑
- [ ] 给每个 sub-skill 标注复杂度/行数
- [ ] 添加 workflow 模板（类似 ARIS 的 `templates/`）
- [ ] 考虑跨平台适配指南（Linux VM、远程服务器）
- [ ] 添加 `references/` 目录存放详细技术文档
- [ ] 参数化配置（如置信度阈值、遗忘阈值）通过统一接口传递
