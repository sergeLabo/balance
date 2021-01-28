
import sys
try:
    sys.path.append('/media/data/3D/projets/balance/my_gym')
except:
    sys.path.append('my_gym')
import gym

from time import time
import numpy as np


from stable_baselines.ddpg.policies import MlpPolicy
from stable_baselines.common.noise import NormalActionNoise,\
                                          OrnsteinUhlenbeckActionNoise,\
                                          AdaptiveParamNoiseSpec
from stable_baselines import DDPG


def train():
    env = gym.make('CartPoleSwingUpContinuous-v0')

    # the noise objects for DDPG
    n_actions = env.action_space.shape[-1]
    param_noise = None
    action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions),
                                        sigma=float(0.5) * np.ones(n_actions))


    model = DDPG(   MlpPolicy,
                    env,
                    verbose=0,
                    param_noise=param_noise,
                    action_noise=action_noise)

    n = 1000201
    model.learn(total_timesteps=n)

    model.save("./weights/DDPG_Swing_" + str(n))


if __name__ == '__main__':
    t0 = time()
    train()
    t = (time()-t0)/3600
    print("    Temps d'apprentissage en heure =", round(t, 3))
