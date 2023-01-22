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


def abstractContLinksAlgorithm(graph=None, default=True):
    """

    :param default:
    :param graph:
    :return:
    """

    tasks_nodes = []
    for key in graph.me_map_graph.nodes:
        if graph.nodes[key].node_type == 'Task' and len(graph.me_map_graph.out_edges(key)) > 0:
            # print(graph.me_map_graph.out_edges(key))
            tasks_nodes.append(key)
    # tasks_nodes = [-8]
    while len(tasks_nodes) > 0:
        # print('======================')
        # print("task nodes" + str(tasks_nodes))
        t_i = tasks_nodes.pop()
        # print("t_i" + str(t_i))
        outgoing_edges_main = graph.me_map_graph.out_edges(t_i)

        for outgoing_edge_main in outgoing_edges_main:

            if graph.edges[(outgoing_edge_main[0], outgoing_edge_main[1])].is_visited:
                continue
            if graph.edges[(outgoing_edge_main[0], outgoing_edge_main[1])].edge_type == 'Association':
                continue

            t_j = outgoing_edge_main[1]
            label = graph.edges[(t_i, t_j)].edge_type
            graph.edges[(t_i, t_j)].is_visited = True

            visited_incoming_edges = True
            incoming_edges = graph.me_map_graph.in_edges(t_j)

            # print(f't_j {t_j}')
            # print(f'incoming_edges of t_j {incoming_edges}')

            for incoming_edge_1 in list(incoming_edges):
                if not graph.edges[(incoming_edge_1[0], incoming_edge_1[1])]:
                    visited_incoming_edges = False
            if visited_incoming_edges:
                tasks_nodes.append(t_j)

            incoming_edges_start_node = list(graph.me_map_graph.in_edges(t_i))
            print(f'incoming_edges of t_i {incoming_edges_start_node}')
            while len(list(incoming_edges_start_node)) > 0:
                t_h = incoming_edges_start_node.pop()[0]
                l = min_edge(label, graph.edges[(t_h, t_i)].edge_type)

                if (t_h, t_j) not in graph.me_map_graph.edges:
                    graph.me_map_graph.add_edge(t_h, t_j)
                    graph.edges[t_h, t_j] = ed(from_node=t_h, to_node=t_j, edge_type=l)
                    graph.edges[t_h, t_j].all_types.append(label)
                    # print('edge', str((t_h, t_j)), 'added')
                else:
                    graph.edges[t_h, t_j].all_types.append(l)

                graph.edges[t_h, t_j].updateLabel()

    for node in list(graph.me_map_graph.nodes):
        if default:
            has_association = False

            if graph.nodes[node].node_label_type == 'M':
                continue

            for edge in graph.me_map_graph.in_edges(node):
                if graph.edges[(edge[0], edge[1])].edge_type == 'Association':
                    has_association = True
                    break
            for edge in graph.me_map_graph.out_edges(node):
                if graph.edges[(edge[0], edge[1])].edge_type == 'Association':
                    has_association = True
                    break
            if not has_association:
                if graph.nodes[node].node_label_type == 'R':
                    graph.me_map_graph.remove_node(node)
        else:
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
