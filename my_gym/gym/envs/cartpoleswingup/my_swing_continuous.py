
"""
voir les comments dans my_gym/gym/envs/cartpoleswingup/cartpoleswingup.py
"""

from time import time, strftime
from json import dumps, loads

import sys
try:
    sys.path.append('/media/data/3D/projets/balance/my_gym')
except:
    sys.path.append('my_gym')
import gym

from gym import spaces
from gym.utils import seeding
import logging
import numpy as np

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer



def write_text(fichier, ligne, mode):
    """Mode de ligne au fichier"""
    with open(fichier, mode) as fd:
        fd.write(ligne)
    fd.close()

def read_file(file_name):
    try:
        with open(file_name) as f:
            data = f.read()
        f.close()
    except:
        data = None
        print("Fichier inexistant ou impossible à lire:", file_name)


class CartPoleSwingUpContinuousEnv(gym.Env):

    def __init__(self):
        self.tzero = time()
        self.step_total = 0  # Nombre total de step
        self.t = -1  # Suivi du nombre de step dans la cycle
        self.cycle_number = 0 # Suivi du nombre de cycle
        self.t_cycle = 0

        self.x_threshold = 8 # 2.4
        self.t_limit = 2000
        self.my_reward_total = 0
        self.reward_old = 0
        # Valeur maxi de teta_dot
        self.VMAX = 1

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
        self.info = [[], [], [], []]
        self.log_file = "./log/log-" + strftime("%Y%m%d-%H%M%S") + ".txt"

    def get_self_state(self):
        """L'initialisation de self.state dans reset, valeurs changées lors de
        Hyperparameters Optimization
        np.random.normal()
            loc floats Mean (centre) of the distribution.
            scale floats Standard deviation (spread or width) of the distribution
            original => np.random.normal(loc=np.array([0.0, 0.0, np.pi, 0.0]),
                                         scale=np.array([0.2, 0.2, 0.2, 0.2]))
        Le pendule est à teta=0 en haut.
        """
        return np.random.normal(loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
                                      scale=np.array([0.1, 0.1, 2.0, 0.1]))

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
        # Calcul du temps par cycle sans le reset
        if self.t_cycle == 0:
            self.t_cycle = time()
        self.step_total += 1
        self.t += 1

        # Envoi à Blender d'une action à réaliser
        # Division par 10000 dans Blender
        self.client.send_message(b'/action', [1, int(action*5000)])

        # Attente de la réponse
        loop = 1
        while loop:
            if self.state_updated == 1:
                x, x_dot, teta, teta_dot = self.state
                self.state_updated = 0
                loop = 0

        done = False
        inf = ""
        # Fin si trop à gauche ou à droite
        if self.t > 2:
            if x < -self.x_threshold or x > self.x_threshold:
                print("\n")
                print("Stop:  x  >", self.x_threshold)
                inf = "Chariot trop à gauche ou à droite"
                done = True

        # Fin si trop de step
        if self.t >= self.t_limit:
            print("\n")
            print("Stop: step dans le cycle =", self.t_limit)
            inf = "Step dans le cycle >" + str(self.t_limit)
            done = True

        # Fin si tourne en rond soit avec vitesse forte en haut
        if self.t > 2:
            vmax = 2
            if abs(teta) < 0.05:
                if abs(teta_dot) > vmax:
                    print("\n")
                    print("Stop: vitesse en haut =",teta_dot,">",vmax,"à",teta)
                    inf = "Vitesse en haut trop rapide"
                    done = True

        reward = self.get_reward()
        self.my_reward_total += reward  # mes stats
        obs = np.array([x, x_dot, np.cos(teta), np.sin(teta), teta_dot])

        # Envoi d'info à Blender
        self.info[0] = inf.encode("utf-8")
        self.info[1] = int(self.my_reward_total)
        self.info[2] = self.t
        self.info[3] = self.step_total
        self.client.send_message(b'/info', self.info)
        self.info = [[], [], [], []]

        return obs, reward, done, {}

    def get_reward(self):
        """Calcul original
        reward_teta = max(0, np.cos(teta))
        reward_x = np.cos((x / self.x_threshold) * (np.pi / 2.0))
        reward = reward_teta * reward_x

        Mon calcul:

        chariot: si x_threshold = 8, rew=0 si x=4 ou -4, rew=1 si x=0
            PLAGE = 4 = x_threshold*2/4
            X varie de 0 à 2 Pi
            x = -4 -->  X = 0   -->  y = reward = 0
            x = 0  -->  X = Pi  -->  y = reward = 1
            x = 4  -->  X = 2Pi -->  y = reward = 0
            X = (x + PLAGE) * (np.pi/PLAGE)
            reward_chariot = 0.5*(1 - np.cos(X))

        balancier: longueur du balancier = rayon = 1
            teta = varie de 0 à 2 Pi
            teta = 0    --> y = reward = 1
            teta = Pi   --> y = reward = 0
            teta = 2Pi  --> y = reward = 1
            reward_balancier = 0.5*(np.cos(teta) + 1)
        """
        x, x_dot, teta, teta_dot = self.state

        # Chariot
        PLAGE = self.x_threshold*2/4  # = 4
        if x < -PLAGE or x > PLAGE:
            reward_chariot = 0
        else:
            X = (x + PLAGE) * (np.pi/PLAGE)
            reward_chariot = 0.5*(1 - np.cos(X))

        # Balancier
        # sans k reward_balancier = 0.5*(np.cos(teta) + 1)
        # koeff entre 1 et 2
        # si 1 --> reward sur [0, pi]
        # si 2 --> reward sur [0, pi/2]
        koeff = 1.2
        if -np.pi/koeff < teta < np.pi/koeff:
            reward_balancier = 0.5*(np.cos(teta*koeff) + 1)
        else:
            reward_balancier = 0

        # Récompense si vitesse basse en haut
        self.VMAX = max(self.VMAX, teta_dot)
        RV = 1
        angle = 0.1 # radian= 12 deg
        penalty = 0.8
        if -angle < teta < angle:
            a = - (angle / self.VMAX)
            b = 1
            K = (a * abs(teta_dot)) + b
            X = np.pi * teta / 0.2
            RV = (1 - penalty) * (0.5 * (np.cos(X) + 1)) + penalty
        else:
            RV = 1

        reward_total = reward_chariot*reward_balancier*RV

        if self.t % 240 == 0:
            beta = teta*180/np.pi
            print(  f"x = {float(x):.2f}"
                    f"\tChariot = \t{float(reward_chariot):.2f}"
                    f"\tteta = \t{int(beta)}"
                    f"\tBalancier = \t{float(reward_balancier):.2f}"
                    f"\tRV = \t{RV:.2f}"
                    f"\tTotal = \t{float(reward_total):.2f}"
                    )

        return reward_total

    def reset(self):

        print("\n    Cycle n°:", self.cycle_number)
        print("        Steps du cycle =", self.t)
        print("        Steps totaux =", self.step_total)
        print("        Récompense du cycle =",
                                    int(self.my_reward_total - self.reward_old))
        if self.t != 0:
            eff = int(100*(self.my_reward_total - self.reward_old)/self.t)
            print("        Efficacité du cycle =", eff)

        eff_tot = 0 if self.step_total == 0 else \
                                 round(self.my_reward_total/self.step_total, 2)
        print("        Récompense totale =", int(self.my_reward_total))
        print("        Efficacité globale =", eff_tot)
        self.reward_old = self.my_reward_total
        temp = time()
        theures = round((temp - self.tzero)/3600, 2)
        print("        Temps écoulé =", theures)
        if self.t != 0:
            tsc = (temp - self.t_cycle)/ self.t
            self.t_cycle = 0
            print("        Temps par step du cycle =", round(tsc, 4))

        ligne = (f"{self.step_total} {self.t} "
                 f"{self.my_reward_total} {time()}\n")
        write_text(self.log_file, ligne, "a")

        self.state = self.get_self_state()
        x, x_dot, teta, teta_dot = self.state
        self.steps_beyond_done = None
        self.t = -1
        self.cycle_number += 1

        # J'ai un gros doute sue l'envoi de float
        msg = [int(x*1000), int(x_dot*1000), int(teta*1000), int(teta_dot*1000)]
        self.client.send_message(b'/reset', msg)

        print("."*118 + "\n\n")
        print("Reset ...", msg)

        obs = np.array([x, x_dot, np.cos(teta), np.sin(teta), teta_dot])
        return obs

    def render(self):
        pass
