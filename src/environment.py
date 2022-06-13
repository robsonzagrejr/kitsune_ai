"""
https://github.com/Kautenja/nes-py/blob/master/nes_py/app/play_human.py
https://github.com/Kautenja/nes-py/blob/master/nes_py/_image_viewer.py

https://github.com/MichaelBosello/f1tenth-RL-BDI
https://github.com/MichaelBosello/jason-RL
"""
import json
import pyglet
from flask import Flask, jsonify, request
#from flask_restful import Resource, Api
from multiprocessing import Process
from threading import Thread

#import uvicorn
#from fastapi import FastAPI
#from flask import Flask

from nes_py.wrappers import JoypadSpace

from src.games.super_mario_bros_env import SuperMarioBrosEnv


# the sentinel value for "No Operation
_NOP = 0


class KitsuneEnvAPI():

    def __init__(self, env):
        #self.app = FastAPI()
        self.app = Flask(__name__)
        self.env = env
        #self.process = Process(target=self._run)
        self.process = Thread(target=self.app.run, kwargs={'port':'5003'})
        self.a = 'banana'

        self.app.add_url_rule(
            '/env/<string:id>', 'route_env',
            self.route_env, methods=["POST", "GET"]
        )
        self.app.add_url_rule(
            '/env/<string:id>/<string:action>', 'route_action',
            self.route_action, methods=["POST", "GET"]
        )


    def _run(self):
        self.app.run(port='5003')


    def start_api(self):
        self.process.start()


    def route_env(self, id:str):
        # implement Env values
        return f"HAHAHA ENV {id}"


    def route_action(self, id:str, action:str):
        # implement Env step action
        print(f'Old {self.env.action}')
        self.env.action = int(action)
        print(f"Id: {id}")
        print(f"New action {self.env.action}")
        result = {
            'state':[0],
            'reward': 0,
            'terminal': False,
        }
        print('starting state', result)
        return jsonify(result)


class KitsuneEnv():

    def __init__(self, rom, actions, window):
        _env = SuperMarioBrosEnv(rom)
        self._env = JoypadSpace(_env, actions)

        self.api = KitsuneEnvAPI(self)
        self._window = window
        self._fps = self._env.metadata['video.frames_per_second']
        self.frame = None
        self.key_mode = True
        self.action = 0

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
        self.start_game()
        self.api.start_api()


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


    def _run_game(self, dt):
        next_state, reward, done, _ = self._env.step(self._action)
        self.frame = self._env.unwrapped.screen
        state = next_state


    def start_game(self):
        frame_duration = 1 / self._fps
        pyglet.clock.schedule_interval(self._run_game, frame_duration)


    def stop_game(self):
        pyglet.clock.unschedule(self._run_game)


