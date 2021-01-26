
from bge import logic as gl

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer


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

def on_action(action):
    gl.action = 1 if action == 1 else -1
    gl.action_new = 1
    # #print("Action ...", gl.action)

def on_reset(*args):
    gl.reset = args
    gl.num_reset = 0
    state = [round(gl.reset[0], 2),
             round(gl.reset[1], 2),
             round(gl.reset[2], 2),
             round(gl.reset[3], 2)]

    print("Reset ...", state)

def osc_server_init():
    gl.server = OSCThreadServer()
    gl.server.listen('localhost', port=3001, default=True)
    # Les callbacks du serveur
    gl.server.bind(b'/action', on_action)
    gl.server.bind(b'/reset', on_reset)

def main_good():

    gl.setLogicTicRate(120)

    gl.all_obj = get_all_objects()
    gl.empty = gl.all_obj["Empty"]
    gl.pendulum = gl.all_obj["pendulum"]
    gl.cube = gl.all_obj["Cube"]

    xyz = gl.pendulum.worldOrientation.to_euler()
    xyz[1] = 3.141592654
    gl.pendulum.worldOrientation = xyz.to_matrix()

    gl.num = 0
    gl.reset = 0
    gl.num_reset = 0
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
