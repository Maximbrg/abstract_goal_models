import networkx as nx
import sys
import matplotlib.pyplot as plt

sys.path.append('../')

from parser.meMap_parser import me_map
from algorithms.inducedSubmodel import induced_subModel
from parser.task_graph import tasks_map
from algorithms.propMand import propMandAlgorithm
from components.edge import edge as ed


def all_paths_to_mandatory(graph: None, root: None):
    """

    :param graph:
    :param root:
    :return:
    """
    paths = []
    for node in graph.me_map_graph:
        if graph.me_map_graph.out_degree(node) == 0:  # it's a leaf
            try:
                path = nx.shortest_path(graph.me_map_graph, root, node)
                paths.append(path)
            except nx.exception.NetworkXNoPath:
                continue

    edges_to_delete = []
    new_edge = []
    for path in paths:
        for id in range(len(path) - 1):
            if graph.nodes[path[id]].node_label_type == 'R':
                edges_to_delete.append((path[id], path[id + 1]))
                if id + 1 == len(path) - 1:
                    new_edge.append(path[id + 1])
            else:
                new_edge.append(path[id])
                break
    return list(dict.fromkeys(edges_to_delete)), list(dict.fromkeys(new_edge))


def absAbCoAlgorithm(graph=None, start_node=None):
    """

    :param graph:
    :param start_node:
    :return:
    """

    if graph.nodes[start_node].is_visited:
        return

    graph.nodes[start_node].is_visited = True
    outgoing_edges = graph.me_map_graph.out_edges(start_node)

    for outgoing_edge in list(outgoing_edges):
        v_label = graph.nodes[outgoing_edge[1]].node_label_type
        if v_label == 'R':
            edges_to_delete, successors = all_paths_to_mandatory(graph=graph, root=outgoing_edge[1])
            for successor in successors:
                graph.me_map_graph.add_edge(outgoing_edge[0], successor)
                graph.edges[(outgoing_edge[0], successor)] = ed(from_node=outgoing_edge[0], to_node=successor,
                                                                edge_type=graph.edges[(outgoing_edge[0], outgoing_edge[1])].edge_type)

                absAbCoAlgorithm(graph=graph, start_node=successor)
            graph.me_map_graph.remove_edge(outgoing_edge[0], outgoing_edge[1])
            for edge in edges_to_delete:
                graph.me_map_graph.remove_edge(edge[0], edge[1])
        else:
            absAbCoAlgorithm(graph=graph, start_node=outgoing_edge[1])


def run():
    path = 'C:\\Users\\max_b\\PycharmProjects\\abstract_goal_models\\me-maps\\example.json'
    mandatory = ['t', 'q1', 'q2', 'q8', 't6', 't7', 't8', 't11']
    me_map_1 = me_map(path, mandatory=mandatory)
    induced_subModel(me_map_1)
    task_graph = tasks_map(me_map_1)
    propMandAlgorithm(graph=task_graph, start_node=task_graph.nodes[-1])
    for key in task_graph.nodes:
        task_graph.nodes[key].is_visited = False
    absAbCoAlgorithm(graph=task_graph, start_node=-1)
    for node in task_graph.nodes.keys():
        if task_graph.nodes[node].node_label_type == 'R' and task_graph.nodes[node].node_type == 'Task':
            try:
                task_graph.me_map_graph.remove_node(node)
            except nx.exception.NetworkXError:
                continue

    plt.figure(figsize=(5, 5))
    nx.draw_kamada_kawai(task_graph.me_map_graph, with_labels=True)
    plt.show()

    print()


if __name__ == '__main__':
    run()
