
import numpy as np
from random import randint
from bge import logic as gl

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer


class RealCam:
    def __init__(self, amplitude, duree):
        """
        amplitude int a adapter si loc ou rot
        longueur int de 1 à 10
        """
        self.amplitude = amplitude
        self.haut = self.amplitude*randint(1, 5)
        self.duree = duree
        self.period = self.duree*randint(50, 500)
        self.reset()
        # Valeur courante
        self.x = 0
        self.y = 0

    def update(self):
        self.x += 1
        self.y = self.haut*np.sin(2*np.pi*self.x/self.period)
        if gl.frame - self.initial_frame == self.period:
            self.reset()

    def reset(self):
        # Frame de début de la sinusoïde
        self.haut = int(self.amplitude*randint(1, 5))
        self.initial_frame = gl.frame
        self.period = int(self.duree*randint(100, 300))
        # Valeur courante
        self.x = 0


def get_all_scenes():
    """Récupération des scènes"""
    # Liste des objets scènes
    activeScenes = gl.getSceneList()

    # Liste des noms de scènes
    scene_name = []
    for scn in activeScenes:
        scene_name.append(scn.name)

    return activeScenes, scene_name

def get_scene_with_name(scn):
    """Récupération de la scène avec le nom"""

    activeScenes, scene_name = get_all_scenes()
    if scn in scene_name:
        return activeScenes[scene_name.index(scn)]
    else:
        print(scn, "pas dans la liste")
        return None

def get_all_objects():
    """
    Trouve tous les objets des scènes actives
    Retourne un dict {nom de l'objet: blender object}
    """
    activeScenes, scene_name = get_all_scenes()

    all_obj = {}
    for scn_name in scene_name:
        scn = get_scene_with_name(scn_name)
        for blender_obj in scn.objects:
            blender_objet_name = blender_obj.name
            all_obj[blender_objet_name] = blender_obj

    return all_obj

def on_action(*args):
    if not args[0]:
        gl.action = 1 if args[1] == 1 else -1
    else:
        gl.action = args[1]/10000
    gl.action_new = 1

def on_reset(*args):

    gl.reset = (args[0]/1000,
                args[1]/1000,
                args[2]/1000,
                args[3]/1000)

    # Pour suivi du reset en cours
    gl.num_reset = 0
    # Pour suivi des reset reçu à afficher
    gl.reset_number += 1

    # Pour l'affichage
    state = [round(gl.reset[0], 2),
             round(gl.reset[1], 2),
             round(gl.reset[2], 2),
             round(gl.reset[3], 2)]
    print("Reset ...", gl.reset_number, ":", state)

def osc_server_init():
    gl.server = OSCThreadServer()
    gl.server.listen('localhost', port=3001, default=True)
    # Les callbacks du serveur
    gl.server.bind(b'/action', on_action)
    gl.server.bind(b'/reset', on_reset)

def main_good():

    gl.setLogicTicRate(120)
    gl.frame = 0
    # Horizontal cam
    gl.rc_h = RealCam(0.02, 1)
    # Vertical cam
    gl.rc_v = RealCam(0.02, 1)
    # Profondeur Cam
    gl.rc_p = RealCam(1, 5)

    gl.all_obj = get_all_objects()
    gl.empty = gl.all_obj["Empty"]
    gl.pendulum = gl.all_obj["pendulum"]
    gl.cube = gl.all_obj["Cube"]
    gl.camera = gl.all_obj["Camera"]

    xyz = gl.pendulum.worldOrientation.to_euler()
    xyz[1] = 3.141592654
    gl.pendulum.worldOrientation = xyz.to_matrix()

    gl.num = 0
    gl.reset = 0
    gl.num_reset = 0
    gl.reset_number = 0
    gl.action = 0
    gl.action_new = 0

    gl.server = None
    gl.send = 0
    gl.client = OSCClient(b'localhost', 3003)
    gl.server_contacted = 0
    osc_server_init()

    # Demande de reset
    gl.client.send_message(b'/reset', [1])

def main():
    print("Lancement de once.py ...")

    main_good()

    print("Fin de once.py")
