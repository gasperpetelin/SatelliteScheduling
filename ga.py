import json
from datetime import datetime
from functools import partial

from platypus import Problem, HUX, GAOperator, BitFlip, GeneticAlgorithm, ProcessPoolEvaluator

from evaluator import ScheduleEvaluator
from operators import Encoding2BitFlip, Encoding2Crossover, Encoding3Mutation
from problem import Schedule, Event
from problem_definitions import getEncoding2, SingleObjectiveSatelliteSchedulingEncoding2, \
    SingleObjectiveSatelliteSchedulingEncoding3, getEncoding3
from problem_parser import XMLProblemParser
from util import ProblemLogger, call_counter, get_results_file_name, get_trace_file_name, encoding2Log, \
    trace_callback_encoding2, encoding3Log

# @call_counter
# def evaluate1(x):
#    sc = Schedule([])
#    for i in range(x[0]):
#        sc.addSolutionPair(Event(SC=x[4 * i + 1], GS=x[4 * i + 2], tStart=x[4 * i + 3], tDur=x[4 * i + 4]))
#    res = ScheduleEvaluator.evaluate(schedule_problem, sc)
#    return 1.5 * res[0] + res[2] + 0.1 * res[1] + 0.01 * res[3]


# def encoding1Log(logger, result):
#    for x in result:
#        log = dict()
#        log['variable'] = []
#        glen = encoding[0].decode(x.variables[0])
#        for i in range(glen):
#            log['variable'].append({'SC': encoding[4 * i + 1].decode(x.variables[4 * i + 1]),
#                                    'GS': encoding[4 * i + 2].decode(x.variables[4 * i + 2]),
#                                    'tStart': encoding[4 * i + 3].decode(x.variables[4 * i + 3]),
#                                    'tDur': encoding[4 * i + 4].decode(x.variables[4 * i + 4])})
#
#        log['objective'] = {'weighted_objective': x.objectives[0]}
#        logger.log(log)


if __name__ == "__main__":
    problem_type = 'small'
    problem_name = 'I_S_01.xml'
    problem_path = './data/' + problem_type + '/' + problem_name
    schedule_problem = XMLProblemParser(problem_path).getProblem()
    max_schedule_length = 250
    population_size = 40
    number_of_evaluations = 2000

    start_time = datetime.now()

    file_header = json.dumps(
        dict(algorithm='GeneticAlgorithm', population_size=population_size, number_of_evaluations=number_of_evaluations,
             problem_type=problem_type, problem_name=problem_name))

    results_file_name = get_results_file_name(problem_type, problem_name, 'ga', start_time)
    results_logger = ProblemLogger(results_file_name, file_header)

    trace_file_name = get_trace_file_name(problem_type, problem_name, 'ga', start_time)
    trace_logger = ProblemLogger(trace_file_name, file_header)

    encoding = getEncoding2(max_schedule_length,
                            schedule_problem.nSC,
                            schedule_problem.nGS,
                            schedule_problem.nDays)

    problem = SingleObjectiveSatelliteSchedulingEncoding2(schedule_problem, max_schedule_length)

    # Define the algorithm and run it
    algorithm = GeneticAlgorithm(problem, population_size=population_size,
                                 variator=GAOperator(HUX(probability=0.1),
                                                     BitFlip(probability=0.001)))

    #algorithm = GeneticAlgorithm(problem,
    #                                 population_size=population_size,
    #                                 variator=GAOperator(Encoding2Crossover(probability=0.2),
    #                                                     Encoding2BitFlip(bit_change_prob=0.0005,
    #                                                                      gs_sc_change_prob=0.0007,
    #                                                                      time_change_prob=0.0001)))

    callback = partial(trace_callback_encoding2, logger=trace_logger, encoding=encoding)

    algorithm.run(number_of_evaluations,
                  callback=callback)

    encoding2Log(logger=results_logger, encoding=encoding, result=algorithm.result)
