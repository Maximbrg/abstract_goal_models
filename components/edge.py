class edge:

    def __init__(self, from_node: int = None, to_node: int = None, edge_type: str = None):
        """

        :param from_node:
        :param to_node:
        :param edge_type:
        """

        self.from_node = from_node
        self.to_node = to_node
        self.edge_type = edge_type
        if self.edge_type is None:
            self.all_types = []
        else:
            self.all_types = [self.edge_type]
        self.is_visited = False

    def updateLabel(self):
        """

        :return:
        """

        score = 0
        for edge_type in self.all_types:
            if edge_type == '++':
                score += 90
            if edge_type == '+':
                score += 70
            if edge_type == '-':
                score += 50
            if edge_type == '--':
                score += 20

        tot = score / len(self.all_types)

        if tot > 90:
            self.edge_type = '++'
        elif tot > 60:
            self.edge_type = '+'
        elif tot > 40:
            self.edge_type = '-'
        else:
            self.edge_type = '--'
