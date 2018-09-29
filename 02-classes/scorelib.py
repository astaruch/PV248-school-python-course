from sys import argv


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


def main():
    print(argv)
    pass


if __name__ == '__main__':
    main()
