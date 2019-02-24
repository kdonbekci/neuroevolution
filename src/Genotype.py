from helpers import Distributions
from Gene import NodeGene, ConnectionGene, PseudoGene

class Genotype:

    def __init__(self, input_dim=None, output_dim=None, generation=None, copy=False, genotype=None):
        self.mutable_genes = {} #innovation number --> gene lookup
        self.fixed_genes = {}
        if not copy:
            self.innovations = []
            self.origin = generation
            for _ in range(input_dim):
                g_in = Genotype.NodeGene(_type='input', generation=self.origin)
                self.add_gene(g_in, fixed=True)
            for _ in range(output_dim):
                g_out = Genotype.NodeGene(_type='output', generation=self.origin,)
                self.add_gene(g_out, fixed=True)
        else:
            self.origin = genotype.origin
            for i in genotype.mutable_genes:
                self.mutable_genes[i] = genotype.mutable_genes[i].copy()
            for i in genotype.fixed_genes:
                self.fixed_genes[i] = genotype.fixed_genes[i].copy()
            self.innovations = genotype.innovations.copy()

    def add_gene(self, gene, fixed=False):
#         assert gene.inno_num not in self.genes #temporary
        if fixed:
            self.fixed_genes[gene.inno_num] = gene
        else:
            self.mutable_genes[gene.inno_num] = gene
            self.innovations.append(gene.inno_num)


    #returns a child genotype after the crossover operation is complete
    @staticmethod
    def crossover(more_fit_parent, less_fit_parent, generation):
        child = Genotype(0, 0, generation) #in order to create empty genotype
        for inno_num in more_fit_parent.innovations:
            if less_fit_parent.mutable_genes.get(inno_num) is not None:
                gene = more_fit_parent.mutable_genes[inno_num] if Distributions.coin_toss() else less_fit_parent.mutable_genes[inno_num]
            else:
                gene = more_fit_parent.mutable_genes[inno_num]
            child.add_gene(gene.copy())
        for inno_num in more_fit_parent.fixed_genes:
            gene = more_fit_parent.fixed_genes[inno_num] if Distributions.coin_toss() else less_fit_parent.fixed_genes[inno_num]
            child.add_gene(gene.copy(), fixed=True)
        return child


    def copy(self):
        clone = Genotype(copy=True, genotype=self)
        return clone

    def __repr__(self):
        return '<Genotype-origin:{},mutable_genes:{}>'.format(self.origin, self.mutable_genes)
