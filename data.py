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
        return game

    def show(self):
        print(' ================')
        print('|     STATUS     |')
        print(' ================')
        print('Gems:', self.gem)
        print('Magic:', self.magic)
        print('Cakes:', self.cakes)

        print('\n')
        print(' ================')
        print('|     TARGET     |')
        print(' ================')
        print(self.targets)

    def suggest(self):
        print('\n')
        print(' ================')
        print('|NEXT ACTIVITIES |')
        print(' ================')
        print("Next Activities")

    def play(self):
        while True:
            command = input("")
            print(command)
            if (command == 'quit' or command == 'q'):
                break


class Character:
    def __init__(self, name):
        pass
