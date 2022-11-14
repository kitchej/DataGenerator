import gen_funcs as gen
import os
import csv
from codecs import decode
from cmd_line.usage_msgs import *


def vet_dates(args):
    if not 1 < len(args) < 5:
        print(USAGE_DATES)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Dates: Invalid value for quantity")
        return -1
    if quantity <= 0:
        print("Dates: Invalid value for quantity")
        return -1
    if len(args[1]) > 32:
        print("Dates: Format string is too long")
        return -1
    if '%' not in args[1]:
        print("Dates: Invalid format string")
        return -1
    try:
        year_start = int(args[2])
    except ValueError:
        print("Dates: Invalid year start")
        return -1
    if len(args) == 4:
        try:
            year_end = int(args[3])
        except ValueError:
            print('Dates: Invalid year end')
            return -1
    else:
        year_end = 2022
    try:
        return gen.gen_dates(quantity, args[1], year_start, year_end)
    except ValueError as e:
        print(e)
        return -1

def vet_ints(args):
    if len(args) != 3:
        print(USAGE_INTS)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Ints: Invalid value for quantity")
        return -1
    if quantity <= 0:
        print("Ints: Invalid value for quantity")
        return -1
    try:
        start = int(args[1])
    except ValueError:
        print("Ints: Invalid value for start")
        return -1
    try:
        end = int(args[2])
    except ValueError:
        print("Ints: Invalid value for end")
        return -1
    try:
        return gen.gen_ints(quantity, start, end)
    except gen.RangeError as e:
        print(e)
        return -1


def vet_floats(args):
    if not 2 < len(args) < 5:
        print(USAGE_INTS)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Floats: Invalid value for quantity")
        return -1
    if quantity <= 0:
        print("Floats: Invalid value for quantity")
        return -1
    try:
        start = float(args[1])
    except ValueError:
        print("Floats: Invalid value for start")
        return -1
    try:
        end = float(args[2])
    except ValueError:
        print("Floats: Invalid value for end")
        return -1
    if len(args) == 4:
        try:
            ndigits = int(args[3])
        except ValueError:
            print("Floats: Invalid value for number of digits")
            return -1
        if ndigtis <= 0:
            print("Floats: Invalid value for number of digits")
            return -1
    else:
        ndigits = 1
    try:
        return gen.gen_floats(quantity, start, end, ndigits)
    except gen.RangeError as e:
        print(e)
        return -1


def vet_names(args):
    if len(args) != 2:
        print(USAGE_NAMES)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Names: Invalid value for quantity")
        return -1
    if quantity <= 0:
        print("Names: Invalid value for quantity")
        return -1
    if len(args[1]) > 10:
        print("Names: Invalid value for option")
        return -1
    try:
        return gen.gen_names(quantity, args[1])
    except ValueError as e:
        print(e)
        return -1


def vet_dice(args):
    if len(args) != 2:
        print(USAGE_DICE)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Dice Rolls: Invalid value for quantity")
        return -1
    if quantity <= 0:
        print("Dice: Invalid value for quantity")
        return -1
    try:
        ndice = int(args[1])
    except ValueError:
        print("Dice Rolls: Invalid value for number of dice")
        return -1
    if ndice <= 0:
        print("Dice Rolls: Invalid value for number of dice")
        return -1

    return gen.gen_dice_rolls(quantity, ndice)


def vet_coin(args):
    if len(args) != 1:
        print(USAGE_DICE)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Coin Tosses: Invalid value for quantity")
        return -1
    if quantity <= 0:
        print("Coin Tosses: Invalid value for quantity")
        return -1
    return gen.gen_coin_tosses(quantity)


def vet_card(args):
    if not 0 < len(args) < 4:
        print(USAGE_CARD)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Card Draws: Invalid value for quantity")
        return -1
    if quantity <= 0:
        print("Card Draws: Invalid value for quantity")
        return -1
    if len(args) >= 2:
        try:
            number_of_decks = int(args[1])
        except ValueError:
            print("Card Draws: Invalid value for number of decks")
            return -1
        if number_of_decks <= 0:
            print("Card Draws: Invalid value for number of decks")
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
            print("Card Draws: Invalid value for discard drawn cards")
            return -1
    else:
        discard = True
    return gen.gen_card_draws(quantity, number_of_decks, discard)


def vet_emails(args):
    if not 0 < len(args) < 3:
        print(USAGE_EMAIL)
        return -1
    if not os.path.exists(args[0]):
        print(f"Emails: {args[0]} does not exist")
        return -1
    if os.path.isdir(args[0]):
        print(f"Emails: {args[0]} is a directory")
        return -1

    try:
        with open(args[0], 'r', encoding='utf-16') as file:
            names = file.read()
            if len(args) == 2:
                names = names.split(decode(args[1], 'unicode_escape'))
            else:
                names = names.split(',')
            if names[-1] == '':
                names.pop()
    except PermissionError:
        print("Emails: Cannot open file")
        return -1
    except OSError:
        print("Emails: Cannot open file")
        return -1

    try:
        return gen.gen_emails(names)
    except ValueError as e:
        print(e)
        return -1


def vet_addrs(args):
    if len(args) != 2:
        print(USAGE_ADDR)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Addresses: Invalid value for quantity")
        return -1
    if quantity <= 0:
        print("Addresses: Invalid value for quantity")
    if len(args[1]) > 6:
        print("Addresses: Invalid value for option")
        return -1
    try:
        return gen.gen_addrs(quantity, args[1])
    except ValueError as e:
        print(e)
        return -1



def vet_phone(args):
    if len(args) != 1:
        print(USAGE_PHONE)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("Phone Numbers: Invalid value for quantity")
        return -1
    if quantity <= 0:
        print("Phone Numbers: Invalid value for quantity")
    return gen.gen_phone_num(quantity)


def vet_user(args):
    if not 2 < len(args) < 5:
        print(USAGE_USER)
        return -1
    try:
        quantity = int(args[0])
    except ValueError:
        print("User Data: Invalid value for quantity")
        return -1
    if quantity <= 0:
        print("User Data: Invalid value for quantity")
    if not os.path.exists(args[1]):
        print(f"User Data: {args[1]} does not exist")
        return -1
    if os.path.isdir(args[1]):
        print(f"User Data: {args[1]} is a directory")
        return -1
    allow_dupes = args[2].lower()
    if allow_dupes == "true" or allow_dupes == "1":
        allow_dupes = True
    elif allow_dupes == "false" or allow_dupes == "0":
        allow_dupes = False
    else:
        print("User Data: Invalid value for allow duplicates")
        return -1
    try:
        with open(args[1], 'r', encoding='utf-16') as file:
            data = file.read()
            if len(args) == 4:
                data = data.split(decode(args[3], 'unicode_escape'))
            else:
                data = data.split(',')
            if data[-1] == '':
                data.pop()
    except PermissionError:
        print("User Data: Cannot open file")
        return -1
    except OSError:
        print("User Data: Cannot open file")
        return -1
    try:
        return gen.gen_user_data(quantity, data, allow_dupes)
    except ValueError as e:
        print(e)
        return -1


FUNCS = {'-d': vet_dates, '-i': vet_ints, '-f': vet_floats, '-n': vet_names, '-r': vet_dice, '-t': vet_coin,
         '-c': vet_card, '-e': vet_emails, '-a': vet_addrs, '-p': vet_phone, '-u': vet_user}
