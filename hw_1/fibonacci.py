def find_fib(n):
    if n == 1:
        return [1]
    t = [0] * n
    t[:2] = [1, 1]
    for i in range(n - 2):
        t[i + 2] = t[i] + t[i + 1]
    return t
