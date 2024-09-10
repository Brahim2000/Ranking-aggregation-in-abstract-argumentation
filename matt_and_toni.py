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

    # Step 3: Find the maximum strength among all calculated strengths
    if strengths:
        max_strength = max(strengths.values())
    else:
        max_strength = 1  # Default if all nodes are non-attacked

    # Step 4: Assign the same highest strength to all non-attacked arguments
    for node in non_attacked_arguments:
        strengths[node] = max_strength

    # Display the non-attacked arguments and the max strength assigned to them
    print("Arguments non attaqués :", non_attacked_arguments)
    print("Force attribuée aux arguments non attaqués :", max_strength)

    return strengths, non_attacked_arguments

# Assign ranks to each argument based on strength and value of zero-sum game
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
    
    # Find the argument with the highest value
    highest_argument = max(values, key=values.get)  # Finds the node with the highest value
    highest_value = values[highest_argument]  # Gets the highest value

    # Print the highest value and the corresponding argument
    print(f"The argument with the highest score is '{highest_argument}' with a score of {highest_value}")
    
    # Step 1: Assign the highest_value to all non-attacked arguments
    for arg in non_attacked_arguments:
        values[arg] = highest_value

    # Print the updated values with non-attacked arguments set to the highest value
    print("Updated values with non-attacked arguments assigned highest value:", values)

    # Step 2: Sort the arguments based on their values
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
