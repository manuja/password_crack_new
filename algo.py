class Algo:

    def __init__(self, current_node_name, current_node_id, current_port_number, current_election=False, current_coordinator=False):
        self.node_name = current_node_name
        self.node_id = current_node_id
        self.port = current_port_number
        self.election = current_election
        self.coordinator = current_coordinator