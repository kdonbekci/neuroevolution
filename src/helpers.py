import numpy as np
import random
import math


class Distributions:
    
    @staticmethod
    def sample_normal(mu=0.0, sigma=1.0, count=None):
        return np.random.normal(mu, sigma, count)
    
    def choice(seq):
        return random.choice(seq)
    
    
class MathOperations:
    
class Activations:
    