import numpy as np

N = 5          # taille de la grille centrale
NB_SIMULATIONS = 20000
MAX_STEPS = 1000000

# fonction pour initialiser une grille 7x7 avec bord fixe à 1
def init_grid(N):
    grid = np.ones((N+2, N+2), dtype=int)   # grille totale 7x7 avec bord
    # remplir le centre (5x5) aléatoirement 0 ou 1
    grid[1:-1, 1:-1] = np.random.randint(0,2,(N,N))
    return grid

# voisins de von Neumann
def von_neumann_neighbors(i,j):
    return [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]

# mise à jour d'une grille
def update(grid):
    new_grid = grid.copy()
    for i in range(1,N+1):
        for j in range(1,N+1):
            total = sum(grid[ni,nj] for ni,nj in von_neumann_neighbors(i,j))
            new_grid[i,j] = 1 if total >= 2 else 0
    return new_grid

# fonction de simulation jusqu'à absorption
def simulate_once():
    grid = init_grid(N)
    center = grid[1:-1, 1:-1]
    maj_initial = 1 if np.sum(center) > (N*N)/2 else 0
    steps = 0
    while steps < MAX_STEPS:
        steps += 1
        new_grid = update(grid)
        if np.all(new_grid[1:-1,1:-1] == 1):
            return maj_initial, steps
        grid = new_grid
    return maj_initial, steps

# simulations
results = {1: [], 0: []}
for _ in range(NB_SIMULATIONS):
    maj, t = simulate_once()
    results[maj].append(t)

# affichage
for maj in [1,0]:
    if results[maj]:
        print(f"Majorité initiale de {maj} :")
        print(f"  - échantillons : {len(results[maj])}")
        print(f"  - temps moyen d'absorption : {np.mean(results[maj]):.2f}")
