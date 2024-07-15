import sys

sys.path.append('/')
import networkx as nx
import matplotlib.pyplot as plt
from algorithms.abstractContLinks import abstractContLinksAlgorithm
from algorithms.propMand import propMandAlgorithm
from algorithms.abstractContLinks import absAbCoAlgorithm
from algorithms.inducedSubmodel import induced_subModel
import argparse
from parser.meMap_parser import me_map
from parser.task_graph import tasks_map
from parser.quality_graph import quality_map

import netgraph
import numpy as np
np.float = float
np.int = int   #module 'numpy' has no attribute 'int'
np.object = object    #module 'numpy' has no attribute 'object'
np.bool = bool    #module 'numpy' has no attribute 'bool'
def extend_graph(target_graph=None, edges=None, nodes=None):
    """

    :param nodes:
    :param target_graph:
    :param edges:
    :return:
    """
    for node in nodes:
        if target_graph.nodes[node].node_type == 'Task':
            target_graph.me_map_graph.add_node(node)
    for edge in edges:
        if target_graph.edges[(edge[0], edge[1])].edge_type == 'ConsistsOf' or \
                target_graph.edges[(edge[0], edge[1])].edge_type == 'AchievedBy' or \
                target_graph.edges[(edge[0], edge[1])].edge_type == 'Association':
            target_graph.me_map_graph.add_edge(edge[0], edge[1])


def abstractGMAlgorithm(path=None, mandatory=None, default=False):
    """

    :param default:
    :param path:
    :param mandatory:
    :return:
    """
    me_map_graph = me_map(path, mandatory=mandatory)
    for node in me_map_graph.me_map_graph.nodes:
        predecessors = me_map_graph.me_map_graph.predecessors(node)
        flag = True
        for predecessor in predecessors:
            if me_map_graph.nodes[predecessor].node_type == 'Task':
                flag = False
                break

        if flag:
            root_id = node
            break

    induced_subModel(me_map_graph)
    task_graph = tasks_map(me_map_graph)


    propMandAlgorithm(graph=task_graph, start_node=task_graph.nodes[root_id])

    for key in task_graph.nodes:
        task_graph.nodes[key].is_visited = False

    absAbCoAlgorithm(graph=task_graph, start_node=root_id)

    for node in task_graph.nodes.keys():
        if task_graph.nodes[node].node_label_type == 'R' and task_graph.nodes[node].node_type == 'Task':
            try:
                task_graph.me_map_graph.remove_node(node)
            except nx.exception.NetworkXError:
                continue

    me_map_2 = me_map(path, mandatory=mandatory)
    induced_subModel(me_map_2)
    quality_graph = quality_map(complete_graph=me_map_2, task_graph=task_graph)

    for key in quality_graph.nodes:
        quality_graph.nodes[key].is_visited = False

    abstractContLinksAlgorithm(graph=quality_graph, default=default)
    extend_graph(target_graph=quality_graph, edges=task_graph.me_map_graph.edges, nodes=task_graph.me_map_graph.nodes)

    return quality_graph


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("--map", type=str
                        ,
                        default='C:\\Users\\max_b\\PycharmProjects\\abstract_goal_models\\me-maps\\version_17.6\\t2_1.json', help="The path to the me-map for abstraction")
    parser.add_argument("--mandatory", type=list, default=['t1', 'q5'], #['t', 'q1', 'q2', 'q8', 't6', 't7', 't8', 't11'] ['Choose Course', 'Course 1', 'Course 2', 'Overall Quality']
                        help="The nodes that we want to keep")
    parser.add_argument("--default", type=bool, default=True)
    args = parser.parse_args()

    graph = abstractGMAlgorithm(path=args.map, mandatory=args.mandatory, default=args.default)

    edge_labels = {}
    nodes_labels = {}

    for edge in graph.me_map_graph.edges:
        edge_labels[edge[0], edge[1]] = graph.edges[edge].edge_type

    for node in graph.me_map_graph.nodes:
        nodes_labels[node] = graph.nodes[node].label

    I = netgraph.InteractiveGraph(graph.me_map_graph,
                                  # node_positions=dict(zip(nodes, pos)),
                                  node_labels=nodes_labels,
                                  edge_labels=edge_labels,
                                  node_label_bbox=dict(fc="lightgreen", ec="black", boxstyle="square", lw=3),
                                  node_size=10,
                                  )

    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    run()
