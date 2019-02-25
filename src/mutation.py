from config import Configuration
from helpers import Distributions
from gene import NodeGene, ConnectionGene, PseudoGene

class Mutations:

    def __init__(self):
        self.node_mutations = [AddConnectionMutation(), ChangeNodeMutation()]
        self.connection_mutations = [AddNodeMutation(), DisableConnectionMutation()]

    def act(self, genome, generation):
        for i in genome.nodes:
            node_gene = genome.nodes[i]
            Distributions.shuffle(self.node_mutations)
            for mutation in self.node_mutations:
                if mutation.attempt(node_gene):
                    break
        for i in genome.connections:
            connection_gene = genome.connections[i]
            Distributions.shuffle(self.connection_mutations)
            for mutation in self.connection_mutations:
                if mutation.attempt(connection_gene):
                    break
        for mutation in self.node_mutations:
            mutation.act(genome)
            mutation.clear()
        for mutation in self.connection_mutations:
            mutation.act(genome)
            mutation.clear()

    def __repr__(self):
        return '<Mutations-mutations:{}>'.format(self.mutations)

class Mutation:

    def __init__(self):
        self.gene = None
        self.p = Configuration.MUTATION_P

    def clear(self):
        self.gene = None

    def attempt(self, gene):
        if self.gene is not None:
            return False
        if Distributions.probability(self.p):
            self.gene = gene
            return True

    def __repr__(self):
        return self.describe()

class AddConnectionMutation(Mutation): #adds a connection between two already existing, unconnected nodes

    def __init__(self):
        super().__init__()
        self.scope = Configuration.GENE_TYPES['node']
        self.max_attempts = 10

    def act(self, genome):
        attempt = 0
        acted = False
        while not acted and attemt < self.max_attempts:
            attempts+=1
            source = Distributions.choice(genome.nodes)
            if self.gene.inno_num in source.incoming or 



        pass

    def describe(self):
        return '<AddConnectionMutation-scope:\'{}\'>'.format(Configuration.INV_GENE_TYPES[self.scope])

class AddNodeMutation(Mutation): #adds a node between an already existing connection

    def __init__(self):
        super().__init__()
        self.scope = Configuration.GENE_TYPES['connection']

    def act(self, genome):
        pass

    def describe(self):
        return '<AddNodeMutation-scope:\'{}\'>'.format(Configuration.INV_GENE_TYPES[self.scope])

class ChangeNodeMutation(Mutation): #changes the node attribute (activation function, aggregation function)

    def __init__(self):
        super().__init__()
        self.scope = Configuration.GENE_TYPES['node']

    def act(self, genome):
        pass

    def describe(self):
        return '<ChangeNodeMutation-scope:\'{}\'>'.format(Configuration.INV_GENE_TYPES[self.scope])

class DisableConnectionMutation(Mutation):

    def __init__(self):
        super().__init__()
        self.scope = Configuration.GENE_TYPES['connection']

    def act(self, genome):
        pass

    def describe(self):
        return '<DisableConnectionMutation-scope:\'{}\'>'.format(Configuration.INV_GENE_TYPES[self.scope])

if __name__ == '__main__':
    print('hi')
    m = Mutations()
    Distributions.shuffle(m.mutations)
    m.mutations


# class SwapPseudoGeneMutation(Mutation):
#
#     def __init__(self):
#         self.scope = Configuration.GENE_TYPES['pseudo']
#
#     def act(self, gene):
#         pass
#
#     def describe(self):
#         return '<SwapPseudoGeneMutation-scope:\'{}\'>'.format(Configuration.INV_GENE_TYPES[self.scope])

# class ResetWeightMutation(Mutation): #resets the weight of a connection
#
#     def __init__(self):
#         pass
#
#     def describe(self):
#         return '<ResetWeightMutation-scope:\'{}\'>'.format(Configuration.INV_GENE_TYPES[self.scope])
