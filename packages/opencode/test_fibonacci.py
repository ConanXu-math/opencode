def fibonacci(n):
    """计算斐波那契数列的第n项"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_iterative(n):
    """迭代版本的斐波那契数列"""
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    # 测试两个函数
    for i in range(10):
        print(f"fibonacci({i}) = {fibonacci(i)}")
        print(f"fibonacci_iterative({i}) = {fibonacci_iterative(i)}")
