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

def plurality_sequential_loser_aggregation(rankings):
    """
    Aggregates rankings sequentially using the Plurality scoring rule and the Sequential Loser method.
    Returns a list of lists where items with the same score are grouped together.
    """
    aggregated_rankings = []
    remaining_rankings = rankings.copy()

    # Collect all unique items from the rankings
    items = set()
    for ranking in rankings:
        for sublist in ranking:
            items.update(sublist)
    
    scores = {item: 0 for item in items}

    # Calculate initial scores based on rankings
    for ranking in rankings:
        if ranking:
            for sublist in ranking:
                if sublist:  # Check if sublist is not empty
                    for item in sublist:
                        scores[item] += 1
                    break  # Only the top-ranked items get a score of 1

    # Sequential Loser process
    while scores:
        # Find the item with the lowest score
        lowest_score_item = min(scores, key=scores.get)
        lowest_score = scores[lowest_score_item]

        # Group items with the same lowest score
        lowest_score_group = [item for item, score in scores.items() if score == lowest_score]
        aggregated_rankings.insert(0, lowest_score_group)  # Insert at the beginning to rank them at the bottom

        # Remove the lowest score items from scores
        for item in lowest_score_group:
            del scores[item]

        # Recalculate scores for the remaining items
        scores = {item: 0 for item in scores}
        for ranking in remaining_rankings:
            if ranking:
                for sublist in ranking:
                    if sublist:  # Check if sublist is not empty
                        for item in sublist:
                            if item in scores:  # Only consider remaining items
                                scores[item] += 1
                        break  # Only the top-ranked items get a score of 1

    return aggregated_rankings

# Example usage with a simple graph
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([(1, 2), (1, 4), (3, 4), (2, 4)])

rankings = [
    [[1], [2, 3], [4]],
    [[2], [1, 4], [3]],
    [[4], [1, 2, 3]],
    [[3], [1, 2, 4]]
]

result = plurality_sequential_loser_aggregation(rankings)
print("Aggregated Rankings (Plurality Sequential Loser):", result)
