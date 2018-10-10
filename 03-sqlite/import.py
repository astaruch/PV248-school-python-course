from sys import argv
import sqlite3
import os


def create_tables(conn, c):
    query = """
create table score ( id integer primary key not null,
                     name varchar,
                     genre varchar,
                     key varchar,
                     incipit varchar,
                     year integer );
    """
    c.execute(query)
    query = """
create table voice ( id integer primary key not null,
                     number integer not null,
                     score integer references score( id ) not null,
                     range varchar,
                     name varchar );
    """
    c.execute(query)
    query = """
create table edition ( id integer primary key not null,
                       score integer references score( id ) not null,
                       name varchar,
                       year integer );
    """
    c.execute(query)
    query = """
create table score_author( id integer primary key not null,
                           score integer references score( id ) not null,
                           composer integer references person( id ) not null );
    """
    c.execute(query)
    query = """
create table edition_author( id integer primary key not null,
                             edition integer references edition( id ) not null,
                             editor integer references person( id ) not null );
    """
    c.execute(query)
    query = """
create table print ( id integer primary key not null,
                     partiture char(1) default 'N' not null,
                     edition integer references edition( id ) );
    """
    c.execute(query)
    conn.commit()


def insert_score(conn, c, score):
    query = "INSERT INTO score VALUES (?, ?, ?, ?, ?)"
    values = (score.name, score.genre, score.key, score.incipit, score.year)
    c.execute(query, values)
    conn.commit()


def insert_voice(conn, c, voice, score_id):
    query = "INSERT INTO voice VALUES (?, ?, ?, ?)"
    values = (voice.number, score_id, voice.range, voice.name)
    c.execute(query, values)
    conn.commit()


def insert_edition(conn, c, edition, score_id):
    query = "INSERT INTO edition VALUES (?, ?, ?)"
    values = (score_id, edition.name, edition.year)
    c.execute(query, values)
    conn.commit()


def insert_score_author(conn, c, score_id, composer_id):
    query = "INSERT INTO score_author VALUES (?, ?)"
    values = (score_id, composer_id)
    c.execute(query, values)
    conn.commit()


def insert_edition_author(conn, c, edition_id, editor_id):
    query = "INSERT INTO edition_autho VALUES (?, ?)"
    values = (edition_id, editor_id)
    c.execute(query, values)
    conn.commit()


def insert_print(conn, c, print, edition_id):
    query = "INSERT INTO print(?, ?)"
    values = (print, edition_id)
    c.execute(query, values)
    conn.commit()


def parse(filename):
    conn = sqlite3.connect(argv[2])
    c = conn.cursor()
    create_tables(conn, c)
    conn.close()


def main():
    if os.path.isfile(argv[2]):
        os.remove(argv[2])
    parse(argv[1])
    pass


if __name__ == '__main__':
    main()
