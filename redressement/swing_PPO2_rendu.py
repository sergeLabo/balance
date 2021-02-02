import sys
try:
    sys.path.append('/media/data/3D/projets/balance/my_gym')
except:
    sys.path.append('my_gym')
import gym
from time import sleep

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2


def rendu():

    env = make_vec_env('CartPoleSwingUpContinuous-v0', n_envs=1)

    model = PPO2.load("./weights/PPO2_Swing_1010112.zip")

    obs = env.reset()
    for _ in range(1000000):
        sleep(0.009)
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)


if __name__ == '__main__':

    rendu()
