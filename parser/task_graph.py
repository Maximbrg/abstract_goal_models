import networkx as nx
from parser.meMap_parser import me_map
from algorithms.inducedSubmodel import induced_subModel


class tasks_map:

    def __init__(self, graph: nx = None):
        """

        :param graph:
        :return:
        """

        self.nodes = graph.nodes
        self.edges = graph.edges
        self.mandatory_nodes = graph.mandatory_nodes

        self.me_map_graph = nx.DiGraph()

        for node in graph.me_map_graph.nodes:
            if graph.nodes[node].node_type == 'Task':
                self.me_map_graph.add_node(node)

        for edge in graph.me_map_graph.edges:
            if graph.edges[edge].edge_type == 'AchievedBy' or graph.edges[edge].edge_type == 'ConsistsOf':
                self.me_map_graph.add_edge(edge[0], edge[1])


def run():
    path = 'C:\\Users\\max_b\\PycharmProjects\\abstract_goal_models\\me-maps\\example.json'
    mandatory = ['t', 'q1', 'q2', 'q8', 't6', 't7', 't8', 't11']
    me_map_1 = me_map(path, mandatory=mandatory)
    induced_subModel(me_map_1)
    task_graph = tasks_map(me_map_1)
    print()


if __name__ == '__main__':
    run()
