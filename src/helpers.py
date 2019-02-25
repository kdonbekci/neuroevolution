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

    def linear(z):
        return z

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
    def __init__(self):
        self.functions = {}
        self.add('sigmoid', MathOperations.sigmoid)
        self.add('tanh', MathOperations.tanh)
        self.add('sin', MathOperations.sin)
        self.add('gauss', MathOperations.gauss)
        self.add('relu', MathOperations.relu)
        self.add('softplus', MathOperations.softplus)
        self.add('identity', MathOperations.identity)
        self.add('clamped', MathOperations.clamped)
        self.add('inv', MathOperations.inv)
        self.add('log', MathOperations.log)
        self.add('exp', MathOperations.exp)
        self.add('abs', abs)
        self.add('hat', MathOperations.hat)
        self.add('square', MathOperations.square)
        self.add('cube', MathOperations.cube)
        self.add('linear', MathOperations.linear)
        self.function_names = list(self.functions.keys())
    
    #maybe implement some sort of validation?
    def add (self, fn, f):
        self.functions[fn] = f
        
    def get(self, fn):
        f = self.functions.get(fn)
        assert f is not None, '{} is not a valid activation function'.format(fn)
        return f
    
    def get_random_func(self):
        return Distributions.choice(self.function_names)
    
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