from platypus import Problem, Integer, NSGAII, HUX, GAOperator, BitFlip
from datetime import datetime
from evaluator import ScheduleEvaluator
from problem import Schedule, Event
from problem_parser import XMLProblemParser
from util import ProblemLogger
import os
import json

problem_type = 'small'
problem_name = 'I_S_01.xml'
problem_path = './' + problem_type + '/' + problem_name
schedule_problem = XMLProblemParser(problem_path).getProblem()
max_schedule_length = 300
population_size = 50
number_of_evaluations = 50000

start_time = datetime.now()
trace_file_name = 'res_' + 'nsga' + '_' + problem_type + '_' + os.path.splitext(os.path.basename(problem_name))[
    0] + '_' + start_time.strftime("%H_%M_%S") + '.txt'

file_header = json.dumps(
    dict(algorithm='NSGAII', population_size=population_size, number_of_evaluations=number_of_evaluations,
         problem_type=problem_type, problem_name=problem_name))

logger = ProblemLogger(trace_file_name, file_header)


class Wrapper:
    def __init__(self):
        self.counter = 0

    def update_counter(self):
        self.counter += 1
        if self.counter % 100 == 0:
            print(self.counter)

    def evaluate(self, x):
        sc = Schedule([])
        for i in range(x[0]):
            sc.addSolutionPair(Event(SC=x[4 * i + 1], GS=x[4 * i + 2], tStart=x[4 * i + 3], tDur=x[4 * i + 4]))
        res = ScheduleEvaluator.evaluate(schedule_problem, sc)
        self.update_counter()
        return res


if __name__ == "__main__":
    schedule_length_variable = Integer(1, max_schedule_length)
    var = [schedule_length_variable]
    for i in range(max_schedule_length):
        var.append(Integer(1, schedule_problem.nSC))
        var.append(Integer(1, schedule_problem.nGS))
        var.append(Integer(0, schedule_problem.nDays * 24 * 60))
        var.append(Integer(0, schedule_problem.nDays * 24 * 60))

    # Define the whole problem
    problem = Problem(nvars=len(var), nobjs=4)
    problem.types[:] = var
    problem.directions[:] = Problem.MAXIMIZE
    problem.function = Wrapper().evaluate

    # Define the algorithm and run it
    algorithm = NSGAII(problem, population_size=population_size,
                       variator=GAOperator(HUX(probability=0.3),
                                           BitFlip(probability=0.001)))
    algorithm.run(number_of_evaluations)
    for x in algorithm.result:
        log = dict()
        log['variable'] = []
        glen = var[0].decode(x.variables[0])
        for i in range(glen):
            log['variable'].append({'SC': var[4 * i + 1].decode(x.variables[4 * i + 1]),
                                    'GS': var[4 * i + 2].decode(x.variables[4 * i + 2]),
                                    'tStart': var[4 * i + 3].decode(x.variables[4 * i + 3]),
                                    'tDur': var[4 * i + 4].decode(x.variables[4 * i + 4])})

        log['objective'] = {'FitAW': x.objectives[0], 'FitCS': x.objectives[1], 'FitTR': x.objectives[2],
                            'FitGU': x.objectives[3]}
        logger.log(log)
