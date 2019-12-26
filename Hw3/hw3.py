import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np

MAX_VAL = 500
ONE_SIG = "one_sigma"
N_SIG = "n_sigma"
LOCAL_INT = "local_int"
GLOBAL_INT = "global_int"
LOCAL_DISC = "local_disc"
GLOBAL_DISC = "global_disc"

population = []
found = False

MAX_GENERATION = 1000
POPULATION_SIZE = 100
N = 5
SIGMA_MODE = "CASE2"

class Individual(object):

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.call_fitness()

    @classmethod
    def create_chromosome(self):
        x = []
        sig = []
        
        # init object variables
        for _ in range(N):
            x.append( random.randrange(-500,500) )
        
        # init random sigma from (0,1)
        if SIGMA_MODE == 'CASE1' :
            sig.append(random.random())
        elif SIGMA_MODE == 'CASE2' :
            for _ in range(N):
                sig.append(random.random())

        chromosome = (x,sig)
        return chromosome

    def mutate(self):
        pass
    @classmethod
    def crossOver(method , population):

        # xP1 = self.chromosome[0]
        # xP2 = parent2.chromosome[0]
        # sigP1 = self.chromosome[1]
        # sigP2 = parent2.chromosome[1]
        
        # xC1 = []
        # xC2 = []
        # sigC1 = []
        # sigC2 = []
        
        # if method == LOCAL_DISC:

        #     pass
        # elif method == GLOBAL_DISC:
        #     pass

        # elif method == LOCAL_INT:
        #     for x1, x2 , sig1, sig2 in zip(xP1, xP2 , sigP1,sigP2):
        #         xC1.append( (x1+x2)/2 )
        #         xC2.append( (x1+x2)/2 )
                
        #         sigC1.append( (sig1+sig2)/2 )
        #         sigC2.append( (sig1+sig2)/2 )
            
        #     child1 = (xC1,sigC1)
        #     child2 = (xC2,sigC2)
            
        # elif method == GLOBAL_INT:
        #     pass

        # return (Individual(child1), Individual(child2))
        pass

    def call_fitness(self):
        fitness = 0
        x = self.chromosome[0]
        for val in x :
            fitness += -val * math.sin(math.sqrt())

        return fitness

def initial_population():
    for _ in range(POPULATION_SIZE):
        chrom = Individual.create_chromosome()
        indiv = Individual(chrom)
        population.append(indiv)


if __name__ == '__main__':
    start = time.time()
    # First Generation
    
    while not found:

        # max generation terminate condition
        if generation == MAX_GENERATION or limit == MAX_LIMIT:
            break

        population = sorted(population, reverse=True, key=lambda x: x.fitness)

        if best_answer == population[0].fitness:
            limit += 1
        else:
            limit = 0
            best_answer = population[0].fitness

        best_fits.append(population[0].fitness)
        avg_fits.append(np.mean([p.fitness for p in population]))

        print("generation:", generation, " best fit:", population[0].fitness)

        besstParent = population[0]
        new_generation = []

        for _ in range(POPULATION_SIZE):

            (parent1, parent2) = Individual.rouletteWheelSelection(population)
            
            (child1, child2) = Individual.crossOver("mode",population)

            child1.mutate()
            child2.mutate()

            new_generation.append(child1)
            new_generation.append(child2)

        new_generation = sorted(
            new_generation, reverse=True, key=lambda x: x.fitness)

        new_generation.insert(len(new_generation)-1, besstParent)

        population = new_generation
        generation += 1

    generation -= 1
    print("generation : ", generation, "       ",
          population[0].gene[0:10],  population[0].fitness)


    duration = time.time() - start
    print("minute:", (duration)//60)
    print("second:", (duration) % 60)
