import random
import time
import math

start = time.time()
generation = 1
found = False
population = []
strg_fitness = 0

POPULATION_SIZE = 240
MAX_NUMBER = 243
ACTION_LIST = ["n","s","e","w","r","st","b"]
GRID_WIDTH = 10
CURR_LOC = (5,5)
CAN_POS = []

METHOD = "uniform"
  
class Individual(object):
      
    def __init__(self, chromosome): 
        self.chromosome = chromosome  
        self.fitness = self.call_fitness()
  
    @classmethod
    def create_gnome(self): 
        
        gene = []
        for i in range(MAX_NUMBER):    
            action = random.choice(list(ACTION_LIST))
            gene.append(action)
            
        return gene
  
    @classmethod
    def rouletteWheelSelection(self,population):
        
        fitness_sum = 0
        parents = []
        min_fit = -1000
        fitnesses = []
        
        for individual in population:
            fitnesses.append(individual.fitness)
        
        min_fit = abs(min(fitnesses))

        # print("fitnesses",fitnesses)
        
        for i in range(len(fitnesses)):
            fitnesses[i] += min_fit +10
            
        fitness_sum = sum(fitnesses)
        
        # print("fitnesses",fitnesses,"fitness_sum",fitness_sum)
        
        filled = 0
            
        for i in range(len(fitnesses)) :
            
            fitnesses[i] = float(filled + fitnesses[i] /float(fitness_sum))
            filled = fitnesses[i]
        
            
        # print("fitnesses",fitnesses)
        # print("population",population)
        
        for j in range(2):
            pointer = random.random()
            
            # print("pointer",pointer)
            
            for i in range(len(fitnesses)):
                
                if pointer < fitnesses[i]:
                    # print("selected",population[i])
                    parents.append(population[i])
                    break
                    
        return parents

    def mutate(self):
        for chrom in self.chromosome:
            mutateProb = random.random()
            if(mutateProb <= 0.005):
                index = self.chromosome.index(chrom)
                action = random.choice(list(ACTION_LIST))
                self.chromosome[index] = action
        
    def crossOver(self, parent2): 

        child = []
        if METHOD == "uniform":
            for c1 , c2 in zip(self.chromosome , parent2.chromosome):
                prob = random.random()
                if(prob > 0.5):
                    child.append(c1)
                else:
                    child.append(c2)
        
        if METHOD == "onePoint":
            size = len(self.chromosome)
            child = self.chromosome[:size/2]
            for i in range(size/2,size):
                child.append(parent2.chromosome[i])
            
        return Individual(child)

    def call_fitness(self): 
        
        global CURR_LOC
        fitness = 0
        (x,y) = CURR_LOC
        can_pos = CAN_POS[:]
        
        for action in self.chromosome :
            
            if action =="st":
                x=x
            elif action =="n":
                y +=1
            elif action =="s":
                y-=1
            elif action == "e":
                x+=1
            elif action == "w":
                x-=1
            elif action == "b" and CURR_LOC in can_pos:
                can_pos.remove(CURR_LOC)
                fitness +=10
            
            elif action == "r":
                r = 0
                dec_inc = random.random()
                if dec_inc>0.5:
                    r = 1
                else:
                    r = -1
                        
                hor_or_ver = random.random()
                if(hor_or_ver > 0.5):
                    x +=r
                else:
                    y +=r
            
            # check if hit the wall
            if x >10 or x<0 or y>10 or y<0:
                fitness -=5
                x = max(0,x)
                y = max(0,x)
                
            
            CURR_LOC = (x,y)
                    
        return fitness 

if __name__ == '__main__':
    
    for i in range(2):
        for j in range(2):
            CAN_POS.append((i,j))  
    
    # First Generation    
    for _ in range(POPULATION_SIZE): 
        gnome = Individual.create_gnome() 
        indiv = Individual(gnome)
        if indiv not in population:
            population.append(indiv) 


    while not found:
        
        population = sorted(population, reverse = True,key = lambda x:x.fitness)
        
        print("generation:",generation," best fit:",population[0].fitness,"others:",
              population[1].fitness,population[2].fitness,population[3].fitness,
              population[4].fitness,population[5].fitness,population[6].fitness)
        
        if population[0].fitness == len(CAN_POS)* 10:
            found = True
            break
        
        new_generation = []
        
        index = int(POPULATION_SIZE* 0.8)
            
        for _ in range(POPULATION_SIZE):
            
            (parent1 , parent2) = Individual.rouletteWheelSelection(population[:index])
            child = parent1.crossOver(parent2)
            
            child.mutate()
            
            new_generation.append(child) 
                
  
        population = new_generation 
        generation += 1


    print("generation->",generation,"       ",population[0].chromosome ,  population[0].fitness)

    duration = time.time() - start
    print ("minute:",(duration)//60)
    print("second:" ,(duration)%60)
