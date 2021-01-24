"""
from
https://github.com/TTitcombe/CartPoleSwingUp
that is fork from
https://github.com/hardmaru/estool

on pypi
https://pypi.org/project/gym-cartpole-swingup/
https://github.com/angelolovatto/gym-cartpole-swingup


discrete Cart pole swing-up:
Adapted from:
hardmaru - https://github.com/hardmaru/estool/blob/master/custom_envs/cartpole_swingup.py
Changes:
* Discrete number of actions.
    Each action gives provides a force in a certain direction of fixed magnitude,
    as in CartPole.
* The reward function has been adapted slightly, to provide 0 reward
    when the pole is below horizontal

Original version from:
https://github.com/zuoxingdong/DeepPILCO/blob/master/cartpole_swingup.py
hardmaru's changes:
More difficult, since dt is 0.05 (not 0.01), and only 200 timesteps
"""

import sys
try:
    sys.path.append('/media/data/3D/projets/balance/my_gym')
except:
    sys.path.append('my_gym')
import gym

from gym import spaces
from gym.utils import seeding
import logging
import math
import numpy as np

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer

logger = logging.getLogger(__name__)


class CartPoleSwingUpEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array'],
                'video.frames_per_second': 50}

    def __init__(self):

        self.step_number = 0
        self.reset_number = 0
        self.action_number = 0
        self.t = 0  # timestep
        self.t_limit = 1000

        # Angle at which to fail the episode
        self.teta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4

        # #high = np.array([
            # #np.finfo(np.float32).max,
            # #np.finfo(np.float32).max,
            # #np.finfo(np.float32).max,
            # #np.finfo(np.float32).max,
            # #np.finfo(np.float32).max])

        self.action_space = spaces.Discrete(2)
        # #self.observation_space = spaces.Box(-high, high)

        self.seed()
        self.viewer = None
        self.state = None

        # Le serveur pour recevoir
        self.osc_server_init()
        self.state_updated = 0
        # Un simple client pour l'envoi
        self.client = OSCClient(b'localhost', 3001)

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

    def on_reset(self, r):
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        # Envoi à Blender d'une action à réaliser
        self.client.send_message(b'/action', [int(action)])
        # #print("Action demandée =", action)
        self.action_number += 1

        if self.step_number % 100 == 0:
            print("                    step number =", self.step_number)
        self.step_number += 1

        # Attente de la réponse
        loop = 1
        while loop:
            if self.state_updated == 1:
                x, x_dot, teta, teta_dot = self.state
                self.state_updated = 0
                loop = 0

        done = False
        if x < -self.x_threshold or x > self.x_threshold:
            done = True

        self.t += 1

        if self.t >= self.t_limit:
            done = True

        # Reward_teta is 1 when teta is 0, 0 if between 90 and 270
        reward_teta = max(0, np.cos(teta))

        # Reward_x is 0 when cart is at the edge of the screen,
        # 1 when it's in the centre
        reward_x = np.cos((x / self.x_threshold) * (np.pi / 2.0))

        # [0, 1]
        reward = reward_teta * reward_x

        obs = np.array([x, x_dot, np.cos(teta), np.sin(teta), teta_dot])

        return obs, reward, done, {}

    def reset(self):
        print("Reset ............ ")
        if self.reset_number % 10 == 0:
            print("    step reset =", self.reset_number)
        self.reset_number += 1
        print("    Nombre d'actions demandée =", self.action_number)
        self.action_number = 0

        self.state = np.random.normal(loc=np.array([0.0, 0.0, np.pi, 0.0]),
                                        scale=np.array([0.2, 0.2, 0.2, 0.2]))
        self.steps_beyond_done = None
        self.t = 0  # timestep
        x, x_dot, teta, teta_dot = self.state

        self.client.send_message(b'/reset', self.state)
        self.steps_beyond_done = None

        obs = np.array([x, x_dot, np.cos(teta), np.sin(teta), teta_dot])
        return obs

    def render(self, mode='human', close=False):
        pass
