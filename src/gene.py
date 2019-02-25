from helpers import Distributions
from config import Configuration

class Gene:

    inno_tracker = 0
    def __init__(self, generation):
        self.inno_num = Gene.inno_tracker
        Gene.inno_tracker+=1
        self.origin = generation

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

    def initialize(self, _type, generation):
        super().__init__(generation)
        assert NodeGene.isValidType(_type), 'Invalid type (\'{}\') for NodeGene'.format(_type) #temporary
        self.sub_type = _type
        self.bias = Configuration.DEFAULT_NODE_BIAS
        self.expressed  = Configuration.DEFAULT_NODE_EXPRESSED
        self.activation = Configuration.DEFAULT_NODE_ACTIVATION
        self.incoming = set()
        self.outgoing = set()

    @staticmethod
    def isValidType(_type):
        return _type in ['hidden', 'input', 'output']

    def copy(self, maintain_bias=False):
        clone = NodeGene()
        clone.sub_type = self.sub_type
        clone.expressed = self.expressed
        clone.activation = self.activation
        clone.incoming = self.incoming.copy()
        clone.outgoing = self.outgoing.copy()
        clone.origin = self.origin
        clone.inno_num = self.inno_num
        clone.bias = self.bias if maintain_bias else Configuration.DEFAULT_NODE_BIAS
        return clone

    def describe(self):
        return '<NodeGene-origin:{},inno_num:{},sub_type:\'{}\',bias:{},activation:\'{}\'>'.format(self.origin,self.inno_num,
                                                                                    self.sub_type, self.bias, self.activation)

class ConnectionGene(Gene):

    def __init__(self):
        self.type = Configuration.GENE_TYPES['connection']

    def initialize(self, inNode, outNode, generation):
        super().__init__(generation)
        self.inNode = inNode
        self.outNode = outNode
        self.weight = Distributions.sample_normal()
        self.expressed = True

    def copy(self, maintain_weights=False):
        clone = ConnectionGene()
        clone.inno_num = self.inno_num
        clone.origin = self.origin
        clone.inNode = self.inNode
        clone.outNode = self.outNode
        clone.weight = self.weight if maintain_weights else Distributions.sample_normal()
        clone.expressed = self.expressed
        return clone

    def describe(self):
        return '<ConnectionGene-origin:{},inno_num:{},inNode:{},outNode:{},weight:{},expressed:{}>'.format(self.origin, self.inno_num,
                                                                                                   self.inNode, self.outNode,
                                                                                                   self.weight, self.expressed)

class PseudoGene(Gene):

    def __init__(self, inno_num=None):
        super().__init__(inno_num)
        self.type = Configuration.GENE_TYPES['pseudo']

if __name__ == '__main__':
    g = NodeGene()
    g.initialize('input', 1)
    g
    g2 = g.copy()
    g2
    g.inno_num = 1
    g2
    g = ConnectionGene()
    g.initialize(1, 2, 1)
    g2 = g.copy()
    
