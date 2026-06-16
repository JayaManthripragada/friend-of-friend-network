import random
import networkx as nx
import matplotlib.pyplot as plt
import time

def uniform_attachment_tree(n,p):
    if n < 1:
        raise ValueError("n must be >= 1")
        
    G = nx.Graph()
    G.add_node(0)  # Start with a single root node
    
    for new_node in range(1, n):
        chosen = random.randint(0, new_node - 1)  # pick uniformly from existing nodes
        
        for neighbor in list(G.neighbors(chosen)): #Look at the neighbors of chosen node
            if random.uniform(0,1)<=p:
                G.add_edge(new_node, neighbor, color = 'b') #add blue edge (copy edges)
        G.add_edge(new_node, chosen, color = 'r') #add red edges
    return G
if __name__ == "__main__":
    start = time.time()
    N = 1000
    tree = uniform_attachment_tree(N, p=.25)
    edges = tree.edges()
    colors = [tree[u][v]['color'] for u,v in edges]
    pos = nx.kamada_kawai_layout(tree)
    nx.draw(tree, pos, node_size=5, node_color="green", edge_color=colors)
    #nx.write_graphml(tree, "output_graph.graphml")
    plt.title(f"Uniform Attachment Tree (n={N})")
    end = time.time()  # record end time
    print(f"Runtime: {end - start:.4f} seconds")
    plt.show()
    
