"""
https://github.com/MichaelBosello/f1tenth-RL-BDI
https://github.com/MichaelBosello/jason-RL
"""
from flask import Flask, jsonify, request
from threading import Thread


class KitsuneAgent():

    def __init__(self, env):
        self.app = Flask(__name__)
        self.env = env
        self.process = Thread(target=self.app.run, kwargs={'port':'5003'})

        self.app.add_url_rule(
            '/env/<string:env>', 'route_env',
            self.route_env, methods=["POST", "GET"]
        )
        self.app.add_url_rule(
            '/env/<string:env>/<string:action>', 'route_action',
            self.route_action, methods=["POST", "GET"]
        )


    def _run(self):
        self.app.run(port='5003')


    def start_api(self):
        self.process.start()


    def route_env(self, env:str):
        return 'KitsuneAgent'


    def route_action(self, env:str, action:str):
        # implement Env step action

        #FIXME what will be the state?
        if self.env.is_training:
            state, reward, done = self.env.step(int(action))
        else:
            self.env.action = int(action)
            #state, reward, done = self.env.get_info()
            state, reward, done = [0], 0 , False

        result = {
            'state': state,
            'reward': reward,
            'terminal': done,
        }
        print('starting state', result)
        return jsonify(result)

