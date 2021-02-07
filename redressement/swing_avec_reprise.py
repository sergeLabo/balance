
import sys
try:
    sys.path.append('/media/data/3D/projets/balance/my_gym')
except:
    sys.path.append('my_gym')
import gym

from time import time, strftime
import numpy as np

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2


def train_avec_reprise(fichier_origin, n):
    """En partant d'un fichier déjà entrainé"""

    t0 = time()
    log = strftime("%Y%m%d-%H%M%S")
    print("Début training à:", log)

    env = make_vec_env('CartPoleSwingUpContinuous-v0', n_envs=1)
    model = PPO2.load(fichier_origin, env=env, verbose=0)

    for i in range(20):
        model.learn(total_timesteps=n)
        partial = "./weights/SR-" + log + "-" + str(i)
        model.save(partial)
        print("Model saved at", strftime("%Y%m%d-%H%M%S"))

    print("Temps d'apprentissage en heure =", round((time()-t0)/3600, 3))

def rendu(fichier_origin):

    env = make_vec_env('CartPoleSwingUpContinuous-v0', n_envs=1)
    model = PPO2.load(fichier_origin)
    obs = env.reset()
    for _ in range(1000000):
        sleep(0.009)
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)


if __name__ == '__main__':

    fichier_origin = "./weights/PPO2_Swing_2000000_35.zip"
    n = 9000000  # 9 000 000
    train_avec_reprise(fichier_origin, n)
