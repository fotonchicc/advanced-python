import time
from threading import Thread
from multiprocessing import Process


def fib(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def sync_execution(n: int, repeats: int) -> int:
    start = time.time()
    for _ in range(repeats):
        fib(n)
    end = time.time()
    return end - start


def threading_execution(n: int, repeats: int) -> int:
    threads = []
    start = time.time()
    for _ in range(repeats):
        thread = Thread(target=fib, args=(n,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end = time.time()
    return end - start


def multiprocessing_execution(n: int, repeats: int) -> int:
    processes = []
    start = time.time()
    for _ in range(repeats):
        process = Process(target=fib, args=(n,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end = time.time()
    return end - start


if __name__ == "__main__":
    n = 35
    repeats = 10
    sync_time = sync_execution(n, repeats)
    threading_time = threading_execution(n, repeats)
    multiprocessing_time = multiprocessing_execution(n, repeats)

    with open("../artifacts/results_4_1.txt", "w", encoding="utf-8") as file:
        file.write(f"Synchronous execution: {sync_time:.2f} sec\n")
        file.write(f"Threading execution: {threading_time:.2f} sec\n")
        file.write(f"Multiprocessing execution: {multiprocessing_time:.2f} sec\n")
