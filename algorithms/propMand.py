import sys

sys.path.append('../')

from parser.meMap_parser import me_map
from algorithms.inducedSubmodel import induced_subModel
from parser.task_graph import tasks_map


def different_edge_type(graph=None, incoming_edges=None, outgoing_edges=None):
    """

    :param graph:
    :param incoming_edges:
    :param outgoing_edges:
    :return:
    """
    for incoming_edge in incoming_edges:
        for outgoing_edge in outgoing_edges:
            type_label_incoming = graph.edges[incoming_edge].edge_type
            type_label_outgoing = graph.edges[outgoing_edge].edge_type
            if type_label_incoming != type_label_outgoing:
                return 'M'
    return 'R'


def propMandAlgorithm(graph=None, start_node=None):
    """

    :param graph:
    :param start_node:
    :return:
    """

    if start_node.is_visited:
        return graph

    successors = graph.me_map_graph.successors(start_node.node_id)
    graph.nodes[start_node.node_id].is_visited = True
    for successor_node in successors:
        if graph.nodes[successor_node].node_label_type != 'M':
            incoming_edges = graph.me_map_graph.in_edges(successor_node)
            outgoing_edges = graph.me_map_graph.out_edges(successor_node)
            new_type_label = different_edge_type(graph=graph, incoming_edges=incoming_edges,
                                                 outgoing_edges=outgoing_edges)
            graph.nodes[successor_node].node_label_type = new_type_label

            propMandAlgorithm(graph=graph, start_node=graph.nodes[successor_node])

    return graph


def run():
    path = 'C:\\Users\\max_b\\PycharmProjects\\abstract_goal_models\\me-maps\\example.json'
    mandatory = ['t', 'q1', 'q2', 'q8', 't6', 't7', 't8', 't11']
    me_map_1 = me_map(path, mandatory=mandatory)
    induced_subModel(me_map_1)
    task_graph = tasks_map(me_map_1)
    propMandAlgorithm(graph=task_graph, start_node=task_graph.nodes[-1])
    print()


if __name__ == '__main__':
    run()
