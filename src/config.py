class Configuration:

    INITIAL_POPULATION_SIZE = 100

    MODEL_FLOAT_PRECISION = 'float16'

    DEFAULT_NODE_ACTIVATION = 'linear'

    DEFAULT_NODE_EXPRESSED = True

    DEFAULT_NODE_BIAS = 0.0

    CHILD_MAINTAINS_BIAS = False

    CHILD_MAINTAINS_WEIGHTS = False

    GENE_TYPES = {'node': 0, 'connection': 1, 'pseudo': 2}

    INV_GENE_TYPES = {0: 'node', 1: 'connection', 2:'pseudo'}

    MUTATION_P = 0.05
