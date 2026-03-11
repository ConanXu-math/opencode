"""
OpenEvolve Python Agent - 模块化集成
"""

from .core.analyzer import CodeAnalyzer
from .core.evaluator_builder import EvaluatorBuilder, TestCaseGenerator
from .core.auto_evaluator import AutoEvaluatorSystem
from .cli.interactive import OpenEvolveInteractive
from .cli.commands import quick_optimize, generate_evaluator
from .config import load_config, get_default_config

__version__ = "1.0.0"
__all__ = [
    "CodeAnalyzer",
    "EvaluatorBuilder",
    "TestCaseGenerator",
    "AutoEvaluatorSystem",
    "OpenEvolveInteractive",
    "quick_optimize",
    "generate_evaluator",
    "load_config",
    "get_default_config",
]
