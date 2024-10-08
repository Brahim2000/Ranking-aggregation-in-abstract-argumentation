def burden_based(G, threshold):
    # Initialization:
    node_to_index = {node: index for index, node in enumerate(G.nodes())}
    predecessors = {node_to_index[node]: [node_to_index[pred] for pred in G.predecessors(node)] for node in G.nodes()}
    num_nodes = G.number_of_nodes()
    nodes = list(G.nodes())
    steps = [1] * num_nodes
    matrix = [steps]

    # Create the steps tab
    for i in range(1, threshold + 1):
        new_steps = [0] * num_nodes
        for j in range(num_nodes):
            if not predecessors[j]:
                new_steps[j] = 1
            else:
                total_sum = sum(1 / steps[pred_index] for pred_index in predecessors[j])
                new_steps[j] = 1 + total_sum

        matrix.append(new_steps)
        steps = new_steps

        if steps == matrix[-2]:
            break

    # Create the burden vectors
    burden_vectors = list(zip(*matrix))
    # print(burden_vectors)

    # Rank
    nodes_bv = list(zip(nodes, burden_vectors))
    sorted_nodes = sorted(nodes_bv, key=lambda x: x[1:])

    # Create the rankings as lists of lists
    rankings = []
    prev_burden_vector = None
    current_group = []

    for node, burden_vector in sorted_nodes:
        if burden_vector == prev_burden_vector:
            current_group.append(node)
        else:
            if current_group:
                rankings.append(current_group)
            current_group = [node]
            prev_burden_vector = burden_vector

    if current_group:
        rankings.append(current_group)

    return rankings
