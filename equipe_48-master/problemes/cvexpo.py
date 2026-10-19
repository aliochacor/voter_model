import numpy as np
import matplotlib.pyplot as plt

# Matrice de transition Q 
# (N=2, d=1, bords opposés)
Q = np.array([
    [1/2, 1/2, 0, 0],
    [1/4, 1/4, 1/4, 1/4],
    [0, 1/2, 1/2, 0],
    [0, 1, 0, 0]
])
NOMBRE_ETATS = Q.shape[0]

#  pi théorique
pi = np.array([2/9, 4/9, 2/9, 1/9])

# Loi initiale état A comme point de départ.
mu_initial = np.array([0, 0, 0, 1]) 


# Simulation et Calcul de la Convergence

N_MAX = 50       # Nombre maximum d'étapes  à analyser
normes_l1 = []   # pour stocker ||mu*Q^n - pi||_1
mu_n = mu_initial.copy()


for n in range(N_MAX + 1):
    difference = mu_n - pi
    norme_l1_n = np.sum(np.abs(difference))
    normes_l1.append(norme_l1_n)
    mu_n = np.dot(mu_n, Q) 



etapes = np.arange(N_MAX + 1)

# calcul de la pente
seuil_numerique = 1e-15
indices_valides = np.array(normes_l1) > seuil_numerique
x_reg = etapes[indices_valides]
y_reg = np.log(np.array(normes_l1)[indices_valides]) # On prend le log népérien

pente, intercept = np.polyfit(x_reg, y_reg, 1)

# valeur propre
valeurs_propres = np.linalg.eigvals(Q)
valeurs_propres.sort()
valeurs_propres_trie = np.flip(valeurs_propres)
ln_lambda2 = np.log(valeurs_propres_trie[1])

# tracé

plt.figure(figsize=(10, 6))
plt.plot(etapes, normes_l1, marker='o', markersize=4, linestyle='-', color='blue',label=f"pente $m = {pente:.4f}$\n" f"ln(lamda2) : {ln_lambda2:.4f}")
plt.yscale('log') 
plt.title(r"Convergence de $\mu Q^n$ vers $\pi$ (Norme $1$)", fontsize=16)
plt.xlabel("Nombre d'Étapes ($n$)", fontsize=14)
plt.ylabel(r"$\|\mu Q^n - \pi\|_1$ (Échelle Logarithmique)", fontsize=14)
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.legend()
plt.show()


