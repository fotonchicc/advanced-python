import sys
from typing import List, Tuple, Deque


def read_file(file_name: str) -> bytes:
    with open(file_name, mode='rb') as file:
        content = file.read()
    return content


def count_statistics(content: bytes) -> Tuple[int, int, int]:
    lines_number: int = len(content.splitlines())
    # Убираем один перенос, если файл не заканчивается на символ новой строки для аналогии с самой утилитой wc
    if content and not content.endswith(b"\n"):
        lines_number -= 1
    decoded_content: str = content.decode('utf-8')
    word_number: int = len(decoded_content.split())
    bytes_number: int = len(content)
    return lines_number, word_number, bytes_number


def main() -> None:
    args: int = len(sys.argv)
    if args > 1:
        totals: List[int] = [0, 0, 0]
        statistics: List[Tuple[int, int, int, str]] = []
        files: List[str] = sys.argv[1:]
        for file_name in files:
            content: bytes = read_file(file_name)
            lines, words, bytes_ = count_statistics(content)
            totals[0] += lines
            totals[1] += words
            totals[2] += bytes_
            statistics.append((lines, words, bytes_, file_name))
        if args > 2:
            statistics.append((totals[0], totals[1], totals[2], "total"))
        max_bytes: int = max(len(str(s[2])) for s in statistics)
        for lines, words, bytes_, file_name in statistics:
            print(f"{lines:>{max_bytes}} {words:>{max_bytes}} {bytes_:>{max_bytes}} {file_name}")

    else:
        content: bytes = sys.stdin.buffer.read()
        lines, words, bytes_ = count_statistics(content)
        print(f"{lines:7} {words:7} {bytes_:7}")


if __name__ == "__main__":
    main()
