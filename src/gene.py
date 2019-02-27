from helpers import Distributions
from config import Configuration

class Gene:

    inno_tracker = 0
    def __init__(self, generation, cause=None):
        self.inno_num = Gene.inno_tracker
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

class NodeGene(Gene):

    def __init__(self):
        self.type = Configuration.GENE_TYPES['node']

    def initialize(self, _type, generation, bias=None, cause=None):
        super().__init__(generation, cause)
        assert NodeGene.isValidType(_type), 'Invalid type (\'{}\') for NodeGene'.format(_type) #temporary
        self.sub_type = _type
        self.bias = Configuration.DEFAULT_NODE_BIAS if bias is None else bias
        self.expressed  = Configuration.DEFAULT_NODE_EXPRESSED
        self.activation = Configuration.DEFAULT_NODE_ACTIVATION
        self.incoming = set() #these are connections
        self.outgoing = set()

    @staticmethod
    def isValidType(_type):
        return _type in ['hidden', 'input', 'output']


    def is_reachable(self, other): # TODO:
        pass

    def is_connected(self, other):
        if self == other: # REVIEW: recurrency?
            return True
        for i in self.incoming:
            if i in other.outgoing:
                return True
        for i in other.incoming:
            if i in self.outgoing:
                return True
        return False


    def copy(self, maintain_bias=False, maintain_incoming_outgoing=False):
        clone = NodeGene()
        clone.sub_type = self.sub_type
        clone.expressed = self.expressed
        clone.activation = self.activation
        clone.incoming = self.incoming.copy() if maintain_incoming_outgoing else set()
        clone.outgoing = self.outgoing.copy() if maintain_incoming_outgoing else set()
        clone.origin = self.origin
        clone.inno_num = self.inno_num
        clone.bias = self.bias if maintain_bias else Configuration.DEFAULT_NODE_BIAS
        return clone

    def describe(self):
        return '<NodeGene-origin:{},inno_num:{},sub_type:\'{}\',incoming:{},outgoing:{},bias:{},activation:\'{}\',cause:\'{}\'>'.format(self.origin,self.inno_num,
                                                                                    self.sub_type, self.incoming, self.outgoing, self.bias, self.activation, self.cause)

    def __eq__(self, other):
        return self.inno_num is other.inno_num and self.expressed is other.expressed and self.incoming == other.incoming and self.outgoing == other.outgoing and self.origin is other.origin

class ConnectionGene(Gene):

    def __init__(self):
        self.type = Configuration.GENE_TYPES['connection']

    def initialize(self, source, target, generation, weight=None, cause=None):
        super().__init__(generation, cause)
        self.source = source
        self.target = target
        self.weight = Distributions.sample_normal() if weight is None else weight
        self.expressed = True

    def copy(self, maintain_weights=False):
        clone = ConnectionGene()
        clone.inno_num = self.inno_num
        clone.origin = self.origin
        clone.source = self.source
        clone.target = self.target
        clone.weight = self.weight if maintain_weights else Distributions.sample_normal()
        clone.expressed = self.expressed
        return clone

    def describe(self):
        return '<ConnectionGene-origin:{},inno_num:{},source:{},target:{},weight:{},expressed:{},cause:\'{}\'>'.format(self.origin, self.inno_num,
                                                                                                   self.source, self.target,
                                                                                                   self.weight, self.expressed,self.cause)

    def __eq__(self, other):
        return self.inno_num is other.inno_num and self.expressed is other.expressed and self.source is other.source and self.target is other.target and self.origin is other.origin


class PseudoGene(Gene):

    def __init__(self, inno_num=None):
        super().__init__(inno_num)
        self.type = Configuration.GENE_TYPES['pseudo']

def gene_tests():
    generation = 1
    node_gene = NodeGene()
    node_gene.initialize('input', generation)
    assert node_gene.origin is generation and node_gene.sub_type is 'input'
    generation+=1
    node_gene_2 = NodeGene()
    node_gene_2.initialize('input', generation)
    assert node_gene.inno_num +1 is node_gene_2.inno_num
    node_gene_3 = NodeGene()
    node_gene_3.initialize('output', generation)
    node_gene_3_copy = node_gene_3.copy()
    assert node_gene_3_copy == node_gene_3
    generation+=1
    connection_gene = ConnectionGene()
    connection_gene.initialize(0, 2, generation)
    assert node_gene_3.inno_num +1 is connection_gene.inno_num
    connection_gene_copy = connection_gene.copy()
    assert connection_gene == connection_gene_copy
    return True

if __name__ == '__main__':
    assert gene_tests()
