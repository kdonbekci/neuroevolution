from config import Configuration
from tensorflow.keras import backend as K
from tensorflow.keras.utils import plot_model
K.set_floatx(Configuration.MODEL_FLOAT_PRECISION)
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Activation, Input, Lambda
from tensorflow.keras.models import load_model, save_model
from genome import Genome

class Phenome:

    def __init__(self, genome, _id): #construct neural network prototype from genome
        self.id = _id
        self.build(genome)

    @property
    def size(self):
        pass

    def build(self, genome):
        num_inputs = 0
        num_outputs = 0
#         layers
        for i in genome.fixed_genes:
            g = genome.fixed_genes[i]
            if g.type == 'input':
                num_inputs+=1
            else:
                num_outputs+=1
        for i in genome.innovations:
            g = genome.mutable_genes[i]
            if g.type == 'connection':
                pass
            elif g.type == 'hidden':
                pass
            else:
                assert False, 'invalid type for a gene {}'.format(g.type)
#         _input = Input(shape=)

    def __repr__(self):
        pass

def phenome_tests():
    pass
if __name__ == '__main__':
    phenome_tests()
