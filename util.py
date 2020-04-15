import json
import os


class ProblemLogger:
    def __init__(self, file, header):
        self.file = file
        self.write_header = True
        self.header = header

    def log(self, instance):
        f = open(self.file, "a+")
        if self.write_header:
            self.write_header = False
            f.write(self.header + '\n')
        f.write(json.dumps(instance) + '\n')
        f.close()


def call_counter(func):
    def helper(*args, **kwargs):
        helper.calls += 1
        if helper.calls % 100 == 0:
            print("Evals: ", helper.calls)
        return func(*args, **kwargs)

    helper.calls = 0
    return helper


def get_results_file_name(problem_type, problem_name, algorithm, start_time):
    return 'res_' + algorithm + '_' + problem_type + '_' + os.path.splitext(os.path.basename(problem_name))[
        0] + '_' + start_time.strftime('%m_%d_%H_%M_%S') + '.txt'


def get_trace_file_name(problem_type, problem_name, algorithm, start_time):
    return 'trace_' + algorithm + '_' + problem_type + '_' + os.path.splitext(os.path.basename(problem_name))[
        0] + '_' + start_time.strftime('%m_%d_%H_%M_%S') + '.txt'


def encoding2Log(logger, encoding, result):
    for x in result:
        log = dict()
        log['variable'] = []
        for i in range(int(len(x.variables) / 5)):
            if x.variables[5 * i][0]:
                log['variable'].append({'SC': encoding[5 * i + 1].decode(x.variables[5 * i + 1]),
                                        'GS': encoding[5 * i + 2].decode(x.variables[5 * i + 2]),
                                        'tStart': encoding[5 * i + 3].decode(x.variables[5 * i + 3]),
                                        'tDur': encoding[5 * i + 4].decode(x.variables[5 * i + 4])})
        log['objective'] = {'weighted_objective': x.objectives[0]}
        if hasattr(x, 'meta_objectives'):
            log['meta_objectives'] = x.meta_objectives
        logger.log(log)


def encoding3Log(logger, encoding, result):
    for x in result:
        log = dict()
        log['variable'] = []

        max_schedule_length = int(len(x.variables) / 3)
        start_times = []
        duration_times = []
        gss = []
        scs = []
        for i in range(max_schedule_length):
            start_times.append(encoding[2 * i].decode(x.variables[2 * i]))
        for i in range(max_schedule_length):
            duration_times.append(encoding[2 * i + 1].decode(x.variables[2 * i + 1]))
        for i in range(2 * max_schedule_length, 3 * max_schedule_length):
            gss.append(encoding[i].decode(x.variables[i]))
        for i in range(max_schedule_length):
            scs.append((i % x.problem.schedule_problem.nSC) + 1)

        for sc, gs, start, dur in zip(scs, gss, start_times, duration_times):
            log['variable'].append({'SC': sc,
                                    'GS': gs,
                                    'tStart': start,
                                    'tDur': dur})

        log['objective'] = {'weighted_objective': x.objectives[0]}
        if hasattr(x, 'meta_objectives'):
            log['meta_objectives'] = x.meta_objectives
        logger.log(log)


def trace_callback_encoding2(algorithm, encoding, logger):
    if not hasattr(trace_callback_encoding2, 'generation_counter'):
        trace_callback_encoding2.generation_counter = 0
    trace_callback_encoding2.generation_counter += 1
    logger.log({'generation_counter': trace_callback_encoding2.generation_counter})
    encoding2Log(logger=logger, encoding=encoding, result=algorithm.result)
