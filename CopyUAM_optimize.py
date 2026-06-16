import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
from scipy.sparse.csgraph import shortest_path
import time

def fast_kamada_kawai_layout(G, pos=None, scale=1.0, tol=1e-4, max_iter=1000):
    nodes = list(G.nodes())
    n = len(nodes)
    node_index = {node: i for i, node in enumerate(nodes)}

    # All-pairs shortest paths
    dist = shortest_path(nx.to_scipy_sparse_array(G, nodelist=nodes, weight=None), directed=False)

    # Handle disconnected pairs: set to large value
    max_dist = np.nanmax(dist[np.isfinite(dist)])
    dist[~np.isfinite(dist)] = max_dist * 10

    # Ideal spring lengths
    L = dist / dist.max()
    np.fill_diagonal(L, 0.0)  # no self-length

    # Spring strengths
    with np.errstate(divide='ignore', invalid='ignore'):
        K = 1.0 / (dist ** 2)
    K[~np.isfinite(K)] = 0.0
    np.fill_diagonal(K, 0.0)

    # Initial positions
    if pos is None:
        pos_arr = np.random.rand(n, 2)
    else:
        pos_arr = np.array([pos[node] for node in nodes], dtype=float)

    # Iterative optimization
    for _ in range(max_iter):
        delta = pos_arr[:, np.newaxis, :] - pos_arr[np.newaxis, :, :]
        dist_xy = np.linalg.norm(delta, axis=2)
        dist_xy[dist_xy == 0] = 1e-9  # avoid /0

        diff = (K * (dist_xy - L) / dist_xy)[:, :, np.newaxis] * delta
        grad = diff.sum(axis=1)

        if np.linalg.norm(grad) < tol:
            break

        pos_arr -= 0.01 * grad

    # Center & scale
    pos_arr -= pos_arr.mean(axis=0)
    pos_arr *= scale / np.abs(pos_arr).max()

    return {node: pos_arr[i] for i, node in enumerate(nodes)}

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
    N = 10000
    tree = uniform_attachment_tree(N, p=.25)
    edges = tree.edges()
    colors = [tree[u][v]['color'] for u,v in edges]
    init_pos = nx.spring_layout(tree, seed=42)
    pos = fast_kamada_kawai_layout(tree, pos=init_pos, scale=2, tol=1e-3, max_iter=200)
    nx.draw(tree, pos, node_size=5, node_color="green", edge_color=colors)
    #nx.write_graphml(tree, "output_graph.graphml")
    plt.title(f"Uniform Attachment Tree (n={N})")
    end = time.time()  # record end time
    print(f"Runtime: {end - start:.4f} seconds")
    plt.show()
    
