class node:

    def __init__(self, node_id: int = None, label: str = None, node_type: str = None, node_label_type: str = 'R'):
        """

        :param node_id:
        :param label:
        :param type:
        """

        self.node_id = node_id
        self.label = label
        self.node_type = node_type
        self.node_label_type = node_label_type
        self.is_visited = False
