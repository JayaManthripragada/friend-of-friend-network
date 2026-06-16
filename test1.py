import random
import networkx as nx
import matplotlib.pyplot as plt

def hierarchy_pos(G, root=0, width=2., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    Positions nodes in a hierarchy.
    Adapted from Joel's networkx tree layout recipe.
    """
    def _hierarchy_pos(G, root, leftmost, width, vert_gap, vert_loc, pos, parent=None):
        children = [n for n in G.neighbors(root) if n != parent]
        if not children:
            pos[root] = (leftmost[0], vert_loc)
            leftmost[0] += width
        else:
            start = leftmost[0]
            for c in children:
                _hierarchy_pos(G, c, leftmost, width/len(children), vert_gap,
                               vert_loc - vert_gap, pos, root)
            end = leftmost[0] - width/len(children)
            pos[root] = ((start + end) / 2., vert_loc)
        return pos
    return _hierarchy_pos(G, root, [0.0], width, vert_gap, vert_loc, {})

def grow_preferential_attachment_tree(n, delay=0.3):
    """
    Show the growth of a preferential attachment tree step-by-step with a clean hierarchical layout.
    """
    G = nx.Graph()
    G.add_node(0)
    degree_list = [0]

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))

    # Build the full tree first (so we know layout)
    edges_all = []
    for new_node in range(1, n):
        chosen = random.choice(degree_list)
        edges_all.append((new_node, chosen))
        degree_list.append(new_node)
        degree_list.append(chosen)

    # Create final graph for stable layout
    G_final = nx.Graph()
    G_final.add_edges_from(edges_all)
    pos = hierarchy_pos(G_final, root=0)  # stable hierarchical layout

    # Now animate adding edges
    G.clear()
    G.add_node(0)
    for step, (u, v) in enumerate(edges_all, start=1):
        G.add_edge(u, v, color='gray')
        ax.clear()
        colors = [G[u][v]['color'] for u, v in G.edges()]
        nx.draw(
            G, pos, with_labels=True,
            node_color="skyblue", edge_color=colors,
            node_size=500, ax=ax
        )
        ax.set_title(f"Preferential Attachment Tree Growth\nStep {step} / {len(edges_all)}")
        plt.pause(delay)

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    grow_preferential_attachment_tree(n=50, delay=0.2)
