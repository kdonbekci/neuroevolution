from helpers import Distributions
from gene import NodeGene, ConnectionGene, PseudoGene
from config import Configuration

class Genome:

    def __init__(self):
        pass

    def initialize(self, input_dim, output_dim, generation):
        self.origin = generation
        self.genes = {}
        self.nodes = []
        self.connections = []
        self.innovations = []
        for _ in range(input_dim):
            g_in = NodeGene()
            g_in.initialize(_type='input', generation=self.origin)
            self.add_gene(g_in)
        for _ in range(output_dim):
            g_out = NodeGene()
            g_out.initialize(_type='output', generation=self.origin)
            self.add_gene(g_out)

    def add_gene(self, gene):
#         assert gene.inno_num not in self.genes #temporary
        if gene.type is Configuration.GENE_TYPES['connection']:
            self.connections.append(gene.inno_num)
            self.genes[gene.source].outgoing.add(gene.inno_num)
            self.genes[gene.target].incoming.add(gene.inno_num)
        elif gene.type is Configuration.GENE_TYPES['node']:
            self.nodes.append(gene.inno_num)
        self.genes[gene.inno_num] = gene
        self.innovations.append(gene.inno_num)

    def remove_node(self, gene):
        for i in gene.incoming:
            self.remove_connection(self.genes[i])
        for i in gene.outgoing:
            self.remove_connection(self.genes[i])
        self.nodes.remove(gene.inno_num)
        del self.genes[gene.inno_num]

    def remove_connection(self, gene):
        self.connections.remove(gene.inno_num)
        del self.genes[gene.inno_num]

    def prune(self, generation): #after some time, start getting rid of long disabled genes
        for i in self.genes:
            gene = self.genes[i]
            if not gene.expressed and generation - gene.last_active > Configuration.PRUNE_THRESHOLD[gene.type]:
                if gene.type is Configuration.GENE_TYPES['node']:
                    self.remove_node(gene)
                elif gene.type is Configuration.GENE_TYPES['connection']:
                    self.remove_connection(gene)

    def mutate(self, generation, mutations):
        mutations.act(self, generation)

    #returns a child genome after the crossover operation is complete
    @staticmethod
    def crossover(more_fit_parent, less_fit_parent, generation):
        child = Genome()
        child.origin = generation
        child.innovations = []
        child.genes = {}
        child.nodes = []
        child.connections = []
        for inno_num in more_fit_parent.innovations:
            if less_fit_parent.genes.get(inno_num) is not None:
                gene = more_fit_parent.genes[inno_num] if Distributions.coin_toss() else less_fit_parent.genes[inno_num]
            else:
                gene = more_fit_parent.genes[inno_num]
            child.add_gene(gene.copy())
        return child

    @property
    def size(self):
        return len(self.genes)

    def copy(self, maintain_bias=False, maintain_weights=False, maintain_incoming_outgoing=True):
        clone = Genome()
        clone.origin = self.origin
        clone.innovations = self.innovations.copy()
        clone.connections = self.connections.copy()
        clone.nodes = self.nodes.copy()
        clone.genes = {}
        for i in self.nodes:
            clone.genes[i] = self.genes[i].copy(maintain_bias=maintain_bias, maintain_incoming_outgoing=maintain_incoming_outgoing)
        for i in self.connections:
            clone.genes[i] = self.genes[i].copy(maintain_weights=maintain_weights)
        return clone

    def plot(self):
        pass

    def __eq__(self, other):
        return self.genes == other.genes and self.origin is other.origin and self.innovations == other.innovations

    def __repr__(self):
        return '<Genome-origin:{},size:{}>'.format(self.origin, self.size)

def genome_tests():
    from mutation import Mutations
    import timeit
    mutations = Mutations()
    genome1 = Genome()
    generation = 1
    genome1.initialize(3, 2, generation)
    generation+=1
    genome2 = genome1.copy(maintain_bias=True)
    assert genome2 == genome1
    while generation < 100:
        generation+=1
        genome1.mutate(generation, mutations)
        genome2.mutate(generation, mutations)
        child = Genome.crossover(genome1, genome2, generation)
        assert child.copy() == child
        mutations.reset()
    genome3 = Genome.crossover(genome2, genome1, generation)
    genome1
    genome2
    assert not genome3 == genome2, 'child is equal to parent'
    genome4 = Genome.crossover(genome3, genome3, generation)
    assert genome4 == genome3, 'child of genome crossed with itself is not equal to the genome'
    while generation < 200:
        generation+=1
        genome1.mutate(generation, mutations)
        genome2.mutate(generation, mutations)
        genome3.mutate(generation, mutations)
        mutations.reset()
    genome4 = Genome.crossover(Genome.crossover(genome3, genome2, generation), genome1, generation)
    genome4
    for gene in genome4:
        pass


if __name__ == '__main__':
    assert genome_tests()
