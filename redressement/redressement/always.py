
from time import time
from bge import logic as gl
from once import osc_server_init
import random
import math


def main():

    # Pour tout le jeu
    gl.frame += 1

    if gl.steps_text != 0:
        moy = round(gl.reward_text/gl.steps_total_text, 2)
    else:
        moy = 0
    gl.reward["Text"] = "Récompense:" + "\n" +\
                        "    Totale  = " + str(gl.reward_text) + "\n" +\
                        "    Moyenne = " + str(moy)
    gl.steps["Text"] = "Steps = " + str(gl.steps_text)
    gl.steps_total["Text"] = "Steps total = " + str(gl.steps_total_text)
    if gl.reset_text:
        gl.reset_obj["Text"] = "Reset: " + str(gl.reset_text)
    else:
        gl.reset_obj["Text"] = ""

    # Freq
    if gl.frame % 120 == 0:
        t = time()
        fps = 120/(t - gl.top)
        gl.top = t
        gl.fps["Text"] = "FPS = " + str(round(fps, 1))

    set_camera_orientation()

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

def set_camera_orientation():
    """alpha = arcsin(x/y)"""
    gl.rc_r_v.update()
    gl.rc_r_ho.update()
    gl.rc_p_p.update()
    gl.rc_p_ha.update()
    gl.rc_p_l.update()

    tg = gl.cube.worldPosition[0]/gl.camera.worldPosition[1]
    alpha = math.atan(tg)
    xyz = gl.camera.worldOrientation.to_euler()
    xyz[2] = alpha + gl.rc_r_ho.y
    xyz[0] = 3.14159/2 + gl.rc_r_v.y
    gl.camera.worldOrientation = xyz.to_matrix()

    # Position
    gl.camera.worldPosition[1] = gl.rc_p_p.y - 12
    gl.camera.worldPosition[2] = gl.rc_p_ha.y
    gl.camera.worldPosition[0] = gl.rc_p_l.y

def reset():

    gl.num_reset += 1
    x, x_dot, teta, teta_dot = gl.reset

    # Blocage des positions
    if 1 < gl.num_reset < 10:
        gl.cube.suspendDynamics()
        gl.pendulum.disableRigidBody()
        gl.cube.worldPosition = [x, 0.738772, 0]
        gl.cube.worldLinearVelocity[0] = 0

    # Blocage du pendule
    if 10 < gl.num_reset < 20:
        gl.cube.restoreDynamics()
        gl.pendulum.enableRigidBody()
        xyz = gl.pendulum.worldOrientation.to_euler()
        # Le pendule est à teta=0 en haut
        xyz[1] = teta
        gl.pendulum.worldOrientation = xyz.to_matrix()
        gl.pendulum.worldAngularVelocity[1] = 0

    # Vitesse initiale
    if 20 < gl.num_reset < 25:
        gl.cube.worldLinearVelocity[0] = x_dot
        gl.pendulum.worldAngularVelocity[1] = teta_dot

    # Fin
    if gl.num_reset == 25:
        gl.num_reset = 0
        gl.reset = 0
        gl.first = 1
        gl.reset_text = ""

def action():
    """Modification de la vitesse du cube
    Envoi de la réponse la frame suivant la réception
    1*5000*0.05/10000=0.025m/s
    """

    vitesse = gl.action * 0.05
    gl.cube.worldLinearVelocity[0] -= vitesse
    # #print("avant", gl.action, gl.action_new)
    if gl.action_new >= 2:
        gl.send = 1
        gl.action_new = 0
    gl.action = 0
    gl.action_new += 1
    # #print("après", gl.action, gl.action_new)

def send_result():
    """Envoi de: np.array(self.state), reward, done"""

    if gl.send and not gl.num_reset:  # pas d'envoi si reset en cours
        gl.send = 0
        x = gl.cube.worldPosition.x
        x_dot = gl.cube.worldLinearVelocity.x
        teta = gl.pendulum.worldOrientation.to_euler()[1]
        teta_dot = gl.pendulum.worldAngularVelocity[1]

        result = [x, x_dot, teta, teta_dot]

        # #print("    Send result =", round(x, 3), round(x_dot, 3),
                                   # #round(teta, 3), round(teta_dot, 3))

        gl.client.send_message(b'/result', result)
