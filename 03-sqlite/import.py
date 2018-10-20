from sys import argv
import sqlite3
import os
import scorelib


def create_tables(db_cursor, input_schema, output_db):
    with open(input_schema, 'r') as sql_schema:
        tables = sql_schema.read()
        db_cursor.executescript(tables)


def persist_voice(db_cursor, number, voice, score_id):
    db_cursor.execute(
        "INSERT INTO voice (number, score, range, name) VALUES (?, ?, ?, ?)",
        (number, score_id, voice.range, voice.name)
    )
    return db_cursor.lastrowid


def persist_score_author(db_cursor, score_id, composer_id):
    db_cursor.execute(
        "INSERT INTO score_author(score, composer) VALUES (?, ?)",
        (score_id, composer_id)
    )
    return db_cursor.lastrowid


def persist_edition_author(db_cursor, edition_id, editor_id):
    db_cursor.execute(
        "INSERT INTO edition_author(edition, editor) VALUES (?, ?)",
        (edition_id, editor_id)
    )
    return db_cursor.lastrowid


def persist_print(db_cursor, _print, edition_id):
    db_cursor.execute(
        "INSERT INTO print(id, partiture, edition) VALUES (?, ?, ?)",
        (_print.print_id, "Y" if _print.partiture else "N", edition_id)
    )
    return db_cursor.lastrowid


def persist_score(db_cursor, score, persisted_scores):
    if score not in persisted_scores:
        db_cursor.execute(
            """INSERT INTO score(name, genre, key, incipit, year)
            VALUES (?, ?, ?, ?, ?)""",
            (score.name, score.genre, score.key, score.incipit, score.year)
        )
        score_id = db_cursor.lastrowid
        persisted_scores[score] = score_id
        return score_id
    else:
        return persisted_scores[score]


def persist_edition(db_cursor, edition, score_id, persisted_editions):
    if edition not in persisted_editions:
        db_cursor.execute(
            "INSERT INTO edition(score, name, year) VALUES (?, ?, ?)",
            (score_id, edition.name, None)
        )
        edition_id = db_cursor.lastrowid
        persisted_editions[edition] = edition_id
        return edition_id
    else:
        return persisted_editions[edition]


def persist_person(db_cursor, person, persisted_people):
    if person.name not in persisted_people:
        db_cursor.execute(
            "INSERT INTO person(born, died, name) VALUES(?, ?, ?)",
            (person.born, person.died, person.name)
        )
        person_id = db_cursor.lastrowid
        persisted_people[person.name] = person_id
        return person_id
    else:
        if person.born is not None:
            db_cursor.execute("UPDATE person SET born = ? WHERE name = ?",
                              (person.born, person.name))
        if person.died is not None:
            db_cursor.execute("UPDATE person SET died = ? WHERE name = ?",
                              (person.died, person.name))
        return persisted_people[person.name]


def persist_records(db_cursor, records):
    persisted_scores = dict()
    persisted_editions = dict()
    persisted_people = dict()
    for record in records:
            score_id = persist_score(db_cursor, record.composition(),
                                     persisted_scores)

            edition_id = persist_edition(db_cursor, record.edition, score_id,
                                         persisted_editions)

            persist_print(db_cursor, record, edition_id)

            for index, voice in enumerate(record.composition().voices):
                persist_voice(db_cursor, index + 1, voice, score_id)

            for editor in record.edition.authors:
                editor_id = persist_person(db_cursor, editor, persisted_people)
                persist_edition_author(db_cursor, edition_id, editor_id)

            for composer in record.composition().authors:
                composer_id = persist_person(db_cursor, composer,
                                             persisted_people)
                persist_score_author(db_cursor, score_id, composer_id)


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
    persist_records(db_cursor, records)

    db_conn.commit()


if __name__ == '__main__':
    main()
