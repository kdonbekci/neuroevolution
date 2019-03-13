from config import Configuration
from tensorflow.keras import backend as K
from tensorflow.keras.utils import plot_model
K.set_floatx(Configuration.MODEL_FLOAT_PRECISION)
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Activation, Input, Lambda
from tensorflow.keras.models import load_model, save_model
from sklearn.model_selection import train_test_split

class Phenome:

    def __init__(self, _id): #construct neural network prototype from genome
        self.id = _id

    @property
    def size(self):
        pass

    def initialize(self, genome):
        nodes = {}
        inputs = []
        outputs = []
        loss = []
        for i in genome.inputs:
            node = genome.genes[i]
            nodes[i] = Input(shape=node.shape, name='input_{}'.format(node.inno_num))
            inputs.append(nodes[i])
        for i in genome.nodes:
            node = genome.genes[i]
            if not node.expressed:
                continue
            nodes[i] = Dense(units=node.units, activation=node.activation, name='node_{}'.format(node.inno_num))
        for i in genome.outputs:
            node = genome.genes[i]
            nodes[i] = Dense(units= node.shape[0], activation=node.activation,  name='output_{}'.format(node.inno_num))
            # outputs.append(nodes[i])
            loss.append(node.loss)
        for i in genome.connections:
            connection = genome.genes[i]
            if not connection.expressed:
                continue
            nodes[connection.target] = nodes[connection.target](nodes[connection.source])
            # print('{} ( {} )'.format(nodes[connection.target], nodes[connection.source]))

        for i in genome.outputs:
            outputs.append(nodes[i])
        self.model = Model(inputs=inputs, outputs=outputs)
        self.loss = loss

    def evaluate(self, data, labels):
        # X_train, X_test, Y_train, Y_test =
        self.model.compile(loss = self.loss, optimizer=Configuration.OPTIMIZER, metrics=['accuracy'])
        model.fit(data, labels, epochs=Configuration.EPOCHS, batch_size=1)






        #
        # while genome.genes[genome.innovations[i]].type == Configuration.GENE_TYPES['input']:
        #     g = genome.genes[genome.innovations[i]]
        #     x = Input(shape=g.shape)
        #     inputs[g.inno_num] = x
        #     i+=1
        # while genome.genes[genome.innovations[i]].type == Configuration.GENE_TYPES['input']:
        #     g = genome.genes[genome.innovations[i]]
        #     x = Output(shape=g.shape)
        #     outputs[g.inno_num] = x
        #     i+=1
        # while i < genome.size:
        #     g = genome.genes[genome.innovations[i]]
        #     if g.type is Configuration.GENE_TYPES['connection']:
        #
        #
        #     elif g.type is Configuration.GENE_TYPES['hidden']:
        #
        #     else:
        #         assert False, 'Unsupported gene type encountered: {}'.format(g.type)
        #     i+=1


    def __repr__(self):
        pass


def phenome_tests():
    from mutation import Mutations
    from genome import Genome
    import timeit
    import sys
    mutations = Mutations()
    genome = Genome()
    generation = 1
    genome.initialize(inputs=[(1,), (1,), (1,)], outputs=[(1,), (1,)], output_activation = ['sigmoid', 'sigmoid'],loss=['binary-cross-entropy', 'binary-cross-entropy'], _id=1, generation=generation)
    while generation < 10:
        generation+=1
        genome.mutate(generation, mutations)
        mutations.reset()
    genome.genes
    phenome = Phenome(1)
    phenome.initialize(genome)
    phenome.model
    phenome.model.summary()
    plot_model(phenome.model, '../img/model_phenome-tests-1.png')

    print('All tests for genome.py completed successfully.')
    return True
if __name__ == '__main__':
    phenome_tests()
