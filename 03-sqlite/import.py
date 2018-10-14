from sys import argv
import sqlite3
import os


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


def create_tables(db_connection, db_cursor, input_schema, output_db):
    with open(input_schema, 'r') as sql_schema:
        tables = sql_schema.read()
        db_cursor.executescript(tables)
        db_connection.commit()


def main():
    input_source = argv[1]
    output_db_filename = argv[2]
    if os.path.isfile(output_db_filename):
        os.remove(output_db_filename)
    db_conn = sqlite3.connect(output_db_filename)
    db_curs = db_conn.cursor()

    sql_source_file = 'scorelib.sql'
    create_tables(db_conn, db_curs, sql_source_file, output_db_filename)


if __name__ == '__main__':
    main()
