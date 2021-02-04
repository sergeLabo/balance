
import sys
try:
    sys.path.append('/media/data/3D/projets/balance/my_gym')
except:
    sys.path.append('my_gym')
import gym

from time import time
import numpy as np

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2


def train():

    env = make_vec_env('CartPoleSwingUpContinuous-v0', n_envs=1)
    model = PPO2(MlpPolicy, env, verbose=0)
    n = 6000000
    model.learn(total_timesteps=n)
    model.save("./weights/PPO2_Swing_" + str(n))


if __name__ == '__main__':
    t0 = time()
    train()
    t = (time()-t0)/3600
    print("Temps d'apprentissage en heure =", round(t, 3))


"""
lancé le 04/02/2021 sur tour sans cuda
n = 6000000
correction bug msg reset x*
self.x_threshold = 8 # 2.4
self.t_limit = 2000
loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
scale=np.array([0.1, 0.1, 1.0, 0.1])
PLAGE = self.x_threshold*2/4
koeff = 1.8
angle = 0.3 # radian= 12 deg
penalty = 0.7
self.t_limit = 2000


04/02/2021
n = 3030303
Cycle n°: 1545
Steps du cycle = 2000
Steps totaux = 3030060
Récompense du cycle = 700
Efficacité du cycle = 35
Récompense totale = 902711
Efficacité globale = 0.3
Temps écoulé = 16.2

03/02/2021
PPO2_Swing_1010101
koeff = 1.8
self.x_threshold = 8 # 2.4
self.t_limit = 2000
angle = 0.3 # radian= 12 deg
penalty = 0.7
PLAGE = self.x_threshold*2/4
Cycle n°: 582
Steps du cycle = 2000
Steps totaux = 1008649
Récompense du cycle = 836
Efficacité du cycle = 41
Récompense totale = 243407
Efficacité globale = 0.24
Temps écoulé = 5.47



nuit du 1 au 2
n = 1 010 112 le meilleur, s'arrete un peu en haut,
mais ne cherche pas à stabiliser
faire train plus long et augmenter la pénalité en haut
koeff = 2
max_episode_steps=1001
self.t_limit = 1000
angle = 0.2 # radian= 12 deg
penalty = 0.8
Cycle n°: 1066
Steps du cycle = 1000
Steps totaux = 1009603
Récompense du cycle = 383
Efficacité du cycle = 38
Récompense totale = 244241
Efficacité globale = 0.24
Temps écoulé = 5.97


n = 1 510 112
koeff = 4
max_episode_steps=1001
self.t_limit = 1000
angle = 0.2 # radian= 12 deg
penalty = 0.8
Diverge le pendule finit par ne plus bouger


n = 610112
max_episode_steps=1001
self.t_limit = 1000
koeff = 1.5
angle = 0.2
penalty = 0.8
Cycle n°: 613
Steps du cycle = 1000
Steps totaux = 609374
Récompense du cycle = 567
Efficacité du cycle = 56
Récompense totale = 209525
Efficacité globale = 0.34
Temps écoulé = 3.58


n = 210112
max_episode_steps=1001
self.t_limit = 1000
Cycle n°: 259
Steps du cycle = 1000
Steps totaux = 209833
Récompense du cycle = 322
Efficacité du cycle = 32
Récompense totale = 55544
Efficacité globale = 0.26
Temps écoulé = 1.28


n = 110111
max_episode_steps=1000
self.t_limit = 1000
Cycle n°: 113
Steps du cycle = 999
Steps totaux = 109303
Récompense du cycle = 119
Efficacité du cycle = 11
Récompense totale = 32767
Efficacité globale = 0.3
Temps écoulé = 0.64



n = 1111111
Cycle n°: 1125
Steps du cycle = 999
Steps totaux = 1110074
Récompense du cycle = 375
Efficacité du cycle = 37
Récompense totale = 411430
Efficacité globale = 0.37
Temps écoulé = 6.52

n = 500001 nul ne remonte pas le pendule
    k = 1.7
    max_episode_steps=500
    Cycle n°: 1095
    Steps du cycle = 499
    Steps totaux = 499569
    Récompense du cycle = 65
    Efficacité du cycle = 13
    Récompense totale = 130021
    Efficacité globale = 0.26
    Temps écoulé = 3.54


n = 100000
    Cycle n°: 78
    Steps du cycle = 1305
    Steps totaux = 99763
    Récompense du cycle = 153
    Efficacité du cycle = 21.58
    Récompense totale = 28167
    Efficacité globale = 0.28
    Temps écoulé = 0.56

n = 100001
    Cycle n°: 53
    Steps du cycle = 1999
    Steps totaux = 99239
    Récompense du cycle = 617
    Efficacité du cycle = 1985
    Récompense totale = 39686
    Efficacité globale = 0.4
    Temps écoulé = 0.53

100002 k = 1.5
    Cycle n°: 117
    Steps du cycle = 559
    Steps totaux = 99194
    Récompense du cycle = 43
    Efficacité du cycle = 7
    Récompense totale = 16988
    Efficacité globale = 0.17
    Temps écoulé = 0.6
"""
