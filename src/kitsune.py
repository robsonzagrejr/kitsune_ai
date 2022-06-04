import pyglet
import time
import cv2 as cv

from src.view import KitsuneView
from src.environment import KitsuneEnv 

from src.config import (
    screen,
    kitsune_images,
)

from src.utils import (
    get_pyglet_image
)


class Kitsune():

    def __init__(self, rom, sprites_paths, env_actions):
        self._window = pyglet.window.Window(width=screen['w'],height=screen['h'])

        self.env = KitsuneEnv(rom, env_actions, self._window)
        self.view = KitsuneView(sprites_paths)

        self.images = {
            "normal": get_pyglet_image(
                cv.cvtColor(
                    cv.imread(kitsune_images['normal'], 3),
                    cv.COLOR_BGR2RGB
                )
            )
        }

        self._window.event(self.on_draw)
        self.play()


    def get_kitsune_image(self):
        return self.images['normal']
 

    def _play_game(self, dt):
        start_time = time.time()
        frame = self.env.frame
        objects = self.view.find_objects(frame)
        self.view.frame_obj = self.view.get_image_with_objects(frame, objects)
        #self.env.action = 1
        #print(f"TEMPO: {time.time() - start_time}")



    def play(self):
        pyglet.clock.schedule_interval(self._play_game, 0.1)


    def stop_play(self):
        pyglet.clock.unschedule(self._play_game)


    def start(self):
        pyglet.app.run()


    def on_draw(self):
        self._window.clear()

        # Game Image
        if self.env.frame is not None:
            get_pyglet_image(self.env.frame).blit(
                x=0, y=0,
                width=self._window.width//2, height=self._window.height//2
            )

        # Kitsune View
        if self.view.frame_obj is not None:
            get_pyglet_image(self.view.frame_obj).blit(
                self._window.width//2,0,
                width=self._window.width//2, height=self._window.height//2
            )

        # FPS
        fps_label = pyglet.text.Label(f'FPS: {pyglet.clock.get_fps()}',
            font_name='Times New Roman',
            font_size=12,
            x=0, y=self._window._height-20,
            anchor_x='left', anchor_y='top'
        )
        fps_label.draw()

        # Mode
        mode = "Keyboard" if self.env.key_mode else "Auto"
        mode_label = pyglet.text.Label(f'Mode: {mode}',
            font_name='Times New Roman',
            font_size=12,
            x=self._window.width, y=self._window._height-20,
            anchor_x='right', anchor_y='top'
        )
        mode_label.draw()
        
        # Kitsune
        self.get_kitsune_image().blit(
            self._window.width//4,self._window.height//2,
            width=self._window.width//2, height=self._window.height//2
        )



