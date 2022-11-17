from codecs import decode
import csv
import itertools
import os
import sys
import shlex

import gen_funcs as gen


USAGE_HEADER = "USAGE:\n"\
               "<arg> = required\n"\
               "[arg] = optional\n"\
               "{arg} = default value\n"\
               "------------------------\n"\
               "Show Usage: dataGen.py help"
USAGE_DATES = "Dates: dataGen.py -d <quantity> <\"format\"> [year_start: {1900}] [year_end: {2022}]"
USAGE_INTS = "Ints: dataGen.py -i <quantity> <range start> <range end>"
USAGE_FLOAT = "Floats: dataGen.py -f <quantity> <range start> <range end> [number of digits {1}]"
USAGE_NAMES = "Names: dataGen.py -n <quantity> <option>\n"\
              "\tNAMES OPTIONS: \"male\", \"female\", \"mixed\", \"surname\", \"fullmale\", \"fullfemale\", \"fullmixed\""
USAGE_DICE = "Dice Rolls: dataGen.py -r <quantity> <number of dice>"
USAGE_COIN = "Coin Tosses: dataGen.py -t <quantity>"
USAGE_CARD = "Card Draws: dataGen.py -c <quantity> [number of decks: {1}] [discard drawn cards: {true}]"
USAGE_EMAIL = "Emails: dataGen.py -e <\"file path to a bank of names\"(should be in csv format)> [csv delimiter: {","}]"
USAGE_ADDR = "Addresses: dataGen.py -a <quantity> <option>\n"\
             "\tADDRESSES OPTIONS: \"street\", \"full\""
USAGE_PHONE = "Phone numbers: dataGen.py -p <quantity>"
USAGE_USER = "User Data: dataGen.py -u <quantity> <\"path to a data bank\"(should be in csv format)> <allow duplicates> [csv delimiter {','}]"
USAGE_CUSTOM = "Custom: dataGen.py -o <quantity> <\"path to config file\"> [output delimiter: ',']"

FULL_USAGE = [USAGE_HEADER, USAGE_DATES, USAGE_INTS , USAGE_FLOAT, USAGE_NAMES, USAGE_DICE , USAGE_COIN , USAGE_CARD,
              USAGE_EMAIL, USAGE_ADDR, USAGE_PHONE, USAGE_USER]


def print_full_usage():
    for msg in FULL_USAGE:
        print(msg)


