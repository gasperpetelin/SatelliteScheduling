from platypus import Integer, Binary, Problem

from evaluator import ScheduleEvaluator
from problem import Schedule, Event
from util import call_counter


def getEncoding1(max_schedule_length, nSC, nGS, nDays):
    """
    The schedule is represented as tuples (space-craft, ground station, starting time, duration).
    The first variable is the number of tuples that will be converted into the schedule. All other
    tuples will be ignored. The first variable thus indicates currently optimal length.

    The encoding has the following format:
    [143, 4, 2, 4523, 535, ..., 3, 3, 125, 754)]
    [length, SC1, GS1, start1, duration1, ..., SCN, GSN, startN, durationN]

    :param max_schedule_length: Maximum possible value of the length of the schedule
    :param nSC: Number of space-crafts
    :param nGS: Number of ground stations
    :param nDays: Number of days
    :return: Schedule encoding format
    """
    schedule_length_variable = Integer(1, max_schedule_length)
    var = [schedule_length_variable]
    for i in range(max_schedule_length):
        var.append(Integer(1, nSC))
        var.append(Integer(1, nGS))
        var.append(Integer(0, nDays * 24 * 60))  # Days to minutes
        var.append(Integer(0, nDays * 24 * 60))
    return var


def getEncoding2(max_schedule_length, nSC, nGS, nDays):
    """
    The schedule is represented as list of tuples (valid, space-craft, ground station, starting time, duration).
    Each tuple is ignored/turned off if valid is set to false.

    The encoding has the following format:
    [True, 4, 2, 4523, 535, ..., False, 3, 3, 125, 754)]
    [valid1, SC1, GS1, start1, duration1, ..., validN, SCN, GSN, startN, durationN]

    :param max_schedule_length: Maximum possible value of the length of the schedule
    :param nSC: Number of space-crafts
    :param nGS: Number of ground stations
    :param nDays: Number of days
    :return: Schedule encoding format
    """
    var = []
    for i in range(max_schedule_length):
        var.append(Binary(1))
        var.append(Integer(1, nSC))
        var.append(Integer(1, nGS))
        var.append(Integer(0, nDays * 24 * 60))  # Days to minutes
        var.append(Integer(0, nDays * 24 * 60))
    return var


def getEncoding3(max_schedule_length, nSC, nGS, nDays):
    if max_schedule_length % nSC != 0:
        raise Exception('max_schedule_length should ba a multiple of nSC')
    var = []
    # Chromosome A
    for i in range(max_schedule_length):
        # SC are always ordered from 1 to nSC
        var.append(Integer(0, nDays * 24 * 60))  # Days to minutes
        var.append(Integer(0, nDays * 24 * 60))

    for i in range(max_schedule_length):
        var.append(Integer(1, nGS))
    return var


class SingleObjectiveSatelliteSchedulingEncoding3(Problem):
    def __init__(self, schedule_problem, max_schedule_length):
        super().__init__(3 * max_schedule_length, 1)
        self.max_schedule_length = max_schedule_length
        self.schedule_problem = schedule_problem
        self.types[:] = getEncoding3(max_schedule_length,
                                     schedule_problem.nSC,
                                     schedule_problem.nGS,
                                     schedule_problem.nDays)
        self.directions[:] = Problem.MAXIMIZE

    @call_counter
    def evaluate(self, solution):
        start_times = []
        duration_times = []
        gss = []
        scs = []
        for i in range(self.max_schedule_length):
            start_times.append(solution.variables[2 * i])
        for i in range(self.max_schedule_length):
            duration_times.append(solution.variables[2 * i + 1])
        for i in range(2 * self.max_schedule_length, 3 * self.max_schedule_length):
            gss.append(solution.variables[i])
        for i in range(self.max_schedule_length):
            scs.append((i % self.schedule_problem.nSC) + 1)
        schedule = Schedule([])
        for sc, gs, start, dur in zip(scs, gss, start_times, duration_times):
            schedule.addSolutionPair(Event(SC=sc, GS=gs, tStart=start, tDur=dur))
        res = ScheduleEvaluator.evaluate(self.schedule_problem, schedule)
        solution.objectives[:] = 1.5 * res[0] + res[2] + 0.1 * res[1] + 0.01 * res[3]
        solution.meta_objectives = {'FitAW': res[0], 'FitCS': res[1], 'FitTR': res[2], 'FitGU': res[3]}


class SingleObjectiveSatelliteSchedulingEncoding2(Problem):
    def __init__(self, schedule_problem, max_schedule_length):
        super().__init__(5 * max_schedule_length, 1)
        self.max_schedule_length = max_schedule_length
        self.schedule_problem = schedule_problem
        self.types[:] = getEncoding2(max_schedule_length,
                                     schedule_problem.nSC,
                                     schedule_problem.nGS,
                                     schedule_problem.nDays)
        self.directions[:] = Problem.MAXIMIZE

    @call_counter
    def evaluate(self, solution):
        sc = Schedule([])
        for i in range(int(len(solution.variables) / 5)):
            if solution.variables[5 * i][0]:
                sc.addSolutionPair(Event(SC=solution.variables[5 * i + 1],
                                         GS=solution.variables[5 * i + 2],
                                         tStart=solution.variables[5 * i + 3],
                                         tDur=solution.variables[5 * i + 4]))
        res = ScheduleEvaluator.evaluate(self.schedule_problem, sc)
        solution.objectives[:] = 1.5 * res[0] + res[2] + 0.1 * res[1] + 0.01 * res[3]
        solution.meta_objectives = {'FitAW': res[0], 'FitCS': res[1], 'FitTR': res[2], 'FitGU': res[3]}
