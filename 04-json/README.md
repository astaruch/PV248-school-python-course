# Memory (Data) Model

Preliminaries
- pull data from scorelib.dat using SQL
- print the results as (nicely formatted) JSON
- invocation: ./search.py Bach
- the scorelib.dat will not be your own
- you must not use the text data

Part 1
- write a script getprint.py
- the input is a print number (argument)
- the output is a list of composers (stdout)
- each composer is a dictionary
- name, born and died

Part 1 Output

        $ ./getprint.py 645
    [
        { "name": "Graupner, Christoph",
        "born": 1683, "died": 1760 },
        { "name": "Grünewald, Gottfried" }
    ]

Part 2
- write a script search.py
- the input is a composer name substring
- the output is a list of all matching composer names
- along with all their prints in the database
- hint: ... where person.name like "%Bach%"

Part 2 Output

        $ ./search.py Bach
    {
        "Bach, Johann Sebastian": [
        { "Print Number": 111,
        "Title": "Konzert für ..." , ... },
        { "Print Number": 139, ... }, ...
        ],
        "Bach, Johann Christian": ...,
        ...
    }