"""
REFACTOR RESULTS:

Excluding function declarations, import statements, comments, whitespace, and the four functions I skipped, this module
went from 364 to 101 lines of code. That's a 72% decrease in lines of code!

Admittedly I gutted the sorting functionality from all the functions that had it, but there was also a TON of repeated
code, unnecessary variables, and some very bizarre design decisions. Frankly, I'm amazed at how BAD it was. Of course
I didn't know any better (it was one of my first programs), however the code still had a lot of bad smells and I'm
satisfied with the finished product.

This was by far my favorite function:

def generate_addresses(quantity, option):
    rand_addresses = []
    while True:
        if option == "Street address only":
            street = random.sample(streets, k=int(quantity))
            for i in range(int(quantity)):
                rand_addresses.append(f"{random.randint(1, 9999)} {street[i]}")
            return rand_addresses
        elif option == "Full address":
            street = random.sample(streets, k=int(quantity))
            city = random.sample(cities, k=int(quantity))
            state = random.choices(states, k=int(quantity))
            for i in range(int(quantity)):
                rand_addresses.append(f"{random.randint(1, 9999)} {street[i]}, {city[i]}, {state[i]}")
            return rand_addresses

The forever while loop that ran once was the most bizarre design decision I encountered. I have no idea why it was
written this way. If it was a mistake, then what the hell was I trying to do? If it wasn't a mistake, then what the
hell was I trying to do?
"""
import random
from datetime import datetime
import random
import os
import csv
import itertools
import data.Names as names
from data.Cards import deck
import data.Address_data as addr_data


class RangeError(Exception):
    pass


def gen_dates(quantity: int, _format: str, year_start: int = 1900, year_end: int = 2022) -> list:
    '''
    The _format parameter is passed directly to datetime.strftime(), so any C standard date code for days, months or
    years will work. (See "strftime() and strptime() Behavior" in the datetime docs for more details).

    NOTE: This function only accounts for days, months, and years when generating dates. As such, adding other
    codes (like the codes for time formatting) will result in undefined behavior.

    This function went from 104 lines of code to 16. That's an 85% decrease!
    '''
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    rand_dates = []
    day = 1
    for i in range(quantity):
        year = random.randint(year_start, year_end)
        month = random.choice(months)
        if '%d' in _format:
            if month in ("January", "March", "May", "July", "August", "October", "December"):
                day = random.randint(1, 31)
            elif month == "February":
                if (year % 400 == 0) or (year % 4 == 0) and (year % 100 != 0):
                    day = random.randint(1, 29)
                else:
                    day = random.randint(1, 28)
            else:
                day = random.randint(1, 30)
        rand_dates.append(datetime.strptime(f"{day} {month} {year}", "%d %B %Y").strftime(_format))
    return rand_dates


def gen_ints(quantity:int, start:int, end:int) -> list:
    '''
    This piece of generate_numbers() went from 5 to 3 lines of code. That's a 40% decrease!
    In total, generate_numbers() went from 11 to 6 lines of code. That's a 45% decrease!
    '''
    if end < start:
        raise RangeError("start must be less than end")
    return [random.randint(start, end) for _ in range(quantity)]


def gen_floats(quantity:int, start:float, end:float, ndigits:int=None) -> list:
    '''
    This piece of generate_numbers() went from 6 to 3 lines of code. That's a 50% decrease!
    In total, generate_numbers() went from 11 to 6 lines of code. That's a 45% decrease!
    '''
    if end < start:
        raise RangeError("start must be less than end")
    return [round(random.uniform(start, end), ndigits) for _ in range(quantity)]


def gen_names(quantity:int, option:str) -> list:
    '''
    Possible values for the option parameter: "male", "female", "mixed", "fullmale", "fullfemale", "fullmixed"

    This function went from 66 to 27 lines of code. That's a 59% decrease!
    '''
    option = option.lower()
    if option == "male":
        return random.sample(names.names_males, k=quantity)
    elif option == "female":
        return random.sample(names.names_females, k=quantity)
    elif option == "mixed":
        rand_name_females = random.sample(names.names_females, k=quantity)
        rand_name_males = random.sample(names.names_males, k=quantity)
        return [rand_name_females[i] if random.randint(0, 1) == 0 else rand_name_males[i] for i in range(quantity)]
    elif option == "surname":
        return random.sample(names.surnames, k=quantity)
    elif option == "fullmale":
        names_first = random.sample(names.names_males, k=quantity)
        names_last = random.sample(names.surnames, k=quantity)
        return [f"{names_first[i]} {names_last[i]}" for i in range(quantity)]
    elif option == "fullfemale":
        names_first = random.sample(names.names_females, k=quantity)
        names_last = random.sample(names.surnames, k=quantity)
        return [f"{names_first[i]} {names_last[i]}" for i in range(quantity)]
    elif option == "fullmixed":
        names_first_f = random.sample(names.names_females, k=quantity)
        names_first_m = random.sample(names.names_males, k=quantity)
        names_last = random.sample(names.surnames, k=quantity)
        return [f"{names_first_f[i]} {names_last[i]}" if random.randint(0, 1) == 0
                else f"{names_first_m[i]} {names_last[i]}" for i in range(quantity)]
    else:
        raise ValueError("Invalid value for option. Valid options are \"male\", \"female\", \"mixed\", \"fullmale\""
                            ", \"fullfemale\", \"fullmixed\"")


