import random
import time
import math
import string

start = time.time()
generation = 1
found = False
population = []
POPULATION_SIZE = 900
MAX_GENERATION = 300
METHOD = "uniform"
TARGET = "salehafzoon9831678"


def create_gnome():
    gene = ""
    possible = list(string.ascii_lowercase)
    for i in range(10):
        possible.append(i)

    for i in range(len(TARGET)):
        gene += str(random.choice(possible))

    return gene

def call_fitness(gene):
    fitness = 0
    for x , y in zip(list(gene), list(TARGET)):
        fitness += abs(ord(x)-ord(y))

    return fitness

def crossOver(parent1, parent2):
    child = ""
    if METHOD == "uniform":
        for c1 , c2 in zip(list(parent1) , list(parent2)):
            prob = random.random()
            if(prob > 0.5):
                child += c1
            else:
                child += c2
    
    if METHOD == "onePoint":
        
        size = len(list(parent1))
        child = parent1[:size/2]
        child = child +parent2[size/2:]
        
    return child
        
def mutate(child):
    possible = list(string.ascii_lowercase)
    for i in range(10):
        possible.append(i)

    index = int(random.random()* len(child))
    
    child="".join((child[:index],str(random.choice(possible)),child[index+1:]))
           
    return child
    

if __name__ == '__main__':

    
    # First Generation
    for i in range(0, POPULATION_SIZE):
        population.append(create_gnome())

    while not found:

        # max generation terminate condition
        if generation > MAX_GENERATION:
            print("---- can't find ----")
            break
        
        population = sorted(population, key=lambda gene:call_fitness(gene))

        print("generation:",generation," best fit:",call_fitness(population[0]))
        
        if call_fitness(population[0]) <= 0:
            found = True
            break
        
        new_generation = []
        
        index = int(POPULATION_SIZE *0.7)
        
        for _ in range(POPULATION_SIZE):
            
            xOverProb = random.random()
            
            parent1 = random.choice(population[:index]) 
            parent2 = random.choice(population[:index]) 
            
                
            if(xOverProb > 0.1):    
                child = crossOver(parent1,parent2)
                
            else:
                child = parent1
            
            mutateProb = random.random()
            if(mutateProb <= 0.01):
                mutate(child)
                
            new_generation.append(child) 
                
  
        population = new_generation 
        generation += 1

    if found:
        print("generation->",generation,"       ",
              population[0] ,  call_fitness(population[0]))

    duration = time.time() - start
    print ("minute:",(duration)//60)
    print("second:" ,(duration)%60)

        
