import os
import re
import subprocess
from typing import List, Dict, Any
from datetime import datetime


SCORING_TEMPLATES = {
    "ai-log.md": {
        "max_score": 15,
        "required_sections": [
            {"name": "目的", "pattern": r"\*\*目的\*\*", "weight": 3},
            {"name": "输入", "pattern": r"\*\*输入\*\*", "weight": 3},
            {"name": "建议", "pattern": r"\*\*建议\*\*", "weight": 3},
            {"name": "人工判断", "pattern": r"\*\*人工判断\*\*", "weight": 3},
            {"name": "验证", "pattern": r"\*\*验证\*\*", "weight": 3},
        ],
    },
    "design.md": {
        "max_score": 15,
        "required_sections": [
            {"name": "数据流", "pattern": r"#+\s*数据流", "weight": 4},
            {"name": "检索策略", "pattern": r"#+\s*检索策略", "weight": 4},
            {"name": "Prompt模板", "pattern": r"#+\s*Prompt\s*模板", "weight": 4},
            {"name": "设计权衡", "pattern": r"#+\s*设计权衡", "weight": 3},
        ],
    },
    "spec.md": {
        "max_score": 15,
        "required_sections": [
            {"name": "目标", "pattern": r"#+\s*目标", "weight": 5},
            {"name": "非目标", "pattern": r"#+\s*非目标", "weight": 5},
            {"name": "验收标准", "pattern": r"#+\s*验收标准", "weight": 5},
        ],
    },
    "reflection.md": {
        "max_score": 15,
        "required_sections": [
            {"name": "认知变化", "pattern": r"#+\s*认知变化", "weight": 4},
            {"name": "遇到的困难", "pattern": r"#+\s*遇到的困难", "weight": 4},
            {"name": "改进方向", "pattern": r"#+\s*改进方向", "weight": 4},
            {"name": "五维能力自评", "pattern": r"#+\s*五维能力自评", "weight": 3},
        ],
    },
    "test-record.md": {
        "max_score": 15,
        "required_sections": [
            {"name": "测试结果表格", "pattern": r"\|.*测试.*\|.*结果.*\|", "weight": 5},
            {"name": "功能测试", "pattern": r"#+\s*功能测试", "weight": 5},
            {"name": "测试总结", "pattern": r"#+\s*测试总结", "weight": 5},
        ],
    },
    "README.md": {
        "max_score": 15,
        "required_sections": [
            {"name": "项目简介", "pattern": r"#+\s*项目简介", "weight": 3},
            {"name": "安装步骤", "pattern": r"#+\s*安装步骤", "weight": 3},
            {"name": "运行命令", "pattern": r"#+\s*运行命令", "weight": 3},
            {"name": "测试命令", "pattern": r"#+\s*测试命令", "weight": 3},
            {"name": "依赖", "pattern": r"#+\s*依赖", "weight": 3},
        ],
    },
}

PASS_THRESHOLD = 0.8
TEST_TIMEOUT = 30


def _score_file(file_path: str, file_name: str) -> Dict[str, Any]:
    template = SCORING_TEMPLATES.get(file_name)
    if not template:
        return {"score": 0, "max_score": 15, "matched": [], "missing": []}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return {"score": 0, "max_score": template["max_score"], "matched": [], "missing": [s["name"] for s in template["required_sections"]]}

    score = 0
    matched = []
    missing = []

    for section in template["required_sections"]:
        if re.search(section["pattern"], content):
            score += section["weight"]
            matched.append(section["name"])
        else:
            missing.append(section["name"])

    return {
        "score": min(score, template["max_score"]),
        "max_score": template["max_score"],
        "matched": matched,
        "missing": missing,
    }


def checkFiles(project_dir: str, required_files: List[str]) -> Dict[str, Any]:
    checked_files = {}
    missing_files = []
    total_score = 0
    max_total_score = 0

    for file_name in required_files:
        file_path = os.path.join(project_dir, file_name)
        exists = os.path.exists(file_path)

        if exists:
            result = _score_file(file_path, file_name)
            checked_files[file_name] = {
                "exists": True,
                "score": result["score"],
                "max_score": result["max_score"],
                "matched": result["matched"],
                "missing": result["missing"],
            }
            total_score += result["score"]
            max_total_score += result["max_score"]
        else:
            missing_files.append(file_name)
            checked_files[file_name] = {
                "exists": False,
                "score": 0,
                "max_score": SCORING_TEMPLATES.get(file_name, {}).get("max_score", 15),
                "matched": [],
                "missing": [s["name"] for s in SCORING_TEMPLATES.get(file_name, {}).get("required_sections", [])],
            }
            max_total_score += SCORING_TEMPLATES.get(file_name, {}).get("max_score", 15)

    if missing_files:
        status_hint = "BLOCKED"
    elif max_total_score > 0 and total_score / max_total_score < PASS_THRESHOLD:
        status_hint = "WARNING"
    else:
        status_hint = "PASS"

    evidence_file = os.path.join(project_dir, "ai-log.md")

    return {
        "checked_files": checked_files,
        "total_score": total_score,
        "max_total_score": max_total_score,
        "missing_files": missing_files,
        "status_hint": status_hint,
        "evidence_file": evidence_file,
    }


