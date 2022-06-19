"""
https://github.com/MichaelBosello/f1tenth-RL-BDI
https://github.com/MichaelBosello/jason-RL
"""
from flask import Flask, jsonify, request
import logging
from threading import Thread
import time


class KitsuneAgent():

    def __init__(self, env, view):
        self.app = Flask(__name__)
        # Removing 200 logging
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


    @property
    def result(self):
        start = time.time()
        self._frame = self.env.frame
        objects = []
        if self._frame is not None:
            ob_start = time.time()
            objects = self.view.find_objects(self._frame)
            print(f"OB_Time = {time.time() - ob_start}")
            vew_start = time.time()
            self.view.frame_obj = self.view.get_image_with_objects(self._frame, objects)
            print(f"VIEW_Time = {time.time() - vew_start}")

        state = [
            [obj['type'], pt[0], pt[1], pt[2], pt[3]] #x, y, w ,h
            for obj in objects
            for pt in obj.get('pts',[])
        ]
        reward = self.env.info.get('reward', 0)
        done = self.env.info.get('done', 0)
        print(f"Time = {time.time() - start}")

        return {
            'state': state,
            'reward': float(reward),
            'terminal': bool(done),
        }


    def _run(self):
        self.app.run(port='5003')


    def start_api(self):
        self.process.start()


    def route_env(self, env:str):
        # Implement Env step info
        return jsonify(self.result)


    def route_action(self, env:str, action:str):
        # Implement Env step action

        #FIXME what will be the state?
        if self.env.is_training:
            _ , reward, done = self.env.step(int(action))
        else:
            self.env.action = int(action)

        return jsonify(self.result)

