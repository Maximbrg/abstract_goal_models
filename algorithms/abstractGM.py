import sys

sys.path.append('../')
import networkx as nx
import matplotlib.pyplot as plt
from algorithms.abstractContLinks import abstractContLinksAlgorithm
from algorithms.propMand import propMandAlgorithm
from algorithms.abstractContLinks import absAbCoAlgorithm
from algorithms.inducedSubmodel import induced_subModel

from parser.meMap_parser import me_map
from parser.task_graph import tasks_map
from parser.quality_graph import quality_map

import netgraph

def extend_graph(target_graph=None, edges=None):
    """

    :param target_graph:
    :param edges:
    :return:
    """
    for edge in edges:
        if target_graph.edges[(edge[0], edge[1])].edge_type == 'ConsistsOf' or \
                target_graph.edges[(edge[0], edge[1])].edge_type == 'AchievedBy':
            target_graph.me_map_graph.add_edge(edge[0], edge[1])


def abstractGMAlgorithm(path=None, mandatory=None):
    """

    :param path:
    :param mandatory:
    :return:
    """
    me_map_graph = me_map(path, mandatory=mandatory)
    induced_subModel(me_map_graph)
    task_graph = tasks_map(me_map_graph)

    propMandAlgorithm(graph=task_graph, start_node=task_graph.nodes[-1])  # NEED TO CHANGE THE ROOT
    ####
    for key in task_graph.nodes:
        task_graph.nodes[key].is_visited = False
    ####
    absAbCoAlgorithm(graph=task_graph, start_node=-1)
    # THIS SHOULD BE OUT OF THE absAbColAlgorithm
    ####
    for node in task_graph.nodes.keys():
        if task_graph.nodes[node].node_label_type == 'R' and task_graph.nodes[node].node_type == 'Task':
            try:
                task_graph.me_map_graph.remove_node(node)
            except nx.exception.NetworkXError:
                continue
    ####
    me_map_2 = me_map(path, mandatory=mandatory)
    quality_graph = quality_map(complete_graph=me_map_2, task_graph=task_graph)

    for key in quality_graph.nodes:
        quality_graph.nodes[key].is_visited = False

    abstractContLinksAlgorithm(graph=quality_graph)
    extend_graph(target_graph=quality_graph, edges=task_graph.me_map_graph.edges)

    return quality_graph


def run():
    path = 'C:\\Users\\max_b\\PycharmProjects\\abstract_goal_models\\me-maps\\example.json'
    mandatory = ['t', 'q1', 'q2', 'q8', 't6', 't7', 't8', 't11']
    graph = abstractGMAlgorithm(path=path, mandatory=mandatory)

    # plt.figure(figsize=(5, 5))
    # nx.draw_kamada_kawai(graph.me_map_graph, with_labels=True)
    # plt.show()

    edge_labels = {}
    nodes_labels = {}

    pos = nx.spring_layout(graph.me_map_graph)

    for edge in graph.me_map_graph.edges:
        edge_labels[edge[0], edge[1]] = graph.edges[edge].edge_type

    for node in graph.me_map_graph.nodes:
        nodes_labels[node] = graph.nodes[node].label

    I = netgraph.InteractiveGraph(graph.me_map_graph,
                                  # node_positions=dict(zip(nodes, pos)),
                                  node_labels=nodes_labels,
                                  edge_labels=edge_labels,
                                  node_label_bbox=dict(fc="lightgreen", ec="black", boxstyle="square", lw=3),
                                  node_size=4,
                                  )

    plt.axis('off')
    plt.show()

    # pos = nx.spring_layout(graph.me_map_graph)
    # plt.figure()
    # nx.draw(
    #     graph.me_map_graph, pos, edge_color='black', width=1, linewidths=1,
    #     node_size=500, node_color='pink', alpha=.5,
    #     labels={node: node for node in graph.me_map_graph.nodes()}
    # )
    # nx.draw_networkx_edge_labels(
    #     graph.me_map_graph, pos,
    #     edge_labels=edge_labels,
    #     font_color='red'
    # )
    # plt.axis('off')
    # plt.show()


if __name__ == '__main__':
    run()
