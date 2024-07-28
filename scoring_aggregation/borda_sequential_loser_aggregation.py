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

def borda_sequential_loser_aggregation(rankings):
    """
    Aggregates rankings using the Borda Count scoring rule and the Sequential Loser method.
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

    # Sequential Loser process
    result = []

    while scores:
        # Find the item with the lowest score
        lowest_score_item = min(scores, key=scores.get)
        lowest_score = scores[lowest_score_item]

        # Group items with the same lowest score
        lowest_score_group = [item for item, score in scores.items() if score == lowest_score]
        result.insert(0, lowest_score_group)  # Insert at the beginning to rank them at the bottom

        # Remove the lowest score items from scores
        for item in lowest_score_group:
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

    return result

# Example usage with a simple graph
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([(1, 2), (1, 4), (3, 4), (2, 4)])

ranking1 = categoriser_based_ranking(G)
ranking2 = discussion_based(G, 1)
rankings.append(ranking1)
rankings.append(ranking2)
print("Rankings:", rankings)

result = borda_sequential_loser_aggregation(rankings)
print("Result:", result)
