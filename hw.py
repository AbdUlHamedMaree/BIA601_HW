from json import JSONEncoder
import json
from pty import fork
import random
from typing import Callable, Type


class Item:
    name: str
    benefit: int
    weight: int

    def __init__(self, n: str, b: int, w: int):
        self.benefit = b
        self.weight = w
        self.name = n


# items = [Item('1', 5, 7), Item('2', 8, 8), Item('3', 3, 4),
#          Item('4', 2, 10), Item('5', 7, 4), Item('6', 9, 6), Item('7', 4, 4)]
# max_size = 22


class GeneticAlgorithm:
    max_weight: int
    items: 'list[Item]'
    population: 'list[list[int]]'
    population_size: int
    max_iterations: int
    mutation_probability: float
    elite: float

    def __init__(self, max_weight: int, items: 'list[Item]', population_size: int, max_iterations: int, mutation_probability: float, elite: float):
        self.max_weight = max_weight
        self.items = items
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.mutation_probability = mutation_probability
        self.elite = elite
        self.population = self.initialize(population_size)

    def fitness(self, individual: 'list[int]') -> int:
        fitness = 0
        for i in range(len(self.items)):
            if(individual[i] == 1):
                fitness += self.items[i].benefit
        return fitness

    def initialize(self, population_size: 'int') -> 'list[list[int]]':
        population: 'list[list[int]]' = []
        for _ in range(population_size):
            individual = [0 for _ in range(len(self.items))]
            for j in range(len(self.items)):
                individual[j] = random.randint(0, 1)
            population.append(individual)
        return population

    def mutation(self, individual: 'list[int]') -> 'list[int]':
        pos = random.randint(0, len(individual)-1)

        return individual[0:pos] + \
            [1 if individual[pos] == 0 else 0]+individual[(pos+1):]

    def crossover(self, parent1: 'list[int]', parent2: 'list[int]') -> 'list[int]':
        pos = random.randint(1, len(parent1)-2)
        return parent1[0:pos]+parent2[pos:]

    def acceptable(self, individual: 'list[int]') -> bool:
        weight = 0
        for i in range(len(individual)):
            if(individual[i] == 1):
                weight += self.items[i].weight
        return weight <= self.max_weight

    def filter_duplicated(self, arr: list):
        result = []
        for i in arr:
            if i not in result:
                result.append(i)
        return result

    def stringify_individual(self, individual: 'list[int]'):
        result = ""
        for i in range(len(individual)):
            if(individual[i] == 1):
                result += "%s, " % self.items[i].name
        return result

    def calc_weight(self, individual: 'list[int]'):
        result = 0
        for i in range(len(individual)):
            if(individual[i] == 1):
                result += self.items[i].weight
        return result

    def solve(self):
        result = []
        result.append("max iterations =%d" % self.max_iterations)
        # How many winners from each generation?

        self.population = list(
            filter(lambda x: self.acceptable(x), self.population))

        # Main loop
        for i in range(self.max_iterations):
            self.population = self.filter_duplicated(self.population)

            individuals_with_score = [(self.fitness(v), v)
                                      for v in self.population]
            individuals_with_score.sort(reverse=True)
            ranked_individuals = [v for (_, v) in individuals_with_score]

            top_elite = int(self.elite*(len(ranked_individuals)-1))
            # Start with the pure winners
            self.population = ranked_individuals[0:top_elite]
            # Add mutated and bred forms of the winners
            while len(self.population) < self.population_size:
                if random.random() < self.mutation_probability:

                    # Mutation
                    c = random.randint(0, top_elite)

                    self.population.append(self.mutation(
                        ranked_individuals[c]))
                else:
                    c1 = random.randint(0, top_elite)
                    c2 = random.randint(0, top_elite)

                    self.population.append(self.crossover(
                        ranked_individuals[c1], ranked_individuals[c2]))
            self.population = list(filter(
                lambda x: self.acceptable(x), self.population))
            # Print current best score
            result.append("best fitness score in iteration (%d) is (%d) and the weight is (%d) for items %s" %
                          (i, individuals_with_score[0][0], self.calc_weight(individuals_with_score[0][1]),
                           self.stringify_individual(individuals_with_score[0][1]))
                          )
            # returns the best solution
        return result
