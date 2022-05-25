from pyglet import clock
import pyglet

from src.view import KitsuneView
from src.environment import KitsuneEnv 

class Kitsune():

    def __init__(self, rom, sprites_paths):
        self.view = KitsuneView(sprites_paths)
        self.env = KitsuneEnv(rom)

        self.env.start()
 

    @staticmethod
    def _play_game(self):
        print("play_game")
        pass


    def play(self):
        clock.schedule_interval(self._play_game, .5)
        pyglet.app.run()

