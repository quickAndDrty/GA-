import random
import operator
import math

class Knapsack():


    def __init__(self, n, values, we, w):
        self.n = n  #objects
        self.values = values
        self.we = we
        #self.x = []
        self.w = w
        self.N = 0  #population

    def readFromFile(self):
        #f = open("knapsack20.txt", "r")
        f = open("knapsack200.txt", "r")
        self.n = f.readline()
        self.values = []
        self.we = []
        for i in range(1, int(self.n) + 1):
            line = f.readline()
            elements = line.split()
            self.values.append(int(elements[1]))
            self.we.append(int(elements[2]))
        self.w = f.readline()

    def fitness(self,v):
        s = 0
        for i in range(1, int(self.n)+1):
            s = s + v[i-1]*self.values[i-1]
        return s

    def validate(self,v):
        s = 0
        for i in range (1, int(self.n)+1):
            s = s + v[i-1]*self.we[i-1]
        if (s <= int(self.w)):
            return 1
        return 0

    def randomChromosome(self):
        ch = []
        for i in range(int(self.n)):
            ch.append(random.randint(0,1))
        while (self.validate(ch) == 0):
            ch.clear()
            for i in range(int(self.n)):
                ch.append(random.randint(0, 1))
        return ch

    def randomPopulation(self, N):
        chromosomes = []
        for i in range (0, N):
            chromosomes.append(self.randomChromosome())
        return chromosomes

    def tournamentSelection(self, population):
    #choose best chromosome from a population, trying k random values
    # k < N
        k = 10
        bestCanditate = 'None'
        bestValue = 0
        for i in range (k):
            canditate = population[random.randint(0, int(self.N) -1 )]
            if (self.fitness(canditate) > bestValue and self.validate(canditate) == 1):
                bestValue = self.fitness(canditate)
                bestCanditate = canditate[:]
        return bestCanditate

    def onePointXover(self, parent1, parent2):
        # choose a random index
        threshold = random.randint(1, len(parent1) - 1)
        # print(threshold)
        cpy1 = parent1[threshold:]
        cpy2 = parent2[threshold:]
        parent1 = parent1[:threshold]
        parent2 = parent2[:threshold]
        parent1.extend(cpy2)
        parent2.extend(cpy1)

        return parent1, parent2

    def strongMutation(self, child, pm):
        q = random.random() #thershold
        for i in range (len(child)):
            if ( pm > q):
                child[i] = (child[i] + 1)%2

        return child

    def weakMutation(self, child, pm):
        q = random.random()  # thershold
        for i in range(len(child)):
            if (pm > q):
                child[i] = random.randint(0,1)

        return child

    def sortPopulation(self, population):
        for i in range(0, len(population) -1):
            for j in range (i + 1, len(population)):
                if (self.fitness(population[i]) < self.fitness(population[j])):
                    tmp = population[i]
                    population[i] = population[j]
                    population[j] = tmp[:]
        return population

    def sumFitness(self, values):
        sum = 0
        for i in values:
            sum += i
        return sum

    def run(self, N, M):
        t = 0 #current generation
        self.N = N #set current max population
        population = self.randomPopulation(N)
        print(population)
        for i in population:
            print(self.fitness(i))
        print('\n')

        best = 0
        avg = 0

        while ( t < M):
            #choose parents
            parents = []
            for i in range (int(int(self.N)/2)):
                parents.append(self.tournamentSelection(population))

            #crossover
            children = []
            for i in range(0, int(int(self.N) / 2) - 1, 2):
                child1, child2 = self.onePointXover(parents[i], parents[i + 1])
                children.append(child1)
                children.append(child2)

            #mutation
            mutations = []
            #set mutation probability
            pm = 0.15
            for i in range(int(int(self.N) / 2) - 1):
                mut = self.strongMutation(children[i], pm)
                if (self.validate(mut) == 1):
                    mutations.append(mut)
            #create a new canditate population from new chromosomes
            newPop = []
            for p in parents:
                newPop.append(p)
            for m in mutations:
                newPop.append(m)

            #sort population based on fitness
            sortPop = self.sortPopulation(population)

            nextGen = sortPop[:math.ceil(N/4)]
            #print(nextGen)
            nextGen.extend(newPop)
            #print(nextGen)

            nextGen = self.sortPopulation(nextGen)

            population = nextGen[:N]
            latestFitness = []
            for i in population:
                latestFitness.append(self.fitness(i))
            #print(population)
            #print(latestFitness, '\n')

            if (best < latestFitness[0]):
                best = latestFitness[0]
            avg = avg + self.sumFitness(latestFitness)/N

            t = t + 1

        print("best ", best)
        print("avg ", avg/M)

