
import sys
sys.path.append('my_gym')
import gym

from time import time

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2


def train():
    env = make_vec_env('CartPoleSwingUp-v0', n_envs=1)

    model = PPO2(MlpPolicy, env, verbose=0)
    n = 1000000
    model.learn(total_timesteps=n)

    model.save("./weights/ppo2_redressement_" + str(n))


if __name__ == '__main__':
    t0 = time()
    train()
    t = (time()-t0)/3600
    print("Temps d'apprentissage en heure =", t)


"""
n°3     self.my_reward_total = 22234 en 3 heures

        n = 320000
        self.x_threshold = 5  # 2.4
        self.t_limit = 500
        loc=np.array([0.0, 0.0, 3.141592654, 0.0])
        scale=np.array([0.05, 0.05, 0.2, 0.05]))
        reward_teta = max(0, np.cos(teta))
        reward_x = np.cos((x / self.x_threshold) * (np.pi / 2.0))
"""

"""
    # Blocage des positions
    if 1 < gl.num_reset < 200:
        gl.cube.worldPosition = [x, 0.738772, 0]
        gl.cube.worldLinearVelocity[0] = 0

    # Blocage du pendule
    if 200 < gl.num_reset < 400:
        xyz = gl.pendulum.worldOrientation.to_euler()
        xyz[1] = teta  # + 3.141592654
        gl.pendulum.worldOrientation = xyz.to_matrix()
        gl.pendulum.worldAngularVelocity[1] = 0

    # Vitesse initiale
    if 400 < gl.num_reset < 450:
        gl.cube.worldLinearVelocity[0] = x_dot
        gl.pendulum.worldAngularVelocity[1] = teta_dot

    # Fin
    if gl.num_reset == 450:
        gl.num_reset = 0
        gl.reset = 0
"""

"""
n°4     self.my_reward_total =  en  heures

        n = 1 000 000
        self.x_threshold = 10  # 2.4
        self.t_limit = 1000
stop
"""

"""
n°5     self.my_reward_total = 378633

        Temps d'apprentissage en heure = 6.02
        n = 1 000 000
        self.x_threshold = 10  # 2.4
        self.t_limit = 1000
        loc=np.array([0.0, 0.0, 3.141592654, 0.0])
        scale=np.array([0.05, 0.05, 2.0, 0.05]))


"""
