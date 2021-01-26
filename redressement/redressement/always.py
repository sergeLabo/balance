
from bge import logic as gl
from once import osc_server_init
import random

def main():

    main_good()

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

def reset():
    """
    x,     x_dot, teta, teta_dot
    -0.03, -0.34, 3.59, 0.21
    """
    gl.num_reset += 1
    x, x_dot, teta, teta_dot = gl.reset

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

        # #print("    Send result =", round(x, 3), round(x_dot, 3),
                                   # #round(teta, 3), round(teta_dot, 3))

        gl.client.send_message(b'/result', result)
