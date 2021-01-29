import sys
try:
    sys.path.append('/media/data/3D/projets/balance/my_gym')
except:
    sys.path.append('my_gym')
import gym
from time import sleep

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import DDPG


def rendu():

    env_id = 'CartPoleSwingUpContinuous-v0'
    num_cpu = 1
    env = make_vec_env(env_id, n_envs=num_cpu, seed=0)

    model = DDPG.load("./weights/DDPG_Swing_101113")

    obs = env.reset()
    for _ in range(100000):
        sleep(0.009)
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        # #print(obs, rewards, dones, info)


if __name__ == '__main__':

    rendu()
