import concurrent.futures as cf
import threading
import logging
from time import time
from math import cos, pi


def integrate(f, a, b, *, n_jobs=1, n_iter=1000, Executor=cf.ThreadPoolExecutor):
    step = (b - a) / n_iter
    logging.basicConfig(filename='artifacts/medium.log', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(message)s',
                        datefmt='%H:%M:%S')
    log_lock = threading.Lock()

    def sum_part(curry):
        fr, to, job = curry
        with log_lock:
            logging.info(f"Started worker {job}")
        acc = 0

        for i in range(fr, to):
            acc += f(a + i * step) * step
        with log_lock:
            logging.info(f"Ended worker {job}")
        return acc

    steps_per_thr = n_iter // n_jobs

    logging.info(f"Started integrating with {n_jobs} workers")
    start = time()

    with Executor(n_jobs) as executor:
        ends = list(range(0, n_iter + steps_per_thr, steps_per_thr))
        ends[-1] = min(ends[-1], n_iter)
        total = sum(list(executor.map(sum_part, zip(ends[:-1], ends[1:], range(len(ends) - 1)))))

    elapsed = time() - start
    logging.info(f"Ended integrating with {n_jobs} workers, taken time: {elapsed * 1000:.3f} ms")
    return total, elapsed


def main():
    cpu_num = 4
    elapsed = []
    for n_jobs in range(1, cpu_num*2 + 1):
        _, t = integrate(cos, 0, pi/2, n_jobs=n_jobs)
        elapsed.append((n_jobs, t))
    with open('artifacts/medium_comparison.txt', 'w') as f:
        f.write('n_jobs\t time(ms)\n')
        f.write('\n'.join('{}\t{:.3f}'.format(i, j*1000) for i, j in elapsed))


if __name__ == '__main__':
    main()
