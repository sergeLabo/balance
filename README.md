# balance

Reinforcement learning

### Documentation à ressources.labomedia.org

[Apprentissage Par Renforcement](https://ressources.labomedia.org/apprentissage_par_renforcement)

### Soft utilisé

* Debian 10 Buster
* python 3.7
* blender game engine 2.79
* gym modifié dans my_gym
* stable-baselines
* [oscpy de kivy super pratique](https://ressources.labomedia.org/kivy_oscpy) pour le lien entre les scripts de Blender et les fichiers d'environnement

### Installation approximative

~~~~
sudo pip3 install oscpy
git clone https://github.com/hill-a/stable-baselines && cd stable-baselines
pip install -e .[docs,tests,mpi]
sudo pip3 install -e .[docs,tests,mpi]
sudo pip3 install tensorflow==1.15
~~~~

### 1ère étape: Maintien du pendule en équilibre

#### Training

#### Testing

### 2ème étape: Redressessement du pendule depuis la position basse

##### Cette étape s'appelle Swing Up

#### Training

#### Testing

### Merci à

  * [LaLabomedia](https://labomedia.org)
