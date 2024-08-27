from itertools import permutations

def same_position_ratio(list1, list2):
    count = 0
    for i in range(len(list1)):
        if i < len(list2) and list1[i] == list2[i]:
            count += 1
    return 1 - count / len(list1)

def kendall_tau_distance(rank1, rank2):
    # Get the number of pairwise disagreements
    disagreements = 0
    for i in range(len(rank1)):
        for j in range(i + 1, len(rank1)):
            # Check for disagreements in the ordering
            if (rank1[i] < rank1[j] and rank2[i] > rank2[j]) or \
               (rank1[i] > rank1[j] and rank2[i] < rank2[j]):
                disagreements += 1

    # Return the raw Kendall Tau distance (not normalized)
    return disagreements


def aggregate_kemeny(rankings):
    candidates = rankings[0]
    min_distance = float('inf')
    best_ranking = None

    # Iterate over all possible permutations of candidates
    for perm in permutations(candidates):
        # Calculate the total Kendall tau distance for this permutation
        total_distance = sum(kendall_tau_distance(perm, rank) for rank in rankings)

        # If this permutation has a smaller total distance, update the best ranking
        if total_distance < min_distance:
            min_distance = total_distance
            best_ranking = perm

    return best_ranking, min_distance

# Example usage:
rankings = [
    ['A', 'B', 'C'],
    ['B', 'A', 'C'],
    ['A', 'C', 'B']
]

best_ranking, min_distance = aggregate_kemeny(rankings)
print(f"Best Kemeny ranking: {best_ranking}")
print(f"Minimum Kendall tau distance: {min_distance}")
