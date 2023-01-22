from unittest import TestCase
from abstractGM import abstractGMAlgorithm
from parser.meMap_parser import me_map
import networkx as nx


class Test(TestCase):

    def test_algorithm_1(self):
        path_input = '../me-maps/input/1_example.json'
        path_expected = '../me-maps/expected/1_expected.json'
        mandatory = ['t', 'q1', 'q2', 'q8', 't6', 't7', 't8', 't11']

        self.algorithm_output = abstractGMAlgorithm(path=path_input, mandatory=mandatory)
        self.expected_output = me_map(path_expected, mandatory=mandatory)

        differ = nx.difference(self.algorithm_output.me_map_graph, self.expected_output.me_map_graph)
        print(differ.nodes)
        print(differ.edges)
