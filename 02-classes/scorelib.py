from sys import argv
import re


class Print:
    def __init__(self, print_id, edition, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        print('Print Number: {}'.format(self.print_id), )

    def composition(self):
        return self.edition.composition


class Edition:
    def __init__(self, composition, name):
        self.composition = composition
        self.authors = []
        self.name = name

    def add_author(self, name):
        self.authors.append(Person(name))


class Composition:
    def __init__(self, name, incipit, key, genre, year, composer):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.composer = Person(composer)
        self.voices = []
        self.authors = []

    def add_voice(self, voice_range, name):
        self.voices.append(Voice(voice_range, name))

    def add_author(self, name):
        self.authors.append(Person(name))


class Voice:
    def __init__(self, voice_range, name):
        self.range = voice_range
        self.name = name


class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = born
        self.died = died


def load(filename):
    re_print = re.compile(r'Print Number: (\d+)')
    re_composer = re.compile(r'Composer: (.*)')
    re_title = re.compile(r'Title: (.*)')
    re_genre = re.compile(r'Genre: (.*)')
    re_key = re.compile(r'Key: (.*)')
    re_composition_year = re.compile(r'Composition Year: (\d+)')
    re_publication_year = re.compile(r'Publication Year: (\d+)')
    re_edition = re.compile(r'Edition: (.*)')
    re_editor = re.compile(r'Editor: (.*)')
    re_voice = re.compile(r'Voice \d+: (.*)')
    re_partiture = re.compile(r'Partiture: (.*)')
    re_incipit = re.compile(r'Incipit: (.*)')
    re_new_line = re.compile(r'\n')

    prints = []
    with open(filename, 'r', encoding='utf8') as f:
        for line in f:
            match = re_print.match(line)
            if match:  # print number
                print_id = match.group(1)
                continue
            match = re_composer.match(line)
            if match:  # composers names and their years of born/die
                composer_line = match.group(1)
                continue
            match = re_title.match(line)
            if match:  # not used
                title = match.group(1)
                continue
            match = re_genre.match(line)
            if match:
                genre = match.group(1)
                continue
            match = re_key.match(line)
            if match:
                key = match.group(1)
                continue
            match = re_composition_year.match(line)
            if match:
                composition_year = match.group(1)
                continue
            match = re_publication_year.match(line)
            if match:
                publication_year = match.group(1)
                continue
            match = re_edition.match(line)
            if match:
                edition = match.group(1)
                continue
            match = re_editor.match(line)
            if match:
                editor = match.group(1)
                continue
            match = re_voice.match(line)
            if match:
                voice_line = match.group(1)
                continue
            match = re_partiture.match(line)
            if match:
                partiture = match.group(1)
                continue
            match = re_incipit.match(line)
            if match:
                incipit = match.group(1)
                continue
            match = re_new_line.match(line)
            if match:
                # create objects and then clear them
                print(print_id, composer_line, title, genre, key,
                      composition_year, publication_year, edition, editor,
                      voice_line, partiture, incipit)
                print_id = composer_line = title = genre = key = None
                composition_year = publication_year = edition = editor = None
                voice_line = partiture = incipit = None
    f.closed

    return prints


def main():
    print(argv)
    load(argv[1])


if __name__ == '__main__':
    main()
