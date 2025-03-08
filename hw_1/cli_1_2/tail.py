import sys
from collections import deque
from typing import Deque


def read_file(file_name: str) -> Deque[str]:
    with open(file_name, 'r') as file:
        lines = deque(file, maxlen=10)
    return lines


def print_lines(lines: Deque[str]) -> None:
    for line in lines:
        print(line, end="")


def main() -> None:
    args: int = len(sys.argv)
    if args > 1:
        count: int = 1
        for file_name in sys.argv[1:]:
            count += 1
            lines: Deque[str] = read_file(file_name)
            if args > 2:
                print(f"==> {file_name} <==")
            print_lines(lines)
            if count != args:
                print()

    else:
        lines: Deque[str] = deque(sys.stdin.readlines(), maxlen=17)
        print_lines(lines)


if __name__ == "__main__":
    main()
