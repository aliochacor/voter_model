import random

# États codés : 0=(0,0), 1=(0,1), 2=(1,0), 3=(1,1)
def next_state(state):
    r = random.random()
    if state == 0:  # (0,0)
        if r < 0.25: return 0
        elif r < 0.5: return 1
        elif r < 0.75: return 2
        else: return 3
    elif state == 1:  # (0,1)
        return 3 if r < 0.5 else 2
    elif state == 2:  # (1,0)
        return 3 if r < 0.5 else 1
    elif state == 3:  # (1,1)
        return 3  # absorbant

# Simulation du temps d'absorption
def absorption_time(initial_state, trials=10000):
    total_time = 0
    for _ in range(trials):
        state = initial_state
        t = 0
        while state != 3:  # tant qu'on n'est pas absorbé
            state = next_state(state)
            t += 1
        total_time += t
    return total_time / trials

for s in [0,1,2]:
    print(f"Temps d'absorption moyen depuis l'état {s} :", absorption_time(s))
