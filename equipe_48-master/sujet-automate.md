# Projet - Automate Cellulaire Probabiliste de l'électeur 

**Contact: Hervé Guiol (herve.guiol@grenoble-inp.fr)**

## Contexte
Le modèle de l'électeur (voter model) est un système de particules en intéraction.
Dans le modèle de base seules deux opinions sont possibles (0 ou 1). 
L'opinion d'un électeur au cours du temps est affectée par le nombre d'électeurs voisins d'avis contraire au sien. 
L'étude proposée ici est de se restreindre au cadre d'un automate cellulaire probabiliste (discrétisation du temps) en volume fini. 
La question centrale qu'on se pose est : y a-t-il convergence vers un consensus (unique opinion)? ou bien la coexitence d'opinions multiple est-elle possible?

## Objectif
Le but de ce projet est d'étudier à travers un modèle simple les questions relatives à l'équilibre d'un processus aléatoire.
Ces questions seront abordées suivant diverses conditions : dimension, voisinage, conditions au bord, nombre d'opinions, conditions initiales, etc...
Pour accomplir cet objectif il faudra créer une application qui simule ces modèles. 
Il faudra également produire une analyse (statistique) de ces simulations afin d'apporter des éléments de réponse aux questions ci-dessus.
Il est attendu que les élèves comprennent, sachent expliquer, argumenter et faire le lien avec les résultats théoriques.

## Modélisation
On notera $S$ l'ensemble des positions des électeurs : $S=[|1,N|]^d$ où $[|1,N|]=\{1,2,...,N\}$ et $d=1,\ 2$ ou $3$.Il s'agit donc d'un ensemble de 
$N^3$ électeurs. Un électeur à la position $x\in S$ a un ensemble d'électeurs voisins $\mathcal{N}_x=\{y\in S : ||y-x||_d\leq 1\}$ (suivant l'étude entreprise on pourra remplacer la distance Euclidienne $||.||_d$ par $||.||_{\infty}$).
On pourra, suivant l'étude, prendre des conditions périodiques aux bords du domaine : par exemple, en dimension $1$, l'électeur sur la position $1$ est voisin de $2$ et de $N$.

Les positions des électeurs sont fixes et n'évoluent pas dans le temps. 
Le temps est considéré de façon discrète par un entier $n$ dans $\mathbb{N}$.

A tout instant $n\in\mathbb{N}$, chaque électeur a une opinion qu'il lui est propre modélisé par une valeur dans l'ensemble $\{0,...,\kappa\}$. 
Dans un premier temps, on considérera le modèle de base avec deux opinions possibles : $\kappa=1$ avant d'étudier le cas $\kappa>1$.

On note $X=\{0,...,\kappa\}^{S}$, à tout instant $n$, l'état de l'opinion du système est représenté par $\xi_n\in X$ où $\xi_n(x)\in\{0,...,\kappa\}$  représente l'opinion de l'électeur à la position $x$ au temps $n$.

Les opinions varient dans le temps suivant la dynamique décrite ci dessous :

- au temps $n+1$, l'électeur à la position $x$ change son opinion pour $i$ avec 
probabilité $\#\{y\in \mathcal{N}_x : \xi_n(y)=i\}/\#\{y\in \mathcal{N}_x\}$: i.e. la proportion de voisins de $x$ ayant l'opinion $i$.
- sinon il conserve son opinion du temps $n$.

On voit donc ainsi que pour simuler $\xi_{n+1}$ l'état de l'opinion au temps $n+1$, il suffit seulement de connaitre $\xi_n$ 
et de simuler les changements d'opinions suivant la règle ci dessus. C'est un exemple de chaine de Markov sur l'espace $X$.

Une analyse simple montre que le système réduit à une seule opinion, avec des conditions périodiques aux bords, est stable : pas de changement possible.

## Données
Les données seront celles issues des simulations produites.


## Références bibliographiques

Cours de Probabilités et Statistique 1, 1A

