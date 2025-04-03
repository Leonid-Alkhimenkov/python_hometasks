import time
import threading
import multiprocessing

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} execution time: {execution_time} seconds")
        return result
    return wrapper

def fibonacci(n):
    if n in (1, 2):
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

@timer
def run_sync(n, times=1):
    for _ in range(times):
        fibonacci(n)

@timer
def run_threads(n, times=1):
    threads = []
    for _ in range(times):
        t = threading.Thread(target=fibonacci, args=(n,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

@timer
def run_processes(n, times=1):
    processes = []
    for _ in range(times):
        p = multiprocessing.Process(target=fibonacci, args=(n,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

def main():
    n = 35
    times = 10

    run_sync(n, times)
    run_threads(n, times)
    run_processes(n, times)  

if __name__ == "__main__":
    main()