import yaml
from peewee import *

db = SqliteDatabase('database.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Character(BaseModel):
    name = CharField()

characters = Character.select()
print(0)
class Game:
    def __init__(self):
        self.magic = 0
        self.gem = 0

    @staticmethod
    def load(state_file):
        state = yaml.safe_load(open(state_file))
        scores = state['scores']
        game = Game()
        game.magic = scores['magic']
        game.gem = scores['gem']
        game.cakes = scores['cakes']
        game.targets = state['targets']
        game.characters = state['characters']
        return game

    def show(self):
        print('+ STATUS:')
        print(f'- Gems ({self.gem})')
        print(f'- Magic ({self.magic})')

        print('\n+ TARGETS')
        for target in self.targets:
            print('- ' + str(target))

        print('\n+ CHARACTERS')
        for character in self.characters:
            print('- ' + str(character))

    def suggest(self):
        print('\n')
        print('+ NEXT ACTIVITIES')
        for target in self.targets:
            if "character" in target:
                character_name = target["character"]
                character = self.get_character(character_name)
                print(character.activies)

    def get_character(self, character_name):
        character = self.characters[character_name]
        return character

    def play(self):
        while True:
            command = input("")
            print(command)
            if (command == 'quit' or command == 'q'):
                break


class Character:
    def __init__(self, name):
        pass
