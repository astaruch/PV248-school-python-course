import sys
import re
from collections import Counter


def composer_stats(filepath):
    stats = Counter()
    with open(filepath, 'r', encoding='utf8') as f:
        re_composer = re.compile(r"Composer: (.*)")
        for line in f:
            composer_line = re_composer.match(line)
            if composer_line: 
                composers = composer_line.group(1).split(';')
                for composer in composers:
                    composer = re.sub(r"\(.*\)", "", composer)
                    composer = composer.strip()
                    stats[composer] += 1
    f.closed
    del stats['']
    return stats


def century_suffix(century):
    century = int(century)
    if century % 10 == 1:
        return 'st century'
    if century % 10 == 2:
        return 'nd century'
    if century % 10 == 3:
        return 'rd century'
    return 'th century'


def century_stats(filepath):
    stats = Counter()
    with open(filepath, 'r', encoding='utf8') as f:
        re_century_line = re.compile(r"Composition Year: (.*)")
        re_year = re.compile(r".*(\d\d\d\d).*")
        re_century = re.compile(r"(\d\d?)(st|nd|rd|th) century")
        for line in f:
            century_line = re_century_line.match(line)
            if century_line and century_line.group(1) != '':
                century_line = century_line.group(1).strip()
                year = re_year.match(century_line)
                if year:
                    century = str((int(year.group(1))) // 100 + 1)
                    stats[century + century_suffix(century)] += 1
                    continue
                century = re_century.match(century_line)
                if century:
                    century = century.group(1)
                    stats[century + century_suffix(century)] += 1
                    continue
    f.closed
    del stats['']
    return stats


def main():
    filepath = sys.argv[1]
    mode = sys.argv[2]
    data = []
    if mode == 'composer':
        data = composer_stats(filepath)
    elif mode == 'century':
        data = century_stats(filepath)
    else:
        raise Exception('Entered wrong mode...')
    data = data.most_common()
    for key, value in data:
        print('{}: {}'.format(key, value))
    

if __name__ == "__main__":
    main()
    