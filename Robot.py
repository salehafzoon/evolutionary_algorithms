import random
import time
import math

start = time.time()
generation = 1
found = False
population = []
fitness = 0

POPULATION_SIZE = 4
MAX_NUMBER = 10
ACTION_LIST = ["n","s","e","w","r","st","b"]
GRID_WIDTH = 10
CURR_LOC = (0,0)
CAN_POS = [(0, 0), (1, 1), (2, 2), (3, 3), 
          (4, 4), (5, 5), (6, 6), (7, 7),
          (8, 8), (9, 9), (10, 10)]

METHOD = "onePoint"

# target = [(1,1),(2,2),(3,3),(4,4)]


def create_gnome():
    gene = []
    
    for i in range(1, MAX_NUMBER + 1):
        
        action = random.choice(list(ACTION_LIST))
        gene.append(action)

    return gene

def check_wall_or_can(action):
    global CURR_LOC
    global fitness
    
    (x,y) = CURR_LOC
    if action =="n":
        y +=1
    elif action =="s":
        y-=1
    elif action == "e":
        x+=1
    elif action == "w":
        x-=1
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
    
    if x >10 or x<0 or y>10 or y<0:
        fitness -=5
    else:
        CURR_LOC = (x,y)
        if (x,y) in CAN_POS:
            fitness +=10     
            
def call_fitness(gene):
    fitness = 0
    for action in gene :
        
        if action =="b":
            if CURR_LOC in CAN_POS:
                fitness +=10
            else:
                fitness -=1
        elif action =="st":
            pass
        else:
            check_wall_or_can(action)
            
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
    
    action = random.choice(list(ACTION_LIST))
    child[index] = action
            
    return child
    
def rouletteWheelSelection(population):
    parents = (0,1)
    
    return parents

if __name__ == '__main__':

    # First Generation
    for i in range(0, POPULATION_SIZE):
        population.append(create_gnome())

    # print(population)
    while not found:

        population = sorted(population, key=lambda gene:call_fitness(gene))

        print("generation:",generation," best fit:",call_fitness(population[0]))
        
        if call_fitness(population[0]) <= 0:
            found = True
            break
        
        new_generation = []
        
        index = int(POPULATION_SIZE *0.4)
        
        for _ in range(POPULATION_SIZE):
            
            (parent1 , parent2) = rouletteWheelSelection(population)
            child = crossOver(parent1,parent2)
            
            mutateProb = random.random()
            if(mutateProb <= 0.5):
                mutate(child)
                
            new_generation.append(child) 
                
  
        population = new_generation 
        generation += 1


    print("generation->",generation,"       ",population[0] ,  call_fitness(population[0]))

    duration = time.time() - start
    print ("minute:",(duration)//60)
    print("second:" ,(duration)%60)

        
