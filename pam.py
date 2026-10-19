import numpy as np

# --- 1. Définition du Modèle ---

# Les états sont codés par leurs indices (0 à 3).
# Selon votre codage (par exemple, pour l'affichage final) :
# État 0: 0001 (Consensus 0)
# État 1: 0011 (Désaccord 0/1)
# État 2: 0111 (Consensus 1)
# État 3: 0101 (Désaccord 1/0)

NOMBRE_ETATS = 4

# Matrice de transition P fournie
# P[i, j] = P(i -> j)
P = np.array([
    [1/2, 1/2, 0, 0],
    [1/4, 1/4, 1/4, 1/4],
    [0, 1/2, 1/2, 0],
    [0, 1, 0, 0]
])

# Calculer la matrice de probabilités cumulées (P_cumulee)
# C'est essentiel pour optimiser la transition dans la boucle de simulation.
P_cumulee = P.cumsum(axis=1)

# --- 2. Paramètres de Simulation ---

N_SIMULATIONS = 2_000_000   # Nombre d'étapes (N très grand, pour la convergence ergodique)
etat_courant = 1             # On commence arbitrairement à l'état 1
compteurs_visites = np.zeros(NOMBRE_ETATS) # Compteurs V (initialisés à zéro)


# --- 3. Simulation de la Trajectoire (Application du Théorème Ergodique) ---

for k in range(N_SIMULATIONS):
    # 1. Tirer un nombre aléatoire uniforme u dans [0, 1]
    u = np.random.rand()
    
    # 2. Déterminer l'état suivant
    # On compare u aux probabilités cumulées de la ligne (P_cumulee[etat_courant, :])
    # argmax trouve le premier indice où la condition est VRAIE, ce qui est le nouvel état.
    etat_suivant = np.argmax(P_cumulee[etat_courant, :] > u)
    
    # 3. Mise à jour du Compteur et de l'état
    compteurs_visites[etat_suivant] += 1
    etat_courant = etat_suivant


# --- 4. Estimation de la Loi Stationnaire ---

# L'estimation est la fréquence relative (Moyenne temporelle)
pi_estime = compteurs_visites / N_SIMULATIONS

# Affichage des résultats
print(f"--- Estimation de la Loi Stationnaire (N={N_SIMULATIONS}) ---")
print(f"Matrice de Transition utilisée:\n{P}")
print("\n--- Résultats de la Simulation ---")

# Calcul de la solution analytique (pour comparaison)
# pi_analytique = (2/9, 4/9, 2/9, 1/9) ≈ (0.2222, 0.4444, 0.2222, 0.1111)
pi_analytique = np.array([2/9, 4/9, 2/9, 1/9])

print("\n| État | Code d'État | Estimation (Simulation) | Valeur Analytique (2/9, 4/9, 2/9, 1/9) | Écart |")
print("|------|-------------|-------------------------|----------------------------------------|-------|")
codes = ["0001", "0011", "0111", "0101"]
for i in range(NOMBRE_ETATS):
    ecart = abs(pi_estime[i] - pi_analytique[i])
    print(f"|  {i}   |    {codes[i]}    |        {pi_estime[i]:.5f}          |                 {pi_analytique[i]:.5f}                  | {ecart:.2e} |")

print("\nLa convergence vers ces valeurs confirme le Théorème Ergodique pour cette chaîne.")