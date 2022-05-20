import random


class Item:
    """
    Holding a real item information
    """

    name: str
    benefit: int
    weight: int

    def __init__(self, n: str, b: int, w: int):
        self.benefit = b
        self.weight = w
        self.name = n


class GeneticAlgorithm:
    """
    Contains all the methods to solve the Genetic problem
    """

    max_weight: int
    """Maximum weight that knapsack can hold"""

    items: 'list[Item]'
    """Items you want to have it's maximum benefits"""

    population: 'list[list[int]]'
    """Your Genetic Algorithm population"""

    population_size: int
    """Size of your Genetic Algorithm population"""

    max_iterations: int
    """The count of maximum iterations you have before you reach the best benefit"""

    mutation_probability: float
    """The probability of applying mutation on a chromosome"""

    elite: float
    """Percentage represent how much to tack from the original population as the best of it"""

    def __init__(self, max_weight: int, items: 'list[Item]', population_size: int, max_iterations: int, mutation_probability: float, elite: float) -> None:
        """Pass all the input that the problem need to be solved"""

        self.max_weight = max_weight
        self.items = items
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.mutation_probability = mutation_probability
        self.elite = elite
        self.population = self.initialize(population_size)

    def initialize(self, population_size: 'int') -> 'list[list[int]]':
        """Give a random initial population to start with"""

        population: 'list[list[int]]' = []
        for _ in range(population_size):
            chromosome = [0 for _ in range(len(self.items))]
            for j in range(len(self.items)):
                chromosome[j] = random.randint(0, 1)
            population.append(chromosome)
        return population

    def fitness(self, chromosome: 'list[int]') -> int:
        """Calculate what is the givin benefit from the passed chromosome"""

        fitness = 0
        for i in range(len(self.items)):
            if(chromosome[i] == 1):
                fitness += self.items[i].benefit
        return fitness

    def mutation(self, chromosome: 'list[int]') -> 'list[int]':
        """Apply mutation on a chromosome"""

        pos = random.randint(0, len(chromosome)-1)

        return chromosome[0:pos] + \
            [1 if chromosome[pos] == 0 else 0]+chromosome[(pos+1):]

    def crossover(self, parent1: 'list[int]', parent2: 'list[int]') -> 'list[int]':
        """Crossover two parents to get a new child"""

        pos = random.randint(1, len(parent1)-2)
        return parent1[0:pos]+parent2[pos:]

    def acceptable(self, chromosome: 'list[int]') -> bool:
        """Check if the passed chromosome is acceptable depending on the maximum weight"""

        weight = 0
        for i in range(len(chromosome)):
            if(chromosome[i] == 1):
                weight += self.items[i].weight
        return weight <= self.max_weight

    def filter_duplicated(self, arr: list):
        """Filter the duplicated chromosomes to get better results when crossover two parents"""

        result = []
        for i in arr:
            if i not in result:
                result.append(i)
        return result

    def stringify_chromosome(self, chromosome: 'list[int]'):
        """Get the names of the items of this chromosome"""

        result = ""
        for i in range(len(chromosome)):
            if(chromosome[i] == 1):
                result += "%s, " % self.items[i].name
        return result

    def calc_weight(self, chromosome: 'list[int]'):
        """Get the sum of the items weights of this chromosome"""

        result = 0
        for i in range(len(chromosome)):
            if(chromosome[i] == 1):
                result += self.items[i].weight
        return result

    def solve(self):
        """To get the logs for solving this problem"""

        result = []

        result.append("max iterations = %d" % self.max_iterations)

        # filter by the criteria
        self.population = list(
            filter(lambda x: self.acceptable(x), self.population))

        for i in range(self.max_iterations):
            # filter the duplication
            self.population = self.filter_duplicated(self.population)

            # get every chromosome score
            chromosomes_with_score = [(self.fitness(v), v)
                                      for v in self.population]

            # sort them by the best
            chromosomes_with_score.sort(reverse=True)
            ranked_chromosomes = [v for (_, v) in chromosomes_with_score]

            # the amount that we pick from the population
            top_elite = int(self.elite*(len(ranked_chromosomes)-1))

            self.population = ranked_chromosomes[0:top_elite]

            while len(self.population) < self.population_size:
                if random.random() < self.mutation_probability:

                    c = random.randint(0, top_elite)

                    # apply mutation on a random chromosome
                    self.population.append(self.mutation(
                        ranked_chromosomes[c]))
                else:
                    c1 = random.randint(0, top_elite)
                    c2 = random.randint(0, top_elite)

                    # crossover on a random two parents
                    self.population.append(self.crossover(
                        ranked_chromosomes[c1], ranked_chromosomes[c2]))

            # filter by the criteria
            self.population = list(filter(
                lambda x: self.acceptable(x), self.population))

            # get the best score of this iteration
            result.append("best fitness score in iteration (%d) is (%d) and the weight is (%d) for items %s" %
                          (i+1, chromosomes_with_score[0][0], self.calc_weight(chromosomes_with_score[0][1]),
                           self.stringify_chromosome(chromosomes_with_score[0][1]))
                          )

        # return the logs
        return result
