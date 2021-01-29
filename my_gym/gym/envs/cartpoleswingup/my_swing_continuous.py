
"""
voir les comments dans my_gym/gym/envs/cartpoleswingup/cartpoleswingup.py
"""

from time import time
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


class CartPoleSwingUpContinuousEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array'],
                'video.frames_per_second': 50}

    def __init__(self):
        self.tzero = time()
        self.step_total = 0  # Nombre total de step
        self.t = -1  # Suivi du nombre de step dans la cycle
        self.cycle_number = 0 # Suivi du nombre de cycle

        self.x_threshold = 8 # 2.4
        self.t_limit = 2000
        self.my_reward_total = 0
        self.reward_old = 0

        high = np.array([
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max])

        # Action Continue dans [-1, 1]
        self.action_space = spaces.Box(-1.0, 1.0, shape=(1,))
        self.observation_space = spaces.Box(-high, high)

        self.seed()
        self.viewer = None
        self.state = None

        self.osc_server_init()
        self.state_updated = 0
        self.client = OSCClient(b'localhost', 3001)

    def get_self_state(self):
        """L'initialisation de self.state dans reset, valeurs changées lors de
        Hyperparameters Optimization
        """
        return np.random.normal(loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
                                      scale=np.array([0.1, 0.1, 5, 0.1]))

    def osc_server_init(self):
        self.server = OSCThreadServer()
        self.server.listen('localhost', port=3003, default=True)
        self.server.bind(b'/result', self.on_result)
        self.server.bind(b'/reset', self.on_reset)
        self.server.bind(b'/contact', self.on_contact)

    def on_contact(self, r):
        self.state_updated = 1
        print("reset demandé par on_contact")
        self.reset()
        self.state_updated = 0

    def on_result(self, *args):
        """result = [x, x_dot, teta, teta_dot]"""

        self.state = np.array(np.array(args))
        self.state_updated = 1

    def on_reset(self, r):
        print("reset demandé par on_reset")
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.step_total += 1
        self.t += 1

        # Envoi à Blender d'une action à réaliser
        self.client.send_message(b'/action', [1, int(action*500)])


        # Attente de la réponse
        loop = 1
        while loop:
            if self.state_updated == 1:
                x, x_dot, teta, teta_dot = self.state
                self.state_updated = 0
                loop = 0

        done = False
        # un reset est fait aussi par max_episode_steps=1000
        # si self.t_limit=1000
        if self.t > 2:
            if x < -self.x_threshold or x > self.x_threshold:
                print("\n\n\n\n..............................................")
                print("Stop:  x  >", self.x_threshold)
                done = True


        if self.t >= self.t_limit:
            print("\n\n\n\n..............................................")
            print("Stop: step dans le cycle =", self.t_limit)
            done = True


        reward = self.get_reward()
        self.my_reward_total += reward  # mes stats
        obs = np.array([x, x_dot, np.cos(teta), np.sin(teta), teta_dot])

        return obs, reward, done, {}

    def get_reward(self):
        """Calcul original
        reward_teta = max(0, np.cos(teta))
        reward_x = np.cos((x / self.x_threshold) * (np.pi / 2.0))
        reward = reward_teta * reward_x

        Mon calcul:

        chariot: si x_threshold = 8, rew=0 si x=6 ou -6, rew=1 si x=0
                PLAGE = 6 = x_threshold*3/4
                sin va de -1 à 1, donc il faut +1
                1 + math.sin((x+PLAGE)*(np.pi/2*PLAGE))

        balancier: longueur du balancier = LONG = 3
            rew=0 si teta=pi=en bas, rew=1 si teta=0=2pi
                sin((x+LONG)(np.pi/4*LONG))
        """
        x, x_dot, teta, teta_dot = self.state

        # Chariot
        PLAGE = self.x_threshold*3/4  # = 6
        if x < -PLAGE or x > PLAGE:
            reward_chariot = 0
        else:
            X = (x + PLAGE) * (np.pi/PLAGE)
            reward_chariot = 0.5*(1 - np.cos(X))

        # Balancier
        X = (1 + np.cos(teta)) * (np.pi/2)
        reward_balancier = 0.5*(1 - np.cos(X))

        reward_total = reward_chariot*reward_balancier

        if self.t % 20 == 0:
            beta = teta*180/np.pi
            print(  f"x = {float(x):.2}"
                    f"\tChariot = \t{float(reward_chariot):.2}"
                    f"\tteta = \t{float(teta):.2}"
                    f"\t{int(beta)}"
                    f"\tBalancier =\t{float(reward_balancier):.2}"
                    f"\tTotal\t{float(reward_total):.2}")

        return reward_total

    def reset(self):
        """np.random.normal()
            loc floats Mean (centre) of the distribution.
            scale floats Standard deviation (spread or width) of the distribution

            np.random.normal(   loc=np.array([0.0, 0.0, np.pi, 0.0]),
                              scale=np.array([0.2, 0.2, 0.2, 0.2]))
        Le pendule est à teta=0 en haut, pi est ajouté dans always.py pour
        avoir le zero en bas.
        """
        print("Reset ...")
        print("    Cycle n°:", self.cycle_number)
        print("                    Steps du cycle =", self.t)
        print("                      Steps totaux =", self.step_total)
        print("                        Récompense du cycle =",
                                    int(self.my_reward_total - self.reward_old))
        if self.t != 0:
            eff = round((self.my_reward_total/self.t), 2)
            print("                        Efficacité du cycle =", eff)

        eff_tot = 0 if self.step_total == 0 else \
                                round(self.my_reward_total/self.step_total, 2)
        print("                 Récompense totale =", int(self.my_reward_total))
        print("                Efficacité globale =", eff_tot)
        self.reward_old = self.my_reward_total
        theures = round((time() - self.tzero)/3600, 2)
        print("                      Temps écoulé =", theures)

        # np.pi remplacé par 3.141592654
        # #self.state = np.random.normal(loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
                                      # #scale=np.array([0.1, 0.1, 5, 0.1]))
        self.state = self.get_self_state()

        x, x_dot, teta, teta_dot = self.state

        self.steps_beyond_done = None
        self.t = -1
        self.cycle_number += 1

        self.client.send_message(b'/reset', self.state)
        obs = np.array([x, x_dot, np.cos(teta), np.sin(teta), teta_dot])
        return obs

    def render(self, mode='human', close=False):
        pass
