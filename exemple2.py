import numpy as np
from scipy.optimize import linprog

def compute_strength(AF):
    A, R = AF
    num_arguments = len(A)

    # Set up the zero-sum game
    c = [-1] * num_arguments  # Minimize the negative of the proponent's payoff
    A_eq = np.zeros((num_arguments, num_arguments))
    b_eq = [1] * num_arguments

    for i, a in enumerate(A):
        for j, b in enumerate(A):
            if (a, b) in R:
                A_eq[i][j] = 1
            else:
                A_eq[i][j] = 0

    bounds = [(0, 1) for _ in range(num_arguments)]
    
    # Solve the linear program to find the Nash equilibrium
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    if result.success:
        strengths = result.x
        ranking = sorted(zip(A, strengths), key=lambda x: -x[1])
        return ranking
    else:
        raise ValueError("Linear program did not converge")

# Example of usage:
AF = (['a', 'b', 'c', 'd', 'e'], [('a', 'e'), ('b', 'a'), ('b', 'c'), ('c', 'e'), ('d', 'a'), ('e', 'd')])
ranking = compute_strength(AF)
print(ranking)
