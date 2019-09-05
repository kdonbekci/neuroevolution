from helpers import Distributions
from config import Configuration
import numpy as np

class Gene:

    inno_tracker = 0
    def __init__(self, generation, cause=None, copy=False):
        self.inno_num = Gene.inno_tracker
        if not copy:
            Gene.inno_tracker+=1
        self.origin = generation
        self.last_active = generation
        self.cause = cause

    def age(self, generation):
        return generation - self.origin

    def __lt__(self, other):
        return self.inno_num < other.inno_num

    def __eq__(self, other):
        return self.inno_num == other.inno_num

    def __repr__(self):
        return self.describe()

    def __hash__(self):
        return self.inno_num

    def describe(self):
        pass


class LayerGene(Gene):

    def __init__(self, generation, cause=None, copy=False):
        super().__init__(generation, cause, copy)
        self.type = Configuration.GENE_TYPES['layer']
        if not copy:
            self.expressed  = Configuration.DEFAULT_LAYER_EXPRESSED
            self.activation = Configuration.DEFAULT_ACTIVATION
            self.incoming = set() #these are for connections
            self.outgoing = set()
            self.units = 1

    # is_connected checks if other is in the outgoing of self.
    def is_connected(self, other):
        if self == other:
            return True
        for i in other.incoming:
            if i in self.outgoing:
                return True
        return False


    def copy(self, maintain_incoming_outgoing=False, **kwargs):
        clone = LayerGene(generation=self.origin, cause=self.cause, copy=True)
        clone.inno_num = self.inno_num
        clone.expressed = self.expressed
        clone.activation = self.activation
        clone.incoming = self.incoming.copy() if maintain_incoming_outgoing else set()
        clone.outgoing = self.outgoing.copy() if maintain_incoming_outgoing else set()
        clone.units = self.units
        return clone

    def describe(self):
        return '<LayerGene-origin:{},inno_num:{},incoming:{},outgoing:{},expressed:{},activation:\'{}\',cause:\'{}\'>'.format(self.origin,self.inno_num,
                                                                                    self.incoming, self.outgoing, self.expressed, self.activation, self.cause)
class ConnectionGene(Gene):

    def __init__(self, generation, source=None, target=None, weight=None, bias=None, cause=None, copy=False):
        super().__init__(generation, cause, copy)
        self.type = Configuration.GENE_TYPES['connection']
        if not copy:
            self.source = source
            self.target = target
            self.weight =  weight if weight else np.random.randn(source.units, target.units)
            self.bias = bias if bias else np.zeros(target.units)
            self.expressed = Configuration.DEFAULT_CONNECTION_EXPRESSED

    def copy(self, maintain_weights=False, **kwargs):
        clone = ConnectionGene(generation=self.origin, cause=self.cause, copy=True)
        clone.inno_num = self.inno_num
        clone.source = self.source
        clone.target = self.target
        clone.weight = self.weight if maintain_weights else np.random.randn(self.source.units, self.target.units)
        clone.expressed = self.expressed
        return clone

    def describe(self):
        return '<ConnectionGene-origin:{},inno_num:{},source:{},target:{},weight:{},expressed:{},cause:\'{}\'>'.format(self.origin, self.inno_num,
                                                                                                   self.source, self.target,
                                                                                                   self.weight, self.expressed,self.cause)

    # def __hash__(self):
    #     return super().__hash__()

class InputGene(Gene):

    def __init__(self, generation, units=None, cause=None, copy=False):
        super().__init__(generation, cause, copy)
        self.type = Configuration.GENE_TYPES['input']
        if not copy:
            self.units = units
            self.expressed = True
            self.outgoing = set()

    def copy(self, maintain_outgoing=False):
        clone = InputGene(generation=self.origin, cause=self.cause, copy=True)
        clone.units = self.units
        clone.expressed = self.expressed
        clone.outgoing = self.outgoing.copy() if maintain_outgoing else set()
        return clone

    def is_connected(self, other):
        if self == other:
            return True
        for i in other.incoming:
            if i in self.outgoing:
                return True
        return False

    def __repr__(self):
        return '<InputGene-outgoing:{},shape:{}>'.format(self.outgoing, self.units)

class OutputGene(Gene):

    def __init__(self, generation, units=None, activation=None, cause=None, copy=False):
        super().__init__(generation, cause, copy)
        self.type = Configuration.GENE_TYPES['output']
        if not copy:
            self.units = units
            self.activation = activation
            self.expressed = True
            self.incoming = set()

    def copy(self, maintain_incoming=False):
        clone = OutputGene(generation=self.origin, cause=self.cause, copy=True)
        clone.units = self.units
        clone.activation = self.activation
        clone.expressed = self.expressed
        clone.incoming = self.incoming.copy() if maintain_incoming else set()
        return clone

    def __repr__(self):
        return '<OutputGene-incoming:{},shape:{}>'.format(self.incoming, self.units)

class OptimizerGene(Gene):
    def __init__(self, generation, cause=None, copy=False):
        super().__init__(generation, cause, copy)
        self.type = Configuration.GENE_TYPES['optimizer']
        if not copy:
            self.name = Configuration.DEFAULT_OPTIMIZER
            self.params = Configuration.DEFAULT_OPTIMIZER_PARAMS[self.name]

class PseudoGene(Gene):
    def __init__(self, generation, cause=None, copy=False):
        super().__init__(generation, cause, copy)
        self.type = Configuration.GENE_TYPES['pseudo']

if __name__ == '__main__':
    def test_gene():
        generation = 1
        gene1 = Gene(generation=generation)
        gene2 = Gene(generation=generation)
        assert gene1 < gene2
        print('gene test successful')

    def test_layer_gene():
        generation = 1
        gene1 = LayerGene(generation=generation)
        gene2 = LayerGene(generation=generation)
        gene1_copy = gene1.copy(maintain_bias=True, maintain_incoming_outgoing=False)
        print(gene1)
        print('layer gene test successful')

    def test_connection_gene():
        print('connection gene test successful')


    def test_input_gene():
        print('input gene test successful')


    def test_output_gene():
        print('output gene test successful')


    # def gene_tests():
    #     generation = 1
    #     node_gene = NodeGene()
    #     node_gene.initialize(generation)
    #     assert node_gene.origin is generation
    #     generation += 1
    #     node_gene_2 = NodeGene()
    #     node_gene_2.initialize(generation)
    #     assert node_gene.inno_num + 1 is node_gene_2.inno_num
    #     node_gene_3 = NodeGene()
    #     node_gene_3.initialize(generation)
    #     node_gene_3_copy = node_gene_3.copy()
    #     assert node_gene_3_copy == node_gene_3
    #     generation += 1
    #     connection_gene = ConnectionGene()
    #     connection_gene.initialize(0, 2, generation)
    #     assert node_gene_3.inno_num + 1 is connection_gene.inno_num
    #     connection_gene_copy = connection_gene.copy()
    #     assert connection_gene == connection_gene_copy
    #     return True

    test_gene()
    test_layer_gene()

    print('all tests succesful')