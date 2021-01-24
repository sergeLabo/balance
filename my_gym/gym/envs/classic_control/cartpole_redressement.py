
from time import sleep
import math

import sys
try:
    sys.path.append('/media/data/3D/projets/balance/my_gym')
except:
    sys.path.append('my_gym')
import gym

from gym import spaces, logger
from gym.utils import seeding
import numpy as np

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import set_global_seeds, make_vec_env
from stable_baselines import ACKTR

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer


class CartPoleRedressementEnv(gym.Env):

    def __init__(self):

        print("Init de MyCartPoleEnv ...............")
        self.seed()
        self.state = None
        self.steps_beyond_done = None

        # Le serveur pour recevoir
        self.server = None
        self.osc_server_init()
        # Un simple client pour l'envoi
        self.client = OSCClient(b'localhost', 3001)

        self.state_updated = 0
        self.set_spaces()

    def set_spaces(self):

        self.action_space = spaces.Discrete(2)
        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4
        high = np.array([self.x_threshold * 2,
                         np.finfo(np.float32).max,
                         self.theta_threshold_radians * 2,
                         np.finfo(np.float32).max],
                         dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def osc_server_init(self):
        self.server = OSCThreadServer()
        self.server.listen('localhost', port=3003, default=True)
        self.server.bind(b'/result', self.on_result)
        self.server.bind(b'/reset', self.on_reset)
        self.server.bind(b'/contact', self.on_contact)

    def on_contact(self, r):
        self.state_updated = 1
        self.reset()
        self.state_updated = 0

    def on_result(self, *args):
        """result = [x, x_dot, teta, teta_dot]"""

        self.state = np.array(np.array(args))
        self.state_updated = 1

    def step(self, action):

        a = 0
        while a < 200:
            # Envoi à Blender d'une action à réaliser
            self.client.send_message(b'/action', [int(action)])
            # #print("Action demandée =", action)

            # Attente de la réponse
            loop = 1
            while loop:
                if self.state_updated == 1:
                    x, x_dot, teta, teta_dot = self.state
                    self.state_updated = 0
                    loop = 0
            a += 1

        done = bool(   teta > 0.5
                    or teta < -0.5
                    or x > 50
                    or x < -50)

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this "
                    "environment has already returned done = True. You "
                    "should always call 'reset()' once you receive 'done = "
                    "True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state), reward, done, {}

    def on_reset(self, r):
        self.reset()

    def reset(self):
        self.state = self.np_random.uniform(low=-0.005, high=0.005, size=(4,))
        print("reset: self.state =", self.state)
        self.client.send_message(b'/reset', self.state)
        self.steps_beyond_done = None
        return self.state

    def render(self, mode='human'):
        pass

    def close(self):
        pass
