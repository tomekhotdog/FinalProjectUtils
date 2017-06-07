import time

import PythonSemantics.Parsing.BABAProgramParser as Parser
from PythonSemantics import Semantics

print('Performing timing tests')

files = ['Parsing/BABA_program_1', 'Parsing/BABA_program_2',
         'Parsing/BABA_program_3', 'Parsing/BABA_program_4',
         'Parsing/BABA_cow_program']


# Calculates the average execution time of a task in milliseconds
def calculate_average_execution_time(task, baba_framework, number_of_trials):
    start_time = time.process_time()
    for i in range(number_of_trials):
        task(baba_framework)
    return 100 * (time.process_time() - start_time)


def calculate_average_probability_execution_time(semantics, baba_framework, number_of_trials):
    start_time = time.process_time()
    for i in range(number_of_trials):
        Semantics.compute_semantic_probability(semantics, baba_framework)

    return 100 * (time.process_time() - start_time)


for file in files:
    print('Execution times for: ' + file)

    baba = Parser.BABAProgramParser(filename=file).parse()

    stable_time = calculate_average_execution_time(Semantics.stable, baba, 10)
    print('Stable: ' + str(stable_time))

    grounded_time = calculate_average_execution_time(Semantics.grounded, baba, 10)
    print('Grounded: ' + str(grounded_time))

    complete_time = calculate_average_execution_time(Semantics.complete, baba, 10)
    print('Complete: ' + str(complete_time))

    preferred_time = calculate_average_execution_time(Semantics.preferred, baba, 10)
    print('Preferred: ' + str(preferred_time))

    ideal_time = calculate_average_execution_time(Semantics.ideal, baba, 10)
    print('Ideal: ' + str(ideal_time))

    grounded_prob = calculate_average_probability_execution_time(Semantics.GROUNDED, baba, 10)
    print('Grounded probability: ' + str(grounded_prob))

    s_preferred_prob = calculate_average_probability_execution_time(Semantics.SCEPTICALLY_PREFERRED, baba, 10)
    print('Sceptically preferred probability: ' + str(s_preferred_prob))

    ideal_prob = calculate_average_probability_execution_time(Semantics.IDEAL, baba, 10)
    print('Ideal probability: ' + str(ideal_prob))

    print('#####################################\n')


