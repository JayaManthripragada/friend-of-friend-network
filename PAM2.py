import networkx as nx
import random
import matplotlib.pyplot as plt

def preferential_attachment_tree(n,p):
    """
    Generate a preferential attachment tree with n nodes.
    Each new node attaches to one existing node with probability proportional to degree.
    """
    G = nx.Graph()
    G.add_node(0)  # Start with a single node

    degrees = [1]  # degree list for efficient sampling (initial node has degree 1 for sampling)

    for new_node in range(1, n):
        # Pick a node to attach to, based on degree
        existing_node = random.choices(
            population=list(range(len(degrees))),
            weights=degrees,
            k=1
        )[0]

        # Add the edge
        
        for neighbor in list(G.neighbors(existing_node)):
            if random.uniform(0,1)<=p:
                G.add_edge(new_node, neighbor, color = 'b')
        G.add_edge(new_node, existing_node, color='r')
        # Update the degrees list
        degrees.append(1)  # new node has degree 1
        degrees[existing_node] += 1
    print("Max degree is", max(degrees))
    return G

# Example usage
if __name__ == "__main__":
    n = 100  # number of nodes
    tree = preferential_attachment_tree(n, p=0.15)
    edges = tree.edges()
    colors = [tree[u][v]['color'] for u,v in edges]
    # Draw the tree
    pos = nx.spring_layout(tree)
    nx.draw(tree, pos, with_labels=True, node_size=100, edge_color=colors)
    plt.title("Preferential Attachment Tree (n=100)")
    plt.show()