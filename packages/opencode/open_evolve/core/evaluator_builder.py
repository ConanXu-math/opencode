"""
评估器构建模块
生成测试用例和评估器
"""

import json
import datetime
from typing import Dict, List, Any, Tuple, Optional


class TestCaseGenerator:
    """测试用例生成器"""

    def generate_for_function(self, func_info: Dict) -> List[Tuple]:
        """为函数生成测试用例"""
        func_name = func_info["name"]
        args = func_info["args"]
        doc = func_info.get("doc", "")

        # 基于函数名和文档的启发式规则
        test_cases = []

        if "sort" in func_name.lower() or "排序" in doc:
            # 排序函数
            test_cases = [
                ([3, 1, 2], [1, 2, 3]),
                ([5, 2, 8, 1], [1, 2, 5, 8]),
                ([], []),
                ([1], [1]),
                ([9, 8, 7, 6, 5], [5, 6, 7, 8, 9]),
            ]

        elif "sum" in func_name.lower() or "求和" in doc:
            # 求和函数
            test_cases = [
                ([1, 2, 3], 6),
                ([], 0),
                ([5], 5),
                ([10, 20, 30], 60),
                ([-1, 1], 0),
            ]

        elif "fib" in func_name.lower() or "斐波" in doc:
            # 斐波那契
            test_cases = [(0, 0), (1, 1), (5, 5), (10, 55), (20, 6765)]

        elif "max" in func_name.lower() or "最大" in doc:
            # 最大值
            test_cases = [
                ([1, 5, 3, 9, 2], 9),
                ([], None),
                ([7], 7),
                ([-1, -5, -3], -1),
            ]

        elif "filter" in func_name.lower() or "过滤" in doc:
            # 过滤函数
            test_cases = [
                ([1, 2, 3, 4, 5], [2, 4]),  # 偶数
                ([], []),
                ([1, 3, 5], []),
            ]

        else:
            # 通用测试用例
            if len(args) == 1:
                test_cases = [(1, None), (0, None), (-1, None), (10, None)]
            elif len(args) == 2:
                test_cases = [(1, 2, None), (0, 0, None), (-1, 1, None), (10, 20, None)]

        return test_cases


class EvaluatorBuilder:
    """评估器构建器"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path

    def build(self, code_path: str, analysis: Dict) -> str:
        """构建评估器代码"""

        main_func = (
            analysis["functions"][0] if analysis["functions"] else {"name": "main"}
        )
        func_name = main_func["name"]

        # 生成测试用例
        test_gen = TestCaseGenerator()
        test_cases = test_gen.generate_for_function(main_func)

        # 构建评估器模板
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evaluator_code = f'''#!/usr/bin/env python3
"""
自动生成的评估器 for {func_name}
生成时间: {timestamp}
"""

import sys
import os
import time
import json
import importlib.util
from typing import Dict, Any

def evaluate(code_path: str) -> Dict[str, Any]:
    """评估函数 - 自动生成"""
    
    # 添加代码路径到系统路径
    code_dir = os.path.dirname(code_path)
    if code_dir not in sys.path:
        sys.path.insert(0, code_dir)
    
    # 提取模块名
    module_name = os.path.basename(code_path).replace('.py', '')
    
    try:
        # 动态导入模块
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        spec = importlib.util.spec_from_file_location(module_name, code_path)
        if spec is None or spec.loader is None:
            return {{"score": 0.0, "error": "无法加载模块"}}
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
    except Exception as e:
        return {{"score": 0.0, "error": str(e)}}

    # 获取要测试的函数
    func = getattr(module, '{func_name}', None)
    if func is None:
        return {{"score": 0.0, "error": "函数 '{func_name}' 不存在"}}
    
    # 测试用例
    test_cases = {json.dumps(test_cases, ensure_ascii=False)}
    
    # 测试正确性
    correct_count = 0
    total_tests = len(test_cases)
    
    for test_input, expected in test_cases:
        try:
            # 排序函数只需要一个参数
            result = func(test_input)
            
            # 如果有期望值就验证
            if expected is not None:
                if result == expected:
                    correct_count += 1
            else:
                # 没有期望值，只要不崩溃就认为正确
                correct_count += 1
                
        except Exception:
            pass
    
    correctness = correct_count / total_tests if total_tests > 0 else 0.0
    
    # 性能测试
    if correctness > 0.5:  # 只有基本正确才测试性能
        try:
            # 创建性能测试数据
            if 'list' in str(type(test_cases[0][0])):
                # 列表类型数据
                perf_data = list(range(1000))
                start_time = time.perf_counter()
                for _ in range(100):
                    func(perf_data)
                elapsed = time.perf_counter() - start_time
            else:
                # 数值类型数据
                start_time = time.perf_counter()
                for i in range(10000):
                    func(i % 100)
                elapsed = time.perf_counter() - start_time
            
            performance = 1.0 / (1.0 + elapsed)
        except Exception:
            performance = 0.0
    else:
        performance = 0.0
    
    # 综合分数 (70%正确性 + 30%性能)
    combined_score = 0.7 * correctness + 0.3 * performance
    
    return {{
        "score": combined_score,
        "combined_score": combined_score,  # OpenEvolve需要这个字段
        "correctness": correctness,
        "performance": performance,
        "tests_passed": f"{{correct_count}}/{{total_tests}}",
        "details": {{
            "function": "{func_name}",
            "test_cases": total_tests,
            "correct_cases": correct_count
        }}
    }}

# 本地测试
if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = evaluate(sys.argv[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("请提供要评估的代码文件路径")
'''

        return evaluator_code
