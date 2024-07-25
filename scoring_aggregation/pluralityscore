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

# Example usage with a simple graph
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([(1, 2), (1, 4), (3, 4), (2, 4)])

ranking1 = categoriser_based_ranking(G)
ranking2 = discussion_based(G, 1)
rankings.append(ranking1)
rankings.append(ranking2)
print("Rankings:", rankings)

result = plurality_score_aggregation(rankings)
print("Result:", result)
