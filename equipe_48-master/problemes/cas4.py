import numpy
import numpy.random as random

# states in alphabetical order
def next(s):
    if s == 0:
        return 0
    elif s == 1:
        return random.choice([0, 2, 4, 6])
    elif s == 2:
        return random.choice([0, 1, 4, 5])
    elif s == 3:
        return random.choice([4, 5, 6, 7])
    elif s == 4:
        return random.choice([0, 1, 2, 3])
    elif s == 5:
        return random.choice([2, 3, 6, 7])
    elif s == 6:
        return random.choice([1, 3, 5, 7])
    else:
        return 7

def sim() -> int:
    n_max = 100000
    state = random.randint(1, 6)

    for _ in range(n_max):
        state = next(state)
        if state == 0 or state == 7:
            return state

    return None

n = 10000
absorb = [0, 0]

for _ in range(n):
    absorb[int(sim() / 7)] += 1

print(f'Probabilité d\'absorption de l\'état 000: {absorb[0] / n}')
print(f'Probabilité d\'absorption de l\'état 111: {absorb[1] / n}')
