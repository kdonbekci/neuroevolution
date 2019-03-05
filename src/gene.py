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

    def __hash__(self):
        return self.inno_num

class NodeGene(Gene):

    def __init__(self):
        self.type = Configuration.GENE_TYPES['hidden']

    def initialize(self, generation, bias=None, cause=None):
        super().__init__(generation, cause)
        self.bias = Configuration.DEFAULT_NODE_BIAS if bias is None else bias
        self.expressed  = Configuration.DEFAULT_NODE_EXPRESSED
        self.activation = Configuration.DEFAULT_NODE_ACTIVATION
        self.incoming = set() #these are connections
        self.outgoing = set()

    # @staticmethod
    # def isValidType(_type):
    #     return _type in ['hidden', 'input', 'output']

    def is_reachable(self, other): # TODO:
        pass

    def is_connected(self, other):
        if self == other:
            return True
        try:
            for i in self.incoming:
                if i in other.outgoing:
                    return True
        except Exception as e:
            pass
        try:
            for i in other.incoming:
                if i in self.outgoing:
                    return True
        except Exception as e:
            pass
        return False


    def copy(self, maintain_bias=False, maintain_incoming_outgoing=False, **kwargs):
        clone = NodeGene()
        clone.expressed = self.expressed
        clone.activation = self.activation
        clone.incoming = self.incoming.copy() if maintain_incoming_outgoing else set()
        clone.outgoing = self.outgoing.copy() if maintain_incoming_outgoing else set()
        clone.origin = self.origin
        clone.inno_num = self.inno_num
        clone.bias = self.bias if maintain_bias else Configuration.DEFAULT_NODE_BIAS
        clone.cause = self.cause
        return clone

    def describe(self):
        return '<NodeGene-origin:{},inno_num:{},incoming:{},outgoing:{},bias:{},expressed:{},activation:\'{}\',cause:\'{}\'>'.format(self.origin,self.inno_num,
                                                                                    self.incoming, self.outgoing, self.bias, self.expressed, self.activation, self.cause)

    def __eq__(self, other):
        return self.inno_num is other.inno_num and self.expressed is other.expressed and self.incoming == other.incoming and self.outgoing == other.outgoing and self.origin is other.origin

    def __hash__(self):
        return super().__hash__()

class ConnectionGene(Gene):

    def __init__(self):
        self.type = Configuration.GENE_TYPES['connection']

    def initialize(self, source, target, generation, weight=None, cause=None):
        super().__init__(generation, cause)
        self.source = source
        self.target = target
        self.weight = Distributions.sample_normal() if weight is None else weight
        self.expressed = True

    def copy(self, maintain_weights=False, **kwargs):
        clone = ConnectionGene()
        clone.inno_num = self.inno_num
        clone.origin = self.origin
        clone.source = self.source
        clone.target = self.target
        clone.weight = self.weight if maintain_weights else Distributions.sample_normal()
        clone.expressed = self.expressed
        clone.cause = self.cause
        return clone

    def describe(self):
        return '<ConnectionGene-origin:{},inno_num:{},source:{},target:{},weight:{},expressed:{},cause:\'{}\'>'.format(self.origin, self.inno_num,
                                                                                                   self.source, self.target,
                                                                                                   self.weight, self.expressed,self.cause)

    def __eq__(self, other):
        return self.inno_num is other.inno_num and self.expressed is other.expressed and self.source is other.source and self.target is other.target and self.origin is other.origin

    def __hash__(self):
        return super().__hash__()

class InputGene(Gene):

    def __init__(self):
        self.type = Configuration.GENE_TYPES['input']

    def initialize(self, shape, generation):
        super().__init__(generation)
        self.shape = shape
        self.expressed = True
        self.outgoing = set()

    def copy(self, maintain_incoming_outgoing=False):
        clone = InputGene()
        clone.shape = self.shape
        clone.outgoing = self.outgoing.copy() if maintain_incoming_outgoing else set()
        return clone

    def is_connected(self, other):
        if self == other:
            return True
        for i in self.outgoing:
            if i in other.incoming:
                return True
        return False

    def __repr__(self):
        return '<InputGene-outgoing:{},shape:{}>'.format(self.outgoing, self.shape)

class OutputGene(Gene):

    def __init__(self):
        self.type = Configuration.GENE_TYPES['output']

    def initialize(self, shape, generation):
        super().__init__(generation)
        self.shape = shape
        self.expressed = True
        self.incoming = set()

    def copy(self, maintain_incoming_outgoing=False):
        clone = OutputGene()
        clone.shape = self.shape
        clone.incoming = self.incoming.copy() if maintain_incoming_outgoing else set()
        return clone

    def is_connected(self, other):
        if self == other:
            return True
        for i in self.incoming:
            if i in other.outgoing:
                return True
        return False

    def __repr__(self):
        return '<OutputGene-incoming:{},shape:{}>'.format(self.incoming, self.shape)

class PseudoGene(Gene):

    def __init__(self, inno_num=None):
        super().__init__(inno_num)
        self.type = Configuration.GENE_TYPES['pseudo']


def gene_tests():
    generation = 1
    node_gene = NodeGene()
    node_gene.initialize(generation)
    assert node_gene.origin is generation
    generation+=1
    node_gene_2 = NodeGene()
    node_gene_2.initialize(generation)
    assert node_gene.inno_num +1 is node_gene_2.inno_num
    node_gene_3 = NodeGene()
    node_gene_3.initialize(generation)
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
