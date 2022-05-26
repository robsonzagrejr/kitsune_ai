"""A method to play gym environments using human IO inputs."""
import gym
import time
from pyglet import clock
import pyglet
from nes_py._image_viewer import ImageViewer
from nes_py.wrappers import JoypadSpace

from src.game_env import SuperMarioBrosEnv


# the sentinel value for "No Operation"
_NOP = 0

class KitsuneEnv():

    def __init__(self, rom, actions, window):
        env = SuperMarioBrosEnv(rom)
        self.env = JoypadSpace(env, actions)
        self.window = window
        if hasattr(env, 'get_keys_to_action'):
            keys_to_action = self.env.get_keys_to_action()
        elif hasattr(env.unwrapped, 'get_keys_to_action'):
            keys_to_action = self.env.unwrapped.get_keys_to_action()
        else:
            raise ValueError('env has no get_keys_to_action method')
        

        self.keys_to_action = keys_to_action
        self.frame = None
        self.pyglet_frame = None
        self.KEY_MAP = {
            pyglet.window.key.ENTER: ord('\r'),
            pyglet.window.key.SPACE: ord(' '),
        }
        self.window.event(self.on_key_press)
        self.window.event(self.on_key_release)
        self.relevant_keys = set(sum(map(list, keys_to_action.keys()), []))
        self._pressed_keys = []

        self.start_game()


    @property
    def pressed_keys(self):
        """Return a sorted list of the pressed keys."""
        return tuple(sorted(self._pressed_keys))
       

    def _run_game(self, dt):
        action = self.keys_to_action.get(self.pressed_keys, _NOP)
        next_state, reward, done, _ = self.env.step(action)
        self.set_frame(self.env.unwrapped.screen)
        # pass the observation data through the callback
        state = next_state
        # shutdown if the escape key is pressed
        #if viewer.is_escape_pressed:
        #    self.stop()


    def start_game(self):
        target_frame_duration = 1 / self.env.metadata['video.frames_per_second']
        clock.schedule_interval(self._run_game, target_frame_duration)


    def stop_game(self):
        clock.unschedule(self._run_game)


    def set_frame(self, frame):
        self.frame = frame
        self.pyglet_frame = pyglet.image.ImageData(
            frame.shape[1],
            frame.shape[0],
            'RGB',
            frame.tobytes(),
            pitch=frame.shape[1]*-3
        )


    def _handle_key_event(self, symbol, is_press):
        """
        Handle a key event.
        Args:
            symbol: the symbol in the event
            is_press: whether the event is a press or release
        Returns:
            None
        """
        # remap the key to the expected domain
        symbol = self.KEY_MAP.get(symbol, symbol)
        # check if the symbol is the escape key
        if symbol == pyglet.window.key.ESCAPE:
            self._is_escape_pressed = is_press
            return
        # make sure the symbol is relevant
        if self.relevant_keys is not None and symbol not in self.relevant_keys:
            return
        # handle the press / release by appending / removing the key to pressed
        if is_press:
            self._pressed_keys.append(symbol)
        else:
            self._pressed_keys.remove(symbol)


    def on_key_press(self, symbol, modifiers):
        """Respond to a key press on the keyboard."""
        self._handle_key_event(symbol, True)


    def on_key_release(self, symbol, modifiers):
        """Respond to a key release on the keyboard."""
        self._handle_key_event(symbol, False)

    """
    @window.event
    @staticmethod
    def on_key_press(symbol, modifiers):
        print('A key was pressed')


    @window.event
    @staticmethod
    def on_draw():
        window.clear()
        label = pyglet.text.Label(f'FPS: {clock.get_fps()}',
          font_name='Times New Roman',
          font_size=36,
          x=window.width//2, y=window.height//2,
          anchor_x='center', anchor_y='center'
        )
        label.draw()

    """

