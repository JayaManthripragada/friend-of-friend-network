import random
import networkx as nx
import matplotlib.pyplot as plt

def preferential_attachment_tree(n):
    """
    Generate a preferential attachment tree with n nodes.
    Starts with a single node (0) and each new node connects
    to one existing node chosen with probability proportional to its degree.
    
    Parameters
    ----------
    n : int
        Number of nodes in the tree.
    
    Returns
    -------
    G : networkx.Graph
        The generated preferential attachment tree.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
        
    # Start with one node
    G = nx.Graph()
    G.add_node(0)
    
    # List for degree-proportional selection
    # We'll store each node as many times as its degree (multiset)
    targets = [0]  
    
    for new_node in range(1, n):
        # Pick one existing node proportional to degree
        chosen = random.choice(targets)
        G.add_edge(new_node, chosen)
        
        # Update targets list
        targets.append(new_node)  # new node has degree 1
        targets.append(chosen)    # chosen node's degree increased by 1
    
    return G

# Example usage
if __name__ == "__main__":
    N = 30  # number of nodes
    tree = preferential_attachment_tree(N)
    
    # Draw the tree
    pos = nx.spring_layout(tree, seed=42)
    nx.draw(tree, pos, with_labels=True, node_size=500, node_color="skyblue", edge_color="gray")
    plt.title(f"Preferential Attachment Tree (n={N})")
    plt.show()
