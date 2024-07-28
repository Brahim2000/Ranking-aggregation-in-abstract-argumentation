import sys
import os

# Get the absolute path of the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

from catergriser_based import categoriser_based_ranking
from discussion_based import discussion_based

rankings = []

def plurality_score_aggregation(rankings):
    """
    Aggregates rankings using the Plurality scoring rule and returns a list of lists where 
    items with the same score are grouped together.
    """
    # Collect all unique items from the rankings
    items = set()
    for ranking in rankings:
        for sublist in ranking:
            items.update(sublist)
    
    scores = {item: 0 for item in items}

    # Calculate scores based on rankings
    for ranking in rankings:
        if ranking:
            for sublist in ranking:
                if sublist:  # Check if sublist is not empty
                    for item in sublist:
                        scores[item] += 1
                    break  # Only the top-ranked items get a score of 1

    # Print the scores
    print("Scores:")
    for item, score in scores.items():
        print(f"{item}: {score}")
    
    # Sort items based on scores in descending order
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Group items with the same score into sublists
    result = []
    current_score = None
    current_group = []

    for item, score in sorted_items:
        if current_score is None or score == current_score:
            current_group.append(item)
        else:
            result.append(current_group)
            current_group = [item]
        current_score = score

    if current_group:
        result.append(current_group)

    return result

def plurality_sequential_winner_aggregation(rankings):
    """
    Aggregates rankings sequentially using the Plurality scoring rule and returns a list of lists 
    where items with the same score are grouped together.
    """
    aggregated_rankings = []
    remaining_rankings = rankings.copy()

    while remaining_rankings:
        current_winner_group = plurality_score_aggregation(remaining_rankings)
        aggregated_rankings.append(current_winner_group[0])  # Append the top group of current winners

        # Remove the current winners from remaining rankings
        new_remaining_rankings = []
        for ranking in remaining_rankings:
            new_ranking = []
            for sublist in ranking:
                new_sublist = [item for item in sublist if item not in current_winner_group[0]]
                if new_sublist:
                    new_ranking.append(new_sublist)
            if new_ranking:
                new_remaining_rankings.append(new_ranking)
        remaining_rankings = new_remaining_rankings

    return aggregated_rankings

import networkx as nx

#G = nx.DiGraph()
#G.add_edges_from([(1, 2), (1, 3), (4, 3), (5, 4),(4, 6), (5, 7), (5, 8), (6, 7),(7, 8), (8, 9)])

ranking1 = [[1], [3], [9], [6], [2, 4], [8], [7], [5]]
print("ranking 1" , ranking1)
ranking2 = [[5], [1], [9], [6], [2, 4], [8], [7], [3]]
print("ranking 2" , ranking2)

rankings.extend(2*[ranking1])
rankings.extend(3*[ranking2])
print("Rankings:", rankings)


result = plurality_sequential_winner_aggregation(rankings)
print("Aggregated Rankings (Plurality Sequential Winner):", result)
