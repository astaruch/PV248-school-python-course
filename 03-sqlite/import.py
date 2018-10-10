from sys import argv
import sqlite3
import os


def create_tables(conn, c):
    query = """create table score ( id integer primary key not null,
                     name varchar,
                     genre varchar,
                     key varchar,
                     incipit varchar,
                     year integer );
    """
    c.execute(query)
    query = """create table voice ( id integer primary key not null,
                     number integer not null,
                     score integer references score( id ) not null,
                     range varchar,
                     name varchar );
    """
    c.execute(query)
    query = """create table edition ( id integer primary key not null,
                       score integer references score( id ) not null,
                       name varchar,
                       year integer );
    """
    c.execute(query)
    query = """create table score_author( id integer primary key not null,
                           score integer references score( id ) not null,
                           composer integer references person( id ) not null );
    """
    c.execute(query)
    query = """create table edition_author( id integer primary key not null,
                             edition integer references edition( id ) not null,
                             editor integer references person( id ) not null );
    """
    c.execute(query)
    query = """create table print ( id integer primary key not null,
                     partiture char(1) default 'N' not null,
                     edition integer references edition( id ) );
    """
    c.execute(query)
    conn.commit()
    conn.close()


def parse(filename):
    conn = sqlite3.connect(argv[2])
    c = conn.cursor()
    create_tables(conn, c)


def main():
    if os.path.isfile(argv[2]):
        os.remove(argv[2])
    parse(argv[1])
    pass


if __name__ == '__main__':
    main()
