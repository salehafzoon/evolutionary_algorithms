import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np

start = time.time()
generation = 1
found = False
population = []
POPULATION_SIZE = 400
MAX_NUMBER = 20
GRID_WIDTH = 7
MAX_GENERATION = 4000
METHOD = "uniform"
avg_fits = []
best_fits = []
target = [(2, 3), (2, 2), (2, 1), (3, 1),
          (4, 1), (4, 2), (4, 3), (5, 1),
          (6, 1), (6, 2), (6, 3), (2, 7),
          (2, 6), (2, 5), (3, 5), (4, 5),
          (5, 5), (6, 5), (6, 6), (6, 7)]


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
    # Euclidean distance between gene and target
    fitness = 0
    for (gx, gy), (tx, ty) in zip(gene, target):
        fitness += math.sqrt(abs(gx - tx) + abs(gy - ty))

    return fitness


def crossOver(parent1, parent2):
    child = []
    if METHOD == "uniform":
        for c1, c2 in zip(parent1, parent2):
            prob = random.random()
            if(prob > 0.5):
                child.append(c1)
            else:
                child.append(c2)

    if METHOD == "onePoint":
        size = len(parent1)
        child = parent1[:size/2]
        for i in range(size/2, size):
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
            child[index] = (x, y)

    return child


def plotResult():
    plt.plot(list(range(generation)), best_fits,'go-', label='best of generations', linewidth=2)
    plt.show()

    plt.plot(list(range(generation)), avg_fits,'bo-', label='avg of generations', linewidth=2)
    plt.show()


if __name__ == '__main__':


    # First Generation
    for i in range(0, POPULATION_SIZE):
        population.append(create_gnome())

    while not found:

        # max generation terminate condition
        if generation > MAX_GENERATION:
            print("---- can't find ----")
            break

        # sort generation for parent selection
        population = sorted(population, key=lambda gene: call_fitness(gene))

        best_fits.append(call_fitness(population[0]))
        avg_fits.append(np.mean([call_fitness(p) for p in population]))

        print("generation:", generation, " best fit:",
              call_fitness(population[0]))

        if call_fitness(population[0]) <= 0:
            found = True
            break

        new_generation = []

        # selection pressure with coefficient 70% of best
        index = int(POPULATION_SIZE*0.7)

        for _ in range(POPULATION_SIZE):

            xOverProb = random.random()

            parent1 = random.choice(population[:index])
            parent2 = random.choice(population[:index])

            # cross overing with probability 90%
            if(xOverProb > 0.1):
                child = crossOver(parent1, parent2)

            else:
                child = parent1

            # muteting with probability 0.1%
            mutateProb = random.random()
            if(mutateProb <= 0.001):
                mutate(child)

            new_generation.append(child)

        population = new_generation
        generation += 1

    if found:

        print("generation : ", generation,
              population[0], call_fitness(population[0]))
        plotResult()
        
    duration = time.time() - start
    print("minute:", (duration)//60)
    print("second:", (duration) % 60)
    