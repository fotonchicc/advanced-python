import sys
from multiprocessing import Process, Queue
from process_a import process_a_worker
from process_b import process_b_worker
from utils import log_message


def main():
    main_to_a = Queue()
    a_to_b = Queue()
    b_to_main = Queue()

    process_a = Process(target=process_a_worker, args=(main_to_a, a_to_b))
    process_b = Process(target=process_b_worker, args=(a_to_b, b_to_main))

    process_a.start()
    process_b.start()

    try:
        print("Введите сообщения:")

        for line in sys.stdin:
            line = line.strip()
            if line:
                main_to_a.put(line)
                log_message(f"В процесс A отправлено сообщение: {line}", "MAIN")

        main_to_a.put("STOP")
        log_message("Инициировано завершение работы", "MAIN")

    except KeyboardInterrupt:
        log_message("Получен сигнал KeyboardInterrupt", "MAIN")
        main_to_a.put("STOP")

    finally:
        try:
            process_a.join(timeout=7)
            process_b.join(timeout=2)

            while not b_to_main.empty():
                log_message(b_to_main.get(), "QUEUE")

        finally:
            if process_a.is_alive():
                process_a.terminate()
            if process_b.is_alive():
                process_b.terminate()

        log_message("Программа завершена", "MAIN")


if __name__ == "__main__":
    main()
