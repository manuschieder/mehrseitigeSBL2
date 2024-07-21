import networkx as nx
import matplotlib.pyplot as plt


class BipartiteGraphPlotter:

    def __init__(self, attack: str, contacts: list[list[int]]):
        self.attack = attack
        self.contacts = contacts
        self.graphs = []
        # Iterate over contact list, keeping in mind that indices start at 0 while sender number starts at 1
        for sender_nr in range(1, len(self.contacts) + 1):
            G = nx.Graph()
            G.add_node(sender_nr, bipartite=0)
            # Add nodes and edges for each receiver
            for receiver_nr in range(1, len(self.contacts[sender_nr - 1]) + 1):
                G.add_node(receiver_nr, bipartite=1)
                G.add_edge(sender_nr, receiver_nr)
            self.graphs.append(G)

    def plot_bipartite_graphs(self):
        for sender_nr in range(1, len(self.contacts) + 1):
            graph = self.graphs[sender_nr - 1]
            pos = nx.bipartite_layout(graph, [sender_nr])
            nx.draw(graph, pos, with_labels=True,
                    node_color=['skyblue' if node == sender_nr else 'lightgreen' for node in graph],
                    edge_color='gray', node_size=500)
            plt.title(f"SDA - Sender {sender_nr}")
            plt.savefig(f'{self.attack} - Sender {sender_nr}')
            plt.show()
