import concurrent.futures as cf
import time


def find_fib(n):
    if n == 1:
        return [1]
    t = [0] * n
    t[:2] = [1, 1]
    for i in range(n - 2):
        t[i + 2] = t[i] + t[i + 1]
    return t


def timeit(func):
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        return time.time() - start

    return inner


@timeit
def multithread_fib(n, times=10, workers=10):
    with cf.ThreadPoolExecutor(workers) as executor:
        executor.map(find_fib, [n] * times)


@timeit
def multiprocess_fib(n, times=10, workers=10):
    with cf.ProcessPoolExecutor(workers) as executor:
        executor.map(find_fib, [n] * times)


@timeit
def synchronous_fib(n, times=10):
    for _ in range(times):
        find_fib(n)


def main():
    N = 60_000
    times = 10
    with open('artifacts/easy.txt', 'w') as f:
        f.write(f'find {N} first fibonacci numbers, {times} times:')
        f.write('\n')
        f.write(f'synchronous - {synchronous_fib(N, times)} seconds')
        f.write('\n')
        f.write(f'multithreading - {multithread_fib(N, times)} seconds')
        f.write('\n')
        f.write(f'multiprocessing with 10 processes - {multiprocess_fib(N, times)} seconds')
        f.write('\n')
        mn = 10 ** 10
        for i in range(1, 11):
            t = multiprocess_fib(N, times, i)
            if t < mn:
                mn = t
            else:
                f.write(f'multiprocessing with {i - 1} processes - {mn} seconds')
                break


if __name__ == '__main__':
    main()
