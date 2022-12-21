import networkx as nx

from parser.meMap_parser import me_map
from algorithms.inducedSubmodel import induced_subModel
from algorithms.propMand import propMandAlgorithm
from algorithms.absAbCo import absAbCoAlgorithm
from parser.quality_graph import quality_map
from parser.task_graph import tasks_map

from components.edge import edge as ed


def min_edge(label_1=None, label_2=None):
    """

    :param label_1:
    :param label_2:
    :return:
    """
    if label_1 == '--' or label_2 == '--':
        return '--'
    if label_1 == '-' or label_2 == '-':
        return '-'
    if label_1 == '+' or label_2 == '+':
        return '+'
    if label_1 == '++' or label_2 == '++':
        return '++'


def add_task_edges(quality_graph=None, task_graph=None):
    """

    :param quality_graph:
    :param task_graph:
    :return:
    """
    for node in task_graph.me_map_graph.nodes:
        quality_graph.me_map_graph.add_node(node)

    for edge in task_graph.me_map_graph.edges:
        if task_graph.edges[edge].edge_type != 'AchievedBy' and task_graph.edges[edge].edge_type != 'ConsistsOf':
            quality_graph.me_map_graph.add_edge(edge[0], edge[1])
            quality_graph.edges[(edge[0], edge[1])] = task_graph.edges[(edge[0], edge[1])]


def abstractContLinksAlgorithm(graph=None):
    """

    :param graph:
    :return:
    """

    tasks_nodes = []
    for key in graph.me_map_graph.nodes:
        if graph.nodes[key].node_type == 'Task' and len(graph.me_map_graph.out_edges(key)) > 0:
            print(graph.me_map_graph.out_edges(key))
            tasks_nodes.append(key)
    tasks_nodes = [-12, -2, -8]
    while len(tasks_nodes) > 0:
        start_node = tasks_nodes.pop()
        successors = graph.me_map_graph.successors(start_node)
        for successor in successors:
            incoming_edges_main = graph.me_map_graph.in_edges(successor)
            for incoming_edge in list(incoming_edges_main):
                if incoming_edge[0] == start_node and not graph.edges[(incoming_edge[0], incoming_edge[1])].is_visited:
                    label = graph.edges[(incoming_edge[0], incoming_edge[1])].edge_type
                    graph.edges[(incoming_edge[0], incoming_edge[1])].is_visited = True

                    visited_incoming_edges = True
                    incoming_edges = graph.me_map_graph.in_edges(successor)

                    for incoming_edge_1 in list(incoming_edges):
                        if not graph.edges[(incoming_edge_1[0], incoming_edge_1[1])]:
                            visited_incoming_edges = False
                    if visited_incoming_edges:
                        tasks_nodes.append(successor)

                    incoming_edges_start_node = list(graph.me_map_graph.in_edges(start_node))

                    while len(list(incoming_edges_start_node)) > 0:
                        incoming_edge_new = incoming_edges_start_node.pop()
                        label = min_edge(label, graph.edges[(incoming_edge_new[0], incoming_edge_new[1])].edge_type)
                        edge_h = (incoming_edge_new[0], incoming_edge[1])
                        if edge_h not in graph.me_map_graph.edges:
                            graph.me_map_graph.add_edge(edge_h[0], edge_h[1])
                            graph.edges[edge_h[0], edge_h[1]] = ed(from_node=edge_h[0], to_node=edge_h[1],
                                                                                edge_type=None)
                            graph.edges[edge_h[0], edge_h[1]].all_types.append(label)
                        else:
                            graph.edges[edge_h[0], edge_h[1]].all_types.append(label)

                        graph.edges[edge_h[0], edge_h[1]].updateLabel()
                        graph.me_map_graph.remove_edge(edge_h[0], edge_h[1])
    for node in list(graph.me_map_graph.nodes):
        if graph.nodes[node].node_label_type == 'R':
            graph.me_map_graph.remove_node(node)


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

    me_map_2 = me_map(path, mandatory=mandatory)
    quality_graph = quality_map(complete_graph=me_map_2, task_graph=task_graph)

    for key in quality_graph.nodes:
        quality_graph.nodes[key].is_visited = False

    abstractContLinksAlgorithm(graph=quality_graph)


if __name__ == '__main__':
    run()
