from itertools import zip_longest
import peewee
from data import *


def load_characters():
    def grouper(iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    lines = open("data/characters.txt").read().splitlines()
    groups = grouper(lines, 2)
    print('- Init characters and films')
    for group in groups:
        film, characters = group
        film_id = Film.create(name=film)
        characters = characters.split(' · ')
        for character_name in characters:
            character_id = Character.create(name=character_name, film=film_id)


if __name__ == '__main__':
    models = [
        Character, Token, Activity, Building, Film,
        ActivityToken
    ]
    for model in models:
        model.create_table()
    print("Init Database")
    load_characters()
