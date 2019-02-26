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

    MUTATION_P = {'add_node': .05, 'change_node': .05, 'toggle_connection': .05,
                    'add_connection': .05, 'toggle_node': .01}

    MUTATION_LIMIT = {'add_node': 5, 'change_node': 5, 'toggle_connection': 5,
                    'add_connection': 5, 'toggle_node': 1}

    MUTATION_MAX_ATTEMPTS = 10
