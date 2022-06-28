"""
https://github.com/MichaelBosello/f1tenth-RL-BDI
https://github.com/MichaelBosello/jason-RL
"""
from flask import Flask, jsonify, request
import logging
from threading import Thread
import time

from src.rl.qlearning import QLearning


class KitsuneAgent():

    def __init__(self, env, view):
        self.app = Flask(__name__)
        # Removing 200 logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        self.env = env
        self.view = view
        self.process = Thread(target=self.app.run, kwargs={'port':'5003'})

        self._frame = None
        self._objects = {}
        self._reset_state = self.env.reset_state

        self.app.add_url_rule(
            '/env/<string:env>', 'route_env_info',
            self.route_env_info, methods=["POST", "GET"]
        )
        self.app.add_url_rule(
             '/env/<string:env>/<string:action>', 'route_env_action',
            self.route_env_action, methods=["POST", "GET"]
        )
        self.app.add_url_rule(
            '/agent/<string:agent_id>', 'route_agent_info',
            self.route_agent_info, methods=["post", "get"]
        )
        self.app.add_url_rule(
            '/agent/<string:agent_id>/<string:action_type>', 'route_agent_action',
            self.route_agent_action, methods=["POST", "GET"]
        )

        self.start_api()


    def start_api(self):
        self.process.start()


    #FIXME remove?
    @property
    def status(self):
        return self._frame, self._objects


    @property
    def result(self):
        state = self.env.info.get('state', None)
        reward = self.env.info.get('reward', [0, 0])
        done = self.env.info.get('done', False)

        objects = []
        if state is not None:
            objects = self.view.find_objects(state)
            self.view.frame_obj = self.view.get_image_with_objects(state, objects)

        info_objects = self.env.step_info(objects, state)
        self._objects = info_objects
        self._frame = state

        return {
            'state': info_objects,
            'reward': reward,
            'terminal': done,
        }


    def route_env_info(self, env:str):
        # Implement Env step info
        return jsonify(self.result)


    def route_env_action(self, env:str, action:str):
        # Implement Env step action

        if self.env.is_training:
            _ , reward, done = self.env.step(int(action))
        else:
            self.env.action = int(action)

        return jsonify(self.result)


    def route_agent_info(self, agent_id:str):
        json_data = request.get_json(force=True)
        print("##################################")
        print("""a_shape {}, a_type {}, a_min {}, a_max {}, o_shape {}, o_type {}, init_state {},
        agent_type {}, parameters {}""".format(json_data['a_shape'], json_data['a_type'],
        json_data['a_min'], json_data['a_max'], json_data['o_shape'], json_data['o_type'],
        json_data['init_state'], json_data['agent_type'], json_data['parameters']))
        print("##################################")
        return  {}
        if json_data['agent_type'] == "dqn":
            agent = DqnAgent(json_data['a_max'][0] + 1, json_data['o_shape'][0], json_data['parameters'], agent_id)
        agents[agent_id] = agent
        return {}


    def route_agent_action(self, agent_id:str, action_type:str):
        return jsonify({'action': [[5]]})
        json_data = request.get_json(force=True)
        #print("##################################")
        #print(json_data)
        if action_type == "next_train_action":
            action = agents[agent_id].epoch_step(np.array(json_data['state'], dtype=json_data['state_type']),
                                      json_data['reward'], json_data['is_terminal'])
        if action_type == "next_best_action":
            action = agents[agent_id].inference(np.array(json_data['state'], dtype=json_data['state_type']),
                                          json_data['reward'], json_data['is_terminal'])
        result = {'action': [int(action)]}
        #print("##################################")
        #print(result)
        return jsonify(result)

