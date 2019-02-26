from helpers import MathOperations, Distributions

class Fitness:

    def __init__(self):
        self.history = []

    def add_fitness_record(self, record):
        self.history.append(record)

    def __lt__(self, other):
        assert not self.is_emtpy() and not other.is_emtpy(), 'One or both fitness is empty'
        mean_dif = MathOperations.mean(self.history) - MathOperations.mean(self.history)
        max_dif = max(self.history) - max(other.history)
        median_dif = MathOperations.median(self.history) - MathOperations.median(other.history)
        c_mean, c_max, c_median = Distributions.sample_normal(3, 1, 3)
        _sum = sum([c_mean, c_max, c_median])
        c_mean, c_max, c_median = c_mean/_sum, c_max/_sum, c_median/_sum
        score = c_mean * mean_dif + c_max * max_dif + c_median * median_dif
        return score < 0.0

    def is_emtpy(self):
        return not self.history

    def clear(self):
        self.history = []

    def __repr__(self):
        return '<Fitness-histrory:{}>'.format(self.history)

def fitness_tests():
    pass
if __name__ == '__main__':
    fitness_tests()
