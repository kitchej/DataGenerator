USAGE_HEADER = "USAGE:\n"\
               "<arg> = required\n"\
               "[arg] = optional\n"\
               "{arg} = default value\n"\
               "------------------------\n"\
               "Show Usage: DataGen.py help"
USAGE_DATES = "Dates: DataGen.py -d <quantity> <\"format\"> [year_start: {1900}] [year_end: {2022}]"
USAGE_INTS = "Ints: DataGen.py -i <quantity> <range start> <range end>"
USAGE_FLOAT = "Floats: DataGen.py -f <quantity> <range start> <range end> [number of digits {1}]"
USAGE_NAMES = "Names: DataGen.py -n <quantity> <option>\n"\
              "\tNAMES OPTIONS: \"male\", \"female\", \"mixed\", \"surname\", \"fullmale\", \"fullfemale\", \"fullmixed\""
USAGE_DICE = "Dice Rolls: DataGen.py -r <quantity> <number of dice>"
USAGE_COIN = "Coin Tosses: DataGen.py -t <quantity>"
USAGE_CARD = "Card Draws: DataGen.py -c <quantity> [number of decks: {1}] [discard drawn cards: {true}]"
USAGE_EMAIL = "Emails: DataGen.py -e <\"file path to a bank of names\"(should be in csv format)> [csv delimiter: {","}]"
USAGE_ADDR = "Addresses: DataGen.py -a <quantity> <option>\n"\
             "\tADDRESSES OPTIONS: \"street\", \"full\""
USAGE_PHONE = "Phone numbers: DataGen.py -p <quantity>"
USAGE_USER = "User Data: DataGe.py n -u <quantity> <\"path to a data bank\"(should be in csv format)> <allow duplicates> [csv delimiter {','}]"

FULL_USAGE = [USAGE_HEADER, USAGE_DATES, USAGE_INTS , USAGE_FLOAT, USAGE_NAMES, USAGE_DICE , USAGE_COIN , USAGE_CARD,
              USAGE_EMAIL, USAGE_ADDR, USAGE_PHONE, USAGE_USER]

def print_full_usage():
    for msg in FULL_USAGE:
        print(msg)
