# Persistent Data

Importing Data
- create an empty scorelib.dat from scorelib.sql
- start by importing composers & editors into the database
- then continue with scores &c.
- use the classes from previous exercise
- you can copy & extend them
- you can also use inheritance or composition

Database Structure
- deϐined in scorelib.sql (see study materials)
- test with: sqlite3 scorelib.dat < scorelib.sql
- you can rm scorelib.dat any time to start over
- consult comments in scorelib.sql
- do not store duplicate rows

Storing People
- the name alone must be unique
- merge born and died ϐields
− NULL iff it is None in all instances
− resolve conϐlicts arbitrarily

 Invocation
- the script should be called import.py
- ./import.py scorelib.txt scorelib.dat
- ϐirst argument is the input text ϐile
- second argument is the output SQLite ϐile
− assume that this ϐile does not exist
− the script must also set up the schema

        $ ./import.py scorelib.txt scorelib.dat