def gen_dice_rolls(quantity:int, dice:int) -> list:
    '''
    This function went from 47 lines of code to 1 line of code. That's a 98% decrease!
    '''
    return [[random.randint(1, 6) for _ in range(dice)] for _ in range(quantity)]


def gen_coin_tosses(quantity:int) -> list:
    '''
    This function went from 8 lines of code to 1 line of code. That's an 87% decrease!
    '''
    return ["h" if random.randint(0, 1) == 1 else "t" for _ in range(quantity)]


def gen_card_draws(quantity:int, num_decks:int, discard_drawn_cards:bool):
    '''
    This function went from 22 to 4 lines of code. That's an 82% decrease!
    '''
    if discard_drawn_cards:
        return random.sample(list(itertools.chain.from_iterable([deck for _ in range(num_decks)])), k=quantity)
    else:
        return random.choices(list(itertools.chain.from_iterable([deck for _ in range(num_decks)])), k=quantity)


def gen_emails(names_bank:list)->list:
    '''
    This function went from 69 lines of code to 27 lines of code. That's a 60% decrease!
    '''
    if len(names_bank) == 0:
        raise ValueError("Names bank cannot be empty")
    out = []
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "aol.com"]
    rand_domains = random.choices(domains, cum_weights=[17.74, 35.08, 32.87, 18.73], k=len(names_bank))
    for name, domain in zip(names_bank, rand_domains):
        num = random.randint(1, random.choice([99, 999, 9999]))
        if len(names_bank[0].split(" ")) == 2:
            email_name = name.split()
            var = random.randint(0,4)
            if var == 0:
                email = f"{email_name[0].lower().strip()}.{email_name[1].lower().strip()}{num}@{domain}"
            elif var == 1:
                email = f"{email_name[1].lower().strip()}.{email_name[0].lower().strip()}{num}@{domain}"
            elif var == 2:
                email = f"{email_name[1].lower().strip()}{num}@{domain}"
            elif var == 3:
                email = f"{email_name[0].lower().strip()}{email_name[1][1].lower().strip()}{num}@{domain}"
            else:
                email = f"{(email_name[0].lower()).strip()}{num}@{domain}"
        else:
            var = random.randint(0, 1)
            if var == 0:
                email =f"{name.lower().strip()}{num}@{domain}"
            else:
                email = f"{num}{name.lower().strip()}@{domain}"
        out.append(email)
    return out


def gen_addrs(quantity:int, option:str) -> list:
    '''
    This function went from 14 lines of code to 9 lines of code. That's a 35% decrease!
    '''
    if option == "street":
        return [f"{random.randint(1, 9999)} {street}" for street in random.sample(addr_data.streets, k=quantity)]
    elif option == "full":
        return [f"{random.randint(1, 9999)} {street}, {city}, {state}" for street, city, state in
                zip(random.sample(addr_data.streets, k=quantity),
                    random.sample(addr_data.cities, k=quantity),
                    random.choices(addr_data.states, k=quantity)
                )]
    else:
        raise ValueError("Invalid value for option. Possible values are \"street\" and \"full\"")


def gen_phone_num(quantity:int) -> list:
    '''
    This function went from 4 lines of code to 1 line of code. That's a 75% decrease!
    '''
    return [f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}" for _ in range(quantity)]


def gen_user_data(quantity:int, data_bank:list, sample:bool) -> list:
    '''
    This function went from 19 to 9 lines of code. That's a 53% decrease!
    '''
    if len(data_bank) == 0:
        raise ValueError("data_bank cannot be empty")
    if sample:
        if len(data_bank) < quantity:
            raise ValueError("Quantity cannot be greater than sample size")
    if sample:
        return random.sample(data_bank, k=int(quantity))
    else:
        return random.choices(data_bank, k=int(quantity))
