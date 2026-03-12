def fibonacci(n):
    """计算斐波那契数列的第n项"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_iterative(n):
    """迭代方式计算斐波那契数列"""
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def main():
    """测试函数"""
    print("斐波那契数列测试:")
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")

    print("\n迭代版本测试:")
    for i in range(10):
        print(f"fib_iterative({i}) = {fibonacci_iterative(i)}")


if __name__ == "__main__":
    main()
