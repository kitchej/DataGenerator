# DataGenerator

Generates dummy data. Output is customizable.

### Requirements

    Python 3.xx

### Usage:

\<arg\> = required

[arg] = optional

{arg} = default value

------------------------

Show Usage: dataGen.py help

Dates: ```dataGen.py -d \<quantity\> \<"format"\> [year_start: {1900}] [year_end: {2022}]```

Ints: ```dataGen.py -i \<quantity\> \<range start\> \<range end\>```

Floats: ```dataGen.py -f \<quantity\> \<range start\> \<range end\> [number of digits {1}]```

Names: ```dataGen.py -n \<quantity\> \<option\>```

    NAMES OPTIONS: "male", "female", "mixed", "surname", "fullmale", "fullfemale", "fullmixed"
        
Dice Rolls: ```dataGen.py -r \<quantity\> \<number of dice\>```

Coin Tosses: ```dataGen.py -t \<quantity\>```

Card Draws: ```dataGen.py -c \<quantity\> [number of decks: {1}] [discard drawn cards: {true}]```

Emails: ```dataGen.py -e \<"file path to a bank of names"(should be in csv format)\> [csv delimiter: {', '}]```

Addresses: ```dataGen.py -a \<quantity\> \<option\>```

    ADDRESSES OPTIONS: "street", "full"
        
Phone numbers: ```dataGen.py -p \<quantity\>```

User Data: ```dataGen.py n -u \<quantity\> \<"path to a data bank"(should be in csv format)\> \<allow duplicates\> [csv delimiter {','}]```

Custom: ```dataGen.py -o <quantity> <\"path to config file\"> [output delimiter: ',']```

### Instructions for Custom

The custom (-o) option requires a file containing the commands needed to generate your data.

<ol>
    <li>Create a file</li>
    <li>Place each command on a separate line</li>
    <li>Pass the path to your file to the "-o" option</li>
</ol>

Your file should look like this:

    (In ConfigFile.txt)
    ----------------
    Command 1
    Command 2
    Command 3
    ...
    Command N

And your output should look like this:
    
    >> dataGen.py -o 10 "ConfigFile.txt"

    Output of 1, Output of 2, Output of 3, ..., Output of N
    Output of 1, Output of 2, Output of 3, ..., Output of N
    Output of 1, Output of 2, Output of 3, ..., Output of N
    ...
    Output of 1, Output of 2, Output of 3, ..., Output of N

<p>
This will work for most configurations, however, there is one special case. If you want the names of randomly generated emails
to match up with randomly generated names, you will need a special command line option:
</p>

    dataGen.py -rf \<quantity\> \<"Path to config file"\> ["delimiter": {','}]

Then follow these steps:

<ol>
    <li>Create a bank of names using the "-n" option</li>
    <li>Create a file</li>
    <li>Place each command on a separate line</li>
    <li>When configuring emails, pass in the pre-generated names bank to the "-e" option</li>
    <li>When configuring names, pass in the pre-generated names bank to the "-rf" option</li>
    <li>Pass the path to your file as an argument to the "-o" option</li>
</ol>

If your input looks like this:

    (In ConfigFile.txt)
    ----------------
    dataGen.py -rf 10 "names.txt" "\n"
    dataGen.py -d 10 "%m/%d/%Y" 1990 1999
    dataGen.py -a 10 "street"
    dataGen.py -e "names.txt" "\n"

Then your output should look like this:

    >> dataGen.py -o 10 "ConfigFile.txt"

    Cruz Delgado,01/16/1999,3020 Ross Aly,cruz.delgado743@gmail.com
    Ariadne Trujillo,01/14/1993,3867 Waldo Aly,ariadne53@gmail.com
    Mallory Gutierrez,09/27/1996,9242 Evelyn Way,mallory3282@gmail.com
    Madison Rosario,07/25/1993,9840 Brotherhood Way,madison.rosario87@gmail.com
    Eli Baker,06/18/1992,8674 Saint Francis Pl,baker23@gmail.com
    Alora Gill,02/22/1992,4928 El Dorado St South,gill.alora316@gmail.com
    Harlow Spencer,07/14/1992,2628 Alta Mar Way,spencer1625@gmail.com
    Matias Rice,12/21/1995,9359 Bessie St,matias.rice8523@gmail.com
    Kash Ponce,04/11/1995,275 Valletta Ct,ponce.kash92@gmail.com
    Itzayana Simmons,02/07/1995,6352 Carr St,itzayanai855@gmail.com


***Notes***
- For custom, the length of each data bank should be the same size. Check to make sure all the commands in your config file have the same value for quantity
  - All data banks that have been pre-generated must also be the same size as the other data banks.
- Make sure to specify what delimiter you are using when reading in files. The program will attempt to read what ever you give it.
- Output is printed directly to the console. Use the '>' operator to redirect it to a file.
