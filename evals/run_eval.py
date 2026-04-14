#!/usr/bin/env python3
"""
Akira-system-autoresearch 自评估脚本。
评估自身作为系统 skill 的质量，输出 JSON 分数。

用法: python3 evals/run_eval.py
输出: {"dimensions": {...}, "total_score": 0-100}
"""

import os
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent

def check_file(path):
    return (SKILL_DIR / path).exists()

def check_content(path, must_contain):
    """检查文件是否包含指定关键词列表，返回覆盖率"""
    fpath = SKILL_DIR / path
    if not fpath.exists():
        return 0.0
    content = fpath.read_text()
    hits = sum(1 for s in must_contain if s.lower() in content.lower())
    return hits / len(must_contain) if must_contain else 1.0

# ── 系统 skill 专属维度 ──

def eval_architecture_coverage():
    """架构覆盖度 (20%): 子系统、模式、接口是否齐全"""
    checks = {
        "has_three_modes": check_content("SKILL.md", ["loop", "reason", "scenario"]),
        "has_phase_protocol": check_content("references/loop-protocol.md", ["phase 0", "phase 1", "phase 2", "phase 3", "phase 4", "phase 5", "phase 6", "phase 7", "phase 8", "phase 9"]),
        "has_eval_dimensions": check_content("references/eval-dimensions.md", ["通用维度", "人物视角", "药物", "系统"]),
        "has_cascade": check_content("references/cascade-protocol.md", ["级联"]),
        "has_meta_improvement": check_content("SKILL.md", ["元改进"]),
    }
    return sum(checks.values()) / len(checks) * 100

def eval_protocol_completeness():
    """协议完整性 (15%): 每阶段有明确输入/输出/判定规则"""
    checks = {
        "has_input_output": check_content("references/loop-protocol.md", ["必需输入", "输出", "判定"]),
        "has_decision_logic": check_content("references/loop-protocol.md", ["保留", "丢弃", "回滚"]),
        "has_pivot_recovery": check_content("references/loop-protocol.md", ["PIVOT", "REFINE", "卡住恢复"]),
        "has_health_check": check_content("references/loop-protocol.md", ["健康检查", "health"]),
    }
    return sum(checks.values()) / len(checks) * 100

def eval_boundary_handling():
    """边界处理 (10%): 异常、错误、中断恢复"""
    checks = {
        "has_rollback": check_content("SKILL.md", ["revert", "回滚"]),
        "has_guard": check_content("SKILL.md", ["guard", "守卫"]),
        "has_no_verify_stall": check_content("references/loop-protocol.md", ["验证失败", "无法解析", "空输出"]),
        "has_context_drift": check_content("references/loop-protocol.md", ["context drift", "重锚", "Context Drift"]),
    }
    return sum(checks.values()) / len(checks) * 100

def eval_composability():
    """可组合性 (10%): 能否与其他系统 skill 协同"""
    checks = {
        "references_other_skills": check_content("SKILL.md", ["eva", "skill-design", "core", "drug-skill-lab"]),
        "cascade_defined": check_content("references/cascade-protocol.md", ["触发", "检查", "标记"]),
        "universal_scope": check_content("SKILL.md", ["域无关", "任意研究领域"]),
    }
    return sum(checks.values()) / len(checks) * 100

# ── 通用维度 ──

def eval_structure_completeness():
    """架构完整度 (15%): 目录结构、frontmatter、refs"""
    # scripts 需要目录存在 + 至少一个可执行文件
    scripts_dir = SKILL_DIR / "scripts"
    scripts_ok = scripts_dir.is_dir() and any(
        (scripts_dir / f).is_file() and (f.endswith('.py') or f.endswith('.sh'))
        for f in os.listdir(scripts_dir)
    )
    checks = {
        "has_skill_md": check_file("SKILL.md"),
        "has_readme": check_file("README.md"),
        "has_references": check_file("references"),
        "has_evals": check_file("evals"),
        "has_scripts": scripts_ok,
        "has_frontmatter": check_content("SKILL.md", ["---", "name:", "version:", "author:"]),
    }
    return sum(checks.values()) / len(checks) * 100

def eval_doc_quality():
    """文档质量 (10%): README 清晰度、安装说明"""
    checks = {
        "readme_has_install": check_content("README.md", ["安装", "setup", "使用"]),
        "readme_has_usage": check_content("README.md", ["触发", "使用方式", "示例"]),
        "readme_has_design": check_content("README.md", ["设计", "原理", "决策"]),
    }
    return sum(checks.values()) / len(checks) * 100

def eval_spec_compliance():
    """规范遵从度 (10%): hermes-skill-authoring-standard"""
    checks = {
        "has_description": check_content("SKILL.md", ["description:"]),
        "has_dependencies": check_content("SKILL.md", ["dependencies:"]),
        "author_is_akira": check_content("SKILL.md", ["AKIRA"]),
    }
    return sum(checks.values()) / len(checks) * 100

def eval_reproducibility():
    """可复现性 (5%): 其他 agent 能否按说明使用"""
    checks = {
        "has_usage_example": check_content("SKILL.md", ["```"]),
        "has_param_table": check_content("SKILL.md", ["| 参数", "|------"]),
    }
    return sum(checks.values()) / len(checks) * 100


def main():
    results = {}

    # 系统 skill 专属 (55%)
    results["architecture_coverage"] = eval_architecture_coverage()
    results["protocol_completeness"] = eval_protocol_completeness()
    results["boundary_handling"] = eval_boundary_handling()
    results["composability"] = eval_composability()

    # 通用 (45%)
    results["structure_completeness"] = eval_structure_completeness()
    results["doc_quality"] = eval_doc_quality()
    results["spec_compliance"] = eval_spec_compliance()
    results["reproducibility"] = eval_reproducibility()

    weights = {
        "architecture_coverage": 0.20,
        "protocol_completeness": 0.15,
        "boundary_handling": 0.10,
        "composability": 0.10,
        "structure_completeness": 0.15,
        "doc_quality": 0.10,
        "spec_compliance": 0.10,
        "reproducibility": 0.05,
    }

    total = sum(results[k] * weights[k] for k in results)

    output = {
        "dimensions": {k: round(v, 1) for k, v in results.items()},
        "total_score": round(total, 1),
        "weakest": min(results, key=results.get),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return output


if __name__ == "__main__":
    main()
