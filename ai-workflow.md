# AI 工作流

## 输入字段

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| `project_dir` | 要检查的项目目录。 | `.` |
| `required_files` | 提交前必须存在的文件或目录。 | `README.md`、`ai-log.md`、`test-record`、`design.md`、`spec.md`、`reflection.md` |
| `test_command` | 用于运行项目测试的命令。 | `python -m pytest tests/ -v` |

## 工具定义

### `checkFiles()`

- 功能：检查 `project_dir` 中是否存在 `required_files` 列出的每个文件或目录。
- 输入：
  - `project_dir`
  - `required_files`
- 输出：
  - `checked_files`：每个必需文件或目录的检查结果，结果为"存在"或"缺失"。
  - `missing_files`：所有缺失的必需文件或目录。
  - `status_hint`：全部存在时为 `PASS`，存在缺失项时为 `BLOCKED`。
  - `evidence_file`：检查证据记录到 `ai-log.md` 的"文件检查"相关记录中。

### `runTests()`

- 功能：在 `project_dir` 中执行 `test_command`，并汇总测试结果。
- 输入：
  - `project_dir`
  - `test_command`
- 输出：
  - `command`：实际执行的测试命令。
  - `passed`：通过的测试数量。
  - `failed`：失败的测试数量。
  - `errors`：收集阶段或运行阶段的错误数量。
  - `timeout`：测试命令是否超时。
  - `error_summary`：关键失败或错误摘要，例如 `ImportError` 或 `ModuleNotFoundError`。
  - `status_hint`：测试通过时为 `PASS`；结果不完整但未确认失败时为 `WARNING`；测试失败或无法运行时为 `BLOCKED`。
  - `evidence_file`：测试证据记录到 `ai-log.md` 的"测试结果"相关记录中。

## 状态定义

| 状态 | 含义 | 下一步 |
| --- | --- | --- |
| `PASS` | 必需文件齐全，并且测试通过。 | 允许提交，或继续后续任务。 |
| `WARNING` | 存在非阻断问题，例如可恢复的超时或证据不完整。 | 记录风险，建议修复，再决定是否继续。 |
| `BLOCKED` | 缺少关键文件、测试失败，或测试命令无法运行。 | 必须先修复阻断问题，然后重新运行工作流。 |

## 判断表

| 条件 | 状态 | 下一步 |
| --- | --- | --- |
| `required_files` 全部存在，且 `test_command` 通过。 | `PASS` | 可以提交或进入下一项任务。 |
| 必需文件存在，测试未失败，但证据不完整或出现可恢复超时。 | `WARNING` | 记录风险，补充证据或重新运行检查。 |
| 任意必需文件缺失。 | `BLOCKED` | 创建或恢复缺失文件，然后重新运行 `checkFiles()`。 |
| `test_command` 失败、出现导入错误，或无法完成测试收集。 | `BLOCKED` | 修复失败测试、错误导入或缺失依赖，然后重新运行 `runTests()`。 |

## 失败兜底

### 缺少必需文件

- 触发条件：`checkFiles()` 在 `missing_files` 中返回一个或多个缺失项。
- 具体处理：
  - 将每个缺失路径记录到 `ai-log.md` 的"文件检查"相关记录中。
  - 最终状态设为 `BLOCKED`。
  - 下一步：创建或恢复缺失文件，然后重新运行 `checkFiles()`。

### 测试失败或导入错误

- 触发条件：`runTests()` 返回 `failed > 0`、`errors > 0`，或出现 `ImportError`、`ModuleNotFoundError` 等错误。
- 具体处理：
  - 将测试命令、失败文件和关键错误摘要记录到 `ai-log.md` 的"测试结果"相关记录中。
  - 最终状态设为 `BLOCKED`。
  - 下一步：修复失败测试、错误导入或缺失依赖，然后重新运行 `runTests()`。

### 测试超时

- 触发条件：`runTests()` 在规定时间内没有完成。
- 具体处理：
  - 将超时命令和耗时记录到 `ai-log.md` 的"测试结果"相关记录中。
  - 如果已有可靠测试证据，则状态可设为 `WARNING`；否则状态设为 `BLOCKED`。
  - 下一步：增加超时时间后重跑，或定位导致测试挂起的问题。

## 证据记录

- 文件检查证据记录到 `ai-log.md` 的"文件检查"相关记录中。
- 测试运行证据记录到 `ai-log.md` 的"测试结果"相关记录中。
- 综合判定、判定原因和下一步动作记录到 `ai-log.md` 的"综合判定"相关记录中。
- 每次最终判断都必须引用 `checkFiles()` 和 `runTests()` 的证据，不能只凭主观判断。
