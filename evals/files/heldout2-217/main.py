import sys

from parser import parse, top


def main():
    for name, score in top(parse(sys.argv[1])):
        print(f"{name}\t{score}")


if __name__ == "__main__":
    main()