def read_in(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf') as file:
            return file.read()
    except PermissionError:
        return ""
    except OSError:
        return ""


def parse_args(args, called_from_custom=False):
    accepted_options = 'difnrtceapuo'
    if args[1].lower() == "help":
        print_full_usage()
        return -1
    if args[1].lower() == "-rf":
        return vet_read_file(args[2:len(args)])
    if len(args[1]) != 2:
        print_full_usage()
        return -1
    if args[1][0] != '-':
        print_full_usage()
        return -1
    if args[1][1] not in accepted_options:
        print_full_usage()
        return -1

    if called_from_custom:
        return FUNCS[args[1]](args[2:len(args)])
    else:
        out = FUNCS[args[1]](args[2:len(args)])
        if isinstance(out, int):
            sys.exit(-1)
        # print(','.join(str(item) for item in out)) for true csv
        for i in out:
            print(i)
        sys.exit(0)


def vet_dates(args):
    if not 1 < len(args) < 5:
        print(USAGE_DATES)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Dates: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("Dates: Invalid value for quantity", file=sys.stderr)
        return -1
    if len(args[1]) > 32:
        print("Dates: Format string is too long", file=sys.stderr)
        return -1
    if '%' not in args[1]:
        print("Dates: Invalid format string", file=sys.stderr)
        return -1
    if len(args) == 4:
        try:
            year_start = int(args[2])
        except ValueError:
            print("Dates: Invalid year start", file=sys.stderr)
            return -1
    else:
        year_start = 1900
    if len(args) == 4:
        try:
            year_end = int(args[3])
        except ValueError:
            print('Dates: Invalid year end', file=sys.stderr)
            return -1
    else:
        year_end = 2022
    try:
        return gen.gen_dates(quantity, args[1], year_start, year_end)
    except ValueError as e:
        print(e, file=sys.stderr)
        return -1

def vet_ints(args):
    if len(args) != 3:
        print(USAGE_INTS)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Ints: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("Ints: Invalid value for quantity", file=sys.stderr)
        return -1
    try:
        start = int(args[1])
    except ValueError:
        print("Ints: Invalid value for start", file=sys.stderr)
        return -1
    try:
        end = int(args[2])
    except ValueError:
        print("Ints: Invalid value for end", file=sys.stderr)
        return -1
    try:
        return gen.gen_ints(quantity, start, end)
    except gen.RangeError as e:
        print(e, file=sys.stderr)
        return -1


def vet_floats(args):
    if not 2 < len(args) < 5:
        print(USAGE_FLOATS)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Floats: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("Floats: Invalid value for quantity", file=sys.stderr)
        return -1
    try:
        start = float(args[1])
    except ValueError:
        print("Floats: Invalid value for start", file=sys.stderr)
        return -1
    try:
        end = float(args[2])
    except ValueError:
        print("Floats: Invalid value for end", file=sys.stderr)
        return -1
    if len(args) == 4:
        try:
            ndigits = int(args[3])
        except ValueError:
            print("Floats: Invalid value for number of digits", file=sys.stderr)
            return -1
        if ndigits <= 0:
            print("Floats: Invalid value for number of digits", file=sys.stderr)
            return -1
    else:
        ndigits = 1
    try:
        return gen.gen_floats(quantity, start, end, ndigits)
    except gen.RangeError as e:
        print(e, file=sys.stderr)
        return -1


def vet_names(args):
    if len(args) != 2:
        print(USAGE_NAMES)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Names: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("Names: Invalid value for quantity", file=sys.stderr)
        return -1
    if len(args[1]) > 10:
        print("Names: Invalid value for option", file=sys.stderr)
        return -1
    try:
        return gen.gen_names(quantity, args[1])
    except ValueError as e:
        print(e, file=sys.stderr)
        return -1


def vet_dice(args):
    if len(args) != 2:
        print(USAGE_DICE)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Dice Rolls: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("Dice: Invalid value for quantity", file=sys.stderr)
        return -1
    try:
        ndice = int(args[1])
    except ValueError:
        print("Dice Rolls: Invalid value for number of dice", file=sys.stderr)
        return -1
    if ndice <= 0:
        print("Dice Rolls: Invalid value for number of dice", file=sys.stderr)
        return -1

    return gen.gen_dice_rolls(quantity, ndice)


def vet_coin(args):
    if len(args) != 1:
        print(USAGE_DICE)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Coin Tosses: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("Coin Tosses: Invalid value for quantity", file=sys.stderr)
        return -1
    return gen.gen_coin_tosses(quantity)


def vet_card(args):
    if not 0 < len(args) < 4:
        print(USAGE_CARD)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Card Draws: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("Card Draws: Invalid value for quantity", file=sys.stderr)
        return -1
    if len(args) >= 2:
        try:
            number_of_decks = int(args[1])
        except ValueError:
            print("Card Draws: Invalid value for number of decks", file=sys.stderr)
            return -1
        if number_of_decks <= 0:
            print("Card Draws: Invalid value for number of decks", file=sys.stderr)
            return -1
    else:
        number_of_decks = 0
    if len(args) == 3:
        discard = args[2].lower()
        if discard == "true" or discard == "1":
            discard = True
        elif discard == "false" or discard == "0":
            discard = False
        else:
            print("Card Draws: Invalid value for discard drawn cards", file=sys.stderr)
            return -1
    else:
        discard = True
    return gen.gen_card_draws(quantity, number_of_decks, discard)


def vet_emails(args):
    if not 0 < len(args) < 3:
        print(USAGE_EMAIL)
        return -1
    if not os.path.exists(args[0]):
        print(f"Emails: {args[0]} does not exist", file=sys.stderr)
        return -1
    if os.path.isdir(args[0]):
        print(f"Emails: {args[0]} is a directory", file=sys.stderr)
        return -1
    names = read_in(args[0])
    if names == "":
        print("Emails: Cannot open file", file=sys.stderr)
        return -1
    if len(args) == 2:
        names = names.split(decode(args[1], 'unicode_escape'))
    else:
        names = names.split(',')
    if names[-1] == '':
        names.pop()
    try:
        return gen.gen_emails(names)
    except ValueError as e:
        print(e, file=sys.stderr)
        return -1


def vet_addrs(args):
    if len(args) != 2:
        print(USAGE_ADDR)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Addresses: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("Addresses: Invalid value for quantity", file=sys.stderr)
    if len(args[1]) > 6:
        print("Addresses: Invalid value for option", file=sys.stderr)
        return -1
    try:
        return gen.gen_addrs(quantity, args[1])
    except ValueError as e:
        print(e, file=sys.stderr)
        return -1



def vet_phone(args):
    if len(args) != 1:
        print(USAGE_PHONE)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Phone Numbers: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("Phone Numbers: Invalid value for quantity", file=sys.stderr)
    return gen.gen_phone_num(quantity)


def vet_user(args):
    if not 2 < len(args) < 5:
        print(USAGE_USER)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("User Data: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("User Data: Invalid value for quantity", file=sys.stderr)
    if not os.path.exists(args[1]):
        print(f"User Data: {args[1]} does not exist", file=sys.stderr)
        return -1
    if os.path.isdir(args[1]):
        print(f"User Data: {args[1]} is a directory", file=sys.stderr)
        return -1
    allow_dupes = args[2].lower()
    if allow_dupes == "true" or allow_dupes == "1":
        allow_dupes = True
    elif allow_dupes == "false" or allow_dupes == "0":
        allow_dupes = False
    else:
        print("User Data: Invalid value for allow duplicates", file=sys.stderr)
        return -1
    data = read_in(args[1])
    if data == "":
        print("User Data: Cannot open file", file=sys.stderr)
        return -1
    if len(args) == 4:
        data = data.split(decode(args[3], 'unicode_escape'))
    else:
        data = data.split(',')
    if data[-1] == '':
        data.pop()

    try:
        return gen.gen_user_data(quantity, data, allow_dupes)
    except ValueError as e:
        print(e, file=sys.stderr)
        return -1


def vet_custom(args):
    if not 1 < len(args) < 4:
        print(USAGE_CUSTOM)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Custom: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("Custom: Invalid value for quantity", file=sys.stderr)
    if not os.path.exists(args[1]):
        print(f"Custom: {args[1]} does not exist", file=sys.stderr)
        return -1
    if os.path.isdir(args[1]):
        print(f"Custom: {args[1]} is a directory", file=sys.stderr)
        return -1
    if len(args) == 3:
        if len(args[2]) > 1:
            print(f"Custom: Invalid output delimiter", file=sys.stderr)
            return -1
        delim = decode(args[2], 'unicode_escape')
    else:
        delim = ','

    cmds = read_in(args[1])
    cmds = cmds.split('\n')
    if cmds[-1] == '':
        cmds.pop()

    # Split the arguments as the shell would
    args_lyst = [shlex.split(c) for c in cmds]
    # Get the results
    data = [parse_args(in_args, True) for in_args in args_lyst]
    if -1 in data:
        print(f"Issue on line {data.index(-1) + 1} in custom config file.", file=sys.stderr)
        return -1
    # Make all lists the same size
    try:
        data = [d[0:quantity] if len(d) >= quantity else -1 for d in data]
    except TypeError:
        print("Custom: All data sets must have the same size. Check config file.", file=sys.stderr)
        return -1
    # Combine all the lists
    try:
        result = list(itertools.zip_longest(*data))
    except TypeError as e:
        print(e, file=sys.stderr)
        return -1
    out = []
    string = ""
    for row in result:
        for col in row:
            if string != "":
                string = f"{string}{delim}{col}"
            else:
                string = col
        out.append(string)
        string = ""
    return out

def vet_read_file(args):
    if not 1 < len(args) < 4:
        print("READ FILE: dataGen.py -rf <quantity> <\"Path to file\"> [csv delimiter: {','}]", file=sys.stderr)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("READ FILE: Invalid value for quantity", file=sys.stderr)
        return -1
    if quantity <= 0:
        print("READ FILE: Invalid value for quantity", file=sys.stderr)
    if not os.path.exists(args[1]):
        print(f"READ FILE: {args[1]} does not exist", file=sys.stderr)
        return -1
    if os.path.isdir(args[1]):
        print(f"READ FILE: {args[1]} is a directory", file=sys.stderr)
        return -1
    data = read_in(args[1])
    if len(args) == 3:
        delim = decode(args[2], 'unicode_escape')
    else:
        delim = ','
    data = data.split(delim)
    return data if data[-1] != "" else data.pop()

FUNCS = {'-d': vet_dates, '-i': vet_ints, '-f': vet_floats, '-n': vet_names, '-r': vet_dice, '-t': vet_coin,
         '-c': vet_card, '-e': vet_emails, '-a': vet_addrs, '-p': vet_phone, '-u': vet_user, '-o': vet_custom}