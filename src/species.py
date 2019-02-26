from helpers import Distributions
from organism import Organism

class Species:
    unique_id = 0

    def __init__(self, input_dim, output_dim, generation):
        self.id = Species.unique_id
        Species.unique_id+=1
        self.organisms={}
        self.origin = generation
        self.cached_organism = None #to be used for speciation after clear

    def add_organism(self, organism):
        assert organism.id not in self.organisms, 'Organism {} already in dictionary'.format(organism.id)
        self.organisms[organism.id] = organism
        organism.species_hint = self.id


    def get_random_member(self):
        return self.organisms[Distributions.choice(self.organisms)]

    @property
    def size(self):
        return len(self.organisms)

    # def genetic_distance(self, organism):
    #     retu

    @staticmethod
    def generate_initial_species(size, input_dim, output_dim, generation):
        first_species = Species(input_dim, output_dim, generation)
        for i in range(size):
            org = Organism.genesis(species_hint=first_species.id, input_dim=input_dim, output_dim=output_dim, generation=generation)
            first_species.add_organism(org)
        return first_species

    def clear(self):
        self.cached_organism = self.get_random_member()
        self.organisms = {}

    def __repr__(self):
        return '<Species-id:{},origin:{},size:{}>'.format(self.id, self.origin, self.size)

def species_tests():
    pass
if __name__ == '__main__':
    species_tests()
