# Calculate the strengths of each argument
import networkx as nx

def calculate_strengths(G):
  strengths = {}
  for node in G.nodes():
    strengths[node] = 1 - max([max([G.edges[x, y].get('weight', nx.pagerank(G)[node]), nx.pagerank(G)[y]]) for x, y in G.in_edges(node)] + [0])
  return strengths



# Assign ranks to each argument based on strength and value of zero-sum game
def zero_sum(G):
  s = calculate_strengths(G)
  values = {}
  for x in G.nodes():
      value = 0
      for y in G.nodes():
          if (x, y) in G.edges:
              value += s[y]
          elif (y, x) in G.edges:
              value -= s[y]
      values[x] = value
  return values



# Define the Matt and Toni ranking 

def mt_ranking(G):
    values = zero_sum(G)
    ranking = sorted(G.nodes(), key=lambda x: values[x], reverse=True)
    print("Matt Toni ranking is ", values)
    
    # Create a dictionary with nodes as keys and their ranks as values
    rank_dict = {node: rank for rank, node in enumerate(ranking, start=1)}
    
    # Create a reverse dictionary with ranks as keys and list of nodes with that rank as values
    reverse_rank_dict = {}
    for node, rank in rank_dict.items():
        reverse_rank_dict.setdefault(rank, []).append(node)
    
    # Convert the reverse dictionary to a list of lists format
    rankings = []
    for rank, nodes in sorted(reverse_rank_dict.items()):
        rankings.append(sorted(nodes))

    return rankings