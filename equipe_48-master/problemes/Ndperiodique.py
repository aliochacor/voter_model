import numpy as np

# Paramètres de Simulation 

MAX_ETAPES = 10000    # Limite maximale d'étapes pour éviter une boucle infinie
VOISINAGE_VON_NEUMANN = [(-1, 0), (1, 0), (0, -1), (0, 1)] # delta_i, delta_j

# Fonctions

def initialiser_grille(N, d):
    """Initialise la grille N x N avec des opinions aléatoires (0 ou 1)."""
    # np.random.randint(2, size=(N, N)) crée une matrice N x N de 0 et 1
    return np.random.randint(d, size=(N, N))

def est_consensus(grille):
    """Vérifie si tous les électeurs ont la même opinion."""
    # Le consensus est atteint si tous les électeurs ont la même opinion.
    return np.all(grille == grille[0,0])


def calculer_proportion_voisins(grille, i, j, N, d):
    """
    Calcule la proportion de voisins ayant chaque opinion (0 et 1 et 2) 
    pour le site (i, j) en utilisant les conditions aux bords périodiques.
    """
    opinions_voisins = []
    
    for di, dj in VOISINAGE_VON_NEUMANN:
        ni = (i + di) % N
        nj = (j + dj) % N
        opinions_voisins.append(grille[ni, nj])
    opinions_voisins = np.array(opinions_voisins)
    nb_voisins = len(opinions_voisins) # Nombre total de voisins (toujours 4 avec conditions périodiques)
    prop_k = []    
    for k in range(d):
        # pour k dans {0,1 ... d-1}
        # proportion de voisins ayant l'opinion k 
        prop_k.append(np.sum(opinions_voisins == k) / nb_voisins)
    return prop_k



def etape_simulation(grille, N,d):
    """
    Exécute une étape complète de l'automate cellulaire probabiliste.
    Une nouvelle grille (xi_{n+1}) est calculée à partir de l'ancienne (xi_n).
    """
    nouvelle_grille = grille.copy()     # opinions mises à jour
    for i in range(N):
        for j in range(N):
            prop_k = calculer_proportion_voisins(grille, i, j, N,d) # Calculer la proportion des voisins pour chaque opinion
            # L'électeur change son opinion pour k avec probabilité prop_k[k]
            nouvelle_grille[i, j] = np.random.choice(np.arange(len(prop_k)), p=prop_k) # Adopte l'opinion k avec probabilité prop_k[k]  
    return nouvelle_grille

def opinion_dominante(grille, d):
    """Retourne l'opinion dominante dans la grille."""
    counts = np.bincount(grille.flatten(), minlength=d)
    return np.argmax(counts)


def simuler_convergence(N,d,max_etapes):
    """Simule la chaîne jusqu'au consensus et retourne le temps d'absorption."""
    grille = initialiser_grille(N,d)
    op_dom = opinion_dominante(grille, d)
    n_etapes = 0
    while not est_consensus(grille) and n_etapes < max_etapes:
        grille = etape_simulation(grille, N,d)
        n_etapes += 1
    # Analyse des résultats
    if est_consensus(grille):
        final_opinion = grille[0, 0] # L'opinion majoritaire finale
        return n_etapes, final_opinion, op_dom
    else:
        print("\n Simulation non convergente : Limite d'etapes Atteinte ")
        return max_etapes, None, op_dom, 


########### simulation

M = 10000
N = 5                 # Taille du côté de la grille (N x N)

# ====  simulation pour dimension d'opinions fixée =====
d = 3                 # Dimension des opinions
T_abs = [] # liste des temps d'absorption pour en faire la moyenne.
corr_final_deb = [] # 1 si l'opinion de consensus est le même que l'opinion dominant, 0 sinon.
for i in range(M): 
    temps_absorption, opinion_finale, opinion_dominant = simuler_convergence(N,d, MAX_ETAPES)
    T_abs.append(temps_absorption)
    if opinion_finale == opinion_dominant:
        corr_final_deb.append(1)

print(f"simulation sur grille {N}x{N} avec {d} opinions, temps d'absorption moyen :",np.mean(T_abs), "\n",np.sum(corr_final_deb), f"correlation pour {M} simulation")




# ====  grosse simulation pour différentes dimensions d'opinions =====
# MAX_DIM = 5                 # Dimension de la grille
# for d in range(2,MAX_DIM):
#     T_abs = [] # liste des temps d'absorption pour en faire la moyenne.
#     corr_final_deb = [] # 1 si l'opinion de consensus est le même que l'opinion dominant, 0 sinon.
#     for i in range(M): 
#         temps_absorption, opinion_finale, opinion_dominant = simuler_convergence(N,d, MAX_ETAPES)
#         T_abs.append(temps_absorption)
#         if opinion_finale == opinion_dominant:
#             corr_final_deb.append(1)

#     print(f"simulation sur grille {N}x{N} avec {d} opinions, temps d'absorption moyen :",np.mean(T_abs), "\n",np.sum(corr_final_deb), f"correlation pour {M} simulation")
#     print("==========================================================================")