import networkx as nx

def calculate_strengths(G):
    strengths = {}
    pageranks = nx.pagerank(G)
    
    for node in G.nodes():
        if G.in_degree(node) == 0:  # Non-attacked arguments
            strengths[node] = 1  # Assign the highest possible strength
        else:
            strengths[node] = 1 - max([max([G.edges[x, y].get('weight', pageranks[node]), pageranks[y]]) for x, y in G.in_edges(node)] + [0])
    
    return strengths

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
