import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np

start = time.time()
generation = 1
found = False
population = []
besstParent = None
best_fits = []
avg_fits = []
points = []
best_answer = 0
limit = 0

POPULATION_SIZE = 100
TOURNAMENT_SIZE = 10
MAX_GENERATION = 1000
MAX_LIMIT = 10
METHOD = "onePoint"

GRID_SIZE = 50
S = 10           # maximum number of antennas
K = 3           # anten types
COSTS = [0, 10, 20, 30]
RADIUS = [0, 10, 20, 30]


class Individual(object):

    def __init__(self, gene):
        self.gene = gene
        self.fitness = self.call_fitness()

    @classmethod
    def create_gnome(self):
        gene = []

        # initail antens
        antNumber = random.choice(list(range(S))) + 1
        for _ in range(antNumber):
            x = random.choice(list(range(GRID_SIZE)))
            y = random.choice(list(range(GRID_SIZE)))

            chromosome = (random.choice(list(range(K))) + 1,
                          x, y)
            gene.append(chromosome)

        # set rest of anten list as empty
        for _ in range(S-antNumber):
            gene.append((0, 0, 0))

        return gene

    @classmethod
    def tournomentSelection(self, population):
        best = None
        for _ in range(TOURNAMENT_SIZE):
            indiv = random.choice(population)
            if (best == None) or indiv.fitness > best.fitness:
                best = indiv

        return (best)

    def mutate(self):
        for chrom in self.gene:
            mutateProb = random.random()
            (a, x, y) = chrom
            if(mutateProb <= 0.05):
                index = self.gene.index(chrom)
                mutateProb = random.random()
                if(mutateProb <= 0.33):
                    a = random.choice(list(range(K))) + 1
                elif(mutateProb <= 0.66):
                    x = random.choice(list(range(GRID_SIZE)))
                else:
                    y = random.choice(list(range(GRID_SIZE)))

                self.gene[index] = (a, x, y)
        return

    def crossOver(self, parent2):

        child = []
        if METHOD == "uniform":
            for c1, c2 in zip(self.gene, parent2.gene):
                prob = random.random()
                if(prob > 0.5):
                    child.append(c1)
                else:
                    child.append(c2)

        if METHOD == "onePoint":
            size = len(self.gene)
            child = self.gene[:int(size/2)]
            for i in range(int(size/2), size):
                child.append(parent2.gene[i])

        return Individual(child)

    def u(self):

        coverdPoints = 0
        temp = points

        self.gene = sorted(self.gene, reverse=True, key=lambda ch: ch[0])

        # print("gene after sort:", self.gene)

        for (a, aX, aY) in self.gene:
            if(a != 0):
                for point in temp:
                    (x, y) = point
                    distance = math.sqrt(abs(aX-x)**2 + abs(aY-y)**2)
                    if distance <= RADIUS[a]:
                        temp = [p for p in temp if p != point]
                        coverdPoints += 1

        return coverdPoints

    def call_fitness(self):
        totalCost = 0
        for (a, x, y) in self.gene:
            totalCost += COSTS[a]

        fit = self.u() - totalCost
        # print("fit:", fit)
        return fit


if __name__ == '__main__':

    # inital points
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            points.append((x, y))


    # First Generation
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        indiv = Individual(gnome)
        population.append(indiv)

    while not found:

        # max generation terminate condition
        if generation > MAX_GENERATION or limit == MAX_LIMIT:
            break

        population = sorted(population, reverse=True, key=lambda x: x.fitness)

        if best_answer == population[0].fitness:
            limit += 1
        else:
            best_answer = population[0].fitness

        best_fits.append(population[0].fitness)
        avg_fits.append(np.mean([p.fitness for p in population]))

        print("generation:", generation, " best fit:", population[0].fitness)

        # solution founded condition

        besstParent = population[0]
        new_generation = []

        for _ in range(POPULATION_SIZE):

            # parent selection with Roulette Wheel method
            parent1 = Individual.tournomentSelection(population)
            parent2 = Individual.tournomentSelection(population)

            child = parent1.crossOver(parent2)

            child.mutate()

            new_generation.append(child)

        new_generation = sorted(
            new_generation, reverse=True, key=lambda x: x.fitness)

        new_generation.insert(len(new_generation)-1, besstParent)

        population = new_generation
        generation += 1

    print("generation : ", generation-1, "       ",
          population[0].gene[0:10],  population[0].fitness)

    # plotResult()

    duration = time.time() - start
    print("minute:", (duration)//60)
    print("second:", (duration) % 60)
