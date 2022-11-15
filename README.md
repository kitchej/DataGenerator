# DataGenerator

USAGE:

\<arg\> = required

[arg] = optional

{arg} = default value

------------------------

Show Usage: DataGen.py help

Dates: DataGen.py -d \<quantity\> \<"format"\> [year_start: {1900}] [year_end: {2022}]

Ints: DataGen.py -i \<quantity\> \<range start\> \<range end\>

Floats: DataGen.py -f \<quantity\> \<range start\> \<range end\> [number of digits {1}]

Names: DataGen.py -n \<quantity\> \<option\>

    NAMES OPTIONS: "male", "female", "mixed", "surname", "fullmale", "fullfemale", "fullmixed"
        
Dice Rolls: DataGen.py -r \<quantity\> \<number of dice\>

Coin Tosses: DataGen.py -t \<quantity\>

Card Draws: DataGen.py -c \<quantity\> [number of decks: {1}] [discard drawn cards: {true}]

Emails: DataGen.py -e \<"file path to a bank of names"(should be in csv format)\> [csv delimiter: {', '}]

Addresses: DataGen.py -a \<quantity\> \<option\>

    ADDRESSES OPTIONS: "street", "full"
        
Phone numbers: DataGen.py -p \<quantity\>

User Data: DataGe.py n -u \<quantity\> \<"path to a data bank"(should be in csv format)\> \<allow duplicates\> [csv delimiter {','}]
