# Objects and Classes

Parsing
- write a load(filename) function that reads the text
- this will be the same scorelib.txt as before
- the function returns a list of Print instances
- the list should be sorted by the print number (print_id)

Module
- the classes should live in scorelib.py
- add a simple test script, test.py
- this will take a single filename
- invocation: ./test.py scorelib.txt
- run load() on that filename
- call format() on each Print, add empty lines

        $ ./test.py scorelib.txt