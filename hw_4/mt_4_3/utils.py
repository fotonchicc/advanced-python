import codecs
import datetime


def rot13(text: str) -> str:
    return codecs.encode(text, 'rot13')


def log_message(message: str, source: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{source}] {message}"

    with open("../artifacts/results_4_3.txt", "a", encoding="utf-8") as file:
        file.write(f"{log_entry}\n")
