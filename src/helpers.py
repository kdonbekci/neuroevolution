import numpy as np
import random
import math
from operator import mul

class Distributions:

    def sample_normal(mu=0.0, sigma=1.0, count=None):
        return np.random.normal(mu, sigma, count)

    def coin_toss():
        return random.random() > .5

    def choice(seq):
        return random.choice(seq)

    def probability(p):
        return random.random() < p

    def shuffle(x):
        random.shuffle(x)


class MathOperations:

    def product(x): # note: `x` is a list or other iterable
        return reduce(mul, x, 1.0)

    def maxabs(x):
        return max(x, key=abs)

    def mean(x):
        values = list(x)
        return sum(map(float, values)) / len(values)

    def median(x):
        values = list(x)
        n = len(values)
        if n <= 2:
            return MathOperations.mean(values)
        values.sort()
        if (n % 2) == 1:
            return values[n//2]
        i = n//2
        return (values[i - 1] + values[i])/2.0

    def sigmoid(z):
        z = max(-60.0, min(60.0, 5.0 * z))
        return 1.0 / (1.0 + math.exp(-z))

    def linear(z, w, b):
        return z * w + b

    def tanh(z):
        z = max(-60.0, min(60.0, 2.5 * z))
        return math.tanh(z)


    def sin(z):
        z = max(-60.0, min(60.0, 5.0 * z))
        return math.sin(z)


    def gauss(z):
        z = max(-3.4, min(3.4, z))
        return math.exp(-5.0 * z**2)


    def relu(z):
        return z if z > 0.0 else 0.0


    def softplus(z):
        z = max(-60.0, min(60.0, 5.0 * z))
        return 0.2 * math.log(1 + math.exp(z))


    def identity(z):
        return z


    def clamped(z):
        return max(-1.0, min(1.0, z))


    def inv(z):
        try:
            z = 1.0 / z
        except ArithmeticError: # handle overflows
            return 0.0
        else:
            return z


    def log(z):
        z = max(1e-7, z)
        return math.log(z)

    def exp(z):
        z = max(-60.0, min(60.0, z))
        return math.exp(z)


    def hat(z):
        return max(0.0, 1 - abs(z))


    def square(z):
        return z ** 2


    def cube(z):
        return z ** 3

class Activations:
    functions = {'sigmoid': MathOperations.sigmoid,
                'tanh': MathOperations.tanh,
                'sin': MathOperations.sin,
                'gauss': MathOperations.gauss,
                'relu': MathOperations.relu,
                'softplus': MathOperations.softplus,
                'identity': MathOperations.identity,
                'clamped': MathOperations.clamped,
                'inv': MathOperations.inv,
                'log': MathOperations.log,
                'exp': MathOperations.exp,
                'abs': abs,
                'hat': MathOperations.hat,
                'square': MathOperations.square,
                'cube': MathOperations.cube,
                'linear': MathOperations.linear}

    function_names = list(functions.keys())

    # def add (fn, f):
    #     functions[fn] = f
    #
    # add('sigmoid', MathOperations.sigmoid)
    # add('tanh', MathOperations.tanh)
    # add('sin', MathOperations.sin)
    # add('gauss', MathOperations.gauss)
    # add('relu', MathOperations.relu)
    # add('softplus', MathOperations.softplus)
    # add('identity', MathOperations.identity)
    # add('clamped', MathOperations.clamped)
    # add('inv', MathOperations.inv)
    # add('log', MathOperations.log)
    # add('exp', MathOperations.exp)
    # add('abs', abs)
    # add('hat', MathOperations.hat)
    # add('square', MathOperations.square)
    # add('cube', MathOperations.cube)
    # add('linear', MathOperations.linear)

    #maybe implement some sort of validation?


    @classmethod
    def get(cls, fn):
        f = cls.functions.get(fn)
        assert f is not None, '{} is not a valid activation function'.format(fn)
        return f

    @classmethod
    def get_random_func(cls):
        return Distributions.choice(cls.function_names)

class Aggregations():

    def __init__(self):
        self.functions = {}
        self.add('product', MathOperations.product)
        self.add('sum', sum)
        self.add('max', max)
        self.add('min', min)
        self.add('maxabs', MathOperations.maxabs)
        self.add('median', MathOperations.median)
        self.add('mean', MathOperations.mean)
        self.function_names = list(self.functions.keys())

    def add(self, fn, f):
        self.functions[fn] = f

    def get(self, fn):
        f = self.functions.get(fn)
        assert f is not None, '{} is not a valid aggregation function'.format(fn)
        return f

    def get_random_func(self):
        return Distributions.choice(self.function_names)
