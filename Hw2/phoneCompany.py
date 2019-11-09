import random
import time
import math
# import matplotlib.pyplot as plt
# import numpy as np

start = time.time()
generation = 1
found = False
population = []
best_fits = []
avg_fits = []
points = []

POPULATION_SIZE = 100
TOURNAMENT_SIZE = 10
MAX_GENERATION = 1000
METHOD = "onePoint"

GRID_SIZE = 4
# maximum number of antennas
S = 4
# anten types
K = 4
COSTS = [0, 1, 2, 3]
RADIUS = [0, 1, 2, 3]


# u(x) = number of covered points in grid for individual x
# p(x) = set of installed antennas for individual x
# t(j) = type of antenna j

# Tournament selection

# Random initialization of each integer value. Only valid triples.
# 5% mutation probability. Randomly set one of the elements of the triple.

# One-point crossover

# 1% elitism. Replace worst offspring with best parent in the next generation.


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
        tournament = []
        for _ in range(TOURNAMENT_SIZE):
            tournament.append(random.choice(population))

        tournament = sorted(tournament, reverse=True,
                            key=lambda ch: ch.fitness)

        return (tournament[0], tournament[1])

    def mutate(self):
        # for chrom in self.chromosome:
        #     mutateProb = random.random()
        #     if(mutateProb <= 0.005):
        #         index = self.chromosome.index(chrom)
        #         action = random.choice(list(ACTION_LIST))
        #         self.chromosome[index] = action
        return

    def crossOver(self, parent2):

        # child = []
        # if METHOD == "uniform":
        #     for c1, c2 in zip(self.chromosome, parent2.chromosome):
        #         prob = random.random()
        #         if(prob > 0.5):
        #             child.append(c1)
        #         else:
        #             child.append(c2)

        # if METHOD == "onePoint":
        #     size = len(self.chromosome)
        #     child = self.chromosome[:size/2]
        #     for i in range(size/2, size):
        #         child.append(parent2.chromosome[i])

        # return Individual(child)

        return

    def u(self):

        coverdPoints = 0
        temp = points

        self.gene = sorted(self.gene, reverse=True, key=lambda ch: ch[0])

        print("gene after sort:", self.gene)

        for (a, aX, aY) in self.gene:
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
        print("fit:", fit)
        return fit


if __name__ == '__main__':

    # inital points
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            points.append((x, y))

    gene = [(2, 0, 0), (2, 3, 3), (0, 0, 0), (0, 0, 0)]
    indiv = Individual(gene)

    # # First Generation
    # for _ in range(POPULATION_SIZE):
    #     gnome = Individual.create_gnome()
    #     indiv = Individual(gnome)
    #     population.append(indiv)

    # while not found:

    #     # max generation terminate condition
    #     if generation > MAX_GENERATION:
    #         print("---- can't find ----")
    #         break

    #     population = sorted(population, reverse=True, key=lambda x: x.fitness)

    #     best_fits.append(population[0].fitness)
    #     avg_fits.append(np.mean([p.fitness for p in population]))

    #     print("generation:", generation, " best fit:", population[0].fitness)

    #     if population[0].fitness == len(CAN_POS) * 10:
    #         found = True
    #         break

    #     new_generation = []

    #     # selection pressure with coefficient 70% of best
    #     index = int(POPULATION_SIZE * 0.7)

    #     for _ in range(POPULATION_SIZE):

    #         # parent selection with Roulette Wheel method
    #         (parent1, parent2) = Individual.rouletteWheelSelection(
    #             population[:index])
    #         child = parent1.crossOver(parent2)

    #         child.mutate()

    #         new_generation.append(child)

    #     population = new_generation
    #     generation += 1

    # if found:
    #     print("generation : ", generation, "       ",
    #           population[0].chromosome[0:10],  population[0].fitness)
    #     plotResult()

    # duration = time.time() - start
    # print("minute:", (duration)//60)
    # print("second:", (duration) % 60)
