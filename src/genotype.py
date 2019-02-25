from helpers import Distributions
from gene import NodeGene, ConnectionGene, PseudoGene
from mutation import Mutations
from config import Configuration

class Genotype:

    mutations = Mutations()

    def __init__(self):
        # self.mutable_genes = {} #innovation number --> gene lookup
        # self.fixed_genes = {}
        self.genes = None
        self.nodes = None
        self.connections = None
        self.innovations = None

    def initialize(self, input_dim, output_dim, generation):
        self.origin = generation
        self.genes = {}
        self.nodes = []
        self.connections = []
        self.innovations = []
        for _ in range(input_dim):
            g_in = NodeGene(_type='input', generation=self.origin)
            self.add_gene(g_in)
        for _ in range(output_dim):
            g_out = NodeGene(_type='output', generation=self.origin,)
            self.add_gene(g_out)

    def add_gene(self, gene):
#         assert gene.inno_num not in self.genes #temporary
        if gene.type is Configuration.GENE_TYPES['connection']:
            self.connections.add(gene.inno_num)
            self.genes[gene.inNode].incoming.add(gene.outNode)
            self.genes[gene.outNode].outgoing.add(gene.inNode)
        elif gene.type is Configuration.GENE_TYPES['node']:
            self.nodes.add(gene.inno_num)
        self.genes[gene.inno_num] = gene
        self.innovations.append(gene.inno_num)

    def mutate(self, generation):
        Genotype.mutations.act(self, generation)

    #returns a child genotype after the crossover operation is complete
    @staticmethod
    def crossover(more_fit_parent, less_fit_parent, generation):
        child = Genotype() #in order to create empty genotype
        child.origin = generation
        for inno_num in more_fit_parent.innovations:
            if less_fit_parent.genes.get(inno_num) is not None:
                gene = more_fit_parent.genes[inno_num] if Distributions.coin_toss() else less_fit_parent.genes[inno_num]
            else:
                gene = more_fit_parent.genes[inno_num]
            child.add_gene(gene.copy())
        return child


    def copy(self):
        clone = Genotype()
        clone.origin = self.origin
        clone.innovations = self.innovations.copy()
        clone.connections = self.connections.copy()
        clone.nodes = self.nodes.copy()
        clone.genes = {}
        for i in self.nodes:
            clone.genes[i] = self.genes[i].copy()
        for i in self.connections:
            clone.genes[i] = self.genes[i].copy()
        return clone

    def __repr__(self):
        return '<Genotype-origin:{},mutable_genes:{}>'.format(self.origin, self.mutable_genes)

if __name__ == '__main__':
    g = Genotype(2, 1, 1)
    g.mutate(2)
    g.add_gene(NodeGene('hidden', 2))
    g.mutable_genes
