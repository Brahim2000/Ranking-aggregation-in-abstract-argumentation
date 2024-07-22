def categoriser_based_ranking(G):
    # Initialize
    categoriser_values = {}
    for node in G.nodes():
        categoriser_values[node] = 1

    # Compute categoriser values
    for node in G.nodes():
        if len(list(G.predecessors(node))) == 0:
            categoriser_values[node] = 1
        else:
            total_sum = sum(categoriser_values[pred] for pred in G.predecessors(node))
            categoriser_values[node] = 1 / (1 + total_sum)

    # Rank
    sorted_nodes = sorted(G.nodes(), key=lambda x: categoriser_values[x], reverse=True)

    # Create rankings
    rankings = []
    previous_value = None
    equal_group = []

    for node in sorted_nodes:
        current_value = categoriser_values[node]
        if previous_value is None:
            equal_group.append(node)
        elif current_value == previous_value:
            equal_group.append(node)
        else:
            if equal_group:
                rankings.append(equal_group)
            equal_group = [node]
        previous_value = current_value

    if equal_group:
        rankings.append(equal_group)

    return rankings
