from helpers import Distributions
from config import Configuration

class Gene:

    inno_tracker = 0

    def __init__(self, generation=None, copy=False, gene=None):
        if not copy:
            self.inno_num = Gene.inno_tracker
            Gene.inno_tracker+=1
            self.origin = generation
        else:
            self.inno_num = gene.inno_num
            self.origin = gene.origin

    def age(self, curGeneration):
        return curGeneration - self.origin

    def __lt__(self, other):
        return self.inno_num < other.inno_num

    def __eq__(self, other):
        return self.inno_num == other.inno_num

    def __repr__(self):
        return self.describe()

class NodeGene(Gene):

    def __init__(self, _type=None, generation=None, copy=False, gene=None):
        if not copy:
            assert generation > 0, 'Generation {} must be > 0'.format(generation)
            assert NodeGene.isValidType(_type), 'Invalid type (\'{}\') for NodeGene'.format(_type) #temporary
            super().__init__(generation=generation)
            self.type = _type
            self.bias = Configuration.DEFAULT_NODE_BIAS
            self.expressed  = Configuration.DEFAULT_NODE_EXPRESSED
            self.activation = Configuration.DEFAULT_NODE_ACTIVATION
        else:
            super().__init__(copy=True, gene=gene)
            self.type = gene.type
            self.bias = gene.bias
            self.expressed = gene.expressed
            self.activation = gene.activation

    @staticmethod
    def isValidType(_type):
        return _type in ['hidden', 'input', 'output']

    def copy(self, maintain_bias=False):
        clone= NodeGene(copy=True, gene=self)
        if not maintain_bias:
            clone.bias = Configuration.DEFAULT_NODE_BIAS
        return clone

    def describe(self):
        return '<NodeGene-origin:{},inno_num:{},type:\'{}\',bias:{},activation:\'{}\'>'.format(self.origin,self.inno_num, self.type,
                                                                                                    self.bias, self.activation)


class ConnectionGene(Gene):

    def __init__(self, inNode=None, outNode=None, generation=None, copy=False, gene=None):
        if not copy:
            super().__init__(generation)
            self.inNode = inNode
            self.outNode = outNode
            self.weight = Distributions.sample_normal()
            self.expressed = True
            self.type = 'connection'
        else:
            super().__init__(copy=True, gene=gene)
            self.inNode = gene.inNode
            self.outNode = gene.outNode
            self.weight = gene.weight
            self.expressed = gene.expressed

    def copy(self, maintain_weights=False):
        clone = ConnectionGene(copy=True, gene=self)
        if not maintain_weights:
            clone.weight = Distributions.sample_normal()
        return clone

    def describe(self):
        return '<ConnectionGene-origin:{},inno_num:{},inNode:{},outNode:{},weight:{},expressed:{}>'.format(self.origin, self.inno_num,
                                                                                                   self.inNode, self.outNode,
                                                                                                   self.weight, self.expressed)


class PseudoGene(Gene):

    def __init__(self, inno_num=None):
        super().__init__(inno_num)
