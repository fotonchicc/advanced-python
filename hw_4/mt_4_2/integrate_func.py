from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import math
import os
import time


def partial_integrate(f, a, step, start, end):
    partial_acc = 0
    for i in range(start, end):
        partial_acc += f(a + i * step) * step
    return partial_acc


def parallel_integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_class):
    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs
    with executor_class(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            start = i * chunk_size
            end = start + chunk_size if i != n_jobs - 1 else n_iter
            futures.append(executor.submit(partial_integrate, f, a, step, start, end))
        total = sum(future.result() for future in futures)
    return total


def compare_executors():
    cpu_num = os.cpu_count()
    results = []
    for n_jobs in range(1, cpu_num * 2 + 1):
        start = time.time()
        parallel_integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_class=ThreadPoolExecutor)
        thread_time = time.time() - start

        start = time.time()
        parallel_integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_class=ProcessPoolExecutor)
        process_time = time.time() - start
        results.append((n_jobs, thread_time, process_time))
    return results


def save_results(results):
    with open("../artifacts/results_4_2.txt", "w", encoding="utf-8") as file:
        file.write(f"n_jobs\tthread_time, sec\tprocess_time, sec\n")
        for n_jobs, thread_time, process_time in results:
            file.write(
                f"{n_jobs}\t\t{thread_time:.4f}\t\t\t\t{process_time:.4f}\n")


if __name__ == "__main__":
    results = compare_executors()
    save_results(results)
