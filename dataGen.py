import sys
from cmd_line import parse_args, print_full_usage


def main():
    if len(sys.argv) == 1:
        print_full_usage()
    else:
        parse_args(sys.argv)


if __name__ == '__main__':
    main()