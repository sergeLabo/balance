
from bge import logic as gl
from once import osc_server_init
import random

def main():

    if gl.test:
        main_test()
    else:
        main_good()

def main_test():

    # Reset tous les ...
    if gl.num % 1000 == 0:
        print("Reset ...")
        gl.reset = [random.uniform(-0.05, 0.05),
                    random.uniform(-0.005, 0.005),
                    random.uniform(-0.05, 0.05),
                    random.uniform(-0.05, 0.05)]
        print("    ", gl.reset)
    if gl.reset: reset()

    # Action +1 ou -1 en dehors du reset
    if gl.num % 5 == 0 and not gl.reset:
        print("Action ...")
        gl.action = random.choice([-1, 1])
        print("    ", gl.action)
    if gl.action:  action()

    # Si angle trop grand --> perdu --> reset
    done()

    # Envoi si gl.send = 1
    send_result()
    gl.num += 1

def main_good():

    # Demande de reset au serveur pour le cas où
    # blender est lancé après le serveur, ou si blender est relancé
    if not gl.server_contacted:
        print("Contact avec le serveur ...")
        gl.client.send_message(b'/contact', [1])
        gl.server_contacted = 1

    if gl.reset:
        reset()

    if gl.action_new and not gl.reset:
        action()

    # Envoi si gl.send = 1
    send_result()
    gl.num += 1

def done():
    """Si angle trop grand --> perdu --> reset"""

    xyz = gl.pendulum.worldOrientation.to_euler()
    teta = xyz[1]
    if teta < -1 or teta > 1:
        gl.reset = [random.uniform(-0.05, 0.05),
                    random.uniform(-0.005, 0.005),
                    random.uniform(-0.05, 0.05),
                    random.uniform(-0.05, 0.05)]
        reset()
        gl.action = 0

def reset():

    gl.num_reset += 1
    x, x_dot, teta, teta_dot = gl.reset

    if 1 < gl.num_reset < 100:
        gl.cube.worldPosition = [x, 0.738772, 0]
        gl.cube.worldLinearVelocity[0] = x_dot

        xyz = gl.pendulum.worldOrientation.to_euler()
        xyz[1] = teta
        gl.pendulum.worldOrientation = xyz.to_matrix()
        gl.pendulum.worldAngularVelocity[1] = teta_dot

    if gl.num_reset == 100:
        gl.num_reset = 0
        gl.reset = 0

def action():
    """Modification de la vitesse du cube"""
    vitesse = gl.action * 0.05
    gl.cube.worldLinearVelocity[0] -= vitesse
    if gl.action_new >= 2:
        gl.send = 1
        gl.action_new = 0
    gl.action = 0
    gl.action_new += 1

def send_result():
    """Envoi de: np.array(self.state), reward, done"""

    if gl.send:
        gl.send = 0
        x = gl.cube.worldPosition.x
        x_dot = gl.cube.worldLinearVelocity.x
        teta = gl.pendulum.worldOrientation.to_euler()[1]
        teta_dot = gl.pendulum.worldAngularVelocity[1]

        result = [x, x_dot, teta, teta_dot]

        print("    Send result =", round(x, 3), round(x_dot, 3),
                                   round(teta, 3), round(teta_dot, 3))

        gl.client.send_message(b'/result', result)
