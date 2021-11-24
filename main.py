import simpy
from States import combat



env = simpy.Environment()
env.process(combat.combat(env))
env.run(until=30)




