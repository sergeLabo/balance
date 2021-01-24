
import sys
sys.path.append('my_gym')
import gym

from time import sleep

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2


def train():
    env = make_vec_env('CartPoleSwingUp-v0', n_envs=1)

    model = PPO2(MlpPolicy, env, verbose=1)
    n = 500000
    model.learn(total_timesteps=n)

    model.save("./weights/ppo2_redressement_" + str(n))


if __name__ == '__main__':
    train()
