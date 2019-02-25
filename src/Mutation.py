class Mutation:

    def __init__(self):
        pass

class AddConnectionMutation(Mutation): #adds a connection between two already existing nodes
    pass

class AddNodeMutation(Mutation): #adds a node between an already existing connection
    pass

class ChangeNodeMutation(Mutation): #changes the node attribute (activation function, aggregation function)
    pass

class ChangeConnectionMutation(Mutation):
    pass

class ResetWeightMutation(Mutation): #resets the weight of a connection
    pass

class DisableConnectionMutation(Mutation):
    pass
