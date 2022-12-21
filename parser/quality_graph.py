import networkx as nx
from parser.meMap_parser import me_map
from algorithms.inducedSubmodel import induced_subModel


class quality_map:

    def __init__(self, complete_graph: nx = None, task_graph: nx = None):
        """

        :param complete_graph:
        :param task_graph
        :return:
        """

        self.nodes = task_graph.nodes
        self.edges = task_graph.edges
        self.mandatory_nodes = task_graph.mandatory_nodes

        self.me_map_graph = nx.DiGraph()

        for node in complete_graph.me_map_graph.nodes:
            if complete_graph.nodes[node].node_type == 'Quality':
                self.me_map_graph.add_node(node)

        for edge in complete_graph.me_map_graph.edges:
            if complete_graph.nodes[edge[0]].node_type == 'Quality' and complete_graph.nodes[edge[1]].node_type\
                    == 'Quality':
                self.me_map_graph.add_edge(edge[0], edge[1])
            elif complete_graph.nodes[edge[0]].node_type == 'Task' and edge[0] in task_graph.me_map_graph.nodes and \
                    complete_graph.nodes[edge[1]].node_type == 'Quality':
                self.me_map_graph.add_edge(edge[0], edge[1])
            elif complete_graph.nodes[edge[1]].node_type == 'Task' and edge[1] in task_graph.me_map_graph.nodes and \
                    complete_graph.nodes[edge[0]].node_type == 'Quality':
                self.me_map_graph.add_edge(edge[0], edge[1])


def run():
    path = 'C:\\Users\\max_b\\PycharmProjects\\abstract_goal_models\\me-maps\\example.json'
    mandatory = ['t', 'q1', 'q2', 'q8', 't6', 't7', 't8', 't11']
    me_map_1 = me_map(path, mandatory=mandatory)
    induced_subModel(me_map_1)
    quality_graph = quality_map(me_map_1)
    print()


if __name__ == '__main__':
    run()