
import sys
sys.path.append('my_gym')
import gym

from time import sleep

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2

def train():
    env = make_vec_env('My-CartPole-v0', n_envs=1)

    model = PPO2(MlpPolicy, env, verbose=1)
    n = 250000
    model.learn(total_timesteps=n)

    model.save("./weights/ppo2_cartpole" + str(n))

def rendu():

    env_id = "My-CartPole-v0"
    num_cpu = 1
    env = make_vec_env(env_id, n_envs=num_cpu, seed=0)

    model = PPO2.load("./weights/ppo2_cartpole250000")

    obs = env.reset()
    for _ in range(100000):
        sleep(0.02)
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        print(obs, rewards, dones, info)

# #

# ## Enjoy trained agent
# #obs = env.reset()
# #while True:
    # #action, _states = model.predict(obs)
    # #obs, rewards, dones, info = env.step(action)
    # #env.render()

if __name__ == '__main__':
    # #train()
    rendu()
