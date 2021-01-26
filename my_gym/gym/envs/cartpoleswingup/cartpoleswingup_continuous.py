"""
Cart pole swing-up:
Adapted from:
hardmaru: https://github.com/hardmaru/estool/blob/master/custom_envs/cartpole_swingup.py


Original version from:
https://github.com/zuoxingdong/DeepPILCO/blob/master/cartpole_swingup.py
hardmaru's changes:
More difficult, since dt is 0.05 (not 0.01), and only 200 timesteps

voir DDPG
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

logger = logging.getLogger(__name__)


class CartPoleSwingUpContinuousEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50
    }

    def __init__(self):
        self.g = 9.82  # gravity
        self.m_c = 0.5  # cart mass
        self.m_p = 0.5  # pendulum mass
        self.total_m = (self.m_p + self.m_c)
        self.l = 0.6  # pole's length
        self.m_p_l = (self.m_p * self.l)
        self.force_mag = 10.0
        self.dt = 0.01  # seconds between state updates
        self.b = 0.1  # friction coefficient

        self.t = 0  # timestep
        self.t_limit = 1000

        # Angle at which to fail the episode
        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4

        high = np.array([
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max])

        self.action_space = spaces.Box(-1.0, 1.0, shape=(1,))
        self.observation_space = spaces.Box(-high, high)

        self._seed()
        self.viewer = None
        self.state = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        # Valid action
        action = np.clip(action, -1.0, 1.0)[0]
        action *= self.force_mag

        state = self.state
        x, x_dot, theta, theta_dot = state

        s = math.sin(theta)
        c = math.cos(theta)

        xdot_update = (-2 * self.m_p_l * (
                    theta_dot ** 2) * s + 3 * self.m_p * self.g * s * c + 4 * action - 4 * self.b * x_dot) / (
                                  4 * self.total_m - 3 * self.m_p * c ** 2)
        thetadot_update = (-3 * self.m_p_l * (theta_dot ** 2) * s * c + 6 * self.total_m * self.g * s + 6 * (
                    action - self.b * x_dot) * c) / (4 * self.l * self.total_m - 3 * self.m_p_l * c ** 2)
        x = x + x_dot * self.dt
        theta = theta + theta_dot * self.dt
        x_dot = x_dot + xdot_update * self.dt
        theta_dot = theta_dot + thetadot_update * self.dt

        self.state = (x, x_dot, theta, theta_dot)

        done = False
        if x < -self.x_threshold or x > self.x_threshold:
            done = True

        self.t += 1

        if self.t >= self.t_limit:
            done = True

        reward_theta = (np.cos(theta) + 1.0) / 2.0
        reward_x = np.cos((x / self.x_threshold) * (np.pi / 2.0))

        reward = reward_theta * reward_x

        obs = np.array([x, x_dot, np.cos(theta), np.sin(theta), theta_dot])

        return obs, reward, done, {}

    def reset(self):
        self.state = np.random.normal(loc=np.array([0.0, 0.0, np.pi, 0.0]),
                                        scale=np.array([0.2, 0.2, 0.2, 0.2]))
        self.steps_beyond_done = None
        self.t = 0  # timestep
        x, x_dot, theta, theta_dot = self.state
        obs = np.array([x, x_dot, np.cos(theta), np.sin(theta), theta_dot])
        return obs

    def render(self, mode='human', close=False):
        pass
