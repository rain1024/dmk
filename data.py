import yaml


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

    def play(self):
        while True:
            command = input("")
            print(command)
            if (command == 'quit' or command == 'q'):
                break


class Character:
    def __init__(self, name):
        pass
