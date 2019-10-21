import random 
import time
  
POPULATION_SIZE = 4
QUEEN_NUM = 8

maxF = 0
counter = 0

class Individual(object): 
  
    def __init__(self, chromosome): 
        self.chromosome = chromosome  
        self.fitness = self.cal_fitness() 
  
    @classmethod
    def mutated_genes(self): 

        GENES = set(range(1,QUEEN_NUM+1)) 
        gene = random.choice(list(GENES)) 
        return gene 
  
    @classmethod
    def create_gnome(self): 

        gene = []
        GENES = set(range(1,QUEEN_NUM+1))
        while len(GENES)>0:
            i = random.choice(list(GENES))
            gene.append(i)
            GENES.remove(i)

        return gene
  
    def mate(self, par2): 

        child_chromosome = [] 
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):     
  
            GENES = list(range(1,QUEEN_NUM+1))
                
            prob = random.random() 
  
            if prob < 0.40 and gp1 not in child_chromosome: 
                child_chromosome.append(gp1) 
                GENES.remove(gp1)
  
            elif prob < 0.80 and gp2 not in child_chromosome: 
                child_chromosome.append(gp2)
                GENES.remove(gp2)
  
            else:

                child_chromosome.append( random.choice( GENES ) )

        return Individual(child_chromosome) 
  
    def cal_fitness(self): 
        global counter
        global maxF
        
        counter +=1

        fitness = 0
        for row in range(len(self.chromosome)):
            fitness +=colision_count(self.chromosome,row)

        if fitness> maxF:
            maxF = fitness
        print(maxF)
        return fitness 

def colision_count(board, row): 

    colisions = 0

    for i in range(row+1, len(board)): 
        if board[i] == board[row]:
            colisions+=1
        else:
            dif_r = abs(row - i)
            dif_c = abs(board[row] - board[i])

            if dif_c == dif_r:
                colisions +=1

    return colisions

  
if __name__ == '__main__': 

    QUEEN_NUM = int(input('QUEEN_NUM:'))
    POPULATION_SIZE = int(input('POPULATION_SIZE :'))
    
    start = time.time()
    
    generation = 1
  
    found = False
    population = [] 
  
    #First Generation
    for _ in range(POPULATION_SIZE): 
        gnome = Individual.create_gnome() 
        indiv = Individual(gnome)
        if indiv not in population:
            population.append(indiv) 

    while not found: 
  
        population = sorted(population, key = lambda x:x.fitness) 
  
        if population[0].fitness <= 0: 
            found = True
            break
  
        new_generation = [] 
  
        s = int((10*POPULATION_SIZE)/100) 
        new_generation.extend(population[:s]) 
  
        s = int((90*POPULATION_SIZE)/100) 
        for _ in range(s): 
            index = int(POPULATION_SIZE/2)
            parent1 = random.choice(population[:index]) 
            parent2 = random.choice(population[:index]) 
            child = parent1.mate(parent2) 
            new_generation.append(child) 
  
        population = new_generation 
  
        # print("generation->",generation," \t",population[0].chromosome ,  population[0].fitness)
  
        generation += 1

    print("generation->",generation," \t",population[0].chromosome ,  population[0].fitness)

    duration = time.time() - start
    print ("minute:",(duration)//60)
    print("second:" ,(duration)%60)

    print("counter:" , counter)

  