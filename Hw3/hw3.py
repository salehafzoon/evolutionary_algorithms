import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from random import gauss
import numpy as np

MAX_VAL = 500
CASE1 = "CASE1"
CASE2 = "CASE2"
NON_ADAPTIVE = "NON_ADAPTIVE"

LOCAL_INT = "LOCAL_INT"
GLOBAL_INT = "GLOBAL_INT"
LOCAL_DISC = "LOCAL_DISC"
GLOBAL_DISC = "GLOBAL_DISC"
ELITISM = "ELITISM"
GENERATIONAL = "GENERATIONAL"

generation = 1
population = []
found = False

MAX_GENERATION = 40
POPULATION_SIZE = 50
N = 10
ALPHA = 418.9829

MUTATION_MODE = CASE2
XOVER_METHOD = GLOBAL_INT
SURVIVOR_SEL_TYPE = ELITISM
sigArray = []
best_fits = []
avg_fits = []

def plotResult():
    # print(best_fits)
    print(avg_fits)
    
    plt.plot(list(range(generation)), best_fits, 'go-',
             label='best of generations', linewidth=2)
    plt.show()

    plt.plot(list(range(generation)), avg_fits, 'bo-',
             label='avg of generations', linewidth=2)
    plt.show()


class Individual(object):

    def __init__(self, chromosome):
            
        self.chromosome = chromosome
        (self.f_array,self.fitness) = self.call_fitness()
        self.valid = True
    @classmethod
    def initConstantSigmas(self):
        for _ in range(N):
            sigArray.append(random.random())

    @classmethod
    def create_chromosome(self):
        x = []
        sig = []
            
        # init object variables
        for _ in range(N):
            x.append( random.randrange(-500,500) )
        
        # init random sigma from (0,1)
        if MUTATION_MODE == CASE1:
            sig.append(random.random())
        elif MUTATION_MODE == CASE2:
            for _ in range(N):
                sig.append(random.random())
        elif MUTATION_MODE == NON_ADAPTIVE:
            sig.extend(sigArray)

        # print("sig:",sig)
        chromosome = (x,sig)
        return chromosome

    def mutate(self):
        x = self.chromosome[0]
        sig = self.chromosome[1]

        # calcute t*N(0,1)
        t = (1/math.sqrt(2*N))
        tCor = (1/math.sqrt( 2*math.sqrt(N)) )
        const = t * gauss(0,1)

        if(MUTATION_MODE == CASE1) :
            sig[0] *= math.exp(const)
        elif (MUTATION_MODE == CASE2) :
            for i in range(len(sig)):
                var = tCor * gauss(0,1)
                sig[i] *= math.exp(const + var)
        
        for i in range(len(x)):
            if(MUTATION_MODE == CASE1) :
                #  x[i] =  round( x[i] + sig[0] * gauss(0,1) ,7)
                 x[i] += sig[0] * gauss(0,1)
                 
            elif MUTATION_MODE == CASE2 or MUTATION_MODE == NON_ADAPTIVE:
                # x[i] =  round( x[i] + sig[i] * gauss(0,1) ,7)
                x[i] += sig[i] * gauss(0,1) 
            
            if x[i] >= 500 or x[i]<-500:
                self.valid = False
        
        # change our chromosome after mutate
        if(self.valid):
            self.chromosome = (x,sig)
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
                
                if MUTATION_MODE == CASE2:
                    sig1 = parent1.chromosome[1][i]
                    sig2 = parent2.chromosome[1][i]
                else:
                    sig1 = parent1.chromosome[1][0]
                    sig2 = parent2.chromosome[1][0]

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
            # f_array.append( round(- x[i]*math.sin(math.sqrt(math.fabs(x[i]))) ,10))
            f_array.append(- x[i]*math.sin(math.sqrt(math.fabs(x[i]))))

        for f in f_array :
            fitness +=f

        fitness = float(fitness) + ALPHA*len(x)

        return (f_array , fitness)

def initial_population():
    population = []
    for _ in range(POPULATION_SIZE):
        chrom = Individual.create_chromosome()
        indiv = Individual(chrom)
        population.append(indiv)
    return population

def ga():

    # First Generation
    global generation
    global population
    global best_fits
    global avg_fits
    best_fits = []
    avg_fits = []
    
    if MUTATION_MODE == NON_ADAPTIVE :
        Individual.initConstantSigmas()
        
    population = initial_population()
    
    found = False
    generation = 0

    while not found:

        # max generation terminate condition
        if generation == MAX_GENERATION :
            break
        
        population = sorted(population, key=lambda x: x.fitness)
        
        best_fits.append(population[0].fitness)
        avg_fits.append(np.mean([p.fitness for p in population]))

        # print("generation:",generation,population[0].fitness,population[0].chromosome[0][0:3])
        
        if population[0].fitness == 0 :
            break
        
        new_generation = []
        
        for _ in range(POPULATION_SIZE *7):
           
            child = Individual.crossOver(population)
            child.mutate()
            if(child.valid) :
                new_generation.append(child)
    
        if(SURVIVOR_SEL_TYPE == ELITISM):
            new_generation.extend(population)

        new_generation = sorted(
            new_generation, key=lambda x: x.fitness)

        population = new_generation[0:POPULATION_SIZE]

        generation += 1

    # print(population[0].fitness,population[0].f_array,"\n")
    plotResult()
    print(population[0].fitness)
    return population[0].fitness

if __name__ == '__main__':

    ga()
    # start = time.time()

    # fitnesses = []

    # for _ in range(10):

    #     fitnesses.append( ga() )

    # print("fitnesses:",fitnesses)

    # print("average:",np.mean(fitnesses))
    # print("variance:",math.sqrt(np.var(fitnesses)))

    # # print("generation :", generation, " x =",
    # #       population[0].chromosome[0], " fitness =",population[0].fitness)
    
    # # for i in range(len(population[0].f_array)):
    # #     population[0].f_array[i] += ALPHA
    
    # # print("f_array:", population[0].f_array)

    # # duration = time.time() - start
    # # print("time :", (duration)//60 ,"min,",round((duration) % 60 , 4) ,"sec")