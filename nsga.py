from platypus import Problem, Integer, NSGAII, HUX, GAOperator, BitFlip
from datetime import datetime
from evaluator import ScheduleEvaluator
from operators import Encoding2BitFlip
from problem import Schedule, Event
from problem_definitions import getEncoding1, getEncoding2
from problem_parser import XMLProblemParser
from util import ProblemLogger, call_counter
import os
import json


@call_counter
def evaluate1(x):
    sc = Schedule([])
    for i in range(x[0]):
        sc.addSolutionPair(Event(SC=x[4 * i + 1], GS=x[4 * i + 2], tStart=x[4 * i + 3], tDur=x[4 * i + 4]))
    res = ScheduleEvaluator.evaluate(schedule_problem, sc)
    return res


@call_counter
def evaluate2(x):
    sc = Schedule([])
    for i in range(int(len(x) / 5)):
        if x[5 * i][0]:
            sc.addSolutionPair(Event(SC=x[5 * i + 1], GS=x[5 * i + 2], tStart=x[5 * i + 3], tDur=x[5 * i + 4]))
    res = ScheduleEvaluator.evaluate(schedule_problem, sc)
    return res


def encoding1Log(logger, result):
    for x in result:
        log = dict()
        log['variable'] = []
        glen = encoding[0].decode(x.variables[0])
        for i in range(glen):
            log['variable'].append({'SC': encoding[4 * i + 1].decode(x.variables[4 * i + 1]),
                                    'GS': encoding[4 * i + 2].decode(x.variables[4 * i + 2]),
                                    'tStart': encoding[4 * i + 3].decode(x.variables[4 * i + 3]),
                                    'tDur': encoding[4 * i + 4].decode(x.variables[4 * i + 4])})
        log['objective'] = {'FitAW': x.objectives[0], 'FitCS': x.objectives[1], 'FitTR': x.objectives[2],
                            'FitGU': x.objectives[3]}
        logger.log(log)


def encoding2Log(logger, result):
    for x in result:
        log = dict()
        log['variable'] = []
        for i in range(int(len(x.variables) / 5)):
            if x.variables[5 * i][0]:
                log['variable'].append({'SC': encoding[5 * i + 1].decode(x.variables[5 * i + 1]),
                                        'GS': encoding[5 * i + 2].decode(x.variables[5 * i + 2]),
                                        'tStart': encoding[5 * i + 3].decode(x.variables[5 * i + 3]),
                                        'tDur': encoding[5 * i + 4].decode(x.variables[5 * i + 4])})
        log['objective'] = {'FitAW': x.objectives[0], 'FitCS': x.objectives[1], 'FitTR': x.objectives[2],
                            'FitGU': x.objectives[3]}
        logger.log(log)


if __name__ == "__main__":
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

    encoding = getEncoding2(max_schedule_length,
                            schedule_problem.nSC,
                            schedule_problem.nGS,
                            schedule_problem.nDays)
    # Define the whole problem
    problem = Problem(nvars=len(encoding), nobjs=4)
    problem.types[:] = encoding
    problem.directions[:] = Problem.MAXIMIZE
    problem.function = evaluate2

    # Define the algorithm and run it
    algorithm = NSGAII(problem, population_size=population_size,
                       variator=GAOperator(HUX(probability=0.3),
                                           Encoding2BitFlip()))
    algorithm.run(number_of_evaluations)

    encoding2Log(logger=logger, result=algorithm.result)
