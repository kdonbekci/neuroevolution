from species import Species

class Population:

    def __init__(self):
        self.species = {}
        self.organisms = {}

    @property
    def size(self):
        total_size = 0
        for i in self.species:
            total_size+= self.species[i].size
        return total_size

    def pressure(self, pressures):
        for i in self.organisms:
            self.organisms[i].evaluate()

    def mutate(self, generation):
        for i in self.organisms: ## REVIEW: possible multicore CPU computation
            self.organisms[i].mutate(generation)

    def speciate(generation):
        pass

    def generate_initial_population(self, size, input_dim, output_dim, generation):
        initial_species = Species.generate_initial_species(size, input_dim, output_dim, generation)
        self.add_species(initial_species)
        self.add_organisms(initial_species.organisms)

    def add_species(self, species):
        assert species.id not in self.species, 'Species {} already in dictionary'
        self.species[species.id] = species

    def add_organisms(self, organisms):
        for i in organisms:
            self.organisms[i] = organisms[i]
        # print(organisms)

    def __repr__(self):
        return '<Population-size:{},species:{}'.format(self.size, self.species)

def population_tests():
    pass
if __name__ == '__main__':
    population_tests()
