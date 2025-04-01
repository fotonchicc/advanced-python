from multiprocessing import Queue
from utils import rot13, log_message


def process_b_worker(input_queue: Queue, output_queue: Queue) -> None:
    while True:
        message = input_queue.get()

        if message == "STOP":
            log_message("Процесс B завершает работу", "PROC_B")
            break

        encoded = rot13(message)
        log_entry = f" Encoded {message} -> {encoded}"
        log_message(log_entry, "PROC_B")
        output_queue.put(log_entry)
        print(log_entry)
