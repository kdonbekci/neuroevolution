from config import Configuration
from tensorflow.keras import backend as K
from tensorflow.keras.utils import plot_model
K.set_floatx(Configuration.MODEL_FLOAT_PRECISION)
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Activation, Input, Lambda
from tensorflow.keras.models import load_model, save_model
from genotype import Genotype

class Phenotype:

    def __init__(self, genotype, _id): #construct neural network prototype from genotype
        self.id = _id
        self.build(genotype)

    @property
    def size(self):
        pass

    def build(self, genotype):
        num_inputs = 0
        num_outputs = 0
#         layers
        for i in genotype.fixed_genes:
            g = genotype.fixed_genes[i]
            if g.type == 'input':
                num_inputs+=1
            else:
                num_outputs+=1
        for i in genotype.innovations:
            g = genotype.mutable_genes[i]
            if g.type == 'connection':
                pass
            elif g.type == 'hidden':
                pass
            else:
                assert False, 'invalid type for a gene {}'.format(g.type)
#         _input = Input(shape=)

    def __repr__(self):
        pass

def phenotype_tests():
    pass
if __name__ == '__main__':
    phenotype_tests()
