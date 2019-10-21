import random
import time
import math

start = time.time()
generation = 1
found = False
population = []
strg_fitness = 0

POPULATION_SIZE = 4
MAX_NUMBER = 10
ACTION_LIST = ["n","s","e","w","r","st","b"]
GRID_WIDTH = 10
CURR_LOC = (0,0)
CAN_POS = [(0, 0), (1, 1), (2, 2), (3, 3), 
          (4, 4), (5, 5), (6, 6), (7, 7),
          (8, 8), (9, 9), (10, 10)]

METHOD = "onePoint"


def create_gnome():
    gene = []
    
    for i in range(1, MAX_NUMBER + 1):
        
        action = random.choice(list(ACTION_LIST))
        gene.append(action)

    return gene
    
def call_fitness(gene):
    global CURR_LOC
    fitness = 0
    
    (x,y) = CURR_LOC
    for action in gene :
            
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
        elif action == "b" and CURR_LOC in CAN_POS:
            CAN_POS.remove(CURR_LOC)
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
        
        # print ("\n")
        # print("before",CURR_LOC)
        
        # check if hit the wall
        if x >10 or x<0 or y>10 or y<0:
            fitness -=5
            x = max(0,x)
            y = max(0,x)
            
        
        CURR_LOC = (x,y)
        
        # print("action:",action,"fitness :",fitness,"after",CURR_LOC)
         
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
    
    fitness_sum = 0
    members = []
    parents = []
    min_fit = 0
    for individual in population:
        fitness = call_fitness(individual)
        if fitness <min_fit:
            min_fit = fitness
        fitness_sum +=fitness
        members.append((individual,fitness))
    
    print("min_fit",min_fit)
    min_fit =- min_fit
    fitness_sum += min_fit * len(population)
    print("fitness_sum",fitness_sum)
    filled = 0
        
    for member in members:
        (individual,fitness) = member
        fitness = min_fit + filled + fitness /fitness_sum
        filled = fitness
        
        member = (individual , fitness)
    
    
    print("members",members)
    
    for i in range(2):
        pointer = random.random()
        
        print("pointer",pointer)
        
        for member in members:
            (individual,fitness) = member
            
            if pointer < fitness:
                print("selected",individual)
                parents.append(individual)
                break
                
    return parents

if __name__ == '__main__':


    for i in range(4):
        population.append(create_gnome())

    parents = rouletteWheelSelection(population)
    
             
    # print("First Position : ",CURR_LOC)
    # # First Generation
    # for i in range(0, POPULATION_SIZE):
    #     population.append(create_gnome())

    # population[0] = ['b', 'r', 'r', 's', 'b', 'e', 'b', 'n', 'b', 'w','b','r','b']
    # print(population[0])
    
    # print("total fitness:",call_fitness(population[0]))
    
    
    # while not found:

    #     population = sorted(population, key=lambda gene:call_fitness(gene))

    #     print("generation:",generation," best fit:",call_fitness(population[0]))
        
    #     if call_fitness(population[0]) <= 0:
    #         found = True
    #         break
        
    #     new_generation = []
        
    #     index = int(POPULATION_SIZE *0.4)
        
    #     for _ in range(POPULATION_SIZE):
            
    #         (parent1 , parent2) = rouletteWheelSelection(population)
    #         child = crossOver(parent1,parent2)
            
    #         mutateProb = random.random()
    #         if(mutateProb <= 0.5):
    #             mutate(child)
                
    #         new_generation.append(child) 
                
  
    #     population = new_generation 
    #     generation += 1


    # print("generation->",generation,"       ",population[0] ,  call_fitness(population[0]))

    # duration = time.time() - start
    # print ("minute:",(duration)//60)
    # print("second:" ,(duration)%60)

        
