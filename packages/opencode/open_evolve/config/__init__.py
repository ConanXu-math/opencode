"""
配置模块
"""

import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    if not Path(config_path).exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_default_config() -> Dict[str, Any]:
    """获取默认配置"""
    default_config_path = (
        Path(__file__).parent.parent.parent / "openevolve_fixed_config.yaml"
    )

    if default_config_path.exists():
        return load_config(str(default_config_path))
    else:
        # 返回内置默认配置
        return {
            "llm": {
                "models": [
                    {
                        "name": "deepseek-chat",
                        "api_key": "",
                        "api_base": "https://api.deepseek.com/v1",
                        "temperature": 0.7,
                        "max_tokens": 4000,
                    }
                ],
                "api_base": "https://api.deepseek.com/v1",
                "temperature": 0.7,
                "max_tokens": 4000,
            },
            "evolution": {
                "population_size": 50,
                "num_islands": 3,
                "crossover_rate": 0.8,
                "mutation_rate": 0.2,
                "elitism_count": 5,
                "max_program_length": 1000,
            },
            "evaluation": {
                "timeout_seconds": 30,
                "max_memory_mb": 1024,
                "cascade_evaluation": False,
            },
            "logging": {"level": "INFO", "file": "evolution.log"},
            "prompt": {
                "system_template": "evaluator_system_message",
                "user_template": None,
            },
        }


__all__ = ["load_config", "get_default_config"]
