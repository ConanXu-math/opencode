"""
代码分析器模块
分析Python代码结构
"""

import ast
from typing import Dict, List, Any


class CodeAnalyzer:
    """代码分析器 - 分析Python代码结构"""

    def __init__(self):
        self.functions = []
        self.imports = []
        self.complexity = 0

    def analyze(self, code: str) -> Dict[str, Any]:
        """分析代码结构"""
        try:
            tree = ast.parse(code)

            # 提取函数信息
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "doc": ast.get_docstring(node),
                        "lines": node.end_lineno - node.lineno
                        if node.end_lineno
                        else 0,
                    }
                    self.functions.append(func_info)

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        self.imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    self.imports.append(
                        f"{node.module}.{', '.join(n.name for n in node.names)}"
                    )

            # 计算复杂度 (简单启发式)
            self.complexity = len(list(ast.walk(tree)))

            return {
                "functions": self.functions,
                "imports": self.imports,
                "complexity": self.complexity,
                "has_loops": any(
                    isinstance(n, (ast.For, ast.While)) for n in ast.walk(tree)
                ),
                "has_conditionals": any(isinstance(n, ast.If) for n in ast.walk(tree)),
                "has_math_ops": any(
                    isinstance(n, (ast.BinOp, ast.UnaryOp)) for n in ast.walk(tree)
                ),
            }

        except Exception as e:
            return {"error": str(e), "functions": [], "imports": []}
