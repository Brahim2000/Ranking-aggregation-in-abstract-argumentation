import sys
import os

# Get the absolute path of the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory path to sys.path
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

from catergriser_based import categoriser_based_ranking
from discussion_based import discussion_based
#from vetoscore import veto_score_aggregation

rankings = []

def veto_score_aggregation(rankings):
    """Aggregates rankings using the Veto scoring rule and returns a list of lists where 
    items with the same score are grouped together."""
    items = set()
    for ranking in rankings:
        for sublist in ranking:
            items.update(sublist)

    scores = {item: 0 for item in items}

    for ranking in rankings:
        if ranking:
            for sublist in reversed(ranking):
                if sublist:  # Check if sublist is not empty
                    for item in sublist:
                        scores[item] -= 1
                    break  # Only the last-ranked items get a score of -1

    sorted_items = sorted(scores.items(), key=lambda x: x[1])

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

def veto_sequential_loser_aggregation(rankings):
    """Aggregates rankings sequentially using the Veto scoring rule and eliminates items with the lowest score iteratively."""
    aggregated_rankings = []
    remaining_rankings = rankings.copy()
    all_scores = []

    while remaining_rankings:
        current_loser_group = veto_score_aggregation(remaining_rankings)
        aggregated_rankings.insert(0, current_loser_group[0])  # Append the lowest score group of current losers at the start

        # Store and print the scores at each step
        all_scores.append(current_loser_group)
        print("Scores at this step:", current_loser_group)

        # Remove the current losers from remaining rankings
        new_remaining_rankings = []
        for ranking in remaining_rankings:
            new_ranking = []
            for sublist in ranking:
                new_sublist = [item for item in sublist if item not in current_loser_group[0]]
                if new_sublist:
                    new_ranking.append(new_sublist)
            if new_ranking:
                new_remaining_rankings.append(new_ranking)
        remaining_rankings = new_remaining_rankings

    return aggregated_rankings

# Example usage with a simple graph
import networkx as nx

G = nx.DiGraph()
ranking1 = [[1], [3], [9], [6], [2, 4], [8], [7], [5]]
print("ranking 1" , ranking1)
ranking2 = [[5], [1], [9], [6], [2, 4], [8], [7], [3]]
print("ranking 2" , ranking2)

rankings.extend(2*[ranking1])
rankings.extend(3*[ranking2])
print("Rankings:", rankings)

result = veto_sequential_loser_aggregation(rankings)
print("Result:", result)
