from importer import *

class Population:
    Species = loader.load_module("Species").Species
    
    def __init__(self):
        self.species = {}
        self.organisms = {}
        
    def generate_initial_population(self, size, input_dim, output_dim, generation):
        initial_species = Population.Species.generate_initial_species(size, input_dim, output_dim, generation)
        self.add_species(initial_species)
        self.add_organisms(initial_species.organisms)
        
    def add_species(self, species):
        assert species.id not in self.species, 'Species {} already in dictionary'
        self.species[species.id] = species
        
    def add_organisms(self, organisms):
        print(organisms)
                    