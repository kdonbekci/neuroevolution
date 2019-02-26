from config import Configuration
from helpers import Distributions, Activations
from gene import NodeGene, ConnectionGene, PseudoGene

class Mutations:

    def __init__(self):
        self.node_mutations = [AddConnectionMutation(), ChangeNodeMutation()]
        self.connection_mutations = [AddNodeMutation(), ToggleConnectionMutation()]

    # a gene can be target of only 1 mutation
    def act(self, genome, generation):
        for i in reversed(genome.nodes): #reversed as later additions are likelier to mutate
            # node_gene = genome.nodes[i]
            Distributions.shuffle(self.node_mutations)
            for mutation in self.node_mutations:
                if mutation.attempt(i):
                    break
        for i in reversed(genome.connections):
            # connection_gene = genome.connections[i]
            Distributions.shuffle(self.connection_mutations)
            for mutation in self.connection_mutations:
                if mutation.attempt(i):
                    break
        for mutation in self.node_mutations:
            mutation.act(genome, generation)
            mutation.clear()
        for mutation in self.connection_mutations:
            mutation.act(genome, generation)
            mutation.clear()

    def __repr__(self):
        return '<Mutations-mutations:{}>'.format(self.mutations)

class Mutation:

    def __init__(self):
        self.genes = []
        self.max_attempts = Configuration.MUTATION_MAX_ATTEMPTS

    def clear(self):
        self.genes = []

    def attempt(self, gene_inno_num):
        if len(self.genes) > self.limit:
            return False
        if Distributions.probability(self.p):
            self.genes.append(gene_inno_num)
            return True

    def __repr__(self):
        return self.describe()

class AddConnectionMutation(Mutation): #adds a connection between two already existing, unconnected nodes

    def __init__(self):
        super().__init__()
        self.scope = Configuration.GENE_TYPES['node']
        self.p = Configuration.MUTATION_P['add_connection']
        self.limit = Configuration.MUTATION_LIMIT['add_connection']

    def act(self, genome, generation):
        attempt = 0
        acted = False
        for i in self.genes:
            if acted or attempt > self.max_attempts:
                break
            target = genome.genes[i]
            if target.sub_type is 'input':
                continue
            acted = False
            while not acted and attempt < self.max_attempts:
                j = Distributions.choice(genome.nodes)
                source = genome.genes[j]
                if not source.expressed:
                    attempt+=1
                    continue
                if target.is_connected(source):
                    attempt+=1
                    continue
                new_gene = ConnectionGene()
                new_gene.initialize(source.inno_num, target.inno_num, generation)
                genome.add_gene(new_gene)
                acted = True

    def describe(self):
        return '<AddConnectionMutation>'

class AddNodeMutation(Mutation): #adds a node between an already existing connection

    def __init__(self):
        super().__init__()
        self.scope = Configuration.GENE_TYPES['connection']
        self.p = Configuration.MUTATION_P['add_node']
        self.limit = Configuration.MUTATION_LIMIT['add_node']

    def act(self, genome, generation):
        for i in self.genes:
            old_connection = genome.genes[i]
            old_connection.expressed = False
            old_connection.last_active = generation-1
            new_node = NodeGene()
            new_node.initialize('hidden', 'generation')
            new_node.incoming.add(old_connection.source)
            new_node.outgoing.add(old_connection.target)
            genome.add_gene(new_node)
            first_connection = ConnectionGene()
            first_connection.initialize(old_connection.source, new_node.inno_num, generation, weight=1.0)
            second_connection = ConnectionGene()
            second_connection.initialize(new_node.inno_num, old_connection.target, generation, weight=old_connection.weight)
            genome.add_gene(first_connection)
            genome.add_gene(second_connection)

    def describe(self):
        return '<AddNodeMutation>'

class ChangeNodeMutation(Mutation): #changes the node attribute (activation function, aggregation function)

    def __init__(self):
        super().__init__()
        self.scope = Configuration.GENE_TYPES['node']
        self.p = Configuration.MUTATION_P['change_node']
        self.limit = Configuration.MUTATION_LIMIT['change_node']

    def act(self, genome, generation): # REVIEW: Should this set node.expressed to false and create new connections and a node gene?
        for i in self.genes:
            node = genome.genes[i]
            node.activation = Activations.get_random_func()

    def describe(self):
        return '<ChangeNodeMutation>'

class ToggleNodeMutation(Mutation):
    def __init__(self):
        super().__init__()
        self.scope = Configuration.GENE_TYPES['node']
        self.p = Configuration.MUTATION_P['toggle_node']
        self.limit = Configuration.MUTATION_LIMIT['toggle_node']

    def act(self, genome, generation):
        for i in self.genes:
            node = genome.genes[i]
            node.expressed = not node.expressed
            if not node.expressed: #need to disable all the connections that touch node
                for j in node.incoming:
                    genome.genes[j].expressed = False
                for j in node.outgoing:
                    genome.genes[j].expressed = False

    def describe(self):
        return '<DisableNodeMutation>'

class ToggleConnectionMutation(Mutation):

    def __init__(self):
        super().__init__()
        self.scope = Configuration.GENE_TYPES['connection']
        self.p = Configuration.MUTATION_P['toggle_connection']
        self.limit = Configuration.MUTATION_LIMIT['toggle_connection']


    def act(self, genome, generation):
        for i in self.genes:
            connection = genome.genes[i]
            connection.expressed = not connection.expressed

    def describe(self):
        return '<ToggleConnectionMutation>'

if __name__ == '__main__':
    print('hi')
    m = Mutations()
    Distributions.shuffle(m.mutations)
    m.mutations
    if (False, True):
        print('c')
    Distributions.choice(tuple(a))
    a = False
    a = 'abc'
    b = 'abc'
    a is b
    a = set([2, 1, 3])
    for i in a:
        print (i)
