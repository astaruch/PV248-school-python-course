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
        if self.composition().authors:
            print("Composer: {}".format(self.composition().format_authors()))
        if self.composition().name:
            print("Title: {}".format(self.composition().name))
        if self.composition().genre:
            print("Genre: {}".format(self.composition().genre))
        if self.composition().key:
            print("Key: {}".format(self.composition().key))
        if self.composition().year:
            print("Composition Year: {}".format(self.composition().year))
        if self.edition.name:
            print("Edition: {}".format(self.edition.name))
        if self.edition.authors:
            print("Editor: {}".format(self.edition.format_authors()))
        if self.composition().voices:
            i = 1
            for voice in self.composition().voices:
                print("Voice {}: {}".format(i, voice.format()))
                i = i + 1
        if self.partiture:
            print("Partiture: {}".format('yes' if self.partiture else 'no'))
        if self.composition().incipit:
            print("Incipit: {}".format(self.composition().incipit))

    def composition(self):
        return self.edition.composition


class Edition:
    def __init__(self, composition, name):
        self.composition = composition
        self.authors = []
        self.name = name

    def add_author(self, name, born, died):
        self.authors.append(Person(name, born, died))

    def format_authors(self):
        authors = []
        for author in self.authors:
            authors.append(author.format())
        return '; '.join(authors)


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

    def format_authors(self):
        authors = []
        for author in self.authors:
            authors.append(author.format())
        return '; '.join(authors)


class Voice:
    def __init__(self, voice_range, name):
        self.range = voice_range
        self.name = name

    def format(self):
        return '; '.join(filter(None, [self.range, self.name]))


class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = None if born == '' else born
        self.died = None if died == '' else died

    def format(self):
        output = self.name
        if self.born or self.died:
            output = output + ' ' + ''.join(filter(None, ['(', self.born, '--',
                                                          self.died, ')']))
        return output


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
                editor_line = match.group(1)
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

                composition = Composition(title, incipit, key, genre,
                                          composition_year)
                composer_line.split(';')
                for composer in composer_line.split(';'):
                    name = born = died = None
                    if re.search(r'\d+--?\d+', composer):
                        match = re.match(r'(.*) \((\d+)?--?(\d+)?',
                                         composer)
                        if match:
                            name = match.group(1)
                            born = match.group(2)
                            died = match.group(3)
                        else:
                            match = re.match(r'(.*) \(', composer)
                            name = match.group(1)
                    else:
                        name = composer
                    composition.add_author(name, born, died)
                for voice_line in voice_lines:
                    voice_range = voice_name = None
                    if '--' in voice_line:
                        match = re.search(r'(\w+--\w+)[,;]? ?(.*)?',
                                          voice_line)
                        voice_range = match.group(1)
                        voice_name = match.group(2)
                    else:
                        voice_name = voice_line
                    if voice_name != '':
                        composition.add_voice(voice_range, voice_name)

                edition = Edition(composition, edition_title)
                editors_substrings = editor_line.split(',')
                if len(editors_substrings) % 2 == 0:
                    name = ''
                    for idx, substring in enumerate(editors_substrings):
                        if idx % 2 == 0:
                            name = name + ', ' + substring
                        else:
                            name = name + substring
                            edition.add_author(name, None, None)
                            name = ''

                record = Print(print_id, edition, partiture)

                prints.append(record)
                continue
            match = re_new_line.match(line)
            if match and print_id:
                print_id = composer_line = title = genre = key = None
                composition_year = publication_year = edition_title = None
                editor_line = None
                voice_lines = []
                partiture = incipit = None
                continue
            print('Some unexpected line')
    f.closed

    return prints


def main():
    print(argv)
    prints = load(argv[1])
    for record in prints:
        record.format()
        print('')
    print('Size is {}'.format(len(prints)))


if __name__ == '__main__':
    main()
