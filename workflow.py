from typing import List, Dict, Any


def checkFiles(project_dir: str, required_files: List[str]) -> Dict[str, Any]:
    """
    检查项目目录中是否存在必需文件。

    Args:
        project_dir: 要检查的项目目录
        required_files: 必需文件或目录列表

    Returns:
        checked_files: 每个文件的检查结果（存在/缺失）
        missing_files: 缺失的文件列表
        status_hint: 状态提示（PASS/BLOCKED）
        evidence_file: 证据记录文件路径
    """
    pass


def runTests(project_dir: str, test_command: str) -> Dict[str, Any]:
    """
    在项目目录中执行测试命令并汇总结果。

    Args:
        project_dir: 项目目录
        test_command: 测试命令

    Returns:
        command: 实际执行的命令
        passed: 通过的测试数量
        failed: 失败的测试数量
        errors: 错误数量
        timeout: 是否超时
        error_summary: 错误摘要
        status_hint: 状态提示（PASS/WARNING/BLOCKED）
        evidence_file: 证据记录文件路径
    """
    pass