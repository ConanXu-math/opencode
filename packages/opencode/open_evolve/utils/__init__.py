"""
工具模块
"""

import json
from pathlib import Path
from typing import Dict, Any, List


def read_json_file(file_path: str) -> Dict[str, Any]:
    """读取JSON文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_file(file_path: str, data: Dict[str, Any]):
    """写入JSON文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def find_output_dirs(base_dir: str = ".") -> List[Path]:
    """查找输出目录"""
    base = Path(base_dir)
    output_dirs = []

    for item in base.iterdir():
        if item.is_dir() and any(
            x in item.name.lower() for x in ["output", "results", "optimized"]
        ):
            output_dirs.append(item)

    return sorted(output_dirs, key=lambda x: x.stat().st_mtime, reverse=True)


def get_optimization_results(output_dir: Path) -> Dict[str, Any]:
    """获取优化结果"""
    best_file = output_dir / "best" / "best_program.py"
    info_file = output_dir / "best" / "best_program_info.json"

    result = {"output_dir": str(output_dir)}

    if best_file.exists():
        result["optimized_code"] = best_file.read_text()

    if info_file.exists():
        result["metrics"] = read_json_file(str(info_file))

    return result


__all__ = [
    "read_json_file",
    "write_json_file",
    "find_output_dirs",
    "get_optimization_results",
]
