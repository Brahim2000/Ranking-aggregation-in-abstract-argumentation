import networkx as nx

def calculate_strengths(G):
    strengths = {}
    non_attacked_arguments = []

    # Step 1: Calculate the pagerank for all nodes only once
    pagerank_values = nx.pagerank(G)

    # Step 2: Calculate initial strengths for all nodes
    for node in G.nodes():
        if G.in_degree(node) > 0:
            # Calculate strength for attacked arguments
            strengths[node] = 1 - max(
                [max(G.edges[x, y].get('weight', pagerank_values[node]), pagerank_values[y]) for x, y in G.in_edges(node)] + [0]
            )
        else:
            # Store non-attacked arguments for later
            non_attacked_arguments.append(node)

    if strengths:
        max_strength = max(strengths.values())
    else:
        max_strength = 1  # Default if all nodes are non-attacked

    for node in non_attacked_arguments:
        strengths[node] = max_strength



    return strengths, non_attacked_arguments

def zero_sum(G):
    s, non_attacked_arguments = calculate_strengths(G)
    values = {}
    for x in G.nodes():
        value = 0
        for y in G.nodes():
            if (x, y) in G.edges:
                value += s[y]
            elif (y, x) in G.edges:
                value -= s[y]
        values[x] = value
    return values, non_attacked_arguments

# Define the Matt and Toni ranking
def mt_ranking(G):
    values, non_attacked_arguments = zero_sum(G)
    
    
    highest_argument = max(values, key=values.get)  
    highest_value = values[highest_argument]  
    
    for arg in non_attacked_arguments:
        values[arg] = highest_value

    rankings = []
    previous_value = None
    equal_group = []

    sorted_nodes = sorted(G.nodes(), key=lambda x: values[x], reverse=True)

    for node in sorted_nodes:
        current_value = values[node]
        if previous_value is None or current_value == previous_value:
            equal_group.append(node)  # Add node to the current group
        else:
            if equal_group:
                rankings.append(sorted(equal_group))  
            equal_group = [node]  

        previous_value = current_value

    if equal_group:
        rankings.append(sorted(equal_group))

    return rankings
