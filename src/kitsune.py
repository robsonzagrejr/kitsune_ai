import pyglet
import time

from src.view import KitsuneView
from src.environment import KitsuneEnv 

from src.utils import (
    get_pyglet_image
)


class Kitsune():

    def __init__(self, rom, sprites_paths, env_actions):
        self.window = pyglet.window.Window()

        self.env = KitsuneEnv(rom, env_actions, self.window)
        self.view = KitsuneView(sprites_paths)

        self.window.event(self.on_draw)
        self.play()
 

    def _play_game(self, dt):
        start_time = time.time()
        frame = self.env.frame
        objects = self.view.find_objects(frame)
        self.view.frame_obj = self.view.get_image_with_objects(frame, objects)
        self.env.action = 1
        #print(f"TEMPO: {time.time() - start_time}")



    def play(self):
        pyglet.clock.schedule_interval(self._play_game, 0.1)


    def stop_play(self):
        pyglet.clock.unschedule(self._play_game)


    def start(self):
        pyglet.app.run()


    def on_draw(self):
        self.window.clear()
        label = pyglet.text.Label(f'FPS: {pyglet.clock.get_fps()}',
            font_name='Times New Roman',
            font_size=18,
            x=self.window.width//2, y=self.window.height//2,
            anchor_x='center', anchor_y='center'
        )
        if self.env.frame is not None:
            get_pyglet_image(self.env.frame).blit(0,0, width=self.window.width/2, height=self.window.height)

        if self.view.frame_obj is not None:
            get_pyglet_image(self.view.frame_obj).blit(self.window.width/2,0, width=self.window.width/2, height=self.window.height)
        label.draw()


    def show(self, frame):
        """
        Show an array of pixels on the window.
        Args:
            frame (numpy.ndarray): the frame to show on the window
        Returns:
            None
        """
        # check that the frame has the correct dimensions
        if len(frame.shape) != 3:
            raise ValueError('frame should have shape with only 3 dimensions')
        # open the window if it isn't open already
        if not self.is_open:
            self.open()
        # prepare the window for the next frame
        self._window.clear()
        self._window.switch_to()
        self._window.dispatch_events()
        # create an image data object
        image = self.pyglet.image.ImageData(
            frame.shape[1],
            frame.shape[0],
            'RGB',
            frame.tobytes(),
            pitch=frame.shape[1]*-3
        )
        # send the image to the window
        image.blit(0, 0, width=self._window.width, height=self._window.height)
        self._window.flip()

