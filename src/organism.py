from genome import Genome
from phenome import Phenome
from fitness import Fitness

class Organism:
    unique_id = 0

    def __init__(self):
        self.id = Organism.unique_id
        Organism.unique_id+=1

    def initialize(self, species_hint):
        self.fitness = Fitness()
        self.species_hint = species_hint

    def mutate(self, generation, mutations):
        self.genome.mutate(generation, mutations)

    #method for sexual reproduction.
    @staticmethod
    def mate(parent1, parent2, generation):
        if parent1 > parent2:
            more_fit_parent = parent1
            less_fit_parent = parent2
        else:
            more_fit_parent = parent2
            less_fit_parent = parent1
        child_genome = Genome.crossover(more_fit_parent.genome, less_fit_parent.genome, generation)
        child = Organism(species_hint = more_fit_parent.species_hint)
        child.add_genome(child_genome)
        return child

    def asexually_reproduce(self):
        child = Organism(self.species_hint)
        child.add_genome(self.genome.copy())
        return child

    def evaluate(self, ):
        self.phenome.evaluate(fn)

    #method for the first organisms created
    @staticmethod
    def genesis(species_hint, input_dim, output_dim, generation):
        organism = Organism(species_hint)
        organism.generate_genome(input_dim, output_dim, generation)
        organism.generate_phenome()
        return organism

    def generate_genome(self, input_dim, output_dim, generation):
        self.genome = Genome(self.id)
        self.genome.initialize(input_dim, output_dim, generation)

    def add_genome(self, genome):
        self.genome = genome

    def generate_phenome(self):
        self.phenome = Phenome(self.id)

    def age(self, generation):
        return generation - self.origin

    @property
    def origin(self):
        assert 'genome' in self.__dict__, 'Genome of organism not yet initialized'
        return self.genome.origin

    def __repr__(self):
        return '<Organism-id:{},species_hint:{},genome:{},fitness:{}>'.format(self.id, self.species_hint, self.genome, self.fitness)

    #compare their fitness
    def __lt__(self, other):
        return self.fitness < other.fitness

def organism_tests():
    pass
if __name__ == '__main__':
    organism_tests()
