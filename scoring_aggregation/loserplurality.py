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
    
    # Sort items based on scores in ascending order (for losers)
    sorted_items = sorted(scores.items(), key=lambda x: x[1])
    
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

def plurality_sequential_loser_aggregation(rankings):
    """
    Aggregates rankings sequentially using the Plurality scoring rule and returns a list of lists 
    where items with the same score are grouped together. All items with the lowest score (0) 
    are selected as losers and prepended to the consensus ranking.
    """
    aggregated_rankings = []
    remaining_rankings = rankings.copy()

    while remaining_rankings:
        current_loser_group = plurality_score_aggregation(remaining_rankings)
        
        # Select all items with the lowest score (0)
        losers = current_loser_group[0]
        aggregated_rankings.insert(0, losers)  # Prepend the losers to the aggregated rankings

        # Remove the current losers from remaining rankings
        new_remaining_rankings = []
        for ranking in remaining_rankings:
            new_ranking = []
            for sublist in ranking:
                new_sublist = [item for item in sublist if item not in losers]
                if new_sublist:
                    new_ranking.append(new_sublist)
            if new_ranking:
                new_remaining_rankings.append(new_ranking)
        remaining_rankings = new_remaining_rankings

    return aggregated_rankings  # No need to reverse, since losers are prepended

import networkx as nx

# Example rankings
ranking1 = [[1], [3], [9], [6], [2, 4], [8], [7], [5]]
print("ranking 1", ranking1)
ranking2 = [[5], [1], [9], [6], [2, 4], [8], [7], [3]]
print("ranking 2", ranking2)

rankings.extend(2 * [ranking1])
rankings.extend(3 * [ranking2])
print("Rankings:", rankings)

result = plurality_sequential_loser_aggregation(rankings)
print("Aggregated Rankings (Plurality Sequential Loser):", result)
