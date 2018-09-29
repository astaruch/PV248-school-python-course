from sys import argv
import re


class Print:
    def __init__(self, print_id, edition, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        if self.print_id:
            print("Print Number: {}".format(self.print_id))

    def composition(self):
        return self.edition.composition


class Edition:
    def __init__(self, composition, name):
        self.composition = composition
        self.authors = []
        self.name = name

    def add_author(self, name, born, died):
        self.authors.append(Person(name, born, died))


class Composition:
    def __init__(self, name, incipit, key, genre, year):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = []
        self.authors = []

    def add_voice(self, voice_range, name):
        self.voices.append(Voice(voice_range, name))

    def add_author(self, name, born, died):
        self.authors.append(Person(name, born, died))


class Voice:
    def __init__(self, voice_range, name):
        self.range = voice_range
        self.name = name


class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = None if born == '' else born
        self.died = None if died == '' else died


def load(filename):
    re_print = re.compile(r'Print Number: (\d+)')
    re_composer = re.compile(r'Composer: (.*)')
    re_title = re.compile(r'Title: (.*)')
    re_genre = re.compile(r'Genre: ?(.*)?')
    re_key = re.compile(r'Key: ?(.*)?')
    re_composition_year = re.compile(r'Composition Year: ?(\d+)?')
    re_publication_year = re.compile(r'Publication Year: ?(\d+)?')
    re_edition = re.compile(r'Edition: (.*)')
    re_editor = re.compile(r'Editor: ?(.*)?')
    re_voice = re.compile(r'Voice \d+: ?(.*)?')
    re_partiture = re.compile(r'Partiture: (.*)')
    re_incipit = re.compile(r'Incipit ?\d?: ?(.*)?')
    re_new_line = re.compile(r'\n')

    prints = voice_lines = []
    with open(filename, 'r', encoding='utf8') as f:
        for line in f:
            match = re_print.match(line)
            if match:
                print_id = match.group(1)
                continue
            match = re_composer.match(line)
            if match:
                composer_line = match.group(1)
                continue
            match = re_title.match(line)
            if match:
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
                edition_title = match.group(1)
                continue
            match = re_editor.match(line)
            if match:
                editor = match.group(1)
                continue
            match = re_voice.match(line)
            if match:
                voice_lines.append(match.group(1))
                continue
            match = re_partiture.match(line)
            if match:
                partiture = True if match.group(1) == 'yes' else False
                continue
            match = re_incipit.match(line)
            if match:
                incipit = match.group(1)
                continue
            match = re_new_line.match(line)
            if match and print_id:
                composition = Composition(title, incipit, key, genre,
                                          composition_year)

                composer_line.split(';')
                for composer in composer_line.split(';'):
                    name = born = died = None
                    if '--' in composer:
                        match = re.match(r'(.*) \((\d+)?--(\d+)?.*\)',
                                         composer)
                        name = match.group(1)
                        born = match.group(2)
                        died = match.group(3)
                    else:
                        name = composer
                    composition.add_author(name, born, died)

                edition = Edition(composition, edition_title)
                record = Print(print_id, edition, partiture)

                print(record)
                record.format()
                prints.append(record)

                print_id = composer_line = title = genre = key = None
                composition_year = publication_year = edition_title = None
                editor = None
                voice_lines = []
                partiture = incipit = None
                continue
            print('Some unexpected line')
    f.closed

    return prints


def main():
    print(argv)
    load(argv[1])


if __name__ == '__main__':
    main()