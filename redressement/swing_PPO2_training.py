
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

    n = 100001
    model.learn(total_timesteps=n)
    model.save("./weights/PPO2_Swing_" + str(n))


if __name__ == '__main__':
    t0 = time()
    train()
    t = (time()-t0)/3600
    print("Temps d'apprentissage en heure =", round(t, 3))

"""
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

"""
