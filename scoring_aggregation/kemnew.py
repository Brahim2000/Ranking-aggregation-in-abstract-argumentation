from itertools import permutations, combinations

def flatten_ranking(ranking):
    """Flattens a ranking into a list while preserving the order."""
    flat_list = []
    for group in ranking:
        flat_list.extend(group)
    return flat_list

def kendall_tau_distance(rank1, rank2):
    """
    Calculate the Kendall Tau distance between two rankings, where ties are allowed.
    """
    # Flatten both rankings
    flat_rank1 = flatten_ranking(rank1)
    flat_rank2 = flatten_ranking(rank2)

    # Create a dictionary of ranks for easier comparison
    rank1_pos = {item: i for i, group in enumerate(rank1) for item in group}
    rank2_pos = {item: i for i, group in enumerate(rank2) for item in group}

    disagreements = 0
    for i in range(len(flat_rank1)):
        for j in range(i + 1, len(flat_rank1)):
            a, b = flat_rank1[i], flat_rank1[j]
            if (rank1_pos[a] < rank1_pos[b] and rank2_pos[a] > rank2_pos[b]) or \
               (rank1_pos[a] > rank1_pos[b] and rank2_pos[a] < rank2_pos[b]):
                disagreements += 1

    return disagreements

def find_consistent_ties(rankings):
    """Identify the consistent tie groups across all rankings."""
    # Start with the tie groups in the first ranking
    consistent_ties = [set(group) for group in rankings[0]]
    
    for ranking in rankings[1:]:
        new_consistent_ties = []
        for tie_group in consistent_ties:
            intersected_groups = []
            for group in ranking:
                intersection = tie_group & set(group)
                if intersection:
                    intersected_groups.append(intersection)
            new_consistent_ties.extend(intersected_groups)
        consistent_ties = new_consistent_ties

    return [list(group) for group in consistent_ties]

def generate_permutations_with_ties(tie_groups):
    """Generate all permutations respecting the tie groups."""
    for perm in permutations(tie_groups):
        flattened = [item for group in perm for item in sorted(group)]
        yield [list(group) for group in perm]

def aggregate_kemeny(rankings):
    # Identify consistent tie groups
    consistent_ties = find_consistent_ties(rankings)
    min_distance = float('inf')
    best_ranking = None

    # Generate all permutations that respect these ties
    for perm in generate_permutations_with_ties(consistent_ties):
        total_distance = sum(kendall_tau_distance(perm, rank) for rank in rankings)
        if total_distance < min_distance:
            min_distance = total_distance
            best_ranking = perm

    return best_ranking

# Example usage:
rankings = [
    [[1, 5], [9], [6], [2, 4], [8], [7], [3]],
    [[1, 5], [9], [6], [2], [4], [8], [3], [7]],
    [[1, 5], [9], [6], [2, 4], [8], [7], [3]]
]

best_ranking = aggregate_kemeny(rankings)
print(f"Best Kemeny ranking: {best_ranking}")
