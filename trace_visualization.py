import glob
import json
import matplotlib.pyplot as plt


def load_trace(file_name):
    """
    Returns a list/trace of algorithm run. Each list is its own generation.
    :param file_name: trace file produced by the algorithm
    :return: generations and a header
    """
    generation_data = []
    header = None
    with open(file_name) as f:
        content = f.readlines()

        for x in content:
            if header is None:
                header = json.loads(x)
            if 'generation_counter' in x:
                generation_data.append([])
            if 'variable' in x:
                data = json.loads(x)
                generation_data[-1].append(data)
    return generation_data, header


def return_statistic_weighted_objective(individual):
    return individual['objective']['weighted_objective']


def compute_mean_stat(generations):
    stat = []
    for generation in generations:
        mean = 0
        for individual in generation:
            mean += return_statistic_weighted_objective(individual)
        mean /= len(generation)
        stat.append(mean)
    return stat


if __name__ == "__main__":
    files = glob.glob('./runs/custom_crossover_test_encoding_2/trace_ga_small_I_S_01*')
    for f in files:
        print(f)
        data, header = load_trace(f)
        st = compute_mean_stat(data)
        plt.plot(st)
    plt.legend()
    plt.show()
