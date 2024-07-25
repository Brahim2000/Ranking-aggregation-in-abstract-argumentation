import sys
import os

# Obtenez le chemin absolu du répertoire contenant le script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ajoutez le chemin du répertoire parent à sys.path
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

from catergriser_based import categoriser_based_ranking
from discussion_based import discussion_based

rankings = []

def borda_sequential_winner_aggregation(rankings):
    """
    Aggregates rankings using the Borda Count scoring rule and the Sequential Winner method.
    Returns a list of lists where items with the same score are grouped together.
    """
    # Collect all unique items from the rankings
    items = set()
    for ranking in rankings:
        for sublist in ranking:
            items.update(sublist)
    
    num_items = len(items)
    scores = {item: 0 for item in items}

    # Calculate initial scores based on rankings
    for ranking in rankings:
        rank = num_items
        for sublist in ranking:
            sublist_size = len(sublist)
            score = sum(range(rank - sublist_size + 1, rank + 1)) / sublist_size
            for item in sublist:
                scores[item] += score
            rank -= sublist_size

    # Sequential Winner process
    result = []

    while scores:
        # Find the item with the highest score
        highest_score_item = max(scores, key=scores.get)
        highest_score = scores[highest_score_item]

        # Group items with the same highest score
        highest_score_group = [item for item, score in scores.items() if score == highest_score]
        result.append(highest_score_group)

        # Remove the highest score items from scores
        for item in highest_score_group:
            del scores[item]

        # Recalculate scores for the remaining items
        scores = {item: 0 for item in scores}
        for ranking in rankings:
            rank = num_items
            for sublist in ranking:
                sublist_size = len(sublist)
                score = sum(range(rank - sublist_size + 1, rank + 1)) / sublist_size
                for item in sublist:
                    if item in scores:
                        scores[item] += score
                rank -= sublist_size
        # Print the scores
    
    return result

# Example usage with a simple graph
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([(1, 2), (1, 3), (4, 3), (5, 4),(4, 6), (5, 7), (5, 8), (6, 7),(7, 8), (8, 9)])

ranking1 = categoriser_based_ranking(G)
print("ranking 1" , ranking1)
ranking2 = discussion_based(G, 1)
print("ranking 2" , ranking2)

rankings.extend(2*[ranking1])
rankings.extend(3*[ranking2])
print("Rankings:", rankings)

result = borda_sequential_winner_aggregation(rankings)
print("Result:", result)
