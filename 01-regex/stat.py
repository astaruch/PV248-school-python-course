import sys
import re
from collections import Counter

def log(msg):
    if DEBUG:
        print(msg)


def composer_stats(filepath):
    log('Detecting how many pieces by each composer...')
    log(f'Parsing {filepath!r} ...')
    stats = Counter()
    with open(filepath, 'r', encoding='utf8') as f:
        re_composer = re.compile(r"Composer: (.*)")
        for line in f:
            composer_line = re_composer.match(line)
            if composer_line: 
                # log(composer_line.group(1))
                composers = composer_line.group(1).split(';')
                for composer in composers:
                    composer = re.sub(r"\(.*\)", "", composer)
                    composer = composer.strip()
                    stats[composer] += 1
    f.closed
    del stats['']
    return stats

def century_stats(filepath):

    return


def main():
    global DEBUG
    DEBUG = False
    if '--debug' in sys.argv:
        DEBUG = True
    filepath = sys.argv[1]
    mode = sys.argv[2]
    data = []
    if mode == 'composer':
        data = composer_stats(filepath)
        data = data.most_common()
    elif mode == 'century':
        data = century_stats(filepath)
    else:
        raise Exception('Entered wrong mode...')
    for key, value in data:
        print(f'{key}: {value}')
    

if __name__ == "__main__":
    main()
    