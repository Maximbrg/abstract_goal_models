__email__ = "maximbr@post.bgu.ac.il"
__author__ = "Maxim Bragilovski"
__date__ = "2022-12-11"

import json
import networkx as nx
import matplotlib.pyplot as plt
import sys

sys.path.append('../')

from components.node import node
from components.edge import edge


class me_map:

    def __init__(self, path: str = None, mandatory: [] = None):
        """

        :param path:
        """

        self.nodes = {}
        self.edges = {}
        self.mandatory = mandatory
        self.mandatory_nodes = []
        self.edge_type = {}

        with open(path) as f:
            data = json.load(f)

        self.me_map_graph = nx.DiGraph()
        self.me_map_graph_labels = nx.DiGraph()
        self.me_map_graph_types = nx.DiGraph()

        for node_in in data["nodeDataArray"]:
            self.me_map_graph.add_node(node_in["key"])
            if node_in["text"] in self.mandatory:
                to_add_node = node(node_id=node_in["key"], label=node_in["text"],
                                   node_type=node_in["category"], node_label_type='M')

                self.mandatory_nodes.append(to_add_node)
                self.nodes[node_in["key"]] = to_add_node
            else:
                self.nodes[node_in["key"]] = node(node_id=node_in["key"], label=node_in["text"],
                                                  node_type=node_in["category"])

        for edge_in in data["linkDataArray"]:
            self.me_map_graph.add_edge(edge_in["from"], edge_in["to"])
            if edge_in["category"] == 'Contribution':
                if edge_in["text"] == "?":
                    self.edges[(edge_in["from"], edge_in["to"])] = edge(from_node=edge_in["from"],
                                                                        to_node=edge_in["to"],
                                                                        edge_type='Association')
                else:
                    self.edges[(edge_in["from"], edge_in["to"])] = edge(from_node=edge_in["from"], to_node=edge_in["to"],
                                                                        edge_type=edge_in["text"])
            else:
                self.edges[(edge_in["from"], edge_in["to"])] = edge(from_node=edge_in["from"], to_node=edge_in["to"],
                                                                    edge_type=edge_in["category"])


def run():
    path = 'C:\\Users\\max_b\\PycharmProjects\\abstract_goal_models\\me-maps\\example.json'
    mandatory = ['t', 'q1', 'q2', 'q8', 't6', 't7', 't8', 't11']
    me_map_1 = me_map(path, mandatory=mandatory)

    plt.figure(figsize=(5, 5))
    nx.draw_kamada_kawai(me_map_1.me_map_graph, with_labels=True)
    plt.show()


if __name__ == '__main__':
    run()
