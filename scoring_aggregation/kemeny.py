def flatten_ranking(ranking):
    return [item for sublist in ranking for item in sublist]

def kendall_tau_distance(rank1, rank2):
    # Flatten the rankings
    flat_rank1 = flatten_ranking(rank1)
    flat_rank2 = flatten_ranking(rank2)
    print("flat rank1" , flat_rank1)
    # Get the number of pairwise disagreements
    disagreements = 0
    for i in range(len(flat_rank1)):
        for j in range(i + 1, len(flat_rank1)):
            # Check for disagreements in the ordering
            if (flat_rank1[i] < flat_rank1[j] and flat_rank2[i] > flat_rank2[j]) or \
               (flat_rank1[i] > flat_rank1[j] and flat_rank2[i] < flat_rank2[j]):
                disagreements += 1
            # Consider cases where elements are equal
            elif (flat_rank1[i] == flat_rank1[j] and flat_rank2[i] != flat_rank2[j]) or \
                 (flat_rank1[i] != flat_rank1[j] and flat_rank2[i] == flat_rank2[j]):
                disagreements += 0.5

    # Calculate the Kendall Tau distance
    tau = disagreements 
    return tau
rank1 = [[1, 2], [3, 4]]
rank2 = [[2, 1], [4, 3]]

distance = kendall_tau_distance(rank1, rank2)
print("Kendall Tau Distance:", distance)
