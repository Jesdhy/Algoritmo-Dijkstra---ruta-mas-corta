import networkx as nx
import matplotlib.pyplot as plt

class MaxFlow:
   
    def __init__(self, graph):
        self.graph = graph
    #LOGICA DEL FLUJO MAXIMO
    def max_flow(self, source, target):
        flow_value, flow_dict = nx.maximum_flow(self.graph, source, target, capacity='weight')
        return flow_value, flow_dict

    def plot_graph_with_flow(self, flow_dict):
        plt.figure()
        pos = nx.spring_layout(self.graph)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw(self.graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=15, font_color='black', font_weight='bold', edge_color='gray')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)

        for u, v in self.graph.edges():
            plt.text((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2,
                     s=f"{flow_dict[u][v]}/{self.graph[u][v]['weight']}",
                     horizontalalignment='center', verticalalignment='center', fontsize=10, color='red')

        plt.title("Flujo Máximo")
        plt.show()

