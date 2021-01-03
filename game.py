from data import Game

if __name__ == '__main__':
    game = Game.load("my_game.yml")
    game.show()
    game.suggest()
    game.play()
