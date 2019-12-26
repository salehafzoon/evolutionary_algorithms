import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np

MAX_VAL = 500
CASE1 = "CASE1"
CASE2 = "CASE2"
LOCAL_INT = "LOCAL_INT"
GLOBAL_INT = "GLOBAL_INT"
LOCAL_DISC = "LOCAL_DISC"
GLOBAL_DISC = "GLOBAL_DISC"

generation = 1
population = []
found = False

MAX_GENERATION = 300
POPULATION_SIZE = 100
N = 5
ALPHA = 418.9829
 
MUTATION_MODE = CASE2
XOVER_METHOD = LOCAL_DISC

class Individual(object):

    def __init__(self, chromosome):
        self.chromosome = chromosome
        (self.f_array,self.fitness) = self.call_fitness()

    @classmethod
    def create_chromosome(self):
        x = []
        sig = []
        
        # init object variables
        for _ in range(N):
            x.append( random.randrange(-500,500) )
            # x.append(420.9687)
        
        # init random sigma from (0,1)
        if SIGMA_MODE == 'CASE1' :
            sig.append(random.random())
        elif SIGMA_MODE == 'CASE2' :
            for _ in range(N):
                sig.append(random.random())

        chromosome = (x,sig)
        return chromosome

    def mutate(self):
        x = self.chromosome[0]
        sig = self.chromosome[1]
        # calcute t*N(0,1)
        const = (1/math.sqrt(2*N)) *
        if(MUTATION_MODE == CASE2) :

    
    @classmethod
    def crossOver(self, population):

        child = None
        
        if XOVER_METHOD == LOCAL_DISC:
            parent1 = random.choice(list(population))
            parent2 = random.choice(list(population))

            print(parent1.chromosome[0],parent2.chromosome[0])
            
            xP1 = parent1.chromosome[0]
            xP2 = parent2.chromosome[0]
            
            sigP1 = parent1.chromosome[1]
            sigP2 = parent2.chromosome[1]

            child_x = []
            child_sig = []

            # randomly selection x from parents
            for x1, x2 in zip(xP1, xP2):
                child_x.append(random.choice([x1,x2]))

            # randomly selection sigma from parents
            for sig1, sig2 in zip(sigP1, sigP2):
                child_sig.append(random.choice([sig1,sig2]))

            child = (child_x,child_sig)
        
        return Individual(child)

    def call_fitness(self):
        f_array = []
        fitness = 0
        x = self.chromosome[0]
        for i in range ( len(x)):
            f_array.append( - x[i]*math.sin(math.sqrt(math.fabs(x[i]))) )
    
        for f in f_array :
            fitness +=f

        fitness = float(fitness) + ALPHA*len(x)

        return (f_array , fitness)

def initial_population():
    for _ in range(POPULATION_SIZE):
        chrom = Individual.create_chromosome()
        indiv = Individual(chrom)
        population.append(indiv)

    

if __name__ == '__main__':
    start = time.time()

    # First Generation
    initial_population()

    for ind in population[0:2]:
        # print("parent",ind.fitness , ind.f_array)
        # print("parent",ind.chromosome[0])
        
    # child = Individual.crossOver(population[0:2])
    # print("child",child.chromosome[0])

    # while not found:

    #     # max generation terminate condition
    #     if generation == MAX_GENERATION :
    #         break
        
    #     population = sorted(population, reverse=True, key=lambda x: x.fitness)
    #     print("generation:", generation, " best fit:", population[0].fitness)

    #     new_generation = []
    #     for _ in range(POPULATION_SIZE):
           
    #         child1 = Individual.crossOver(XOVER_METHOD,population)

    # #         child1.mutate()
    # #         child2.mutate()

    # #         new_generation.append(child1)
    # #         new_generation.append(child2)

    # #     new_generation = sorted(
    # #         new_generation, reverse=True, key=lambda x: x.fitness)

    # #     new_generation.insert(len(new_generation)-1, besstParent)

    # #     population = new_generation
    # #     generation += 1

    # # generation -= 1
    # # print("generation : ", generation, "       ",
    # #       population[0].gene[0:10],  population[0].fitness)


    # # duration = time.time() - start
    # # print("minute:", (duration)//60)
    # # print("second:", (duration) % 60)
