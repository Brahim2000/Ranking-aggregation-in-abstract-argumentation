import networkx as nx

def calculate_strengths(G):
    strengths = {}
    non_attacked_arguments = []

    # Step 1: Calculate initial strengths for all nodes
    for node in G.nodes():
        if G.in_degree(node) > 0:
            # Calculate strength for attacked arguments
            strengths[node] = 1 - max([max([G.edges[x, y].get('weight', nx.pagerank(G)[node]), nx.pagerank(G)[y]]) for x, y in G.in_edges(node)] + [0])
        else:
            # Store non-attacked arguments
            non_attacked_arguments.append(node)
    
    # Step 2: Determine the maximum strength among all calculated strengths
    if strengths:
        max_strength = max(strengths.values())
    else:
        max_strength = 1  # Default if all nodes are non-attacked
    
    # Step 3: Assign the maximum strength to all non-attacked arguments
    for node in non_attacked_arguments:
        strengths[node] = max_strength

    # Display the non-attacked arguments and the max strength assigned to them
    print("Arguments non attaqués :", non_attacked_arguments)
    print("Force attribuée aux arguments non attaqués :", max_strength)
    
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
