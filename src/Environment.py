from importer import *
from config import Configuration
from helpers import Distributions

class Environment:
    Population = loader.load_module("Population").Population
    Pressure = loader.load_module("Pressure").Pressure
    
    def __init__(self, input_dim, output_dim):
        self.population = Environment.Population
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.pressures = []
        self.active_pressures = []
        self.generation = 0
        self.population = Environment.Population()
        
    def assemble(self):
        self.active_pressures = []
        for pressure in self.pressures:
            if pressure.is_active(generation=self.generation):
                self.active_pressures.append(pressure)
    
    def pressure(self):
        pass
    
    def select(self):
        pass
    
    def mutate(self):
        pass
    
    def speciate(self):
        pass

    def epoch(self):
        self.generation+=1 
        self.assemble()
        self.pressure()
        self.select()
        self.mutate()
        self.speciate()
    
    def generate_initial_population(self, initial_population_size):
        self.population.generate_initial_population(initial_population_size, self.input_dim, self.output_dim, self.generation)

    def add_pressure(self, pressure):
        self.pressures.append(pressure)
    
    def __repr__(self):
        return '<Environment-generation:{},pressures:{}>'.format(self.generation, self.pressures)