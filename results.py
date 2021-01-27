""" 1
loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
scale=np.array([0.05, 0.05, 2.0, 0.05]))

              n = 50000
    x_threshold = 5
        vitesse = gl.action * 0.05
        t_limit = 500
          temps = 0.53
my_reward_total = 3369
"""

""" 2
            n = 50000
    x_threshold = 10                 --> modif
        vitesse = gl.action * 0.1    --> modif
        t_limit = 500
          temps = 0.53
my_reward_total = 4897              mieux
"""

""" 3
             n = 50000
   x_threshold = 10
       vitesse = gl.action * 0.1
        t_limit = 500               --> maxi = 500 dans __init__
          temps = 0.45
my_reward_total = 2004              très mauvais
"""

""" 4
             n = 50000 49889
   x_threshold = 10                 --> seule modif par rapport à 1
       vitesse = gl.action * 0.05
        t_limit = 500
          temps = 0.618
my_reward_total = 5702              mieux que 1
Efficacité globale = 0.11
"""

""" 5
             n = 50000
   x_threshold = 10
       vitesse = gl.action * 0.01   --> modif
        t_limit = 500
          temps = 0.379
my_reward_total = 4533
Efficacité globale = 0.09
"""

""" 6
             n = 50000             --> modif
   x_threshold = 10
       vitesse = gl.action * 0.05   --> modif
        t_limit = 1000              --> modif et maxi = 1000 dans __init__
          temps = 0.36
my_reward_total = 6468
Efficacité globale = 0.36
"""

""" 7
             n = 100 000             --> modif
   x_threshold = 10
       vitesse = gl.action * 0.05
        t_limit = 1000
          temps = 0.89
my_reward_total = 11491
Efficacité globale = 0.11

8 stop
loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
scale=np.array([0.01, 0.01, 1.0, 0.01]))

             n = 1 000 000             --> modif
   x_threshold = 10
       vitesse = gl.action * 0.05
        t_limit = 1000
          temps =
my_reward_total =
Efficacité globale =  stop angle de départ trop faible
"""

""" 9
loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
scale=np.array([0.1, 0.1, 2.5, 0.1]))

                 n = 1 000 000             --> modif
       x_threshold = 10
           vitesse = gl.action * 0.05
           t_limit = 1000
             temps = 7.11
Récompense totale  = 223329
Efficacité globale = 0.22
"""

""" 10
loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
scale=np.array([0.1, 0.1, 4, 0.1]))      --> modif

                 n = 67830             --> modif
       x_threshold = 10
           vitesse = gl.action * 0.05
           t_limit = 1000
             temps = 7.11
Récompense totale  = 7493
Efficacité globale = 0.11
"""

""" 11
loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
scale=np.array([0.1, 0.1, 4, 0.1]))

                 n = 50 010
       x_threshold = 10                  --> modif
           vitesse = gl.action * 0.05
           t_limit = 1000
             temps = 0.421
Récompense totale  = 4386
Efficacité globale = 0.09
"""

""" 12
loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
scale=np.array([0.1, 0.1, 5, 0.1]))     --> modif

                 n = 50 012
       x_threshold = 8                  --> modif
           vitesse = gl.action * 0.05
           t_limit = 1000
             temps =0.442
Récompense totale  =5973
Efficacité globale =0.12

"""

""" 14                                       --> modif double reset
loc=np.array([0.0, 0.0, 3.141592654, 0.0]),
scale=np.array([0.1, 0.1, 5, 0.1]))

                 n = 50 012
       x_threshold = 8
           vitesse = gl.action * 0.05
           t_limit = 1000
                      Steps totaux = 49729
               Récompense du cycle = 289
                 Récompense totale = 7864
                Efficacité globale = 0.16
    Temps d'apprentissage en heure = 0.453

"""

""" 15 idem 14 mais 100 015
                       x_threshold = 8
                 Récompense totale = 16354
                Efficacité globale = 0.16
    Temps d'apprentissage en heure = 0.887
"""

""" 16 idem 15 mais
                       x_threshold = 16
    Cycle n°: 240
                      Steps totaux = 99435
                 Récompense totale = 12798
                Efficacité globale = 0.13
    Temps d'apprentissage en heure = 0.819
"""

""" 17
                 n = 100 017
       x_threshold = 4
           t_limit = 1000
      self.t_limit = 500
    Cycle n°: 338
                      Steps totaux = 99808
                 Récompense totale = 11645
                Efficacité globale = 0.12
    Temps d'apprentissage en heure = 0.943
"""

""" 18
idem 17 mais 1 000 000
sur MSI
"""
