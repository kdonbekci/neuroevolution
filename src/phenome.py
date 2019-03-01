from config import Configuration
from tensorflow.keras import backend as K
from tensorflow.keras.utils import plot_model
K.set_floatx(Configuration.MODEL_FLOAT_PRECISION)
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Activation, Input, Lambda
from tensorflow.keras.models import load_model, save_model
from genome import Genome

class Phenome:

    def __init__(self, _id): #construct neural network prototype from genome
        self.id = _id

    @property
    def size(self):
        pass

# Thhis returns a tensor
# inputs = Input(shape=(784,))
#
# a layer instance is callable on a tensor, and returns a tensor
# x = Dense(64, activation='relu')(inputs)
# x = Dense(64, activation='relu')(x)
# predictions = Dense(10, activation='softmax')(x)
#
# # This creates a model that includes
# # the Input layer and three Dense layers
# model = Model(inputs=inputs, outputs=predictions)
# model.compile(optimizer='rmsprop',
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])
# model.fit(data, labels)  # starts training

    def build(self, genome):
        i = 0
        inputs = []
        while genome.genes[genome.innovations[i]].type == Configuration.GENE_TYPES['input']:
            x = Input(shape)



    def __repr__(self):
        pass

def phenome_tests():
    pass
if __name__ == '__main__':
    phenome_tests()
