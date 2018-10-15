from sys import argv
import sqlite3
import os
import scorelib


def create_tables(db_cursor, input_schema, output_db):
    with open(input_schema, 'r') as sql_schema:
        tables = sql_schema.read()
        db_cursor.executescript(tables)


def insert_voice(db_cursor, number, voice, score_id):
    query = """
    INSERT INTO voice (number, score, range, name) VALUES (?, ?, ?, ?)
    """
    values = (number, score_id, voice.range, voice.name)
    db_cursor.execute(query, values)


def insert_edition(db_cursor, edition, score_id):
    query = "INSERT INTO edition(score, name, year) VALUES (?, ?, ?)"
    values = (score_id, edition.name, None)
    db_cursor.execute(query, values)
    return db_cursor.lastrowid


def insert_score_author(db_cursor, score_id, composer_id):
    query = "INSERT INTO score_author(score, composer) VALUES (?, ?)"
    values = (score_id, composer_id)
    db_cursor.execute(query, values)


def insert_edition_author(db_cursor, edition_id, editor_id):
    query = "INSERT INTO edition_author(edition, editor) VALUES (?, ?)"
    values = (edition_id, editor_id)
    db_cursor.execute(query, values)


def insert_print(db_cursor, _print, edition_id):
    query = "INSERT INTO print(partiture, edition) VALUES (?, ?)"
    partiture = "Y" if _print.partiture else "N"
    values = (partiture, edition_id)
    db_cursor.execute(query, values)


def insert_score(db_cursor, score):
    query = """
    INSERT INTO score(name, genre, key, incipit, year) VALUES (?, ?, ?, ?, ?)
    """
    values = (score.name, score.genre, score.key, score.incipit, score.year)
    db_cursor.execute(query, values)
    return db_cursor.lastrowid


def persist_print(db_cursor, _print):
    score_id = insert_score(db_cursor, _print.composition())

    edition_id = insert_edition(db_cursor, _print.edition, score_id)

    insert_print(db_cursor, _print, edition_id)

    for index, voice in enumerate(_print.composition().voices):
        insert_voice(db_cursor, index + 1, voice, score_id)

    for editor in _print.edition.authors:
        editor_id = persist_person(db_cursor, editor)
        insert_edition_author(db_cursor, edition_id, editor_id)

    for composer in _print.composition().authors:
        composer_id = persist_person(db_cursor, composer)
        insert_score_author(db_cursor, score_id, composer_id)


def insert_person(db_cursor, person):
    query = "INSERT INTO person(born, died, name) VALUES(?, ?, ?)"
    values = (person.born, person.died, person.name)
    db_cursor.execute(query, values)


def persist_person(db_cursor, person):
    # check if person is in DB
    query = "SELECT COUNT(*) FROM person WHERE person.name = ?"
    db_cursor.execute(query, (person.name,))
    row = db_cursor.fetchone()[0]
    if row == 0:
        # person is not in a db
        insert_person(db_cursor, person)
        return db_cursor.lastrowid
    else:
        # person is alraedy in db. try to update born+died
        query = "SELECT id, born, died FROM person WHERE person.name = ?"
        db_cursor.execute(query, (person.name,))
        row = db_cursor.fetchone()
        person_id = row[0]
        born = row[1]
        if born is None and person.born is not None:
            db_cursor.execute("UPDATE person SET born = ? WHERE name = ?",
                              (person.born, person.name))
        died = row[2]
        if died is None and person.died is not None:
            db_cursor.execute("UPDATE person SET died = ? WHERE name = ?",
                              (person.died, person.name))
        return person_id


def main():
    input_source = argv[1]
    output_db_filename = argv[2]
    if os.path.isfile(output_db_filename):
        os.remove(output_db_filename)
    db_conn = sqlite3.connect(output_db_filename)
    db_curs = db_conn.cursor()

    sql_source_file = 'scorelib.sql'
    create_tables(db_curs, sql_source_file, output_db_filename)

    prints = scorelib.load(input_source)
    for p in prints:
        persist_print(db_curs, p)

    db_conn.commit()


if __name__ == '__main__':
    main()
