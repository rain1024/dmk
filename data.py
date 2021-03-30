import yaml
from peewee import *

db = SqliteDatabase('database.sqlite')
db = SqliteDatabase('database_example.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class Film(BaseModel):
    name = TextField()


class Character(BaseModel):
    name = TextField()
    film = ForeignKeyField(Film, backref='character')


class Token(BaseModel):
    name = TextField()


class Activity(BaseModel):
    name = TextField()


class Building(BaseModel):
    name = TextField()


class ActivityToken(Model):
    activity = ForeignKeyField(Activity, backref='activity_token')
    token = ForeignKeyField(Token, backref='activity_token')

    class Meta:
        database = db
        db_table = 'activity_token'


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
