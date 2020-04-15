from platypus import Mutation, copy, Binary, random, Variator
import numpy as np

"""
Operator implementations are not final.
"""


class Encoding2BitFlip(Mutation):

    def __init__(self, bit_change_prob=0.002, gs_sc_change_prob=0.002, time_change_prob=0.01):
        super(Encoding2BitFlip, self).__init__()

        self.bit_change_prob = bit_change_prob
        self.gs_sc_change_prob = gs_sc_change_prob
        self.time_change_prob = time_change_prob

    def mutate(self, parent):
        result = copy.deepcopy(parent)
        problem = result.problem

        for i in range(problem.nvars):
            if i % 5 == 0:  # Indicator bit
                if random.uniform(0.0, 1.0) <= self.bit_change_prob:
                    result.variables[i][0] = not result.variables[i][0]
                    result.evaluated = False

            if i % 5 == 1 or i % 5 == 2:  # SC or GS
                for j in range(problem.types[i].nbits):
                    if random.uniform(0.0, 1.0) <= self.gs_sc_change_prob:
                        result.variables[i][j] = not result.variables[i][j]
                        result.evaluated = False

            if i % 5 == 3 or i % 5 == 4:
                if random.uniform(0.0, 1.0) <= self.time_change_prob:
                    v = problem.types[i].decode(result.variables[i])
                    v += int(np.random.normal(loc=0.0, scale=100.0))
                    t = problem.types[i]
                    v = max(0, min(v, t.max_value))
                    result.variables[i] = problem.types[i].encode(v)
                    result.evaluated = False

        return result


class Encoding2Crossover(Variator):

    def __init__(self, probability=1.0):
        super(Encoding2Crossover, self).__init__(2)
        self.probability = probability

    def evolve(self, parents):
        parent1 = copy.deepcopy(parents[0])
        parent2 = copy.deepcopy(parents[1])
        result1 = copy.deepcopy(parent1)
        result2 = copy.deepcopy(parent2)
        problem = result1.problem

        if random.uniform(0.0, 1.0) <= self.probability:
            for i in range(int(problem.nvars / 5)):
                v11 = parent1.variables[5 * i]
                v12 = parent2.variables[5 * i]

                v21 = parent1.variables[5 * i + 1]
                v22 = parent2.variables[5 * i + 1]

                v31 = parent1.variables[5 * i + 2]
                v32 = parent2.variables[5 * i + 2]

                v41 = parent1.variables[5 * i + 3]
                v42 = parent2.variables[5 * i + 3]

                v51 = parent1.variables[5 * i + 4]
                v52 = parent2.variables[5 * i + 4]

                if random.uniform(0.0, 1.0) <= 0.2:
                    result1.variables[5 * i] = v11
                    result2.variables[5 * i] = v12

                    result1.variables[5 * i + 1] = v21
                    result2.variables[5 * i + 1] = v22

                    result1.variables[5 * i + 2] = v31
                    result2.variables[5 * i + 2] = v32

                    result1.variables[5 * i + 3] = v41
                    result2.variables[5 * i + 3] = v42

                    result1.variables[5 * i + 4] = v51
                    result2.variables[5 * i + 4] = v52
                else:
                    result1.variables[5 * i] = v12
                    result2.variables[5 * i] = v11

                    result1.variables[5 * i + 1] = v22
                    result2.variables[5 * i + 1] = v21

                    result1.variables[5 * i + 2] = v32
                    result2.variables[5 * i + 2] = v31

                    result1.variables[5 * i + 3] = v42
                    result2.variables[5 * i + 3] = v41

                    result1.variables[5 * i + 4] = v52
                    result2.variables[5 * i + 4] = v51
        result1.evaluated = False
        result2.evaluated = False

        return [result1, result2]


# class Encoding3Crossover(Variator):
#    def __init__(self, probability=1.0):
#        super(Encoding3Crossover, self).__init__(2)
#        self.probability = probability
#
#    def evolve(self, parents):
#        result1 = copy.deepcopy(parents[0])
#        result2 = copy.deepcopy(parents[1])
#        problem = result1.problem
#
#        if random.uniform(0.0, 1.0) <= self.probability:
#            pass
#
#        if random.uniform(0.0, 1.0) <= self.probability:
#            for i in range(problem.nvars):
#                if isinstance(problem.types[i], Binary):
#                    for j in range(problem.types[i].nbits):
#                        if result1.variables[i][j] != result2.variables[i][j]:
#                            if bool(random.getrandbits(1)):
#                                result1.variables[i][j] = not result1.variables[i][j]
#                                result2.variables[i][j] = not result2.variables[i][j]
#                                result1.evaluated = False
#                                result2.evaluated = False
#
#        return [result1, result2]


class Encoding3Mutation(Mutation):
    """
    Mutation as described in the paper
    """

    def __init__(self, chromosomeAProbability=0.0001, chromosomeBProbability=0.0001):
        super(Encoding3Mutation, self).__init__()
        self.chromosomeAProbability = chromosomeAProbability
        self.chromosomeBProbability = chromosomeBProbability

    def mutate(self, parent):
        result = copy.deepcopy(parent)
        problem = result.problem

        max_schedule_length = int(problem.nvars / 3)
        for i in range(max_schedule_length):
            if random.uniform(0.0, 1.0) <= self.chromosomeAProbability:
                t = problem.types[2 * i]
                value = t.decode(result.variables[2 * i])
                offset = int(np.random.normal(loc=0.0, scale=40.0 ** 2))
                value += offset
                value = max(0, min(value, t.max_value))
                result.variables[2 * i] = t.encode(value)
                result.evaluated = False

            if random.uniform(0.0, 1.0) <= self.chromosomeAProbability:
                t = problem.types[2 * i + 1]
                value = t.decode(result.variables[2 * i + 1])
                offset = int(np.random.normal(loc=0.0, scale=30.0 ** 2))
                value += offset
                value = max(0, min(value, t.max_value))
                result.variables[2 * i + 1] = t.encode(value)
                result.evaluated = False

        for i in range(2 * max_schedule_length, 3 * max_schedule_length):
            t = problem.types[i]
            if isinstance(t, Binary):
                for j in range(t.nbits):
                    if random.uniform(0.0, 1.0) <= self.chromosomeBProbability:
                        result.variables[i][j] = not result.variables[i][j]
                        result.evaluated = False

        return result
