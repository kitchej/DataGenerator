import sys
from cmd_line.vet_args import FUNCS
from cmd_line.usage_msgs import *


def parse_args(args):
    accepted_options = 'difnrtceapu'
    if args[1].lower() == "help":
        print_full_usage()
        return -1
    if len(args[1]) != 2:
        print_full_usage()
        return -1
    if args[1][0] != '-':
        print_full_usage()
        return -1
    if args[1][1] not in accepted_options:
        print_full_usage()
        return -1
    out = FUNCS[args[1]](args[2:len(args)])
    if isinstance(out, int):
        return sys.exit(-1)
    for i in out:
        print(i)
    return sys.exit(0)


def main():
    if len(sys.argv) == 1:
        print_full_usage()
    else:
        parse_args(sys.argv)


if __name__ == '__main__':
    main()