import numpy as np

# Paramètres de Simulation
MAX_ETAPES = 10000
VOISINAGE_VON_NEUMANN = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # haut, bas, gauche, droite


# ======= Initialisation avec bords fixés =======
def initialiser_grille_bord_fixe(N, d, bord_opinion):
    """
    Grille totale (N+2)x(N+2) avec un bord fixé à bord_opinion,
    et un centre NxN aléatoire dans {0,...,d-1}.
    """
    grid = np.full((N + 2, N + 2), bord_opinion, dtype=int)  # bord fixé
    grid[1:-1, 1:-1] = np.random.randint(d, size=(N, N))     # centre aléatoire
    return grid


def est_consensus_centre(grille):
    """Consensus seulement sur le centre (NxN)."""
    centre = grille[1:-1, 1:-1]
    return np.all(centre == centre[0, 0])


def calculer_proportion_voisins_bord_fixe(grille, i, j, d):
    """
    Calcule les proportions des opinions parmi les 4 voisins von Neumann
    pour la case (i,j) DANS LA GRILLE TOTALE (N+2)x(N+2).
    Ici pas de modulo: les bords existent et sont fixés.
    """
    voisins = []
    for di, dj in VOISINAGE_VON_NEUMANN:
        ni, nj = i + di, j + dj
        voisins.append(grille[ni, nj])

    voisins = np.array(voisins)
    nb_voisins = len(voisins)  # 4

    prop_k = []
    for k in range(d):
        prop_k.append(np.sum(voisins == k) / nb_voisins)
    return prop_k


def etape_simulation_bord_fixe(grille, N, d):
    """
    Mise à jour synchrone du centre NxN uniquement.
    Le bord reste fixé.
    """
    nouvelle = grille.copy()

    # On met à jour uniquement le centre : indices 1..N
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            prop_k = calculer_proportion_voisins_bord_fixe(grille, i, j, d)
            nouvelle[i, j] = np.random.choice(d, p=prop_k)

    return nouvelle


def opinion_dominante_centre(grille, d):
    """Opinion dominante dans le centre NxN."""
    centre = grille[1:-1, 1:-1]
    counts = np.bincount(centre.ravel(), minlength=d)
    return np.argmax(counts)


def simuler_convergence_bord_fixe(N, d, bord_opinion, max_etapes):
    """
    Simule jusqu'au consensus sur le centre.
    Retourne (temps_absorption, opinion_finale, opinion_dominante_initiale).
    """
    grille = initialiser_grille_bord_fixe(N, d, bord_opinion)
    op_dom = opinion_dominante_centre(grille, d)

    n = 0
    while not est_consensus_centre(grille) and n < max_etapes:
        grille = etape_simulation_bord_fixe(grille, N, d)
        n += 1

    if est_consensus_centre(grille):
        opinion_finale = grille[1, 1]  # une case du centre suffit
        return n, opinion_finale, op_dom
    else:
        # pas convergé dans la limite
        return max_etapes, None, op_dom


# ========== Simulation ==========
M = 10000
N = 5
d = 3
BORD_OPINION = np.random.randint(d)  # <-- on choisis (0..d-1) ou bien random.randint(d)

T_abs = []
corr_final_deb = []

for _ in range(M):
    t, opin_fin, opin_dom = simuler_convergence_bord_fixe(N, d, BORD_OPINION, MAX_ETAPES)
    T_abs.append(t)
    if opin_fin == opin_dom:
        corr_final_deb.append(1)

print(f"Grille {N}x{N}, d={d}, bord fixé à {BORD_OPINION}")
print("Temps d'absorption moyen :", np.mean(T_abs))
print(f"{np.sum(corr_final_deb)} corrélations (final = dominante initiale) sur {M} simulations")
