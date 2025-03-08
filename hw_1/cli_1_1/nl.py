import sys
from typing import List


def print_numbered_lines(lines: List[str]) -> None:
    for i, line in enumerate(lines, start=1):
        print(f"{i:6}\t{line}", end="")
    if lines and not lines[-1].endswith("\n"):
        print()


def main() -> None:
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            lines: List[str] = list(file)
            print_numbered_lines(lines)

    else:
        lines: List[str] = sys.stdin.readlines()
        print_numbered_lines(lines)


if __name__ == "__main__":
    main()
