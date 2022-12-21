import networkx as nx
from parser.meMap_parser import me_map


def induced_subModel(graph=None):
    """

    :param graph:
    :return:
    """
    nodes_id_to_remove = []

    restore_edges = []
    for edge in list(graph.me_map_graph.edges):
        if graph.edges[edge].edge_type == 'Association' or graph.edges[edge].edge_type == 'Contribution':
            restore_edges.append(edge)
            graph.me_map_graph.remove_edge(edge[0], edge[1])

    for key in graph.me_map_graph.nodes:
        if graph.nodes[key].node_label_type == 'M':
            continue
        to_remove = True

        for mandatory_node in graph.mandatory_nodes:
            if mandatory_node.node_type != 'Task':
                continue

            if nx.has_path(graph.me_map_graph, graph.nodes[key].node_id, mandatory_node.node_id):
                to_remove = False
                break

        if to_remove:
            nodes_id_to_remove.append(graph.nodes[key].node_id)

    for edge in list(restore_edges):
        graph.me_map_graph.add_edge(edge[0], edge[1])

    for remove in nodes_id_to_remove:
        if graph.nodes[remove].node_type == 'Quality':
            incoming_edges = graph.me_map_graph.in_edges(remove)
            if len(incoming_edges) == 0:
                graph.me_map_graph.remove_node(remove)
        else:
            graph.me_map_graph.remove_node(remove)



def run():
    path = 'C:\\Users\\max_b\\PycharmProjects\\abstract_goal_models\\me-maps\\example.json'
    mandatory = ['t', 'q1', 'q2', 'q8', 't6', 't7', 't8', 't11']
    me_map_1 = me_map(path, mandatory=mandatory)
    induced_subModel(me_map_1)
    print()


if __name__ == '__main__':
    run()
