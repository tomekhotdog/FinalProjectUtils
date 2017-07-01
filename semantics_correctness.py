import time, os

import AspartixSemantics.aspartix_semantics as aspartix_semantics
from AspartixSemantics.abap_parser import DuplicateSymbolException, InvalidContraryDeclarationException
import PythonSemantics.python_semantics as python_semantics
from PythonSemantics.Semantics import Sentence, SemanticSet


def compare_semantics(framework_name, framework_string):
    a_stable, a_grounded, a_complete, a_preferred, a_ideal = aspartix_semantics.compute_semantics(framework_string)
    p_stable, p_grounded, p_complete, p_preferred, p_ideal = python_semantics.compute_semantics(framework_string)

    compare_extensions(framework_name, 'stable', a_stable, p_stable)
    compare_extensions(framework_name, 'grounded', a_grounded, p_grounded)
    compare_extensions(framework_name, 'complete', a_complete, p_complete)
    compare_extensions(framework_name, 'preferred', a_preferred, p_preferred)
    # compare_extensions(framework_name, 'ideal', a_ideal, p_ideal)


def compare_execution_times(framework_name, framework_string, elements):
    admissible = python_semantics.compute_admissible(framework_string)

    ad_time = time_function_execution(lambda: python_semantics.compute_admissible(framework_string))
    print('Admissible computation time: ' + str(ad_time))

    asp_stable_time = time_function_execution(lambda: aspartix_semantics.compute_stable(framework_string))
    py_stable_time = time_function_execution(lambda: python_semantics.compute_stable(framework_string, admissibles=admissible))

    asp_grounded_time = time_function_execution(lambda: aspartix_semantics.compute_grounded(framework_string))
    py_grounded_time = time_function_execution(lambda: python_semantics.compute_grounded(framework_string, admissibles=admissible))

    asp_complete_time = time_function_execution(lambda: aspartix_semantics.compute_complete(framework_string))
    py_complete_time = time_function_execution(lambda: python_semantics.compute_complete(framework_string, admissibles=admissible))

    asp_preferred_time = time_function_execution(lambda: aspartix_semantics.compute_preferred(framework_string))
    py_preferred_time = time_function_execution(lambda: python_semantics.compute_preferred(framework_string, admissibles=admissible))

    # asp_ideal_time = time_function_execution(lambda: aspartix_semantics.compute_ideal(framework_string))
    # py_ideal_time = time_function_execution(lambda: python_semantics.compute_ideal(framework_string))

    with open('semantics_time_test.txt', 'a') as file:
        file.write(framework_name + ': ' + str(elements))
        file.write('Admissible. Python: ' + str(ad_time) + '(' + str(len(admissible)) + 'admissible sets)\n')
        file.write('Stable. Aspartix: ' + str(asp_stable_time))
        file.write('Stable. Aspartix: ' + str(asp_stable_time) + '. Python: ' + str(py_stable_time + ad_time) + '\n')
        file.write('Grounded. Aspartix: ' + str(asp_grounded_time) + '. Python: ' + str(py_grounded_time + ad_time) + '\n')
        file.write('Complete. Aspartix: ' + str(asp_complete_time) + '. Python: ' + str(py_complete_time + ad_time) + '\n')
        file.write('Preferred. Aspartix: ' + str(asp_preferred_time) + '. Python: ' + str(py_preferred_time + ad_time) + '\n')
        # file.write('Ideal. Aspartix: ' + str(asp_ideal_time) + '. Python: ' + str(py_ideal_time) + '\n')

        aspartix_total = asp_stable_time + asp_grounded_time + asp_complete_time + asp_preferred_time
        python_total = ad_time + py_stable_time + py_grounded_time + py_complete_time + py_preferred_time

        file.write('All semantics. Aspartix: ' + str(aspartix_total) + '. Python: ' + str(python_total) + '\n\n')


def compare_extensions(framework_name, semantics_name, aspartix_exts, python_exts):
    aspartix_semantic_sets = []
    for ext in aspartix_exts:
        elements = [Sentence(s.symbol, negation=False, random_variable=False) for s in ext]
        aspartix_semantic_sets.append(SemanticSet(elements))

    equal = all(a_set in python_exts for a_set in aspartix_semantic_sets) and \
        len(aspartix_semantic_sets) == len(python_exts)

    with open('semantics_correctness_test.txt', 'a') as file:
        if not equal:
            aspartix_ext_string = ' '.join([str(ext) for ext in aspartix_semantic_sets])
            python_ext_string = ' '.join([str(ext) for ext in python_exts])
            file.write('extension difference observed: ' + framework_name + ', ' + semantics_name + ', aspartix_exts: ' +
                       aspartix_ext_string + '. python exts: ' + python_ext_string + '\n')
        else:
            file.write(framework_name + ': ' + semantics_name + ' extensions match.\n')


def time_function_execution(function_to_call):
    start_time = time.process_time()
    function_to_call()
    end_time = time.process_time()

    return end_time - start_time


# Goes to directory '../generated_frameworks' and compares
# all the frameworks for correctness and execution time
def test_generated_frameworks():
    file_names = os.listdir('../generated_frameworks/.')

    # file_names = ['framework_51.pl']

    for file_name in file_names:
        try:
            if file_name == 'randomaf.pl':
                continue
            framework_file = open('../generated_frameworks/' + file_name, 'r')
            framework_string = ''

            elements = 0

            for line in framework_file:
                if line.startswith('myAsm'):
                    framework_string += line
                    elements += 1

                elif line.startswith('c'):
                    framework_string += line
                    elements += 1

                elif line.startswith('myRule'):
                    framework_string += line
                    elements += 1

        except UnicodeDecodeError:
            print('Could not decode file ' + file_name + '\n')
            continue

        try:
            print('Comparing semantics for: ' + file_name)
            print('Number of framework elements: ' + str(elements))
            compare_semantics(file_name, framework_string)
            # compare_execution_times(file_name, framework_string, elements)

        except DuplicateSymbolException:
            print('DuplicateSymbolException in: ' + file_name)

        except InvalidContraryDeclarationException:
            print('InvalidContraryDeclarationException in: ' + file_name)


framework_1 = "myAsm(a).\n myAsm(b).\n myAsm(c).\n myAsm(d).\n contrary(a, _a).\n contrary(b, _b).\n" \
              "contrary(c, _c).\n contrary(d, _d).\n myRule(_a, [b]).\n myRule(_b, [c]).\n" \
              "myRule(_c, [d]).\n myRule(_d, [c])."

framework_2 = "myAsm(a).\n myAsm(b).\n myAsm(c).\n myAsm(d).\n myAsm(e).\n myAsm(f).\n contrary(a, _a).\n " \
              "contrary(b, _b).\n contrary(c, _c).\n contrary(d, _d).\n contrary(e, _e).\n contrary(f, _f).\n" \
              "myRule(_a, [b]).\n myRule(_b, [c]).\n myRule(_c, [d]).\n myRule(_d, [c]).\n myRule(_d, [e]).\n" \
              "myRule(_e, [d]).\n myRule(_e, [f]).\n myRule(_f, [e])."

###########################
test_generated_frameworks()
###########################-        QW5 E4W