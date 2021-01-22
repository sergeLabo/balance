
import sys
sys.path.append('my_gym')
import gym

from time import sleep

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines.common import set_global_seeds, make_vec_env
from stable_baselines import ACKTR


def rendu():

    env_id = "My-CartPole-v0"
    num_cpu = 1
    env = make_vec_env(env_id, n_envs=num_cpu, seed=0)

    model = ACKTR.load("./weights/acktr_blender_250000_1")

    obs = env.reset()
    for _ in range(100000):
        sleep(0.02)
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        print(obs, rewards, dones, info)


if __name__ == '__main__':
    rendu()
