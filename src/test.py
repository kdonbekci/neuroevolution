from mutation import AddConnectionMutation,AddNodeMutation,ChangeNodeMutation,ChangeConnectionMutation,ToggleConnectionMutation,ToggleNodeMutation,tests
from gene import ConnectionGene, NodeGene, PseudoGene, tests
from genome import Genome, tests
from phenome import Phenome, tests
from fitness import Fitness, tests
from organism import Organism, tests
from pressure import Pressure, tests
from environment import Environment, tests

print('hello')

env1 = Environment(1, 2)
env1
p1 = Pressure(lambda:True, [], lambda x: x , ['loss'], 10, 'minimize cross entropy loss')
p2 = Pressure(lambda x: x>20 and x%3 == 0, ['generation'], lambda x: -x, ['network-size'], 5, 'decrease network size')
env1.add_pressure(p1)
env1.add_pressure(p2)
env1.generate_initial_population(100)
env1.population
env1.active_pressures
env1.assemble()
env1.active_pressures

env1.size
