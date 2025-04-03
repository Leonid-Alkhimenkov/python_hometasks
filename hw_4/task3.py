import multiprocessing
import threading
import time
import codecs
from datetime import datetime

def process_a(input_queue, output_queue):
    while True:
        if not input_queue.empty():
            message = input_queue.get()
            lower_message = message.lower()
            time.sleep(5)
            output_queue.put(lower_message)

def process_b(input_queue, output_queue):
    while True:
        if not input_queue.empty():
            message = input_queue.get()
            rot13_message = codecs.encode(message, 'rot_13')
            print(f"{datetime.now().strftime('%H:%M:%S')} process B: {rot13_message}")
            output_queue.put(rot13_message)

def main_read(queue):
    while True:
        if not queue.empty():
            received = queue.get()
            print(f"{datetime.now().strftime('%H:%M:%S')} main received: {received}")

def main():
    queue_to_a = multiprocessing.Queue()
    queue_a_to_b = multiprocessing.Queue()
    queue_b_to_main = multiprocessing.Queue()

    proc_a = multiprocessing.Process(target=process_a, args=(queue_to_a, queue_a_to_b))
    proc_b = multiprocessing.Process(target=process_b, args=(queue_a_to_b, queue_b_to_main))

    main_reader_thread = threading.Thread(target=main_read, args=(queue_b_to_main,), daemon=True)

    proc_a.start()
    proc_b.start()
    main_reader_thread.start()

    try:
        while True:
            user_input = input(f"{datetime.now().strftime('%H:%M:%S')} main: enter message: ")
            queue_to_a.put(user_input)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        proc_a.terminate()
        proc_b.terminate()
        proc_a.join()
        proc_b.join()
        print("Processes terminated.")

if __name__ == "__main__":
    main()