from game import Game

g = Game()

for n in range(4):
    print(n)
    print(g.snake.pos)
    g.updateOnTick()
