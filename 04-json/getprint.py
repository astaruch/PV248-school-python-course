from sys import argv
import json
import sqlite3


def main():
    print_number = argv[1]
    db_connection = sqlite3.connect("scorelib.dat")
    db_cursor = db_connection.cursor()
    score_id = db_cursor.execute(
        """SELECT score.id FROM print
        INNER JOIN edition ON print.edition = edition.id
        INNER JOIN score ON edition.score = score.id
        WHERE print.id = ?""",
        (print_number,)
    ).fetchall()[0][0]
    composers_db = db_cursor.execute(
        """SELECT name, born, died FROM score_author
        INNER JOIN person ON score_author.composer = person.id
        WHERE score_author.score = ?""",
        (score_id,)
    ).fetchall()
    composers = []
    for composer in composers_db:
        person = {}
        if composer[0]:
            person['name'] = composer[0]
        if composer[1]:
            person['born'] = composer[1]
        if composer[2]:
            person['died'] = composer[2]
        composers.append(person)
    print(json.dumps(composers, indent=2, ensure_ascii=False))
    db_connection.close()


if __name__ == '__main__':
    main()
