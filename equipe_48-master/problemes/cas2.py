import random

# États codés : 0=(0,0), 1=(0,1), 2=(1,0), 3=(1,1)
def next_state(state):
    if state == 0:  # (0,0)
        return 0 if random.random() < 0.5 else 1
    elif state == 1:  # (0,1)
        r = random.random()
        if r < 0.25: return 0
        elif r < 0.5: return 1
        elif r < 0.75: return 2
        else: return 3
    elif state == 2:  # (1,0)
        return 1  # (0,1)
    elif state == 3:  # (1,1)
        return 1 if random.random() < 0.5 else 3

# Simulation
N_steps = 1000000
state = 0  # état initial
counts = [0,0,0,0]

for _ in range(N_steps):
    counts[state] += 1
    state = next_state(state)

pi_est = [c / N_steps for c in counts]
print("Estimation de la loi stationnaire :", pi_est)