def _parse_test_record(file_path: str) -> List[Dict[str, str]]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    tests = []
    code_blocks = re.findall(r"```(?:bash|shell|powershell)?\n(.*?)```", content, re.DOTALL)

    for block in code_blocks:
        lines = block.strip().split("\n")
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("cd ") or line.startswith("export "):
                continue
            if line.startswith("python ") or line.startswith("python3 "):
                tests.append({
                    "name": line,
                    "command": line,
                })

    return tests


def _run_single_test(command: str, project_dir: str, timeout: int = TEST_TIMEOUT) -> Dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=project_dir,
        )
        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timeout": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "command": command,
            "returncode": -1,
            "stdout": "",
            "stderr": f"命令超时（{timeout}秒）",
            "timeout": True,
        }
    except Exception as e:
        return {
            "command": command,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "timeout": False,
        }


def runTests(project_dir: str, test_command: str) -> Dict[str, Any]:
    test_record_path = os.path.join(project_dir, "test-record.md")

    if not os.path.exists(test_record_path):
        return {
            "command": test_command,
            "passed": 0,
            "failed": 0,
            "errors": 1,
            "timeout": False,
            "error_summary": "test-record.md 不存在，无法执行测试",
            "status_hint": "BLOCKED",
            "evidence_file": os.path.join(project_dir, "ai-log.md"),
            "test_details": [],
        }

    parsed_tests = _parse_test_record(test_record_path)
    test_details = []
    passed = 0
    failed = 0
    errors = 0
    has_timeout = False
    error_messages = []

    if test_command:
        main_result = _run_single_test(test_command, project_dir)
        test_details.append({
            "name": "主测试命令",
            "command": test_command,
            "returncode": main_result["returncode"],
            "passed": main_result["returncode"] == 0,
            "timeout": main_result["timeout"],
            "output_snippet": main_result["stdout"][:500] if main_result["stdout"] else main_result["stderr"][:500],
        })
        if main_result["timeout"]:
            has_timeout = True
        if main_result["returncode"] == 0:
            passed += 1
        elif main_result["returncode"] > 0:
            failed += 1
            error_messages.append(f"{test_command}: exit code {main_result['returncode']}")
        else:
            errors += 1
            error_messages.append(f"{test_command}: {main_result['stderr'][:200]}")

    for test in parsed_tests:
        result = _run_single_test(test["command"], project_dir)
        test_details.append({
            "name": test["name"],
            "command": test["command"],
            "returncode": result["returncode"],
            "passed": result["returncode"] == 0,
            "timeout": result["timeout"],
            "output_snippet": result["stdout"][:500] if result["stdout"] else result["stderr"][:500],
        })
        if result["timeout"]:
            has_timeout = True
        if result["returncode"] == 0:
            passed += 1
        elif result["returncode"] > 0:
            failed += 1
            error_messages.append(f"{test['command']}: exit code {result['returncode']}")
        else:
            errors += 1
            error_messages.append(f"{test['command']}: {result['stderr'][:200]}")

    if failed > 0 or errors > 0:
        status_hint = "BLOCKED"
    elif has_timeout:
        status_hint = "WARNING"
    else:
        status_hint = "PASS"

    return {
        "command": test_command,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "timeout": has_timeout,
        "error_summary": "; ".join(error_messages)[:500],
        "status_hint": status_hint,
        "evidence_file": os.path.join(project_dir, "ai-log.md"),
        "test_details": test_details,
    }


if __name__ == "__main__":
    import json

    project_dir = "."
    required_files = ["README.md", "ai-log.md", "test-record.md", "design.md", "spec.md", "reflection.md"]
    test_command = "python -m pytest tests/ -v"

    print("=" * 60)
    print("文件检查")
    print("=" * 60)
    file_result = checkFiles(project_dir, required_files)
    print(json.dumps(file_result, ensure_ascii=False, indent=2))

    print()
    print("=" * 60)
    print("测试执行")
    print("=" * 60)
    test_result = runTests(project_dir, test_command)
    print(json.dumps(test_result, ensure_ascii=False, indent=2))
