# AI 协作日志

## 记录格式

每条记录包含五字段：目的、输入、建议、人工判断、验证。

---

## [2026-06-23] S1: 初始化 AI 协作文件

**目的**：在当前项目目录中建立 AI 协作记录和工作流说明文件。

**输入**：用户要求"先给出一个 `ai-log.md`，与 `ai-worklow.md` 文件"。

**建议**：
- AI 建议先创建基础版 `ai-log.md`，用于记录 AI 协作过程。
- AI 建议先创建基础版工作流文件，说明 AI 辅助开发流程。

**人工判断**：
- 接受先创建基础文件。
- 初始文件名按用户第一次输入创建为 `ai-worklow.md`。

**验证**：目录中生成了 `ai-log.md` 和 `ai-worklow.md` 两个文件。


---

## [2026-06-23] S2: 编写工作流与计划文件

**目的**：实现计划，写出满足最低要求的 `ai-workflow.md` 和 `PLAN.md`。

**输入**：已确认的实施计划，以及图片中提交检查报告的结构。

**建议**：
- AI 建议 `ai-workflow.md` 明确三个输入字段：`project_dir`、`required_files`、`test_command`。
- AI 建议 `ai-workflow.md` 明确两个工具：`checkFiles()` 和 `runTests()`，并写清功能、输入、输出。
- AI 建议 `ai-workflow.md` 明确三个状态：`PASS`、`WARNING`、`BLOCKED`，并写清含义和下一步。
- AI 建议用判断表把"条件、状态、下一步"绑定起来。
- AI 建议至少提供缺文件、测试失败或导入错误、测试超时三个失败兜底。
- AI 建议所有证据都记录到 `ai-log.md`，分为"文件检查""测试结果""综合判定"三类。

**人工判断**：
- 接受按最低要求逐项写入 `ai-workflow.md`。
- 接受新增 `PLAN.md`，说明如何按 `ai-workflow.md` 生成类似图片的检查报告。

**验证**：目录中保留 `ai-log.md`、`ai-workflow.md`、`PLAN.md`。

---

## [2026-06-23] S3: 重写计划验证方式并准备 Git 备份

**目的**：将 `PLAN.md` 中的"验证方式"改成更具体、可执行的验收清单，并将当前项目备份到 GitHub。

**输入**：用户要求"`PLAN.md` 中的验证方式需要重新编写，完成后上传 Git 备份至 `lktr-wq/ai-workflow`"。

**建议**：
- AI 建议把验证方式拆成文件验证、工作流内容验证、报告逻辑验证、证据记录验证和 Git 备份验证。
- AI 建议在验证方式中明确远程仓库地址为 `https://github.com/lktr-wq/ai-workflow.git`。
- AI 建议保留用户已精简的日志结构，只追加本次关键决策记录。

**人工判断**：
- 接受重写 `PLAN.md` 的验证方式。
- 接受将本地三个 Markdown 文件作为备份内容提交到 GitHub 仓库。

**验证**：`PLAN.md` 的"验证方式"已改为分组验收清单；本地 Git 提交已创建，远程仓库已设置为 `https://github.com/lktr-wq/ai-workflow.git`，并已推送到 `origin/main`。
