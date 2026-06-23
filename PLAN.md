# 计划

## 目标

根据 `ai-workflow.md` 生成提交检查报告，报告风格参考用户提供的图片示例。

## 报告结构

1. 标题区：
   - 项目名称。
   - 检查时间。
   - 工作流文件：`ai-workflow.md`。
2. 文件检查区：
   - 运行 `checkFiles()`。
   - 逐项列出 `required_files`。
   - 标记每个文件或目录为"存在"或"缺失"。
3. 测试结果区：
   - 运行 `runTests()`。
   - 展示 `test_command`。
   - 展示通过、失败、错误、超时数量。
   - 测试失败时展示关键错误信息。
4. 综合判定区：
   - 输出 `PASS`、`WARNING` 或 `BLOCKED`。
   - 列出选择该状态的原因。
5. 下一步动作区：
   - 先列必须修复项，再列建议修复项。
   - 每个 `BLOCKED` 原因都必须对应一个具体动作。
6. 总结区：
   - 用一句话说明当前项目是否可以提交。

## 目标示例

当 `README.md` 缺失，并且测试命令在收集阶段因为测试文件导入不存在的模块而失败时，报告必须判定为 `BLOCKED`。

预期原因：

- `README.md` 是必需文件，但当前缺失。
- 测试命令无法完成，因为出现导入错误。

预期下一步：

- 创建 `README.md`，写明项目用途和使用方式。
- 修复错误导入，或补充缺失依赖。
- 两个阻断问题都修复后，重新运行工作流。

## 要求检查清单

- `ai-workflow.md` 写清 `project_dir`、`required_files`、`test_command`。
- `ai-workflow.md` 写清 `checkFiles()` 和 `runTests()` 的功能、输入、输出。
- `ai-workflow.md` 写清 `PASS`、`WARNING`、`BLOCKED` 的含义和下一步。
- `ai-workflow.md` 包含至少三行"条件、状态、下一步"判断表。
- `ai-workflow.md` 包含缺文件、测试失败或导入错误、测试超时的失败兜底。
- `ai-workflow.md` 写清证据记录到 `ai-log.md` 的"文件检查""测试结果""综合判定"相关记录中。

## 验证方式

- 工作流内容验证：
  - `ai-workflow.md` 必须写清 `project_dir`、`required_files`、`test_command` 三个输入字段。
  - `ai-workflow.md` 必须写清 `checkFiles()` 和 `runTests()` 的功能、输入、输出。
  - `ai-workflow.md` 必须写清 `PASS`、`WARNING`、`BLOCKED` 的含义和下一步。
  - `ai-workflow.md` 必须包含至少三行"条件、状态、下一步"判断表。
  - `ai-workflow.md` 必须包含至少两个失败兜底，并说明具体处理方式。
- 报告逻辑验证：
  - 使用图片中的示例场景进行人工推演：缺少 `README.md` 且测试导入错误时，最终状态必须为 `BLOCKED`。
  - 每个 `BLOCKED` 原因都必须能在"下一步动作区"找到对应修复动作。
  - 最终总结必须明确说明当前项目是否可以提交。
- 证据记录验证：
  - 文件检查证据必须能追溯到 `ai-log.md` 的"文件检查"相关记录。
  - 测试运行证据必须能追溯到 `ai-log.md` 的"测试结果"相关记录。
  - 综合判定、原因和下一步必须能追溯到 `ai-log.md` 的"综合判定"相关记录。

