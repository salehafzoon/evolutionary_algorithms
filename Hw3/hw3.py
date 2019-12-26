import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from random import gauss

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

MAX_GENERATION = 600
POPULATION_SIZE = 400
N = 2
ALPHA = 418.9829
 
MUTATION_MODE = CASE2
XOVER_METHOD = GLOBAL_INT

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
        if MUTATION_MODE == 'CASE1' :
            sig.append(random.random())
        elif MUTATION_MODE == 'CASE2' :
            for _ in range(N):
                sig.append(random.random())

        chromosome = (x,sig)
        return chromosome

    def mutate(self):
        x = self.chromosome[0]
        sig = self.chromosome[1]

        # calcute t*N(0,1)
        t = (1/math.sqrt(2*N))
        const = t * gauss(0,1)

        if(MUTATION_MODE == CASE2) :
            for i in range(len(sig)):
                var = t * gauss(0,1)
                sig[i] = round(sig[i] *math.exp(const + var) ,8)
            for i in range(len(x)):
                x[i] = round(x[i] + sig[i] * gauss(0,1) ,8)
        
        # change our chromosome after mutate
        self.chromosome = (x,sig)
        # calculate fitness again
        (self.f_array,self.fitness) = self.call_fitness()
    
    @classmethod
    def crossOver(self, population):

        child = None
        
        if XOVER_METHOD == LOCAL_DISC or  XOVER_METHOD == LOCAL_INT:
            parent1 = random.choice(list(population))
            parent2 = random.choice(list(population))
            # print(parent1.chromosome[0],parent2.chromosome[0])
            
            xP1 = parent1.chromosome[0]
            xP2 = parent2.chromosome[0]

            sigP1 = parent1.chromosome[1]
            sigP2 = parent2.chromosome[1]

            child_x = []
            child_sig = []

            # randomly selection x from parents
            for x1, x2 in zip(xP1, xP2):
                if XOVER_METHOD == LOCAL_DISC:
                    child_x.append(random.choice([x1,x2]))
                else: 
                    child_x.append( (x1+x2)/2 )

            # randomly selection sigma from parents
            for sig1, sig2 in zip(sigP1, sigP2):
                if XOVER_METHOD == LOCAL_DISC:
                    child_sig.append(random.choice([sig1,sig2]))
                else :
                     child_sig.append( (sig1+sig2)/2 )
        
        elif XOVER_METHOD == GLOBAL_DISC or  XOVER_METHOD == GLOBAL_INT:
            child_x = []
            child_sig = []

            for i in range(N):
                parent1 = random.choice(list(population))
                parent2 = random.choice(list(population))
                # print(parent1.chromosome[0],parent2.chromosome[0])
                
                x1 = parent1.chromosome[0][i]
                x2 = parent2.chromosome[0][i]

                sig1 = parent1.chromosome[1][i]
                sig2 = parent2.chromosome[1][i]

                if XOVER_METHOD == GLOBAL_DISC:
                    child_x.append(random.choice([x1,x2]))
                else: 
                    child_x.append( (x1+x2)/2 )

                # randomly selection sigma from parents
                if XOVER_METHOD == GLOBAL_INT:
                    child_sig.append(random.choice([sig1,sig2]))
                else :
                    child_sig.append( (sig1+sig2)/2 )
        
        child = (child_x,child_sig)
        
        return Individual(child)

    def call_fitness(self):
        f_array = []
        fitness = 0
        x = self.chromosome[0]
        for i in range ( len(x)):
            f_array.append( round(- x[i]*math.sin(math.sqrt(math.fabs(x[i]))) ,10))
    
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

    # for ind in population[0:2]:
        # print("parent",ind.fitness , ind.f_array)
        # print("parent",ind.chromosome[0])
        
    # child = Individual.crossOver(population[0:2])
    # print("child",child.chromosome[0])
    # child.mutate()
    # print("mutated child",child.chromosome[0])
    
    while not found:

        # max generation terminate condition
        if generation == MAX_GENERATION :
            break
        
        population = sorted(population, key=lambda x: x.fitness)
        
        # for ind in population[0:3]:
        #     print(ind.f_array,ind.chromosome[0])
        # print("----------------")    
        
        if population[0].fitness == 0 :
            break

        new_generation = []
        
        for _ in range(POPULATION_SIZE * 7):
           
            child = Individual.crossOver(population)
            child.mutate()
            new_generation.append(child)
        
        new_generation = sorted(
            new_generation, key=lambda x: x.fitness)
   
        population = new_generation[0:POPULATION_SIZE]
        generation += 1

    print("generation :", generation, " x =",
          population[0].chromosome[0], " f =",population[0].fitness)


    duration = time.time() - start
    print("time :", round((duration) % 60 , 4) ," sec")