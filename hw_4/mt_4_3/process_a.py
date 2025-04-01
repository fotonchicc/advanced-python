from multiprocessing import Queue
from queue import Empty
import time
from utils import log_message


def process_a_worker(input_queue: Queue, output_queue: Queue) -> None:
    while True:
        try:
            message = input_queue.get(timeout=3)

            if message == "STOP":
                output_queue.put("STOP")
                log_message("Процесс A завершает работу", "PROC_A")
                break

            processed = message.lower()
            time.sleep(5)
            output_queue.put(processed)
            log_message(f"В процесс B отправлено сообщение: {processed}", "PROC_A")

        except Empty:
            continue
