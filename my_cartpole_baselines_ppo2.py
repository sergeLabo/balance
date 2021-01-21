
import sys
sys.path.append('my_gym')
import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2

# multiprocess environment
env = make_vec_env('CartPole-v1', n_envs=8)

model = PPO2(MlpPolicy, env, verbose=1)
n = 2500
model.learn(total_timesteps=n)

model.save("./weights/ppo2_cartpole" + str(n))
del model # remove to demonstrate saving and loading
model = PPO2.load("./weights/ppo2_cartpole" + str(n))

# Enjoy trained agent
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
