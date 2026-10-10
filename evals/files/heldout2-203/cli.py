import argparse
import sys


def count_lines(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Count lines in text files.")
    parser.add_argument("files", nargs="+", help="files to count")
    args = parser.parse_args(argv)

    total = 0
    for path in args.files:
        total += count_lines(path)
    print(total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
