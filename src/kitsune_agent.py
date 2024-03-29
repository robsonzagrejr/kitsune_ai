"""
https://github.com/MichaelBosello/f1tenth-RL-BDI
https://github.com/MichaelBosello/jason-RL
"""
from flask import Flask, jsonify, request
import logging
from threading import Thread
import time
import json

from src.rl.qlearning import QLearning
from src.rl.sarsa import Sarsa
from src.genetic.natural_evolution import NaturalEvolution


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
        self.info = {}
        self.n_response_frame = 3

        self.agent = None

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

        if int(action) == -1:
            self.env.reset()
        elif self.env.is_training:
            # Make selected action work for next X frames
            #to simulate the human behavior
            for i in range(self.n_response_frame):
                _ , reward, done = self.env.step(int(action))
                if done:
                    break
        else:
            # Make selected action work for next X frames
            #to simulate the human behavior
            for i in range(self.n_response_frame):
                self.env.action = int(action)
                if self.env.info.get('done', False):
                    break

        return jsonify(self.result)


    def route_agent_info(self, agent_id:str):
        json_data = request.get_json(force=True)
        actions = list(range(json_data['a_min'][0], json_data['a_max'][0]+1))
        parameters = json_data['parameters']

        print("Agent".center(30,"-"))
        print(f"type: {json_data['agent_type']}")
        print(f"actions: [{min(actions)}, {max(actions)}]")
        print(f"parameters: \n{json.dumps(parameters, indent=4)}")

        if json_data['agent_type'] == "qlearning":
            self.agent = QLearning(
                len(actions)-1,
                **parameters
            )
        if json_data['agent_type'] == "py_sarsa":
            self.agent = Sarsa(
                len(actions)-1,
                **parameters
            )
        if json_data['agent_type'] == "natural_evolution":
            self.agent = NaturalEvolution(
                len(actions)-1, #Removing reset
                **parameters
            )
        self.info["algorithm"] = json_data["agent_type"]

        print("Successfully Loaded".center(30,"-"))

        return {}


    def route_agent_action(self, agent_id:str, action_type:str):
        if self.agent == None:
            raise(ValueError("Agent not initialize"))
        json_data = request.get_json(force=True)
        # Each model need to handle how the data in
        #state will be set
        state = json_data['state']
        reward = json_data['reward'] 
        done = json_data['is_terminal']
        is_training = action_type == 'next_train_action'

        action = self.agent.step(state, reward, done, is_training)
        if self.info["algorithm"] == "natural_evolution":
            self.info["specie"] = self.agent.specie
            self.info["generation"] = self.agent.generation
            self.info["acc_reward"] = self.agent._last_acc_score

        # For some reason tis need to be a list of list
        result = {'action': [[int(action)]]}
        return jsonify(result)

