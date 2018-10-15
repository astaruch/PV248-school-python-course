from sys import argv
import sqlite3
import os
import scorelib


def create_tables(db_cursor, input_schema, output_db):
    with open(input_schema, 'r') as sql_schema:
        tables = sql_schema.read()
        db_cursor.executescript(tables)


def insert_voice(db_cursor, number, voice, score_id):
    db_cursor.execute(
        "INSERT INTO voice (number, score, range, name) VALUES (?, ?, ?, ?)",
        (number, score_id, voice.range, voice.name)
    )
    return db_cursor.lastrowid


def insert_score_author(db_cursor, score_id, composer_id):
    db_cursor.execute(
        "INSERT INTO score_author(score, composer) VALUES (?, ?)",
        (score_id, composer_id)
    )
    return db_cursor.lastrowid


def insert_edition_author(db_cursor, edition_id, editor_id):
    db_cursor.execute(
        "INSERT INTO edition_author(edition, editor) VALUES (?, ?)",
        (edition_id, editor_id)
    )
    return db_cursor.lastrowid


def persist_print(db_cursor, _print, edition_id):
    db_cursor.execute(
        "INSERT INTO print(partiture, edition) VALUES (?, ?)",
        ("Y" if _print.partiture else "N", edition_id)
    )
    return db_cursor.lastrowid


def score_in_db(db_cursor, score):
    db_cursor.execute(
        """SELECT id FROM score AS s WHERE (s.name = ? AND s.genre = ? AND
        s.key = ? AND s.incipit = ? AND s.year = ?)""",
        (score.name, score.genre, score.key, score.incipit, score.year)
    )
    row = db_cursor.fetchone()
    return None if row is None else row[0]


def persist_edition(db_cursor, edition, score_id):
    db_cursor.execute(
        "SELECT id FROM edition AS e WHERE (e.score = ? AND e.name = ?)",
        (score_id, edition.name)
    )
    row = db_cursor.fetchone()
    edition_id = None if row is None else row[0]
    if not edition_id:
        db_cursor.execute(
            "INSERT INTO edition(score, name, year) VALUES (?, ?, ?)",
            (score_id, edition.name, None)
        )
        return db_cursor.lastrowid
    else:
        return edition_id


def persist_person(db_cursor, person):
    # check if person is in DB
    query = "SELECT COUNT(*) FROM person WHERE person.name = ?"
    db_cursor.execute(query, (person.name,))
    row = db_cursor.fetchone()[0]
    if row == 0:
        # person is not in a db
        db_cursor.execute(
            "INSERT INTO person(born, died, name) VALUES(?, ?, ?)",
            (person.born, person.died, person.name)
        )
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


def persist_score(db_cursor, score):
    db_cursor.execute(
        """SELECT id FROM score AS s WHERE (s.name = ? AND s.genre = ? AND
        s.key = ? AND s.incipit = ? AND s.year = ?)""",
        (score.name, score.genre, score.key, score.incipit, score.year)
    )
    row = db_cursor.fetchone()
    score_id = None if row is None else row[0]
    if not score_id:
        db_cursor.execute(
            """INSERT INTO score(name, genre, key, incipit, year)
            VALUES (?, ?, ?, ?, ?)""",
            (score.name, score.genre, score.key, score.incipit, score.year)
        )
        return db_cursor.lastrowid
    else:
        return score_id


def persist_one_record(db_cursor, _print):
    score_id = persist_score(db_cursor, _print.composition())

    edition_id = persist_edition(db_cursor, _print.edition, score_id)

    persist_print(db_cursor, _print, edition_id)

    for index, voice in enumerate(_print.composition().voices):
        insert_voice(db_cursor, index + 1, voice, score_id)

    for editor in _print.edition.authors:
        editor_id = persist_person(db_cursor, editor)
        insert_edition_author(db_cursor, edition_id, editor_id)

    for composer in _print.composition().authors:
        composer_id = persist_person(db_cursor, composer)
        insert_score_author(db_cursor, score_id, composer_id)


def main():
    input_source = argv[1]
    output_db_filename = argv[2]
    if os.path.isfile(output_db_filename):
        os.remove(output_db_filename)
    db_conn = sqlite3.connect(output_db_filename)
    db_cursor = db_conn.cursor()

    sql_source_file = 'scorelib.sql'
    create_tables(db_cursor, sql_source_file, output_db_filename)

    records = scorelib.load(input_source)
    for record in records:
        persist_one_record(db_cursor, record)

    db_conn.commit()


if __name__ == '__main__':
    main()
