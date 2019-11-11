import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np
import turtle
import thread

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

POPULATION_SIZE = 50
TOURNAMENT_SIZE = 10
MAX_GENERATION = 1000
MAX_LIMIT = 5
METHOD = "uniform"

GRID_SIZE = 50
S = 5           # maximum number of antennas
K = 5           # antenna types
COSTS = [0, 0.5, 1, 3, 5, 7, 10, 12, 15, 20, 24]
RADIUS = [0, 2, 5, 8, 10, 15, 20, 25, 30, 32, 40]

COLORS = ['red', 'blue', 'green', 'purple', 'orange', 'black', "#006600", "#9999ff", "#ff5050", "#996633",
          "#006699", "#669999", "#993333"]

SCALE = 8

totalCoverPoints = 0


def drawAnswer():

    t = turtle.Turtle()
    t.pensize(4)
    t.forward(GRID_SIZE * SCALE)
    t.left(90)
    t.forward(GRID_SIZE * SCALE)
    t.left(90)
    t.forward(GRID_SIZE * SCALE)
    t.left(90)
    t.forward(GRID_SIZE * SCALE)
    t.left(90)

    for (a, x, y) in population[0].gene:
        t.color(COLORS[a])
        t.penup()
        t.setpos(x * SCALE, y * SCALE)
        t.pendown()
        t.circle(RADIUS[a] * SCALE)

    input()


def plotResult():
    plt.plot(list(range(generation)), best_fits, 'go-',
             label='best of generations', linewidth=2)
    plt.show()

    plt.plot(list(range(generation)), avg_fits, 'bo-',
             label='avg of generations', linewidth=2)
    plt.show()


def printHi():
    print('hi')


class Individual(object):

    def __init__(self, gene):
        self.gene = gene
        self.fitness = self.call_fitness()

    @classmethod
    def create_gnome(self):
        gene = []

        # select antenna number to init
        antNumber = random.choice(list(range(S))) + 1

        # randomly placing antenna in grid
        for _ in range(antNumber):
            x = random.choice(list(range(GRID_SIZE)))
            y = random.choice(list(range(GRID_SIZE)))

            chromosome = (random.choice(list(range(K))) + 1,
                          x, y)
            gene.append(chromosome)

        # set rest of antenna list as empty
        for _ in range(S-antNumber):
            gene.append((0, 0, 0))

        random.shuffle(gene)
        return gene

    @classmethod
    def tournomentSelection(self, population):
        best = None
        for _ in range(TOURNAMENT_SIZE):
            indiv = random.choice(population)
            if (best == None) or indiv.fitness > best.fitness:
                best = indiv

        return (best)

    @classmethod
    def rouletteWheelSelection(self, population):

        fitness_sum = 0
        parents = []
        min_fit = -100
        fitnesses = []

        for individual in population:
            fitnesses.append(individual.fitness)

        min_fit = abs(min(fitnesses))

        for i in range(len(fitnesses)):
            fitnesses[i] += min_fit + 10

        fitness_sum = sum(fitnesses)
        filled = 0

        for i in range(len(fitnesses)):

            fitnesses[i] = float(filled + fitnesses[i] / float(fitness_sum))
            filled = fitnesses[i]

        for j in range(2):
            pointer = random.random()

            for i in range(len(fitnesses)):

                if pointer < fitnesses[i]:
                    parents.append(population[i])
                    break

        return parents

    def mutate(self):
        for chrom in self.gene:
            mutateProb = random.random()
            (a, x, y) = chrom
            if(mutateProb <= 0.05):
                index = self.gene.index(chrom)
                mutateProb = random.random()

                # with equal probablity change one of triple index
                if(mutateProb <= 0.33):
                    a = random.choice(list(range(K))) + 1
                elif(mutateProb <= 0.66):
                    x = random.choice(list(range(GRID_SIZE)))
                else:
                    y = random.choice(list(range(GRID_SIZE)))

                self.gene[index] = (a, x, y)
        return

    def crossOver(self, parent2):

        child1 = []
        child2 = []

        if METHOD == "onePoint":
            size = len(self.gene)
            child1 = self.gene[:int(size/2)]
            for i in range(int(size/2), size):
                child1.append(parent2.gene[i])

            child2 = self.gene[int(size/2):]
            for i in range(int(size/2)):
                child2.append(parent2.gene[i])

        if METHOD == "uniform":
            for c1, c2 in zip(self.gene, parent2.gene):
                prob = random.random()
                if(prob > 0.5):
                    child1.append(c1)
                    child2.append(c2)

                else:
                    child1.append(c2)
                    child2.append(c1)

        if METHOD == "arithmetic":
            for c1, c2 in zip(self.gene, parent2.gene):
                bound = random.random()
                prob = random.random()
                if(prob > bound):
                    child1.append(c1)
                    child2.append(c2)

                else:
                    child1.append(c2)
                    child2.append(c1)

        return (Individual(child1), Individual(child2))

    def coverCount(self, index, total):
        coverdPoints = 0
        temp = points
        (a, aX, aY) = self.gene[index]
        if(a != 0):
            for point in temp:
                (x, y) = point
                distance = math.sqrt(abs(aX-x)**2 + abs(aY-y)**2)
                if distance <= RADIUS[a]:
                    temp = [p for p in temp if p != point]
                    coverdPoints += 1
        
        total += coverdPoints

    def u2(self):

        total = 0
        for i in range(len(self.gene)):
            thread.start_new_thread(self.coverCount, (i, total))

        print("total points:", total)

        return total

    def u(self):

        coverdPoints = 0
        temp = points

        # sort antennas by radius size
        self.gene = sorted(self.gene, reverse=True, key=lambda ch: ch[0])

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
        if generation == MAX_GENERATION or limit == MAX_LIMIT:
            break

        population = sorted(population, reverse=True, key=lambda x: x.fitness)

        if best_answer == population[0].fitness:
            limit += 1
        else:
            limit = 0
            best_answer = population[0].fitness

        best_fits.append(population[0].fitness)
        avg_fits.append(np.mean([p.fitness for p in population]))

        print("generation:", generation, " best fit:", population[0].fitness)

        besstParent = population[0]
        new_generation = []

        for _ in range(POPULATION_SIZE):

            # parent selection with tournomant selection
            parent1 = Individual.tournomentSelection(population)
            parent2 = Individual.tournomentSelection(population)

            (child1, child2) = parent1.crossOver(parent2)

            child1.mutate()
            child2.mutate()

            new_generation.append(child1)
            new_generation.append(child2)

        new_generation = sorted(
            new_generation, reverse=True, key=lambda x: x.fitness)

        new_generation.insert(len(new_generation)-1, besstParent)

        population = new_generation
        generation += 1

    generation -= 1
    print("generation : ", generation, "       ",
          population[0].gene[0:10],  population[0].fitness)

    plotResult()
    drawAnswer()

    duration = time.time() - start
    print("minute:", (duration)//60)
    print("second:", (duration) % 60)
