"""
https://github.com/MichaelBosello/f1tenth-RL-BDI
https://github.com/MichaelBosello/jason-RL
"""
from flask import Flask, jsonify, request
import logging
from threading import Thread


class KitsuneAgent():

    def __init__(self, env, view):
        self.app = Flask(__name__)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        self.env = env
        self.view = view
        self.process = Thread(target=self.app.run, kwargs={'port':'5003'})

        self._frame = self.env.frame
        self._objects = {}

        self.app.add_url_rule(
            '/env/<string:env>', 'route_env',
            self.route_env, methods=["POST", "GET"]
        )
        self.app.add_url_rule(
            '/env/<string:env>/<string:action>', 'route_action',
            self.route_action, methods=["POST", "GET"]
        )

        self.start_api()


    @property
    def status(self):
        return self._frame, self._objects


    def update_status(self):
        self._frame = self.env.frame
        objects = []
        if self._frame is not None:
            objects = self.view.find_objects(self._frame)
            self.view.frame_obj = self.view.get_image_with_objects(self._frame,
                objects)
        player = [0.0]
        for obj in objects:
            if obj['type'] == 'mario':
                player = [ float(x) for x in obj['pts'][0]]
                break

        self._mario_pos = player
        return [self._mario_pos]


    def _run(self):
        self.app.run(port='5003')


    def start_api(self):
        self.process.start()


    def route_env(self, env:str):
        _ = self.env.info.get('state', [[]])
        reward = self.env.info.get('reward', 0)
        done = self.env.info.get('done', 0)

        state = self.update_status()

        result = {
            'state': state,
            'reward': float(reward),
            'terminal': bool(done),
        }
        print(result)
        return jsonify(result)


    def route_action(self, env:str, action:str):
        # implement Env step action

        #FIXME what will be the state?
        if self.env.is_training:
            _ , reward, done = self.env.step(int(action))

        else:
            self.env.action = int(action)
            #state, reward, done = self.env.get_info()
            _ , reward, done = [0], 0 , False

        state = self.update_status()

        result = {
            'state': state,
            'reward': float(reward),
            'terminal': bool(done),
        }
        print('starting state', result)
        return jsonify(result)

