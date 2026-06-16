import random
import networkx as nx
import matplotlib.pyplot as plt
import time

def grow_uniform_attachment_tree(n, delay=0.5):
    """
    Show the growth of a uniform attachment tree step-by-step.
    
    Parameters
    ----------
    n : int
        Total number of nodes.
    delay : float
        Delay in seconds between steps for visualization.
    """
    G = nx.Graph()
    G.add_node(0)  # Start with a single root node
    
    # Layout fixed so nodes don't jump around
    pos = {0: (0, 0)}
    
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots(figsize=(6, 6))
    
    for new_node in range(1, n):
        chosen = random.randint(0, new_node - 1)
        G.add_edge(new_node, chosen)
        
        # Give new node a random position near chosen node
        pos[new_node] = (
            pos[chosen][0] + random.uniform(-1, 1),
            pos[chosen][1] + random.uniform(-1, 1)
        )
        
        ax.clear()
        nx.draw(
            G, pos, with_labels=True,
            node_color="lightgreen", edge_color="gray",
            node_size=500, ax=ax
        )
        ax.set_title(f"Uniform Attachment Tree Growth\nStep {new_node} / {n-1}")
        plt.pause(delay)
    
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    grow_uniform_attachment_tree(n=20, delay=0.4)
