
import sys
try:
    sys.path.append('/media/data/3D/projets/balance/my_gym')
except:
    sys.path.append('my_gym')
import gym

from gym import make as gym_make

from .cartpoleswingup import CartPoleSwingUpEnv
from .my_swing_continuous import CartPoleSwingUpContinuousEnv

def make(env_name, *make_args, **make_kwargs):
    if env_name == "CartPoleSwingUp":
        return CartPoleSwingUpEnv()
    elif env_name == "CartPoleSwingUpContinuous":
        return CartPoleSwingUpContinuousEnv()
    else:
        return gym_make(env_name, *make_args, **make_kwargs)
