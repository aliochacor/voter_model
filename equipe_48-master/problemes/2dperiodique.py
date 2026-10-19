import numpy as np

# Paramètres de Simulation 

N = 5                 # Taille du côté de la grille (N x N)
MAX_ETAPES = 10000    # Limite maximale d'étapes pour éviter une boucle infinie
VOISINAGE_VON_NEUMANN = [(-1, 0), (1, 0), (0, -1), (0, 1)] # delta_i, delta_j

# Fonctions

def initialiser_grille(N):
    """Initialise la grille N x N avec des opinions aléatoires (0 ou 1)."""
    # np.random.randint(2, size=(N, N)) crée une matrice N x N de 0 et 1
    return np.random.randint(2, size=(N, N))

def est_consensus(grille):
    """Vérifie si tous les électeurs ont la même opinion."""
    # Le consensus est atteint si la somme des opinions est 0 (tous à 0) 
    # ou si elle est N*N (tous à 1).
    somme = np.sum(grille)
    return somme == 0 or somme == N * N

def calculer_proportion_voisins(grille, i, j, N):
    """
    Calcule la proportion de voisins ayant chaque opinion (0 et 1) 
    pour le site (i, j) en utilisant les conditions aux bords périodiques.
    """
    opinions_voisins = []
    
    for di, dj in VOISINAGE_VON_NEUMANN:
        ni = (i + di) % N
        nj = (j + dj) % N
        opinions_voisins.append(grille[ni, nj])
    opinions_voisins = np.array(opinions_voisins)
    nb_voisins = len(opinions_voisins) # Nombre total de voisins (toujours 4 avec conditions périodiques)
    nb_voisins_un = np.sum(opinions_voisins) # Compte le nombre de voisins à 1
    prop_un = nb_voisins_un / nb_voisins # Proportion d'opinion 1 (et 0 est 1 - prop_1)
    return prop_un


def etape_simulation(grille, N):
    """
    Exécute une étape complète de l'automate cellulaire probabiliste.
    Une nouvelle grille (xi_{n+1}) est calculée à partir de l'ancienne (xi_n).
    """
    nouvelle_grille = grille.copy()     # opinions mises à jour
    for i in range(N):
        for j in range(N):
            prop_un = calculer_proportion_voisins(grille, i, j, N) # Calculer la proportion de voisins ayant l'opinion 1
            # L'électeur change son opinion pour 1 avec probabilité prop_un
            # L'électeur change son opinion pour 0 avec probabilité (1 - prop_un)
            if np.random.rand() < prop_un:
                nouvelle_grille[i, j] = 1 # Adopte l'opinion 1
            else:
                nouvelle_grille[i, j] = 0 # Adopte l'opinion 0        
    return nouvelle_grille


def simuler_convergence(N, max_etapes):
    """Simule la chaîne jusqu'au consensus et retourne le temps d'absorption."""
    grille = initialiser_grille(N)
    op_dom = np.sum(grille)
    if op_dom > N*N/2:
        op_dom = 1
    else :
        op_dom =0
    n_etapes = 0
    while not est_consensus(grille) and n_etapes < max_etapes:
        grille = etape_simulation(grille, N)
        n_etapes += 1
    # Analyse des résultats
    if est_consensus(grille):
        final_opinion = grille[0, 0] # L'opinion majoritaire finale
        return n_etapes, final_opinion, op_dom
    else:
        print("\n Limite d'étapes Atteinte ")
        return max_etapes, None, op_dom, 


########### simulation

M = 10000
T_abs = [] # liste des temps d'absorption pour en faire la moyenne.
corr_final_deb = [] # 1 si l'opinion de consensus est le même que l'opinion dominant, 0 sinon.
for i in range(M):
    temps_absorption, opinion_finale, opinion_dominant = simuler_convergence(N, MAX_ETAPES)
    T_abs.append(temps_absorption)
    if opinion_finale == opinion_dominant:
        corr_final_deb.append(1)

print(f"simulation sur grille {N}x{N}, temps d'absorption moyen :",np.mean(T_abs), "\n",np.sum(corr_final_deb), f"correlation pour {M} simulation")