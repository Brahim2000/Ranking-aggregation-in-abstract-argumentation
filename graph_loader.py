import networkx as nx

def load_graph_from_file(filename="graph.gml"):
    G = nx.read_gml(filename)
    print(f"Graph loaded from {filename}")
    return G
