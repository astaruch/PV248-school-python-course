from sys import argv
import scorelib


def main():
    prints = scorelib.load(argv[1])
    for record in prints:
        record.format()
        print('')


if __name__ == '__main__':
    main()
