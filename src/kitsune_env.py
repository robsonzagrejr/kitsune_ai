"""
https://github.com/Kautenja/nes-py/blob/master/nes_py/app/play_human.py
https://github.com/Kautenja/nes-py/blob/master/nes_py/_image_viewer.py

"""
import pyglet
from nes_py.wrappers import JoypadSpace

from src.games.super_mario_bros_env import KitsuneSuperMarioBrosEnv


# the sentinel value for "No Operation
_NOP = 0


class KitsuneEnv():

    def __init__(self, rom, actions, window, is_training):
        _env = KitsuneSuperMarioBrosEnv(rom)
        self._env = JoypadSpace(_env, actions)

        self._window = window
        self._fps = self._env.metadata['video.frames_per_second']
        self.reward = 0
        self.score = 0
        self.episode = 0
        self.n_step = 0
        self.max_step = 60*30
        self.key_mode = not is_training
        self.action = 0
        self.is_training = is_training
        self.info = {}

        # Map between pyglet and nes-py
        self.KEY_MAP = {
            pyglet.window.key.ENTER: ord('\r'),
            pyglet.window.key.SPACE: ord(' '),
        }

        self.keys_to_action = self._env.get_keys_to_action()
        self.relevant_keys = set(sum(map(list, self.keys_to_action.keys()), []))
        self._pressed_keys = []

        # Informing the keyboard functions handler
        self._window.event(self.on_key_press)
        self._window.event(self.on_key_release)

        # Making a scheduler to game loop
        if not self.is_training:
            self.start_game()


    @property
    def pressed_keys(self):
        """Return a sorted list of the pressed keys."""
        return tuple(sorted(self._pressed_keys))
       

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

        # Check if mode was change
        if symbol == pyglet.window.key.M and not is_press:
            print(f"Change mode key_mode={self.key_mode}")
            self.key_mode = not self.key_mode
            return
        # If in key_mode, validate moviment
        if self.key_mode:
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


    @property
    def _action(self):
        if self.key_mode:
            return self.keys_to_action.get(self.pressed_keys, _NOP)
        else:
            return self.action


    def step(self, action):
        state, reward, done, _ = self._env.step(action)
        self.n_step += 1;
        self.reward = reward[0]
        self.score = reward[1]

        # Reseting when traning and get too much steps
        if self.is_training and self.n_step == self.max_step:
            done = True

        # Reseting values and env
        if done:
            _ = self._env.reset()
            self.n_step = 0
            self.episode += 1
            self.reward = 0

        self.info = {
            'state': state,
            'reward': reward,
            'done': bool(done),
        }
        return state, reward, done


    def step_info(self, objects, state):
        return self._env.step_info(objects, state)


    def _run_game(self, dt):
        self.step(self._action)


    def start_game(self):
        frame_duration = 1 / self._fps
        pyglet.clock.schedule_interval(self._run_game, frame_duration)


    def stop_game(self):
        pyglet.clock.unschedule(self._run_game)

