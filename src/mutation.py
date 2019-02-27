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
        return '<Mutations-node_mutations:{},connection_mutations:{}>'.format(self.node_mutations, self.connection_mutations)

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
            if attempt > self.max_attempts:
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
                new_gene.initialize(source.inno_num, target.inno_num, generation, cause='AddConnectionMutation on gene-{}'.format(i))
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
            new_node.initialize('hidden', generation, cause='AddNodeMutation on gene-{}'.format(i))

            first_connection = ConnectionGene()
            first_connection.initialize(old_connection.source, new_node.inno_num, generation, weight=1.0, cause='AddNodeMutation on gene-{}'.format(i))
            second_connection = ConnectionGene()
            second_connection.initialize(new_node.inno_num, old_connection.target, generation, weight=old_connection.weight, cause='AddNodeMutation on gene-{}'.format(i))
            new_node.incoming.add(first_connection.inno_num)
            new_node.outgoing.add(second_connection.inno_num)
            genome.add_gene(new_node)
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
            else:
                node.last_active = generation

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
            if connection.expressed:
                connection.last_active = generation

    def describe(self):
        return '<ToggleConnectionMutation>'

def mutation_tests():
    from genome import Genome
    genome = Genome()
    generation = 1
    genome.initialize(3, 2, generation)
    while generation < 1000:
        generation+=1
        genome.mutate(generation)
    found_connections = set()
    inno_nums = set()
    for i in genome.genes:
        gene = genome.genes[i]
        assert gene.inno_num not in inno_nums
        inno_nums.add(gene.inno_num)
        if gene.type is Configuration.GENE_TYPES['node']:
            for j in gene.incoming:
                assert j in genome.genes, 'Incoming connection-{} of node-{} is not in genome'.format(j, gene.inno_num)
                assert genome.genes[j].type is Configuration.GENE_TYPES['connection'], 'Incoming connection-{} of node-{} is not a connection'.format(j, gene.inno_num)
                assert genome.genes[j].target is gene.inno_num, 'Target of incoming connection-{} is not the gene-{}'.format(j, gene.inno_num)
                if not gene.expressed:
                    assert not genome.genes[j].expressed, 'Incoming connection-{} of unexpressed node-{} is expressed'.format(j, gene.inno_num)
            for j in gene.outgoing:
                assert j in genome.genes, 'Outgoing connection-{} of node-{} is not in genome'.format(j, gene.inno_num)
                assert genome.genes[j].source is gene.inno_num, 'Source of outgoing connection-{} is not the gene-{}'.format(j, gene.inno_num)
                if not gene.expressed:
                    assert not genome.genes[j].expressed, 'Outgoing connection-{} of unexpressed node-{} is expressed'.format(j, gene.inno_num)
        elif gene.type is Configuration.GENE_TYPES['connection']:
            assert (gene.source, gene.target) not in found_connections and (gene.target, gene.source) not in found_connections, 'Connection-{} is duplicate wrt to Nodes-{},{}'.format(gene.inno_num, gene.target, gene.source)
            found_connections.add((gene.source, gene.target))
            assert gene.source in genome.genes, 'Source-{} of connection-{} not in genome'.format(gene.source, gene.inno_num)
            assert gene.target in genome.genes, 'Target-{} of connection-{} not in genome'.format(gene.target, gene.inno_num)
        else:
            assert False, 'Invalid gene type encountered: {}'.format(gene.type)
    print('All tests for mutation.py completed successfully.')
    return True
if __name__ == '__main__':
    assert mutation_tests()
