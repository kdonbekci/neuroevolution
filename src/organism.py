from genotype import Genotype
from phenotype import Phenotype
from fitness import Fitness

class Organism:
    unique_id = 0

    def __init__(self, species_hint):
        self.fitness = Fitness()
        self.id = Organism.unique_id
        Organism.unique_id+=1
        self.species_hint = species_hint

    def mutate(self, generation):
        self.genotype.mutate(generation)

    #method for sexual reproduction.
    @staticmethod
    def mate(parent1, parent2, generation):
        if parent1 > parent2:
            more_fit_parent = parent1
            less_fit_parent = parent2
        else:
            more_fit_parent = parent2
            less_fit_parent = parent1
        child_genotype = Genotype.crossover(more_fit_parent.genotype, less_fit_parent.genotype, generation)
        child = Organism(species_hint = more_fit_parent.species_hint)
        child.add_genotype(child_genotype)
        return child

    def asexually_reproduce(self):
        child = Organism(self.species_hint)
        child.add_genotype(self.genotype.copy())
        return child

    def evaluate(self, ):
        self.phenotype.evaluate(fn)

    #method for the first organisms created
    @staticmethod
    def genesis(species_hint, input_dim, output_dim, generation):
        organism = Organism(species_hint)
        organism.generate_genotype(input_dim, output_dim, generation)
        organism.generate_phenotype()
        return organism

    def generate_genotype(self, input_dim, output_dim, generation):
        self.genotype = Genotype()
        self.genotype.initialize(input_dim, output_dim, generation)

    def add_genotype(self, genotype):
        self.genotype = genotype

    def generate_phenotype(self):
        self.phenotype = Phenotype(self.genotype, self.id)

    def age(self, generation):
        return generation - self.origin

    @property
    def origin(self):
        assert 'genotype' in self.__dict__, 'Genotype of organism not yet initialized'
        return self.genotype.origin

    def __repr__(self):
        return '<Organism-id:{},species_hint:{},genotype:{},fitness:{}>'.format(self.id, self.species_hint, self.genotype, self.fitness)

    #compare their fitness
    def __lt__(self, other):
        return self.fitness < other.fitness

def organism_tests():
    pass
if __name__ == '__main__':
    organism_tests()
