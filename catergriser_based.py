def categoriser_based_ranking(G) :
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

    #affichage console
    print("categoriser values" , categoriser_values)

    # Rank
    sorted_nodes = sorted(G.nodes(), key=lambda x: categoriser_values[x], reverse=True)
    #print("categoriser rank" , sorted_nodes)
    #return sorted_nodes

    # Create ranking string
    rank_string = ""
    previous_value = None
    equal_group = []

    for i, node in enumerate(sorted_nodes):
        current_value = categoriser_values[node]
        if previous_value is None:
            equal_group.append(f'"{node}"')
        elif current_value == previous_value:
            equal_group.append(f'"{node}"')
        else:
            if equal_group:
                rank_string += " ≃ ".join(equal_group) + " ≻ "
            equal_group = [f'"{node}"']
        previous_value = current_value

    if equal_group:
        rank_string += " ≃ ".join(equal_group)

    #affichage console
    print("categoriser values", categoriser_values)
    print("categoriser rank", sorted_nodes)
    print("ranking string", rank_string)
    
    return rank_string



