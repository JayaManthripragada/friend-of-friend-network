import random
import networkx as nx
import matplotlib.pyplot as plt

def grow_preferential_attachment_tree(n, delay=0.5):
    """
    Show the growth of a preferential attachment tree step-by-step.
    Each new node attaches to an existing node with probability proportional to its degree.
    
    Parameters
    ----------
    n : int
        Total number of nodes in the tree.
    delay : float
        Delay in seconds between steps for visualization.
    """
    G = nx.Graph()
    G.add_node(0)  # Start with one root node
    
    # This list will hold nodes repeated according to their degree
    degree_list = [0]
    
    # Fixed positions for consistent layout
    pos = {0: (0, 0)}
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))
    
    for new_node in range(1, n):
        chosen = random.choice(degree_list)  # preferential choice
        G.add_edge(new_node, chosen, color='r')
        
        # Update degree_list for proportional selection
        degree_list.append(new_node)  # degree 1 for new node
        degree_list.append(chosen)    # chosen node gets +1 degree
        
        # Assign position near chosen node
        # pos[new_node] = (
        #     pos[chosen][0] + random.uniform(-1, 1),
        #     pos[chosen][1] + random.uniform(-1, 1)
        # )
        edges = G.edges()
        colors = [G[u][v]['color'] for u,v in edges]
        ax.clear()
        nx.draw(
            G, pos, with_labels=True,
            node_color="skyblue", edge_color=colors,
            node_size=500, ax=ax
        )
        ax.set_title(f"Preferential Attachment Tree Growth\nStep {new_node} / {n-1}")
        plt.pause(delay)
    
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    grow_preferential_attachment_tree(n=100, delay=0.4)
