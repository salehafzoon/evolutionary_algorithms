import random
import time
import math

start = time.time()
generation = 1
found = False
population = []
POPULATION_SIZE = 1000
METHOD = "uniform"
target = "salehafzoon9432176"


def create_gnome():
    gene = []
    possible = set(range(1, GRID_WIDTH + 1))

    for i in range(1, MAX_NUMBER + 1):
        coll = True
        while(coll):
            coll = False
            x = random.choice(list(possible))
            y = random.choice(list(possible))

            for (gx, gy) in gene:
                if (gx == x and gy == y):
                    coll = True
            if coll == False:
                gene.append((x, y))

    return gene

def call_fitness(gene):
    fitness = 0
    for (gx, gy), (tx, ty) in zip(gene, target):
        fitness += math.sqrt(abs(gx - tx) + abs(gy - ty))

    return fitness

def crossOver(parent1, parent2):
    child = []
    if METHOD == "uniform":
        for c1 , c2 in zip(parent1 , parent2):
            prob = random.random()
            if(prob > 0.5):
                child.append(c1)
            else:
                child.append(c2)
    
    if METHOD == "onePoint":
        size = len(parent1)
        child = parent1[:size/2]
        for i in range(size/2,size):
            child.append(parent2[i])
        
    return child
        
def mutate(child):
    chrom = random.choice(child)
    index = child.index(chrom)
    
    possible = set(range(1, GRID_WIDTH + 1))
    coll = True
    while(coll):
        coll = False
        x = random.choice(list(possible))
        y = random.choice(list(possible))

        for (gx, gy) in child:
            if (gx == x and gy == y):
                coll = True
        if coll == False:
            child[index] = (x,y)
            
    return child
    

if __name__ == '__main__':

    # First Generation
    for i in range(0, POPULATION_SIZE):
        population.append(create_gnome())

    while not found:

        population = sorted(population, key=lambda gene:call_fitness(gene))

        print("generation:",generation," best fit:",call_fitness(population[0]))
        
        if call_fitness(population[0]) <= 0:
            found = True
            break
        
        new_generation = []
        
        index = int(POPULATION_SIZE *0.4)
        
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


    print("generation->",generation,"       ",population[0] ,  call_fitness(population[0]))

    duration = time.time() - start
    print ("minute:",(duration)//60)
    print("second:" ,(duration)%60)

        
