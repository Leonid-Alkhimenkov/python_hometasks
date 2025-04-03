import math
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import cpu_count

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.4f} seconds")
        return result
    return wrapper

def compute_chunk(f, a, step, start, end):
    acc = 0
    for i in range(start, end):
        acc += f(a + i * step) * step
    return acc

def integrate(f, a, b, *, n_jobs=1, n_iter=10000000):
    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs
    futures = []

    with executor_type(n_jobs) as executor:
        for i in range(n_jobs):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i != n_jobs - 1 else n_iter
            futures.append(executor.submit(compute_chunk, f, a, step, start, end))

        total = sum(future.result() for future in futures)
    return total

@timer
def run_integration(f, a, b, n_jobs, executor_name):
    global executor_type
    executor_type = ThreadPoolExecutor if executor_name == "ThreadPoolExecutor" else ProcessPoolExecutor
    return integrate(f, a, b, n_jobs=n_jobs)

def main():
    func = math.cos
    a = 0
    b =math.pi / 2
    max_jobs = cpu_count() * 2

    for n_jobs in range(1, max_jobs + 1):
        print(f"n_jobs = {n_jobs}")
        
        print("ThreadPoolExecutor:")
        run_integration(func, a, b, n_jobs, "ThreadPoolExecutor")

        print("ProcessPoolExecutor:")
        run_integration(func, a, b, n_jobs, "ProcessPoolExecutor")

if __name__ == "__main__":
    main()